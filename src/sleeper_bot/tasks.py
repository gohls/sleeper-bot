import time
from celery import shared_task
from services.perplexity.client import ask_perplexity_for_draft_advice
from services.sleeper.automation import SleeperAutomationBot
from services.sleeper.client import get_draft_picks, get_nfl_players
from services.sleeper.utils import *
from sleeper_bot.models import Player
from django.db.models import Q
from django.forms import model_to_dict

sleeper_automator = SleeperAutomationBot()

@shared_task
def run_draft_process():

    draft_picks = get_draft_picks()
    last_pick_no = max(pick['pick_no'] for pick in draft_picks) if draft_picks else 0

    if not has_picks_remaining(last_pick_no + 1, 5, 12):
        return 
    
    if not sleeper_automator.is_logged_in:
        sleeper_automator.login()
        get_nfl_players()
        time.sleep(90)

    draft_picks = get_draft_picks()
    on_roster = positions_on_roster(draft_picks)
    needed_positions = position_roster_needs(on_roster)

    required_positions = set()
    for position in needed_positions:
        if position == 'FLEX':
            required_positions.update(['RB', 'WR', 'TE']) # This is wrong
        elif position != 'BN':
            required_positions.add(position)
    
    if is_current_pick_mine(last_pick_no + 1, 5, 12):
        drafted_player_ids = get_drafted_player_ids(draft_picks)
        position_query = Q()
        for position in required_positions:
            position_query |= Q(fantasy_positions__contains=position)
        available_players_queryset = Player.objects \
                        .exclude(player_id__in=drafted_player_ids) \
                        .filter(active=True) \
                        .filter(search_rank=None) \
                        .filter(position_query) \
                        .order_by('search_rank')[:50] # this is not an ideal way of getting the top ranked players
        
        available_players = list(available_players_queryset.values('player_id', 'full_name', 'fantasy_positions', 'search_rank'))

        # If fantasy_positions is stored as a string, split it into a list
        for player in available_players:
            if isinstance(player['fantasy_positions'], str):
                player['fantasy_positions'] = player['fantasy_positions'].split(',')
        
        recommanded_player_id = ask_perplexity_for_draft_advice(model_to_dict(available_players), needed_positions)
        recommanded_player = Player.objects.get(player_id=recommanded_player_id)
        make_draft_pick()


        
