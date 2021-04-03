import json

from flask import Flask, request

from .recipes import Recipes
from .pump_controller import PumpController


class BarpyAPI(Flask):
    def __init__(self):
        super().__init__("barpy")

        self.recipes = None
        self.pump_controller = None

    def init(self, db, locked_hardware):
        self.recipes = Recipes(db)
        self.pump_controller = PumpController(db, self.recipes, locked_hardware)


app = BarpyAPI()


@app.route('/', methods=['get'])
def get_default_page():
    recipe_names = app.recipes.get_recipe_names()
    json_str = json.dumps(recipe_names)
    return json_str


@app.route('/make', methods=['post'])
def make_drink():
    req = request.json
    app.pump_controller.make_drink(req["cocktail"])
    return "{}", 200