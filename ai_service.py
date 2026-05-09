import ollama
import random


def get_pet_response(pet_stats):
    
    personalities = {
        "Sarcastic": "Witty, slightly mean, and unimpressed by the owner",
        "Excited": "Uses ALL CAPS, super energetic and loves everything.",
        "Stoic": "Dramatic, deep, and talks about the 'void' or 'destiny'."
    }

    moods = ["Sarcastic", "Excited", "Stoic"]
    current_mood = random.choice(moods)

    prompt = f"""
You are pixel, a digital pet.
You current mood is: {current_mood}.
Current Stats: Hunger: {pet_stats['Hunger']}/10, Stage: {pet_stats['stage']}.
Write exactly one short sentence reacting to your owner.
"""
    
    try:
        response = ollama.chat(model='gemma4:e2b', messages=[
            {
                'role': 'user',
                'content': prompt,
                
            },
        ])
        return response['message']['content']
    except Exception as e:
        return "*Pixel is staring into the digital abyss...*"