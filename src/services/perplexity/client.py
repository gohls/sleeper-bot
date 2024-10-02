import os
import requests
import json
from typing import List, Dict
from openai import OpenAI


PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")

'''
    GENERAL OPERATIONS
'''
def ask_perplexity_for_trash_talk() -> str:
    return "trash talk"
    

'''
    DRAFT OPERATIONS
'''
def ask_perplexity_for_draft_advice(available_players: List[Dict], needed_positions: List[str]) -> str:
    """
    Ask Perplexity AI for advice on which player to draft.

    :param available_players: List of dictionaries containing player information
    :param needed_positions: List of positions still needed for the team
    :return: Perplexity AI's recommendation as a string
    """

    # Prepare the prompt
    player_info = "\n".join([f"{player['full_name']} ({', '.join(player['fantasy_positions'])}) - Rank: {player['search_rank']}, ID: {player['player_id']}" 
                             for player in available_players])  # Limit to top 10 for brevity
    prompt = f"""Given the following list of available players and the positions I still need for my fantasy football team, 
    who should I draft next? Consider the player's rank and my team needs. Only respond with the player ID

    Available players:
    {player_info}

    Positions I still need: {', '.join(needed_positions)}

    Please provide a recommendation with a brief explanation."""

    try:
        messages = [
                    {
                        "role": "user",
                        "content": (
                            prompt
                        ),
                    },
                ]
        response = client.chat.completions.create(
            model="llama-3-sonar-large-32k-online",
            messages=messages,
        )
        # response.raise_for_status()
        return response.model_dump_json()
        # return result["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        return f"Error calling Perplexity API: {str(e)}"
