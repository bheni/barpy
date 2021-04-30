from time import sleep


class PumpController(object):
    def __init__(self, db, recipes, locked_hardware):
        self.recipes = recipes
        self.locked_hardware = locked_hardware

        self.pump_info = []
        results = db.get_pump_info()
        expected_idx = 0
        for result in results:
            idx = int(result['idx'])

            if idx != expected_idx:
                raise Exception("pump results not in expected order")

            self.pump_info.append(result)
            expected_idx += 1

    def make_drink(self, recipe_name):
        fluid_idx_to_ounces = self.recipes.get_fluid_idx_to_ozs(recipe_name)
        timeline = []
        for idx, ounces in fluid_idx_to_ounces.items():
            pump_info = self.pump_info[idx]
            on_seconds = float(pump_info['seconds_per_oz'])*ounces
            tup = (idx, on_seconds)
            timeline.append(tup)

        timeline.sort(key=lambda x: x[1])

        with self.locked_hardware as hardware:
            for timeline_entry in timeline:
                pump_idx = timeline_entry[0]
                hardware.pump_on(pump_idx)

            t = 0
            for timeline_entry in timeline:
                pump_idx, on_seconds = timeline_entry
                if t < on_seconds:
                    sleep_time = on_seconds-t
                    sleep(sleep_time)
                    t += sleep_time

                hardware.pump_off(pump_idx)

            # unnecessary
            hardware.turn_off_all_pumps()
