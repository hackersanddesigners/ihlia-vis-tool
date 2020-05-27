# ihlia visualization tool

## intro

these scripts do the following:
1. `get-records.py`, fetch all the records from the OBA library API with keyword `Bibliotheek=IHLIA`, and save it to a json file inside `data` folder
2. `get-gender.py`, read over the above records and query `wikidata` to lookup the authors’ gender from each record, then write another file with each record from with the new gender data;
  - if `wikidata` does not found the author name, the gender field is set to `not-found`

## prerequisites

- an API key for the zoeken.oba.nl API (ask H&D)

## usage

before doing anything, you need to place your API key in a `.env` file like so:

```
oba_api_key=aaaabbbbcccc  # replace with the actual API key
```

all code runs with `python 3.7.3`. the list of packages needed are listed in the `Pipfile`. we use [pipenv](https://pipenv.pypa.io/en/latest/) to manage the python environment. use whatever fits your workflow, as long as you install the packages.

if using `pipenv`:

```
# install packages
$ pipenv install

# activate python environment
$ pipenv shell
```

then, make a new folder called `data`:

```
$ mkdir data
```

### to fetch all the records

```
$ python get-records.py IHLIA
```

### to update the records with gender data

```
$ python get-gender.py <name-of-the-file-with-records>
```

the script picks the file in the data folder directly, just pass the filename. for example:

```
$ python get-gender.py IHLIA_2020-05-25-234454
```

a new file named `IHLIA-<timestamp>-update.json` should appear in the `data` folder.

## current limits, to improve

many records from the OBA APIs / IHLIA have no authors field. more double-checking should be done in here.

lots of author names are not found on `wikidata`. the current code does not handle data with a fallback to a different source, so the gender field gets set to `not-found`.

## options

when querying `wikidata` in `get-gender.py`, currently the `&sites=` parameters (line 15) is hard-coded to `nlwiki`. changing that to `enwiki` did not improve the results, but should be kept into account for further experimentation.

in the same, way, on line 33, the `props` passed when querying for the author are hard-coded, they could possibly be changed and adapted to something else.
