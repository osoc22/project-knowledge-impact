import pandas as pd
import requests

from doi_request_fris import make_request_doi_fris
from doi_request_fris import get_title_fris
from doi_request_fris import get_author_fris
from doi_request_fris import get_year_fris
from doi_request_fris import get_abstract_fris


def get_citations_doi(doi: str):
    api_url = "https://w3id.org/oc/index/api/v1/citations/"
    r = requests.get(api_url + doi)
    data = r.json()

    dois = []
    for elem in data:
        dois += [elem['citing'].replace('coci => ', '')]

    num = []
    for elem in dois:
        r2 = requests.get(api_url + elem)
        data2 = r2.json()
        num += [len(data2)]
    #print(num)

    matrix = pd.Series(dois, num)
    matrix.sort_index(ascending=False, inplace=True)
    dois_sorted = matrix.values
    return dois_sorted

def get_recs_doi_fris(doi):
    dois_sorted = get_citations_doi(doi)
    fris_dois = []
    for d in dois_sorted:
        soapResult = make_request_doi_fris(0, 10, 0, d)
        if len(soapResult['_value_1']) != 0:
            fris_dois += [d]
    return fris_dois

def get_recs_title_author_year_abstract_fris(doi):
    dois_sorted = get_citations_doi(doi)
    fris_titles = []
    fris_authors = []
    fris_years = []
    fris_abstracts = []
    for d in dois_sorted:
        soapResult = make_request_doi_fris(0, 10, 0, d)
        if len(soapResult['_value_1']) != 0:
            fris_titles += [get_title_fris(soapResult)]
            fris_authors += [get_author_fris(soapResult)]
            fris_years += [get_year_fris(soapResult)]
            fris_abstracts += [get_abstract_fris(soapResult)]

    return fris_titles, fris_authors, fris_years, fris_abstracts

#fris_titles, fris_authors, fris_years, fris_abstracts = get_recs_title_author_year_abstract_fris('10.1080/15325008.2012.749554')
#
#print(fris_authors)
#print(fris_titles)
#print(fris_years)
#print(fris_abstracts)

def get_recs_author_fris(doi): #connecting feature
    dois_sorted = get_citations_doi(doi)
    fris_authors = []
    for d in dois_sorted:
        soapResult = make_request_doi_fris(0, 10, 0, d)
        if len(soapResult['_value_1']) != 0:
            authors = get_author_fris(soapResult)
            for a in authors:
                fris_authors += [a]
    fris_authors = list(dict.fromkeys(fris_authors)) #eliminates duplicates
    return fris_authors

print(get_recs_author_fris('10.1080/15325008.2012.749554'))

# request = make_request_doi_fris(0,10,0,"10.3390/en10101500")
# print(get_author_fris(request))
# print(get_title_fris(request))

# doi = "10.1080/15325008.2012.749554"
# dois_sorted = get_citations_doi(doi)
# fris_titles = []
# fris_authors = []
# for d in dois_sorted:
#     soapResult = make_request_doi_fris(0, 10, 0, d)
#     if len(soapResult['_value_1']) != 0:
#         fris_titles += [get_title_fris(soapResult)]
#         fris_authors += [get_author_fris(soapResult)]
# print(fris_authors)
# print(fris_titles)