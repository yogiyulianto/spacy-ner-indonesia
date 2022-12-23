from flask import Flask, jsonify, request
import json
from spacy import load

app = Flask(__name__)

@app.route("/", methods=['GET'])
def all():
    # Opening JSON file
    f = open('data.json')
    data = json.load(f)
    data = data['data']['marketplace']
    result_list = []
    # looping through the data
    for i in data:
        load_id = i['loanId']
        platfrom = 'Amartha'
        peminjam = i['borrowerName']
        lokasi = i['provinceName'] + ', ' + i['areaName']
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
            'tanggal_mulai' : tanggal_mulai,
            'tanggal_selesai' : tanggal_selesai,
            'progress_pendanaan': progress_pendanaan
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