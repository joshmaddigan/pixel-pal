from flask import Flask, render_template
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

if __name__ == "__main__":
    app.run(debug=True)