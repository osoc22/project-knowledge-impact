import pandas as pd
import requests

from backend.doi_request_fris import get_abstract_fris, get_author_fris, get_title_fris, get_year_fris, make_request_doi_fris
from backend.profile_fris import get_publications_fris, get_uuid_fris, make_request_orcid_fris, make_request_uuid_fris

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


def filter_recs_fris(doi):
    """
    :param doi: '10.1016/j.foodchem.2022.132915' (example format)
    :return: list of dois that cite doi and are in FRIS
    """
    dois = get_citations_doi(doi)
    fris_dois = []
    for d in dois:
        soapResult = make_request_doi_fris(d, 0, 3, 0)
        if len(soapResult['_value_1']) != 0:
            fris_dois += [d]
    return fris_dois

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

    matrix = pd.Series(dois, num)
    matrix.sort_index(ascending=False, inplace=True)
    dois_sorted = matrix.values
    return dois_sorted


def sort_recs_year(dois):
    """
    :param dois: list of dois
    :return: list of dois sorted by year (most recent to least)
    """
    return

def get_recs_title_author_year_abstract_fris(doi):#suggested papers to read
    """
    :param doi: '10.1016/j.foodchem.2022.132915' (example format)
    :return: lists of disctionaries with keys: title, authors, years and abstracts from all dois citing doi, sorted by popularity
    """
    dois = filter_recs_fris(doi)
    dois_sorted = sort_recs_popularity(dois)
    output=[]
    for d in dois_sorted:
        soapResult = make_request_doi_fris(d, 0, 3, 0)
        if len(soapResult['_value_1']) != 0:
            try:
                soapResult['_value_1'][0]['journalContribution']
                data={}
                data["title"] =get_title_fris(soapResult)
                data["year"] =get_year_fris(soapResult)
                data["abstract"] =get_abstract_fris(soapResult)
                data["author"]=get_author_fris(soapResult)
                output.append(data)
            except KeyError as e:
                print(e)
    return output

def get_recs_author_fris(doi): #connecting feature
    """
    :param doi: '10.1016/j.foodchem.2022.132915' (example format)
    :return: list of authors from all dois citing doi (without repetition, without specific order)
    """
    dois = get_citations_doi(doi)
    fris_authors = []
    for d in dois:
        soapResult = make_request_doi_fris(d, 0, 3, 0)
        if len(soapResult['_value_1']) != 0:
            authors = get_author_fris(soapResult)
            for a in authors:
                fris_authors += [a]
    fris_authors = list(dict.fromkeys(fris_authors)) #eliminates duplicates
    return fris_authors


def get_all_recs_author(orcid):
    """
        :param ORCID: '0000-0003-4706-7950' (example format)
        :return: list of authors from all dois citing all research papers published by orcid id (without repetition, without specific order)
        """
    soapResult = make_request_orcid_fris(orcid, 0, 2, 0)
    uuid = get_uuid_fris(soapResult)
    soapResult2 = make_request_uuid_fris(uuid, 0, 15, 0)
    dois = get_publications_fris(soapResult2)
    fris_authors = []
    for d in dois:
        authors = get_recs_author_fris(d)
        for a in authors:
            fris_authors += [a]
    fris_authors = list(dict.fromkeys(fris_authors))
    return fris_authors

def get_all_seggested_papers(orcid):
    """
        :param ORCID: '0000-0003-4706-7950' (example format)
        :return: list of authors from all dois citing all research papers published by orcid id (without repetition, without specific order)
        """
    soapResult = make_request_orcid_fris(orcid, 0, 2, 0)
    uuid = get_uuid_fris(soapResult)
    soapResult2 = make_request_uuid_fris(uuid, 0, 15, 0)
    dois = get_publications_fris(soapResult2)
    papers=[]
    for d in dois:
        papers.append(get_recs_title_author_year_abstract_fris(d))
    return papers

