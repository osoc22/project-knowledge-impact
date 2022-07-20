import pandas as pd
import requests

from doi_request_fris import make_request_doi_fris, get_title_fris, get_author_fris, get_year_fris, get_abstract_fris
from profile_fris import make_request_orcid_fris, get_publications_fris, get_uuid_fris, make_request_uuid_fris

def get_citations_doi(doi: str):
    """
    :param doi: '10.1016/j.foodchem.2022.132915' (example format)
    :return: list of dois that cite doi
    """
    api_url = "https://w3id.org/oc/index/api/v1/citations/"
    r = requests.get(api_url + doi)
    data = r.json()

    dois = []
    for elem in data:
        dois += [elem['citing'].replace('coci => ', '')]
    return dois

#print(get_citations_doi('10.1080/15325008.2012.749554'))

def filter_recs_fris(doi):
    """
    :param doi: '10.1016/j.foodchem.2022.132915' (example format)
    :return: list of dois that cite doi and are in FRIS
    """
    dois = get_citations_doi(doi)
    fris_dois = []
    for d in dois:
        soapResult = make_request_doi_fris(d, 0, 10, 0)
        if len(soapResult['_value_1']) != 0:
            fris_dois += [d]
    return fris_dois

#k = filter_recs_fris('10.1080/15325008.2012.749554')
#print(k)

def sort_recs_popularity(dois):
    """
    :param dois: list of dois
    :return: list of dois sorted by popularity (most popular to least)
    """
    api_url = "https://w3id.org/oc/index/api/v1/citations/"
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

#print(sort_recs_popularity(k))

def sort_recs_year(dois):
    """
    :param dois: list of dois
    :return: list of dois sorted by year (most recent to least)
    """
    return

def get_recs_title_author_year_abstract_fris(doi):
    """
    :param doi: '10.1016/j.foodchem.2022.132915' (example format)
    :return: lists of titles, authors, years and abstracts from all dois citing doi, sorted by popularity
    """
    dois = filter_recs_fris(doi)
    dois_sorted = sort_recs_popularity(dois)
    fris_titles = []
    fris_authors = []
    fris_years = []
    fris_abstracts = []
    for d in dois_sorted:
        soapResult = make_request_doi_fris(d, 0, 10, 0)
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
    """
    :param doi: '10.1016/j.foodchem.2022.132915' (example format)
    :return: list of authors from all dois citing doi (without repetition, without specific order)
    """
    dois = get_citations_doi(doi)
    fris_authors = []
    for d in dois:
        soapResult = make_request_doi_fris(d, 0, 10, 0)
        if len(soapResult['_value_1']) != 0:
            authors = get_author_fris(soapResult)
            for a in authors:
                fris_authors += [a]
    fris_authors = list(dict.fromkeys(fris_authors)) #eliminates duplicates
    return fris_authors

#print(get_recs_author_fris('10.1080/15325008.2012.749554'))

def get_all_recs_author(orcid):
    """
        :param doi: '0000-0003-4706-7950' (example format)
        :return: list of authors from all dois citing all research papers published by orcid id (without repetition, without specific order)
        """
    soapResult = make_request_orcid_fris(orcid, 0, 10, 0)
    uuid = get_uuid_fris(soapResult)
    soapResult2 = make_request_uuid_fris(uuid, 0, 10, 0)
    dois = get_publications_fris(soapResult2)
    fris_authors = []
    for d in dois:
        authors = get_recs_author_fris(d)
        for a in authors:
            fris_authors += [a]
    fris_authors = list(dict.fromkeys(fris_authors))
    return fris_authors

#a = get_all_recs_author('0000-0003-4706-7950')
#print(a)

# soapResult = make_request_orcid_fris(0, 10, 0, '0000-0003-4706-7950')
# dois = get_publications_fris(soapResult)
# print(get_recs_author_fris(dois[0]))
# print(get_recs_author_fris(dois[1]))
# print(get_recs_author_fris(dois[2]))

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
