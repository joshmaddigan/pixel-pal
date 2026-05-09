## Pixel self! ##
import random
import os
import json
from ai_service import get_pet_response

class PixelPal:
    def __init__(self, name, age=1, hunger=10, happiness=10, energy=10, max_value=10, evo_stage='baby'):
        self.name = name
        self.age = 1
        self.hunger = 10
        self.happiness = 10
        self.energy = 10
        self.max_value = 10
        self.hunger_decay = random.randint(1, 2)
        self.happiness_decay = random.randint(1, 4)
        self.energy_decay = random.randint(1, 2)
        self.is_alive = True

    def save_game(self):
        game_data = {
            "name": self.name,
            "age": self.age,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "max_value": self.max_value,
            "evo_stage": self.check_evo()
        }
        with open ("save_pet.json", "w") as f:
            json.dump(game_data, f, indent=4)

    def check_evo(self):
        if self.age == 10:
            self.max_value += 10
            print(f"{self.name} has evolved! Max stats increased.")
        elif self.age == 20:
            self.max_value += 10
            print(f"{self.name} has evolved! Max stats increased.")
        elif self.age == 30:
            self.max_value += 10
            print(f"{self.name} has evolved! Max stats increased.")

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
        self.hunger = min(self.max_value, self.hunger + recovery)
        self.happiness = min(self.happiness +3, self.max_value)
        self.energy = min(self.energy + 4, self.max_value)
        stats_for_ai = {"Hunger": self.hunger, "stage": self.check_evo()}
        ai_voice = get_pet_response(stats_for_ai)
        print(f"{self.name} says: {ai_voice}")

    def play(self):
        recovery = int(self.max_value * 0.6)
        self.happiness = min(self.happiness + recovery, self.max_value)
        self.energy = min(self.energy - 2, self.max_value)
        self.hunger = min(self.hunger - 2, self.max_value)
        stats_for_ai = {"happiness": self.happiness, "stage": self.check_evo()}
        ai_voice = get_pet_response(stats_for_ai)
        print(f"{self.name} says: {ai_voice}")

    def rest(self):
        self.energy += 7
        if self.energy > self.max_value:
            self.energy = self.max_value
        self.hunger -= 1
        self.happiness += 1
        stats_for_ai = {"energy": self.energy, "stage": self.check_evo()}
        ai_voice = get_pet_response(stats_for_ai)
        print(f"{self.name} says: {ai_voice}")

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


    pal.age += 1
    pal.check_evo()
    pal.hunger -= pal.hunger_decay
    pal.happiness -= pal.happiness_decay
    pal.energy -= pal.energy_decay
    pal.save_game()


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
