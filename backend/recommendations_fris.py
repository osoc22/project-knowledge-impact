import pandas as pd
import requests

from typing import List
from doi_request_fris import get_abstract_fris, get_author_fris, get_title_fris, get_year_fris, make_request_doi_fris
from profile_fris import get_publications_fris, get_uuid_fris, make_request_orcid_fris, make_request_uuid_fris

def get_citations_doi(doi: str) -> List[str]:
    """
    :param doi: doi from which to get citing dois (example format: '10.1016/j.foodchem.2022.132915')
    :return: list of dois that cite doi and figure in opencitations.net
             - if doi is not found in opencitations.net or no other dois cite it -> returns []
    """
    api_url = "https://w3id.org/oc/index/api/v1/citations/" # opencitations.net endpoint
    r = requests.get(api_url + doi)
    data = r.json()

    dois = []
    for elem in data:
        dois += [elem['citing'].replace('coci => ', '')] # clean results
    return dois


def filter_recs_fris(doi: str) -> List[str]:
    """
    :param doi: doi from which to get citing dois (example format: '10.1016/j.foodchem.2022.132915')
    :return: list of dois that cite doi and figure in opencitations.net AND in FRIS.
             - if any of conditions mentioned in get_citations_doi() take place -> returns []
             - if no citing dois figure in FRIS -> returns []
    """
    dois = get_citations_doi(doi)
    fris_dois = []
    for d in dois:
        soapResult = make_request_doi_fris(d, 0, 3, 0)
        if len(soapResult['_value_1']) != 0: # check if response is empty
            fris_dois += [d]
    return fris_dois


def sort_recs_popularity(dois: List[str]) -> List[str]:
    """
    :param dois: list of dois to sort by popularity (number of times cited according to opencitations.net)
    :return: list of dois sorted by popularity (most popular to least)
            - if any doi is not found in opencitations.net or no other dois cite it -> it appears last on the returned list
    """
    api_url = "https://w3id.org/oc/index/api/v1/citations/"
    num = []
    for elem in dois:
        r2 = requests.get(api_url + elem)
        data2 = r2.json()
        num += [len(data2)]

    matrix = pd.Series(dois, num)
    matrix.sort_index(ascending=False, inplace=True) # sort by popularity
    dois_sorted = list(matrix.values)
    return dois_sorted


def sort_recs_year(dois: List[str]) -> List[str]:
    """
    :param dois: list of dois to sort by year
    :return: list of dois sorted by year (most recent to least)
    """
    return dois


def get_recs_title_author_year_abstract_fris(doi: str) -> List[dict]: # suggests other research papers
    """
    :param doi: doi from which to get research paper recommendations (example format: '10.1016/j.foodchem.2022.132915')
    :return: list of dictionaries with info from each citing doi (title, author(s), year and abstract), sorted by popularity
             - if any of conditions mentioned in functions used take place -> returns []
             - if no doi is a research paper -> returns []
    """
    dois = filter_recs_fris(doi)
    dois_sorted = sort_recs_popularity(dois)
    output = []
    for d in dois_sorted:
        soapResult = make_request_doi_fris(d, 0, 3, 0)
        try:
            soapResult['_value_1'][0]['journalContribution'] # check if response is a research paper
            data = {}
            data["title"] = get_title_fris(soapResult)
            data["year"] = get_year_fris(soapResult)
            data["abstract"] = get_abstract_fris(soapResult)
            data["author"] = get_author_fris(soapResult)
            output.append(data)
        except KeyError:
            pass # if it is not, then skip
    return output


def get_all_recs_title_author_year_abstract(orcid: str) -> List[dict]: # suggests other research papers
    """
        :param ORCID: orcid from which to get research paper recommendations (example format: '0000-0003-4706-7950')
        :return: list of dictionaries with info from each citing doi (title, author(s), year and abstract), sorted by popularity
                 - if any of conditions mentioned in functions used take place -> returns []
        """
    soapResult = make_request_orcid_fris(orcid, 0, 2, 0)
    uuid = get_uuid_fris(soapResult)
    soapResult2 = make_request_uuid_fris(uuid, 0, 15, 0)
    dois = get_publications_fris(soapResult2)
    fris_papers = []
    for d in dois:
        papers = get_recs_title_author_year_abstract_fris(d)
        for p in papers:
            fris_papers.append(p)
    # suggestion: eliminate duplicates (dict type objects)
    return fris_papers

# print(get_all_recs_title_author_year_abstract('0000-0003-4706-7950'))

def get_recs_author_fris(doi: str) -> List[str]: # suggests other authors (those that have noticed/cited researcher)
    """
    :param doi: doi from which to get author recommendations (example format: '10.1016/j.foodchem.2022.132915')
    :return: list of authors from all citing dois (without repetition, without specific order)
             - if any of conditions mentioned in functions used take place -> returns []
    """
    dois = filter_recs_fris(doi)
    fris_authors = []
    for d in dois:
        soapResult = make_request_doi_fris(d, 0, 3, 0)
        authors = get_author_fris(soapResult)
        for a in authors:
            fris_authors += [a]
    fris_authors = list(dict.fromkeys(fris_authors)) # eliminate duplicates
    return fris_authors


def get_all_recs_author(orcid: str) -> List[str]: # suggests other authors (those that have noticed/cited researcher)
    """
        :param ORCID: orcid from which to get author recommendations (example format: '0000-0003-4706-7950')
        :return: list of authors from all dois citing all research papers published by orcid id (without repetition, without specific order)
                 - if any of conditions mentioned in get_recs_author_fris() take place -> returns []
                 if orcid id doesnt exist
                 if researcher has no publications
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
    fris_authors = list(dict.fromkeys(fris_authors)) # eliminate duplicates
    return fris_authors

#print(get_all_recs_author('0000-0003-4706-7950'))


