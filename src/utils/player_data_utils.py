import json
from django.db import transaction
from sleeper_bot.models import Player, PlayerMetadata, PlayerIDs
from datetime import datetime


def parse_date(date_string):
    if not date_string:
        return None
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        return None


def update_or_create_player(player_data):
    with transaction.atomic():
        player, created = Player.objects.update_or_create(
            player_id=player_data["player_id"],
            defaults={
                "first_name": player_data.get("first_name", ""),
                "last_name": player_data.get("last_name", ""),
                "full_name": player_data.get("full_name", ""),
                "search_full_name": player_data.get("search_full_name", ""),
                "search_first_name": player_data.get("search_first_name", ""),
                "search_last_name": player_data.get("search_last_name", ""),
                "team": player_data.get("team", ""),
                "position": player_data.get("position", ""),
                "fantasy_positions": player_data.get("fantasy_positions", []),
                "years_exp": player_data.get("years_exp"),
                "active": player_data.get("active", False),
                "status": player_data.get("status", ""),
                "number": player_data.get("number"),
                "depth_chart_position": player_data.get("depth_chart_position", ""),
                "depth_chart_order": player_data.get("depth_chart_order"),
                "sport": player_data.get("sport", "nfl"),
                "search_rank": player_data.get("search_rank", 9999999),
            },
        )

        PlayerMetadata.objects.update_or_create(
            player=player,
            defaults={
                # 'rookie_year': player_data.get('metadata', {}).get('rookie_year', ''),
                "birth_date": parse_date(player_data.get("birth_date")),
                "age": player_data.get("age", 0),
                "height": player_data.get("height", ""),
                "weight": player_data.get("weight", ""),
                "college": player_data.get("college", ""),
                "high_school": player_data.get("high_school", ""),
            },
        )

        PlayerIDs.objects.update_or_create(
            player=player,
            defaults={
                # 'channel_id': player_data.get('metadata', {}).get('channel_id', ''),
                "fantasy_data_id": player_data.get("fantasy_data_id"),
                "stats_id": player_data.get("stats_id", 0),
            },
        )

        # if player_data.get('injury_body_part'):
        #     Injury.objects.update_or_create(
        #         player=player,
        #         defaults={
        #             'body_part': player_data.get('injury_body_part', ''),
        #             'injury_status': player_data.get('injury_status', ''),
        #             'notes': player_data.get('injury_notes', ''),
        #             'start_date': parse_date(player_data.get('injury_start_date')),
        #         }
        #     )

    return player, created


# Ex
json_data = """
{
  "6462": {
    "high_school": "Douglas County",
    "opta_id": null,
    "age": 26,
    "injury_body_part": null,
    "fantasy_data_id": 21427,
    "search_full_name": "ellisrichardson",
    "team": null,
    "first_name": "Ellis",
    "rotoworld_id": null,
    "search_first_name": "ellis",
    "years_exp": 3,
    "active": true,
    "team_abbr": null,
    "birth_state": null,
    "search_last_name": "richardson",
    "metadata": { "channel_id": "1116853254748110848" },
    "rotowire_id": 14134,
    "team_changed_at": null,
    "injury_start_date": null,
    "height": "75",
    "status": "Active",
    "college": "Georgia Southern",
    "sportradar_id": "efd6f3c3-b752-4bc2-a4f2-b776c15c3ec0",
    "depth_chart_position": null,
    "sport": "nfl",
    "fantasy_positions": ["TE"],
    "swish_id": null,
    "stats_id": 887183,
    "gsis_id": " 00-0035057",
    "player_id": "6462",
    "birth_city": null,
    "competitions": [],
    "yahoo_id": 32262,
    "pandascore_id": null,
    "depth_chart_order": null,
    "last_name": "Richardson",
    "oddsjam_id": null,
    "search_rank": 9999999,
    "injury_notes": null,
    "practice_participation": null,
    "full_name": "Ellis Richardson",
    "hashtag": "#ellisrichardson-NFL-FA-45",
    "birth_country": null,
    "position": "TE",
    "birth_date": "1995-02-12",
    "news_updated": null,
    "practice_description": null,
    "weight": "245",
    "injury_status": null,
    "espn_id": 3926590,
    "number": 45
  }
}
"""
