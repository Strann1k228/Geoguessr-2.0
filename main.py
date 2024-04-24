from flask import *
import sys
import requests
import os
from random import *
from geopy.distance import geodesic

api_server = "http://static-maps.yandex.ru/1.x/"
delta_l = ["0.0", "0.001", "0.002", "0.003", "0.006", "0.011", "0.021", "0.042", "0.083", "0.166", "0.332", "0.664",
           "1.327", "2.652", "5.295", "10.521", "20.523", "37.416"]
lon = "65.996826"
lat = "57.843589"
delta = "37.416"
map_type = "map"
m_types = ["map", "sat"]
point = None
line = None
p_coords, r_p_coords = None, None
img_path = "static/download.jpg"
total = 0
n_of_picture = 10
checked = None
result = None
params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
    "l": map_type,
    "pt": point,
    "pl": line
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


def conclusion(rasst):
    global total, checked
    max_b, distance = 100, int(rasst)
    total_b = max_b - (distance // 100)
    if total_b < 0:
        total_b = 0
    total += total_b
    checked = True
    print(total)


create_map(params)

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', image_path=img_path, result_km=f"{result} km")


@app.route("/-", methods=["POST"])
def minus():
    global delta
    delta = delta_l[delta_l.index(delta) + 1] if delta_l.index(delta) != len(delta_l) - 1 else delta
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point,
        "pl": line
    }
    create_map(params)
    return render_template('base.html', image_path=img_path, result_km=f"{result} km")


@app.route("/+", methods=["POST"])
def plus():
    global delta
    delta = delta_l[delta_l.index(delta) - 1] if delta_l.index(delta) != 0 else delta
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point,
        "pl": line
    }
    create_map(params)
    return render_template('base.html', image_path=img_path, result_km=f"{result} km")


@app.route("/UP", methods=["POST"])
def UP():
    global lat
    lat = str(float(lat) + float(delta) / 2) if float(lat) + float(delta) / 2 < 85 else str(-float(lat))
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point,
        "pl": line
    }
    create_map(params)
    return render_template('base.html', image_path=img_path, result_km=f"{result} km")


@app.route("/DOWN", methods=["POST"])
def DOWN():
    global lat
    lat = str(float(lat) - float(delta) / 2) if float(lat) - float(delta) / 2 > -85 else str(-float(lat))
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point,
        "pl": line
    }
    create_map(params)
    return render_template('base.html', image_path=img_path, result_km=f"{result} km")


@app.route("/RIGHT", methods=["POST"])
def RIGHT():
    global lon
    lon = str(float(lon) + float(delta) / 2) if float(lon) + float(delta) < 179 else str(-float(lon))
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point,
        "pl": line
    }
    create_map(params)
    return render_template('base.html', image_path=img_path, result_km=f"{result} km")


@app.route("/LEFT", methods=["POST"])
def LEFT():
    global lon
    lon = str(float(lon) - float(delta) / 2) if float(lon) - float(delta) > -179 else str(-float(lon))
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point,
        "pl": line
    }
    create_map(params)
    return render_template('base.html', image_path=img_path, result_km=f"{result} km")


@app.route("/MAP", methods=["POST"])
def change_map():
    global map_type
    map_type = m_types[(m_types.index(map_type) + 1) % 2]
    print(map_type)
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point,
        "pl": line
    }
    create_map(params)
    return render_template('base.html', image_path=img_path, result_km=f"{result} km")


@app.route("/MARK", methods=["POST"])
def place_mark():
    global point, params
    point = f"{params["ll"]},org"
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point,
        "pl": line
    }
    create_map(params)
    return render_template('base.html', image_path=img_path, result_km=f"{result} km")


@app.route("/MARK_R", methods=["POST"])
def remove_mark():
    global point, line
    point, line = None, None
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point,
        "pl": line
    }
    create_map(params)
    return render_template('base.html', image_path=img_path, result_km=f"{result} km")


@app.route("/CHECK", methods=["POST"])
def check():
    global lat, lon, map_type, delta, point, img_path, line, p_coords, r_p_coords, checked, result
    # lat, lon, map_type, delta = "57.843589", "65.996826", "map", "37.416"
    if point is None:
        return render_template('base.html', image_path=img_path, result_km=f"{result} km")
    else:
        right_point = (
            f"{(img_path.split("/")[-1][0:-4]).split(",")[1]},{(img_path.split("/")[-1][0:-4]).split(",")[0]},comma")
        line = f"c:47AB6BF0,{point[0:-4]},{right_point[0:-6]}"
        p_coords = point[0:-4].split(",")[::-1]
        r_p_coords = right_point[0:-6].split(",")[::-1]
        print(str(geodesic(p_coords, r_p_coords)).split(".")[0])
        result = str(geodesic(p_coords, r_p_coords)).split(".")[0]
        # if point != f"{point}~{right_point}":
        #     point = f"{point}~{right_point}"
        # params["pt"] = f"{point}~{right_point}
        print()
        print(point)
        print(right_point)
        print()
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": f"{point}~{right_point}",
        "pl": line
    }
    print(params)
    create_map(params)
    if checked is None:
        conclusion(result)
    else:
        print("already checked")
    return render_template('base.html', image_path=img_path, result_km=f"{result} km")


@app.route("/NEXT", methods=["POST"])
def next():
    global point, line, checked
    point, line, checked = None, None, None
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": map_type,
        "pt": point,
        "pl": line
    }
    create_map(params)
    open_random_map()
    return render_template('base.html', image_path=img_path)


def open_random_map():
    global img_path
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
    # выводим рандомный континент
    main_cont = list(cont_and_countr.keys())[randint(0, len(list(cont_and_countr.keys())) - 1)]
    print(main_cont)
    cntrs = []
    for cntr in os.listdir(f"static/map_continents/{main_cont}"):
        cntrs.append(cntr)
    # выводим рандомную страну, находящуюся на континенте
    main_cntr = cntrs[randint(0, len(cntrs)) - 1]
    print(main_cntr)
    images = []
    for img in os.listdir(f"static/map_continents/{main_cont}/{main_cntr}"):
        images.append(img)
    main_image = images[randint(0, len(images)) - 1]
    print(main_image)
    print(f"static/map_continents/{main_cont}/{main_cntr}/{main_image}")
    if f"static/map_continents/{main_cont}/{main_cntr}/{main_image}" == img_path:
        open_random_map()
    else:
        img_path = f"static/map_continents/{main_cont}/{main_cntr}/{main_image}"


open_random_map()

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
