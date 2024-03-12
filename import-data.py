import sys
import os
import json
from pprint import pprint
from collections import Counter

def hashsplitter(item):
    try:
        return item.split(' # ')
    except Exception:
        import pdb; pdb.set_trace()

input_path = sys.argv[1]
topic = sys.argv[2]

with open(input_path, 'r') as f:
    data = json.load(f)

counter = Counter()

#find each term in terms which doesn't get included in the generated json
#change the python to include each term (skipping because no description)
#json will have items empty apart from description eg gehoorproblemen
#add a key to those items which is show = false
#change js where it creates rectangles (disability line 65)to skip those items with show false

terms = { 'disability': ["gehandicapten",
                 "handicaps",
                 "handicapisme",
                 "visueel_gehandicapten",
                 "visuele_handicaps",
                 "lichamelijk_gehandicapten",
                 "lichamelijke_handicaps",
                 "auditief_gehandicapten",
                 "doven",
                 "gehoorproblemen",
                 "verstandelijk_gehandicapten",
                 "gehandicaptenstudies",
                 "lichamelijke_stoornissen",
                 "lichamelijke gezondheid"],
          'gender': ["gender",
                     "genderidentiteit",
                     "genderisme",
                     "genderminderheden",
                     "vrouwen",
                     "mannen",
                     "transgenders",
                     "genderdiversiteit",
                     "genderrelaties", "genderstudies",
                     "interseks"],
          'race': ["culturen",
             "etnische_groepen",
             "zwarten",
             "niet-witte mensen",
             "inheemse_volken",
             "blanken",
             "migranten",
             "vluchtelingen",
             "etnische_studies",
             "etnische_verhoudingen",
             "kolonialisme",
             "racisme"],
          'sexuality': ["seksuele_identiteit",
                        "seksuele_orientatie",
                        "seksuele_minderheden",
                        "biseksuelen",
                        "homomannen",
                        "lesbische_vrouwen",
                        "LHBTI"],
          'structural-oppression': ["racisme",
                                 "seksisme",
                                 "genderisme",
                                 "handicapisme",
                                 "klassisme",
                                 "homofobie",
                                 "transfobie",
                                 "discriminatie",
                                 "pesten",
                                 "etnische_verhoudingen"]
         }

publisher_cleaner = ["s.n.", "s.n.]", "[s.n.]", "s.n.] "]

print (len(data))

newdata = []

for item in data:

    if 'description' in item:
        if not item['description']:
            continue
        item['description'] = hashsplitter(item['description'])

        newlist = []
        otherdescr = []
        found = False
        publisher_found = False
        for description in item['description']:
            if description in terms[topic]:
                if 'publisher' in item and item['publisher'] not in publisher_cleaner:
                    if not item['publisher']:
                        continue

                    if not publisher_found:
                        publisher = item['publisher']
                        if publisher in counter:
                            counter[publisher] +=1
                            publisher_found = True
                        else:
                            counter[publisher] = 1
                            publisher_found = True
                newlist.append(description)
                found = True
            else:
                otherdescr.append(description)


            if found:
                if len(newlist) >= 2:
                    item['description_second'] = newlist[1]
                    item['other_descriptions'] = otherdescr
                else:
                    item['description'] = newlist[0]
                    item['other_descriptions'] = otherdescr
                # print (newlist[0])
                newdata.append(item)

            publisher_found = False

for object in newdata:
    newdescr = []
    for term in terms[topic]:
        if term not in object['description']:
            newdescr.append(term)
for descr in newdescr:
    newitem = {'description': descr, 'show': 'false'}
    newdata.append(newitem)
# import pdb; pdb.set_trace()


most_common = [i[0] for i in counter.most_common(800)]
# print(most_common)
print(([x for x in counter.most_common(800)]))

# import pdb; pdb.set_trace()
extranewdata = []
for item in newdata:
    # import pdb; pdb.set_trace()
    if 'publisher' in item:
        if not item['publisher']:
            continue
        # import pdb; pdb.set_trace()
        if item['publisher'] in most_common:
            extranewdata.append(item)
    elif item['description'] in newdescr:
        extranewdata.append(item)



with open('data/dataset_%s.json' % topic, 'w') as f:
    f.write(json.dumps(extranewdata))

print(extranewdata)
# import pdb; pdb.set_trace()
print (len(extranewdata))
