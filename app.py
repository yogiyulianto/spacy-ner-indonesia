from flask import Flask, jsonify, request
import json
from spacy import load
# import the geocoder
import geocoder
from math import sin, cos, sqrt, atan2, radians

app = Flask(__name__)

def get_latlong(location):
    # get the coordinates
    g = geocoder.osm(location)
    # get distance between two points
    latlng = g.latlng
    return latlng

# herversine formula
def get_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

@app.route("/", methods=['GET'])
def all():
    # Opening JSON file
    f = open('data-limit.json')
    data = json.load(f)
    data = data['data']['marketplace']
    result_list = []
    # looping through the data
    for i in data:
        load_id = i['loanId']
        platfrom = 'Amartha'
        peminjam = i['borrowerName']
        lokasi = i['provinceName'] + ', ' + i['areaName']
        lokasi = lokasi.lower()
        lokasi_latlong = get_latlong(lokasi)
        lokasi_awal = get_latlong('yogyakarta')
        jarak = get_distance(lokasi_latlong[0], lokasi_latlong[1], lokasi_awal[0], lokasi_awal[1])
        total_plafond = i['plafond']
        tenor = i['tenor']
        bunga = i['returnOfInvestment'] * 100
        riwayat_sebelumnya = 'Berhasil'
        tkb_platform = 98.76
        type_pendanaan = 'konvensional'
        tanggal_mulai = i['submittedLoanDate']
        # tanggal selesai + 50 from tanggal mulai
        tanggal_selesai = '2023-07-28T00:00:00+07:00'
        progress_pendanaan = 100 - ((i['sisaPlafond']/total_plafond)*100)
        description = i['purpose']
        if jarak > 30:
            jarak_text = 'Jauh'
        else:
            jarak_text = 'Dekat'
        result = {
            'load_id' : load_id,
            'description' : description,
            'platform' : platfrom,
            'peminjam': peminjam,
            'lokasi': lokasi,
            'tenor' : tenor,
            'bunga' : bunga,
            'riwayat_sebelumnya' : riwayat_sebelumnya,
            'tkb_platform' : tkb_platform,
            'type_pendanaan' : type_pendanaan,
            'total_plafond' : i['sisaPlafond'],
            'tanggal_mulai' : tanggal_mulai,
            'tanggal_selesai' : tanggal_selesai,
            'progress_pendanaan': progress_pendanaan,
            'jarak': f'{round(jarak, 2)} Km',
            'jarak_text': jarak_text
        }
        result_list.append(result)
    return jsonify(result_list)
    
@app.route("/ner", methods=['POST'])
def ner():
    description = request.form.get('description')
    # import model
    link_to_model = "ner_indo"
    loaded_model = load(link_to_model)
    description = description.lower()
    # show the results
    doc = loaded_model(description)
    entitas = doc.ents
    if entitas:
        entitas_text = ''
        for x in entitas:
            entitas_text = entitas_text +  ',' + str(x)
        entitas_text = entitas_text[1:]
        result = {
            "status":True,
            "message":"terdapat NER terdeteksi",
            "ner": entitas_text
        }
    else:
        result = {
            "status":False,
            "message":"tidak terdapat NER terdeteksi",
        }
    return result
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)