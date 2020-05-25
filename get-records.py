# -- search for a book in the oba api
import os
from dotenv import load_dotenv
import sys
import requests
import xmltodict
import json
import time

load_dotenv()

# -- get dict of python environment variables loaded from `.env`
oba_api = os.getenv('oba_api_key')

result_index = []
query = "https://zoeken.oba.nl/api/v1/search/?authorization=" + oba_api + "&q=Bibliotheek=" + sys.argv[1]
result = requests.get(query)
data = result.text
data = xmltodict.parse(data)['aquabrowser']

records_total = int
for k, v in data.items():
  if (k == 'meta'):
    records_total = int(v['count'])

# we get all the records in each page of result
# little math, each page contains 20 records:
# we divide the total count (`records_total`) by 20 and round up
# then loop over it
count = round(records_total / 20)
for i in range(0, count):
  for k, v in data.items():
    if (k == 'results'):
      for item in v['result']:

        record = {'title': '',
                  'authors': [],
                  'publishers': [],
                  'year': '',
                  'summary': ''}

        #-- title
        try:
          for k, v in item['titles']['short-title'].items():
            if k == '#text':
              record['title'] = v
        except Exception as e:
          print('title-field missing', e)

        #-- authors
        try:
          for k, v in item['authors'].items():
            record['authors'].append(v['@search-term'])
        except Exception as e:
          print('author-field missing', e)

        #-- year and publishers
        try:
          for k, v in item['publication']['year'].items():
            if k == '#text':
              record['year'] = v

          for k, v in item['publication']['publishers'].items():
            record['publishers'].append(v['@search-term'])

        except Exception as e:
          print('pub-field is missing', e)

        #-- summaries
        try:
          for k, v in item['summaries'].items():
            record['summary'] = v['#text']
        except Exception as e:
          print('summaries-field is missing', e)

        # ---
        result_index.append(record)

# print('\n---\n', result_index)

timestamp = time.strftime("%Y-%m-%d-%H%M%S")
filename = sys.argv[1] + '_' + timestamp
with open('data/%s.json' % filename, 'w') as fp:
  json.dump(result_index, fp)
  print('dumped to json!')
