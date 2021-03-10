from flask import Flask


app = Flask("barpy")


@app.route('/', methods=['get'])
def get_default_page():
    return '{}'