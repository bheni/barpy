import mysql.connector


def _connect(user, host, port, database):
    return mysql.connector.connect(user=user, host=host, port=port, database=database)


class DoltConnection(object):
    def __init__(self, user='root', host='127.0.0.1', port=3306, database='dolt', auto_commit=False):
        self.user = user
        self.host = host
        self.port = port
        self.database = database
        self.auto_commit = auto_commit
        self.cnx = None

    def connect(self):
        self.cnx = _connect(self.user, self.host, self.port, self.database)
        self.cnx.autocommit = self.auto_commit

    def close(self):
        self.cnx.close()

    def query(self, query_str):
        cursor = self.cnx.cursor()
        cursor.execute(query_str)

        if cursor.description is None:
            return [], cursor.rowcount

        raw = cursor.fetchall()

        row_maps = []
        for curr in raw:
            r = {}
            for i, k in enumerate(cursor.column_names):
                r[k] = str(curr[i])
            row_maps.append(r)

        return row_maps, cursor.rowcount


class DB(object):
    possible_recipes_query = '''
SELECT cocktails.recipe_ingredients.*, barpydb.fluids.idx AS fluid_idx 
FROM cocktails.recipe_ingredients 
JOIN barpydb.fluids ON cocktails.recipe_ingredients.ingredient_name = barpydb.fluids.fluid 
WHERE recipe_name IN (
    SELECT we_need.recipe_name FROM (
        SELECT recipe_name, COUNT(recipe_name) AS cnt
        FROM cocktails.recipe_ingredients 
        GROUP BY recipe_name
    ) we_need
    JOIN (
        SELECT recipe_name, COUNT(recipe_name) AS cnt
        FROM cocktails.recipe_ingredients ri
        WHERE ri.ingredient_name IN (SELECT fluid FROM barpydb.fluids) 
        GROUP BY recipe_name
    ) we_have
    ON we_have.recipe_name = we_need.recipe_name and we_have.cnt = we_need.cnt
);'''

    get_pump_info_query = '''
SELECT *
FROM barpydb.pumps
ORDER BY idx ASC;'''

    fluid_names = 'SELECT fluid FROM barpydb.fluids'
    all_ingredient_name_query = 'SELECT name FROM cocktails.ingredients;'

    def __init__(self):
        while True:
            try:
                self.conn = DoltConnection(user="barpy", database="cocktails", auto_commit=True)
                self.conn.connect()
                return
            except:
                pass

    def query_possible_recipes(self):
        rows, count = self.conn.query(DB.possible_recipes_query)
        return rows

    def get_pump_info(self):
        rows, count = self.conn.query(DB.get_pump_info_query)
        return rows

    def get_ingredients(self):
        rows, count = self.conn.query(DB.all_ingredient_name_query)
        return rows

    def get_fluids(self):
        rows, count = self.conn.query(DB.fluid_names)
        return rows

    def update_fluids(self, idx_to_fluids):
        query_str_template = "UPDATE barpydb.fluids SET fluid = '%s' where idx = %d"
        total_count = 0
        for idx, fluid in idx_to_fluids.items():
            rows, count = self.conn.query(query_str_template % (fluid, idx))
            total_count += count

        return total_count

    def query_pins(self):
        query_str = "SELECT * FROM pumps;"
        rows, count = self.conn.query(query_str)

        pump_pins = [int(row['pin']) for row in rows]
        button_pins = [int(row['button_pin']) for row in rows]

        return pump_pins, button_pins

