from flask import Flask, render_template,redirect, url_for, request
from pixel_pal import PixelPal
import os, json
app = Flask (__name__)

@app.route("/")
def home():
    SAVE_FILE = "save_pet.json"
    if os.path.exists(SAVE_FILE):
        with open (SAVE_FILE, "r") as f:
            save_data = json.load(f)
        pal = PixelPal(**save_data)
    else:
        pal = PixelPal("Pixel")

    return render_template("index.html", name=pal.name, hunger=pal.hunger, energy=pal.energy, happiness=pal.happiness, age=pal.age )

@app.route("/feed", methods=["POST"])
def feed():
    if os.path.exists("save_pet.json"):
        with open("save_pet.json", "r") as f:
            save_data = json.load(f)
        pal = PixelPal(**save_data)
        pal.feed()
    else:
        pal = PixelPal("Pixel")
        pal.feed()

    pal.save_game()
    return redirect(url_for("home"))

@app.route("/play", methods=["POST"])
def play():
    if os.path.exists("save_pet.json"):
        with open("save_pet.json", "r") as f:
            save_data = json.load(f)
        pal = PixelPal(**save_data)
        pal.play()
    else:
        pal = PixelPal("Pixel")
        pal.play()

    pal.save_game()
    return redirect(url_for("home")) 

@app.route("/rest", methods=["POST"])
def rest():
    if os.path.exists("save_pet.json"):
        with open("save_pet.json", "r") as f:
            save_data = json.load(f)
        pal = PixelPal(**save_data)
        pal.rest()
    else:
        pal = PixelPal("Pixel")
        pal.rest()

    pal.save_game()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)