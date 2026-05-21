from flask import Flask, render_template, redirect, url_for, request, flash, session
from pixel_pal import PixelPal
from database import db, Pet
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

database_url = os.getenv("DATABASE_URL", "sqlite:///pixelpal.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url

db.init_app(app)
with app.app_context():
    db.create_all()


def load_pal():
    pet_id = session.get('pet_id')
    if not pet_id:
        return None
    pet = db.session.get(Pet, pet_id)
    if not pet:
        return None
    return PixelPal(
        name=pet.name,
        age=pet.age,
        mood=pet.mood,
        hunger=pet.hunger,
        happiness=pet.happiness,
        energy=pet.energy,
        max_value=pet.max_value,
        evo_stage=pet.evo_stage
    )


def save_pal(pal):
    pet_id = session.get('pet_id')
    pet = db.session.get(Pet, pet_id) if pet_id else None
    if pet:
        pet.name = pal.name
        pet.age = pal.age
        pet.mood = pal.mood
        pet.hunger = pal.hunger
        pet.happiness = pal.happiness
        pet.energy = pal.energy
        pet.max_value = pal.max_value
        pet.evo_stage = pal.get_stage()
    else:
        pet = Pet(
            name=pal.name,
            age=pal.age,
            mood=pal.mood,
            hunger=pal.hunger,
            happiness=pal.happiness,
            energy=pal.energy,
            max_value=pal.max_value,
            evo_stage=pal.get_stage()
        )
        db.session.add(pet)
        db.session.flush()
        session['pet_id'] = pet.id
    db.session.commit()


@app.route("/")
def home():
    pal = load_pal()
    if not pal:
        return redirect(url_for("welcome"))
    can_feed = pal.hunger >= pal.max_value * 0.8
    can_play = pal.happiness >= pal.max_value * 0.9
    can_rest = pal.energy >= pal.max_value * 0.9
    return render_template("index.html", name=pal.name, hunger=pal.hunger, energy=pal.energy,
                           happiness=pal.happiness, age=pal.age, can_feed=can_feed,
                           can_play=can_play, can_rest=can_rest, get_sprite=pal.get_sprite(), evo_stage=pal.get_stage())


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


@app.route("/feed", methods=["POST"])
def feed():
    pal = load_pal() or PixelPal("Pixel")
    response = pal.feed()
    flash(f"{pal.name} says: {response}")
    pal.tick()
    death_cause = pal.is_dead()
    if death_cause:
        flash(death_cause)
        return redirect(url_for("death"))
    save_pal(pal)
    return redirect(url_for("home"))


@app.route("/play", methods=["POST"])
def play():
    pal = load_pal() or PixelPal("Pixel")
    response = pal.play()
    flash(f"{pal.name} says: {response}")
    pal.tick()
    death_cause = pal.is_dead()
    if death_cause:
        flash(death_cause)
        return redirect(url_for("death"))
    save_pal(pal)
    return redirect(url_for("home"))


@app.route("/rest", methods=["POST"])
def rest():
    pal = load_pal() or PixelPal("Pixel")
    response = pal.rest()
    flash(f"{pal.name} says: {response}")
    pal.tick()
    death_cause = pal.is_dead()
    if death_cause:
        flash(death_cause)
        return redirect(url_for("death"))
    save_pal(pal)
    return redirect(url_for("home"))

@app.route("/talk", methods=["POST"])
def talk():
    pal = load_pal() or PixelPal("Pixel")
    response = pal.talk()
    flash(f"{pal.name} says: {response}")
    pal.tick()
    death_cause = pal.is_dead()
    if death_cause:
        flash(death_cause)
        return redirect(url_for("death"))
    save_pal(pal)
    return redirect(url_for("home"))

@app.route("/idle", methods=["POST"])
def idle():
    pal = load_pal() or PixelPal("Pixel")
    pal.tick()
    death_cause = pal.is_dead()
    if death_cause:
        flash(death_cause)
        return redirect(url_for("death"))
    save_pal(pal)
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
    save_pal(pal)
    flash(f"Your new PixelPal '{name}' has been created!")
    return redirect(url_for("home"))


@app.route("/death")
def death():
    pet_id = session.pop('pet_id', None)
    pet = db.session.get(Pet, pet_id) if pet_id else None
    name = pet.name if pet else "Pixel"
    if pet:
        db.session.delete(pet)
        db.session.commit()
    return render_template("death.html", name=name)


if __name__ == "__main__":
    app.run(debug=True)
