from flask import Flask, jsonify
from lyrics import search
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


app.config.update(
    SECRET_KEY='abc123',
    TEMPLATES_AUTO_RELOAD=True
)


@app.route("/<string:artist>/<string:title>")
def show(artist, title):
    results = search(artist, title)

    return jsonify(results)
