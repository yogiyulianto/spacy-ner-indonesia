# import necessary libraries to get the data
import requests
import html5lib
from bs4 import BeautifulSoup as bs
from nltk.tokenize import sent_tokenize
import pandas as pd

link = 'https://republika.co.id/berita/qcsbt4383/akhlak-sebagai-emcore-valueem-bumn-erick-thohir-bismillah' #'https://ekonomi-islam.com/tag/teori-teori-ekonomi-islam/'
req = requests.get(link)
soup = bs(req.content, 'html5lib')

paragraphs = soup.findAll('p')

text = []
for p in paragraphs:
  text.append(p.text)

text_ready = ' '.join(text[5:7])
annotations = sorted([
               'peternakan'
               ])
from BIOtagging import text_to_tagReadyDF, convert_to_spaCyformat

tagready_df = text_to_tagReadyDF(pd.Series([text_ready]), isCSV=False)

link_for_save = "C:/Users/userk/OneDrive/Documents/development/research/NER/spaCy-NER/text_tagged.csv"
tagready_df.to_csv(link_for_save, index=False)

# import BIO-tagged csv file
link_BIOtagged_file = "C:/Users/userk/OneDrive/Documents/development/research/NER/spaCy-NER/text_tagged_pti.csv"
df_tagged = pd.read_csv(link_BIOtagged_file)
# lowercase value on column BIO_tag_0
df_tagged['BIO_tag_0'] = df_tagged['BIO_tag_0'].str.lower()
# delete rows with value 'B-nama, I-nama' on column BIO_tag_0
df_tagged = df_tagged[df_tagged['BIO_tag_0'] != 'b-nama']
df_tagged = df_tagged[df_tagged['BIO_tag_0'] != 'i-nama']
BIO_tag_0_list = []
token_0_list = []
for i in range(len(df_tagged)):
  # add bio_tag_0 to list
  BIO_tag_0_list.append(df_tagged['BIO_tag_0'][i])
  BIO_tag_0_list.append('O')
  token_0_list.append(df_tagged['token_0'][i])
  token_0_list.append(' ')
# create new dataframe
df_tagged_new = pd.DataFrame({'token_0': token_0_list, 'BIO_tag_0': BIO_tag_0_list})
train_data = convert_to_spaCyformat(df_tagged, annotations)
from train_spacy import train_spacy

model, loss = train_spacy([train_data], 100) # using 100 iterations
# Save our trained model
modelfile = input("Enter your Model Name: ")
model.to_disk(modelfile)



