
def positions_on_roster(draft_picks, user_id="1130174389980434432"):
    return [pick['metadata']['position'] for pick in draft_picks if pick['picked_by'] == user_id]

def get_drafted_player_ids(draft_picks):
    return [pick['player_id'] for pick in draft_picks]

def position_roster_needs(drafted_positions):
    requirements = {
        'WR': 6,
        'TE': 2,
        'RB': 3,
        'QB': 2,
        'K': 1,
        'DEF': 1,
        'FLEX': 0,
        'BN': 0
    }

    drafted_counts = {}
    for position in drafted_positions:
        drafted_counts[position] = drafted_counts.get(position, 0) + 1
    
    needs = []
    flex_count = 0
    
    for position, count in requirements.items():
        if position == 'FLEX':
            continue 
        
        drafted = drafted_counts.get(position, 0)
        if drafted < count:
            needs.extend([position] * (count - drafted))
        elif position in ['RB', 'WR', 'TE']:
            # Extra RBs, WRs, and TEs can count towards FLEX
            flex_count += drafted - count
    
    flex_needed = max(0, requirements['FLEX'] - flex_count)
    needs.extend(['FLEX'] * flex_needed)
    
    bench_spots = requirements['BN'] - max(0, sum(drafted_counts.values()) - sum(requirements.values()) + requirements['BN'])
    needs.extend(['BN'] * bench_spots)
    
    return needs


def is_current_pick_mine(pick_number, team_position, total_teams):
    # Calculate the round number
    round_number = (pick_number - 1) // total_teams + 1
    # Calculate the position within the round
    position_in_round = (pick_number - 1) % total_teams + 1

    if round_number % 2 == 1:
        # Odd round: regular order
        return position_in_round == team_position
    else:
        # Even round: reverse order
        return position_in_round == (total_teams + 1 - team_position)
    

def has_picks_remaining(pick_number, team_position, total_teams, total_rounds=15):
    total_picks = total_teams * total_rounds
    
    # Check if there are any picks remaining in the draft
    if pick_number >= total_picks:
        return False  # No more picks for anyone
    
    # Calculate the round number
    round_number = (pick_number - 1) // total_teams + 1
    # Calculate the position within the round
    position_in_round = (pick_number - 1) % total_teams + 1

    # Check if there are more picks for the user after this one
    if round_number < total_rounds:
        return True
    elif round_number == total_rounds:
        return position_in_round <= team_position
    else:
        return False


def make_draft_pick(pick_number):
    # Calculate the round number
    wip = "wip"