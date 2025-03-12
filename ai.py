
import spacy
from flask import Flask, request, jsonify
import json
import random

# Load SpaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Load recipes dataset
with open("data/recipes.json", "r") as f:
    recipes = json.load(f)

app = Flask(__name__)

# Function to extract ingredients from text
def extract_ingredients(text):
    doc = nlp(text)
    ingredients = [token.text.lower() for token in doc if token.pos_ == "NOUN"]
    return ingredients

# Function to get a matching recipe
def get_recipe(ingredients):
    for recipe in recipes:
        if all(ing in recipe["ingredients"] for ing in ingredients):
            return recipe
    return random.choice(recipes)  # Return a random recipe if no exact match

@app.route("/generate_recipe", methods=["POST"])
def generate_recipe():
    user_input = request.json.get("text", "")
    ingredients = extract_ingredients(user_input)
    recipe = get_recipe(ingredients)
    return jsonify(recipe)

if __name__ == "__main__":
    app.run(debug=True)
