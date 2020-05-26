import sys
import requests
import json
import time

# -- read file
fn = sys.argv[1]

result_index = []

def lookup_gender(author_list):
  gender_list = []

  for author in author_list:
    query_author = url_root + '&sites=nlwiki' + '&titles=' + author
    result = requests.get(query_author)
    data = json.loads(result.text)

    author_id = ''
    if '-1' in data['entities']:
      # print('\n\nAUTHOR NOT FOUND', data['entities'])
      gender_list.append('not-found')

    else:
      for k, v in data['entities'].items():
        # print('\n\n AUTHOR FOUND!', v['title'])
        author_id = v['title']

        # get full author info by querying id
        # https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids=Q20978355&props=labels|descriptions|claims&languages=en

        if author_id != '':
          query_gender = url_root + '&ids=' + author_id + '&props=labels|descriptions|claims&languages=en'
          result = requests.get(query_gender)
          data = json.loads(result.text)

          gender_id = ''
          for k, v in data['entities'].items():
              gender_id = v['claims']['P21'][0]['mainsnak']['datavalue']['value']['id']

              # ref <https://www.wikidata.org/wiki/Property:P21>
              gender = {'Q6581097': 'male',
                        'Q6581072': 'female',
                        'Q1097630': 'intersex',
                        'Q1052281': 'transgender female',
                        'Q2449503': 'transgender male'}.get(gender_id, 'unknown')

          gender_list.append(gender)

  return gender_list


with open('data/%s.json' % fn) as data:
  d = json.load(data)
  url_root = 'https://www.wikidata.org/w/api.php?action=wbgetentities&format=json'

  # q = 'https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&sites=nlwiki&titles=Marian%20Bakker'

  for record in d:
    try:
      # loop over each author in the record
      gender_l = lookup_gender(record['authors'])
      record['gender'] = gender_l

      result_index.append(record)

    except Exception as e:
      print('ERR =>', e)


timestamp = time.strftime("%Y-%m-%d-%H%M%S")
filename = sys.argv[1] + '_' + timestamp
with open('data/%s-update.json' % filename, 'w') as fp:
  json.dump(result_index, fp)
  print('dumped to json!')
