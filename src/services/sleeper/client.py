from datetime import datetime
import json
import os
from django.forms import model_to_dict
import requests
from utils.player_data_utils import update_or_create_player
from utils.storage import LocalStorage
from django.db import transaction
from sleeper_bot.models import Player


SLEEPER_API_BASE_URL = "https://api.sleeper.app/v1"
TIMESTAMP_CALL_KEY = "get_nfl_players_timestamp"
DRAFT_ID = os.getenv("DRAFT_ID") or ""
LEAGUE_ID = os.getenv("LEAGUE_ID") or ""

local_storage = LocalStorage("sleeper.json")


def fetch_data(endpoint, **kwargs):
    url = f"{SLEEPER_API_BASE_URL}{endpoint.format(**kwargs)}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_state(sport):
    return fetch_data("/state/{sport}", sport=sport)


def get_nfl_players():
    """
    Use this call sparingly, as it is intended only to be used once per day
    at most to keep your player IDs updated. The average size of this query is 5MB.
    """
    last_call = local_storage.load(TIMESTAMP_CALL_KEY)
    now = datetime.now()

    # If last call was on the same day, don't make a new call
    if last_call and last_call.date() == now.date():
        players = Player.objects.all()
        return [model_to_dict(player) for player in players]

    nfl_players = fetch_data("/players/nfl")

    players = []
    with transaction.atomic():
        for player_id, data in nfl_players.items():
            data["player_id"] = player_id
            update_or_create_player(data)
            players.append(data)

    local_storage.save(TIMESTAMP_CALL_KEY, now)

    return players


def get_players_trending(type_, lookback_hours, limit):
    return fetch_data(
        "/players/nfl/trending/{type}?lookback_hours={lookback_hours}&limit={limit}",
        type=type_,
        lookback_hours=lookback_hours,
        limit=limit,
    )


def get_user_drafts(user_id, sport, season):
    return fetch_data(
        "/user/{user_id}/drafts/{sport}/{season}",
        user_id=user_id,
        sport=sport,
        season=season,
    )


def get_league_drafts(league_id=LEAGUE_ID):
    return fetch_data("/league/{league_id}/drafts", league_id=league_id)


def get_draft():
    return fetch_data("/draft/{draft_id}", draft_id=DRAFT_ID)


def get_draft_picks():
    return fetch_data("/draft/{draft_id}/picks", draft_id=DRAFT_ID)


def get_draft_traded_picks():
    return fetch_data("/draft/{draft_id}/traded_picks", draft_id=DRAFT_ID)


def get_league_info(league_id):
    return fetch_data("/league/{league_id}", league_id=league_id)


def get_league_rosters(league_id=LEAGUE_ID):
    return fetch_data("/league/{league_id}/rosters", league_id=league_id)


def get_league_users(league_id=LEAGUE_ID):
    return fetch_data("/league/{league_id}/users", league_id=league_id)


def get_league_matchups(league_id=LEAGUE_ID, week=None):
    return fetch_data(
        "/league/{league_id}/matchups/{week}", league_id=league_id, week=week
    )


def get_league_transactions(league_id, round_):
    return fetch_data(
        "/league/{league_id}/transactions/{round}", league_id=league_id, round=round_
    )


def get_league_traded_picks(league_id):
    return fetch_data("/league/{league_id}/traded_picks", league_id=league_id)
