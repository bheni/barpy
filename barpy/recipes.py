
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
        for recipe_ingrediant in makable_recipes:
            recipe_name = recipe_ingrediant['recipe_name']

            if recipe_name not in self.recipes:
                ingrediants = []
            else:
                ingrediants = self.recipes[recipe_name]

            ingrediants.append(recipe_ingrediant)
            self.recipes[recipe_name] = ingrediants

    def get_fluid_idx_to_ozs(self, recipe_name):
        fluid_idx_to_oz = {}

        if recipe_name in self.recipes:
            recipe_ingrediants = self.recipes[recipe_name]

            for ingrediant in recipe_ingrediants:
                idx = int(ingrediant['fluid_idx'])
                amount = ingrediant['amount']
                unit = ingrediant['amount_unit']
                ozs = to_ounces(unit, amount)
                fluid_idx_to_oz[idx] = ozs

        return fluid_idx_to_oz

    def get_recipe_names(self):
        recipe_names = []
        for key in self.recipes.keys():
            recipe_names.append(key)

        return recipe_names

