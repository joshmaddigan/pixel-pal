import random
import os
import json
from ai_service import get_pet_response, get_talk_response, get_petting_response

class PixelPal:
    def __init__(self, name, age=1, hunger=10, happiness=10, energy=10, max_value=10, evo_stage='baby', mood=None):
        self.name = name
        self.age = age
        self.hunger = hunger
        self.happiness = happiness
        self.energy = energy
        self.max_value = max_value
        self.mood = mood if mood else random.choice(["Sarcastic", "Energetic", "Stoic"])
        self.hunger_decay = random.uniform(0.1, 0.15)
        self.happiness_decay = random.uniform(0.05, 0.20)
        self.energy_decay = random.uniform(0.05, 0.15)
        self.is_alive = True

    def save_game(self):
        game_data = {
            "name": self.name,
            "age": self.age,
            "mood": self.mood,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "max_value": self.max_value,
            "evo_stage": self.get_stage()
        }
        with open ("save_pet.json", "w") as f:
            json.dump(game_data, f, indent=4)

    def check_evo(self):
        if self.age in [10, 20, 30]:
            self.max_value += 10
            print(f"{self.name} has evolved! They are now a {self.get_stage()} stage pet!")

    def get_stage(self):
        if self.age < 10:
            return "Baby"
        elif self.age < 20:
            return "Teen"
        elif self.age < 30:
            return "Adult"
        else:
            return "Elder"        
    
    def get_bar(self, stat_name, current_value, max_value):
        #clamping logic
        clamped_val = max(0, min(current_value, self.max_value))
        number_of_blocks = int((clamped_val / max_value) *10)
        bar = "#" * number_of_blocks + "-" * (10 - number_of_blocks)
        return f'{stat_name:10}: [{bar}] {clamped_val}/{max_value}'

    def feed(self):
        recovery = int(self.max_value * 0.7)
        self.hunger = int(min(self.max_value, self.hunger + recovery))
        self.happiness = int(min(self.max_value, self.happiness + random.uniform(0.1, 0.2) * self.max_value))
        self.energy = int(min(self.max_value, self.energy + random.uniform(0.1, 0.2) * self.max_value))
        stats_for_ai = {"Hunger": self.hunger, "stage": self.get_stage()}
        ai_voice = get_pet_response(stats_for_ai, self.mood)
        return ai_voice
    
    def play(self):
        recovery = int(self.max_value * 0.7)
        self.happiness = int(min(self.max_value, self.happiness + recovery))
        self.energy = int(min(self.max_value, self.energy - random.uniform(0.1, 0.2) * self.max_value))
        self.hunger = int(min(self.max_value, self.hunger - random.uniform(0.1, 0.2) * self.max_value))
        stats_for_ai = {"happiness": self.happiness, "stage": self.get_stage()}
        ai_voice = get_pet_response(stats_for_ai, self.mood)
        return ai_voice
    
    def rest(self):
        recovery = int(self.max_value * 0.7)
        self.energy = int(min(self.max_value, self.energy + recovery))
        self.hunger = int(min(self.max_value, self.hunger - random.uniform(0.1, 0.2) * self.max_value))
        self.happiness = int(min(self.max_value, self.happiness + random.uniform(0.1, 0.2) * self.max_value))
        stats_for_ai = {"energy": self.energy, "stage": self.get_stage()}
        ai_voice = get_pet_response(stats_for_ai, self.mood)
        return ai_voice

    def tick(self):
        self.age += 1
        self.check_evo()
        self.hunger -= int(self.hunger_decay * self.max_value)
        self.happiness -= int(self.happiness_decay * self.max_value)
        self.energy -= int(self.energy_decay * self.max_value)

    def get_sprite(self):
        if self.hunger < self.max_value * 0.5 and self.happiness < self.max_value * 0.5 and self.energy < self.max_value * 0.5:
            return "pal_sick.png"
        elif self.hunger < self.max_value * 0.5:
            return "pal_hungry.png"
        elif self.happiness < self.max_value * 0.5:
            return "pal_tired.png"
        elif self.energy < self.max_value * 0.5:
            return "pal_tired.png"
        elif self.hunger > self.max_value * 0.7 and self.happiness > self.max_value * 0.7 and self.energy > self.max_value * 0.7:
            return "pal_happy.png"
        else: 
            return "pal_neutral.png"

    def is_dead(self):
        if self.hunger <= 0:
            return (f"Sadly, {self.name} starved to death. Please feed you pal better next time!")
        elif self.happiness <= 0:
            return (f"Sadly, {self.name} died of sadness. Please play with your pal more next time!")
        elif self.energy <= 0:
            return (f"Sadly, {self.name} died of exhaustion. Please let your pal rest more next time!")
        else:
            return False
    
    def talk(self):
        stats_for_ai = {"Hunger": self.hunger, "stage": self.get_stage()}
        ai_voice = get_talk_response(stats_for_ai, self.mood)        
        return ai_voice

    def petting(self):
        self.happiness = int(min(self.max_value, self.happiness + random.uniform(0.4, 0.5) * self.max_value))
        stats_for_ai = {"Happiness": self.happiness, "stage": self.get_stage()}
        ai_voice = get_petting_response(stats_for_ai, self.mood)
        return ai_voice
    
if __name__ == "__main__":

    SAVE_FILE = "save_pet.json"
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            save_data = json.load(f)
        pal = PixelPal(**save_data)
        print(f"Welcome back! Your pal {pal.name} has been waiting for you!")
    else:
        name = input("Welcome to Pixel Pal! Please name you new Pal: ")
        pal = PixelPal(name)

    while pal.is_alive:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Your pal's name is {pal.name}! and they are a {pal.age} day old {pal.get_stage()}.")
        print(pal.get_bar("Hunger", pal.hunger, pal.max_value))
        print(pal.get_bar("Happiness", pal.happiness, pal.max_value))
        print(pal.get_bar("Energy", pal.energy, pal.max_value))

        action = input(f"What would you like to do with {pal.name}? (feed, play, rest or quit)").lower()

        if action == 'feed':
            pal.feed()
        elif action == 'rest':
            pal.rest()
        elif action == "play":
            pal.play()
        elif action == 'quit':
            pal.save_game()
            print("Game saved. Goodbye!")
            break     
        else:
            print("Invalid action. please choose 'feed', 'play', or 'rest'.") 
        input("Press Enter to continue...")

        pal.tick()

    if pal.hunger <= 0:
        print(f"Sadly, {pal.name} has died of hunger. Take better care of your next self.")
        pal.is_alive = False
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
    elif pal.happiness <= 0:
        print(f"Sadly, {pal.name} has died of sadness. Please take better care of your next self.")
        pal.is_alive = False
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
    elif pal.energy <= 0:
        print(f"Sadly, {pal.name} has died of exhaustion. Please take better care of your next self.")
        pal.is_alive = False
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
