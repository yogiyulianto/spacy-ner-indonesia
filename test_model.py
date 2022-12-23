# import package for displaying NER results
from spacy import load, displacy

# import model
link_to_model = "ner_indo"
loaded_model = load(link_to_model)

# text source: 'https://www.antaranews.com/berita/1584798/erick-tetapkan-akhlak-sebagai-core-value-bumn'
test_text = """Modal Dagang Sayuran Jumirah Modal Dagang Pakan Ternak Cahyo Asri Kriswanti Modal Dagang Warung Sembako SRI NURYATI Modal Dagang Pakaian siti hanafiyah Modal Tani Padi SITI ATIKAH Modal Pupuk FITRI RISTANTI Modal Tani Sayur PERA MITA SARI Modal Pupuk LIAN SIHMIATI Modal Ternak Sapi PURWANTI Modal Dagang Ikan Asin SINTA RAHAYU Modal Dagang Sayuran ARTISNI Modal Tani Karet ASWATI Modal Tani Sawit YANA Modal Dagang Warung Makan LISTI FITRIANI Modal Pupuk YULIANTI Modal Ternak Sapi SITI NUR AMINAH Modal Tani Padi SARIANI Modal Ternak Unggas DEVI FITRIANI Modal Ternak Ikan sukemi Modal Tani Tebu RASMIATI Modal Tani Buah MAGRITA TIWA Modal Dagang Warung Kecil EUIS Modal Tani Padi AMINAH Modal Tani Padi rohimah Modal Beli Pupuk FITRIA NOVITA NINGSIH"""
test_text = "Modal Tani Karet ASWATI"
test_text = test_text.lower()

# show the results
doc = loaded_model(test_text)
print(displacy.render(doc, style="ent"))
print(doc.ents)