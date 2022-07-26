from typing import List

import zeep

def make_request_doi_fris(doi: str, pageNumber: int = 0, pageSize: int = 15) -> zeep.AnyObject:
    """
    :param doi: doi from which to get xml response (example format: '10.1016/j.foodchem.2022.132915')
    :param pageNumber: requested page number
    :param pageSize: quantity of results returned in each page
    :return: xml response from doi (zeep object) (contains info such as title, author(s), year and abstract)
            - if doi is not found in FRIS -> returns xml response with '_value_1': [] and 'total': 0 (empty)
    """
    data = {
        "criteria": {
            "window": {
                "pageSize": "",
                "pageNumber": "",
                "orderings": {
                    "order": {
                        "id": "entity.created",
                        "locale": "*",
                        "direction": "ASCENDING"
                    }
                }
            },
            "sources": {
                "source": {
                    "authority": "DOI",
                    "identifier": ""
                }
            }
        }
    }

    data['criteria']['window']['pageNumber'] = str(pageNumber)
    data['criteria']['window']['pageSize'] = str(pageSize)
    data['criteria']['sources']['source']['identifier'] = 'https://doi.org/' + str(doi)
    # print(data)
    wsdl = 'https://frisr4.researchportal.be/ws/ResearchOutputServiceFRIS?wsdl'
    settings = zeep.Settings(strict=False, xml_huge_tree=True)
    client = zeep.Client(wsdl=wsdl, settings=settings)
    soapResult = client.service.getResearchOutput(**data)
    return soapResult


def get_title_fris(soapResult: zeep.AnyObject) -> str:
    """
    :param soapResult: xml result of make_request_doi_fris() function (zeep object)
    :return: title of publication (str)
            - if xml result has no title -> returns ''
    """
    try:
        return soapResult['_value_1'][0]['journalContribution']['title']['texts']['text'][0]['_value_1']
    except:
        return ''


def get_author_fris(soapResult: zeep.AnyObject) -> List[str]:
    """
    :param soapResult: xml result of make_request_doi_fris() function (zeep object)
    :return: author(s) of publication (list[str])
            - if xml result has no author -> returns []
    """
    try:
        data = soapResult['_value_1'][0]['journalContribution']['unpaywallDoi']['ZAuthors']
        list_names = []
        for i in range(0, len(data)):
            list_names += [data[i]['given'] + ' ' + data[i]['family']]  # THE GOOD WAY
        return list_names
    except:
        return []


def get_year_fris(soapResult: zeep.AnyObject) -> str:
    """
    :param soapResult: xml result of make_request_doi_fris() function (zeep object)
    :return: year of publication (int)
            - if xml result has no year -> returns ''
    """
    try:
        return soapResult['_value_1'][0]['journalContribution']['publicationYear']
    except:
        return ''


def get_abstract_fris(soapResult: zeep.AnyObject) -> str:
    """
    :param soapResult: xml result of make_request_doi_fris() function (zeep object)
    :return: abstract of publication (str)
            - if xml result has no abstract -> returns ''
    """
    try:
        return soapResult['_value_1'][0]['journalContribution']['researchAbstract']['texts']['text'][0]['_value_1']
    except:
        return ''
