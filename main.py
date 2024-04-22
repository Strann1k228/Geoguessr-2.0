from flask import *
import sys
import requests
import os
from random import *


api_server = "http://static-maps.yandex.ru/1.x/"
delta_l = ["0.0", "0.001", "0.002", "0.003", "0.006", "0.011", "0.021", "0.042", "0.083", "0.166", "0.332", "0.664", "1.327", "2.652", "5.295", "10.521", "20.523", "37.416"]
lon = "65.996826"
lat = "57.843589"
delta = "37.416"
map_type = "map"
m_types = ["map", "sat"]
point = None
params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
    "l": map_type,
    "pt": point
}


def create_map(pr):
    response = requests.get(api_server, params=pr)
    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map0_file = "map0.png"
    with open(f"static/{map0_file}", "wb") as file:
        file.write(response.content)


create_map(params)


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')

@app.route("/-", methods=["POST"])
def minus():
    global delta
    delta = delta_l[delta_l.index(delta) + 1] if delta_l.index(delta) != len(delta_l) - 1 else delta
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point
    }
    create_map(params)
    return render_template('base.html')

@app.route("/+", methods=["POST"])
def plus():
    global delta
    delta = delta_l[delta_l.index(delta) - 1] if delta_l.index(delta) != 0 else delta
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point
    }
    create_map(params)
    return render_template('base.html')


@app.route("/UP", methods=["POST"])
def UP():
    global lat
    lat = str(float(lat) + float(delta) / 2) if float(lat) + float(delta) / 2 < 85 else str(-float(lat))
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point
    }
    create_map(params)
    return render_template('base.html')


@app.route("/DOWN", methods=["POST"])
def DOWN():
    global lat
    lat = str(float(lat) - float(delta) / 2) if float(lat) - float(delta) / 2 > -85 else str(-float(lat))
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point
    }
    create_map(params)
    return render_template('base.html')


@app.route("/RIGHT", methods=["POST"])
def RIGHT():
    global lon
    lon = str(float(lon) + float(delta) / 2) if float(lon) + float(delta) < 179 else str(-float(lon))
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point
    }
    create_map(params)
    return render_template('base.html')


@app.route("/LEFT", methods=["POST"])
def LEFT():
    global lon
    lon = str(float(lon) - float(delta) / 2) if float(lon) - float(delta) > -179 else str(-float(lon))
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point
    }
    create_map(params)
    return render_template('base.html')


@app.route("/MAP", methods=["POST"])
def change_map():
    global map_type
    map_type = m_types[(m_types.index(map_type) + 1) % 2]
    print(map_type)
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point
    }
    create_map(params)
    return render_template('base.html')

@app.route("/MARK", methods=["POST"])
def place_mark():
    global point, params
    point = f"{params["ll"]},flag"
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point
    }
    create_map(params)
    return render_template('base.html')

@app.route("/MARK_R", methods=["POST"])
def remove_mark():
    global point
    point = None
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),

        "l": map_type,
        "pt": point
    }
    create_map(params)
    return render_template('base.html')


def open_random_map():
    # создание словаря стран и континентов
    continents, cont_and_countr = [], {}
    for file in os.listdir("static/map_continents"):
        continents.append(file)
    for i in continents:
        countries = []
        for file in os.listdir(f"static/map_continents/{i}"):
            countries.append(file)
        cont_and_countr[i] = countries
    print(cont_and_countr)

    # выводим рандомную страну
    print(list(cont_and_countr.keys())[randint(0, len(list(cont_and_countr.keys())) - 1)])


open_random_map()

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
