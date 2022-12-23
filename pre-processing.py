import pandas as pd

df = pd.read_excel('C:/Users/userk/OneDrive/Documents/development/research/NER/spaCy-NER/dataset.xlsx')
# lower case value on column desc
df['desc'] = df['desc'].str.lower()
# tokenize value on column desc
df['desc'] = df['desc'].apply(lambda x: x.split())
desc_list = []
bio_tagging_list = []
ner_tagging_list = ['sayuran','ternak','unggas','tani','padi','pupuk','sayur','sapi','ikan','asin','karet','sawit' ,'tebu','buah']
# loop through each row in df
for i in range(len(df)):
  # loop through each token in each row
  for j in range(len(df['desc'][i])):
    desc = df['desc'][i][j]
    # if desc is in ner_tagging_list
    if desc in ner_tagging_list:
      # add desc to desc_list
      desc_list.append(desc)
      # add 'B-nama' to bio_tagging_list
      bio_tagging_list.append('B-peternakan')
    else:
        # add desc to desc_list
        desc_list.append(desc)
        # add 'O' to bio_tagging_list
        bio_tagging_list.append('O')
    desc_list.append(' ')
    bio_tagging_list.append('O')
    
# create new dataframe
df = pd.DataFrame({'token_0': desc_list, 'BIO_tag_0': bio_tagging_list})
# save to csv
df.to_csv('C:/Users/userk/OneDrive/Documents/development/research/NER/spaCy-NER/text_tagged_pti.csv', index=False)