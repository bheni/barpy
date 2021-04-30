
unit_to_multiplier = {"OZ": 1.0, "ML": 0.033814,  "DASH": 0.025}


def to_ounces(unit, amount):
    if unit in unit_to_multiplier:
        multiplier = unit_to_multiplier[unit]
        return float(amount) * multiplier
    else:
        raise Exception("unsupported unit")


class Recipes(object):
    def __init__(self, db):
        makable_recipes = db.query_possible_recipes()

        self.recipes = {}
        for recipe_ingredient in makable_recipes:
            recipe_name = recipe_ingredient['recipe_name']

            if recipe_name not in self.recipes:
                ingredients = []
            else:
                ingredients = self.recipes[recipe_name]

            ingredients.append(recipe_ingredient)
            self.recipes[recipe_name] = ingredients

    def get_fluid_idx_to_ozs(self, recipe_name):
        fluid_idx_to_oz = {}

        if recipe_name in self.recipes:
            recipe_ingredients = self.recipes[recipe_name]

            for ingredient in recipe_ingredients:
                idx = int(ingredient['fluid_idx'])
                amount = ingredient['amount']
                unit = ingredient['amount_unit']
                ozs = to_ounces(unit, amount)
                fluid_idx_to_oz[idx] = ozs

        return fluid_idx_to_oz

    def get_recipe_names(self):
        recipe_names = []
        for key in self.recipes.keys():
            recipe_names.append(key)

        return recipe_names

