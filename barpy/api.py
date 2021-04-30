import json

from flask import Flask, request
from jinja2 import Environment, PackageLoader, select_autoescape

from .recipes import Recipes
from .pump_controller import PumpController

env = Environment(
    loader=PackageLoader('barpy', 'templates'),
    autoescape=select_autoescape(['html'])
)


class BarpyAPI(Flask):
    def __init__(self):
        super().__init__("barpy")

        self.db = None
        self.recipes = None
        self.pump_controller = None
        self.locked_hardware = None
        self.num_fluids = 0

    def init(self, db, locked_hardware):
        self.db = db
        self.locked_hardware = locked_hardware
        self.refresh_recipes()
        with locked_hardware as hardware:
            self.num_fluids = hardware.num_fluids()
    
    def refresh_recipes(self):
        self.recipes = Recipes(self.db)
        self.pump_controller = PumpController(self.db, self.recipes, self.locked_hardware)


app = BarpyAPI()


@app.route('/', methods=['get'])
def get_default_page():
    drink_names = app.recipes.get_recipe_names()

    drinks = []
    for i, drink in enumerate(drink_names):
        drinks.append({"id": drink, "display_name": drink.title()})

    template = env.get_template('index.html')
    return template.render(drinks=drinks)


@app.route('/make', methods=['post'])
def make_drink():
    req = request.json
    requested_drink = req["cocktail"]
    print('making a "%s"' % requested_drink)
    app.pump_controller.make_drink(requested_drink)
    return "{}", 200


@app.route('/fluids', methods=['post'])
def fluids_post():
    idx_to_fluid={}
    for k, v in request.values.items():
        if k.lower().startswith('fluid'):
            n_str = k[5:]
            if n_str.isdigit():
                n = int(n_str)
                idx_to_fluid[n] = v
    app.db.update_fluids(idx_to_fluid)
    app.refresh_recipes()
    return fluids()


@app.route('/fluids', methods=['get'])
def fluids():
    fluids = []
    for fluid in app.db.get_fluids():
        name = fluid['fluid']
        if name == '' or name == 'None' or name is None:
            name = "NULL"
        fluids.append(name)

    ingredients = [{'id': "NULL", 'display_name': "Empty"}]
    for ingredient in app.db.get_ingredients():
        name = ingredient['name']
        ingredients.append({'id': name, 'display_name': name.title()})

    template = env.get_template('fluids.html')
    return template.render(fluids=fluids, ingredients=ingredients)
