import os
import anthropic
import random
from dotenv import load_dotenv

load_dotenv()

def get_pet_response(pet_stats, mood):
    client = anthropic.Anthropic()
    
    personalities = {
        "Sarcastic": "Witty, slightly mean, and unimpressed by the owner",
        "Energetic": "Uses ALL CAPS, super energetic and loves everything.",
        "Stoic": "Dramatic, deep, and talks about the 'void' or 'destiny'."
    }

    prompt = f"""You are a {mood} pixel pet. Your current stats are: {pet_stats}. Respond to the owner in one small sentence, reflecting on your mood and stats.  {personalities[mood]}"""

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=100,
            messages=[
                {"role": "user", "content": prompt}
            ]    
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error calling AI API: {e}")
        print("Pixel pet has no thoughts behind those eyes... (Api call fail)")
        return "..."
    