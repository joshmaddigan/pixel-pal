from flask import Flask, render_template,redirect, url_for, request, flash
from pixel_pal import PixelPal
import os, json
app = Flask (__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def home():
    SAVE_FILE = "save_pet.json"
    if os.path.exists(SAVE_FILE):
        with open (SAVE_FILE, "r") as f:
            save_data = json.load(f)
        pal = PixelPal(**save_data)
    else:
        return redirect(url_for("welcome"))

    return render_template("index.html", name=pal.name, hunger=pal.hunger, energy=pal.energy, happiness=pal.happiness, age=pal.age )

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/feed", methods=["POST"])
def feed():
    if os.path.exists("save_pet.json"):
        with open("save_pet.json", "r") as f:
            save_data = json.load(f)
        pal = PixelPal(**save_data)
    else:
        pal = PixelPal("Pixel")
        response = pal.feed()
        flash(f"{pal.name} says: {response}")
    pal.tick()
    death_cause = pal.is_dead()
    if death_cause:
        flash(death_cause)
        return redirect(url_for("death"))
    else:
        pal.save_game()
    return redirect(url_for("home"))

@app.route("/play", methods=["POST"])
def play():
    if os.path.exists("save_pet.json"):
        with open("save_pet.json", "r") as f:
            save_data = json.load(f)
        pal = PixelPal(**save_data)
    else:
        pal = PixelPal("Pixel")
        response = pal.play()
        flash(f"{pal.name} says: {response}")
    pal.tick()
    death_cause = pal.is_dead()
    if death_cause:
        flash(death_cause)
        return redirect(url_for("death"))
    else:
        pal.save_game()
    return redirect(url_for("home")) 

@app.route("/rest", methods=["POST"])
def rest():
    if os.path.exists("save_pet.json"):
        with open("save_pet.json", "r") as f:
            save_data = json.load(f)
        pal = PixelPal(**save_data)
    else:
        pal = PixelPal("Pixel")
        response = pal.rest()
        flash(f"{pal.name} says: {response}")
    pal.tick()
    death_cause = pal.is_dead()
    if death_cause:
        flash(death_cause)
        return redirect(url_for("death"))
    else:
        pal.save_game()
    return redirect(url_for("home"))

@app.route("/quit", methods=["POST"])
def quit():
    flash("Game saved. Goodbye!")
    return redirect(url_for("home"))

@app.route("/create", methods=["POST"])
def create():
    name = request.form.get("pet_name")
    if not name:
        flash("Please enter a name for your PixelPal!")
        return redirect(url_for("welcome"))
    pal = PixelPal(name)
    pal.save_game()
    flash(f"Your new PixelPal '{name}' has been created!")
    return redirect(url_for("home"))

@app.route("/death")
def death():
    if os.path.exists("save_pet.json"):
        with open("save_pet.json", "r") as f:
            save_data = json.load(f)
        pal = PixelPal(**save_data)
    else:
        pal = PixelPal("Pixel")
    if os.path.exists("save_pet.json"):
        os.remove("save_pet.json")

    return render_template("death.html", name=pal.name)





if __name__ == "__main__":
    app.run(debug=True)