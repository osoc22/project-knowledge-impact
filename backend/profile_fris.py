
import zeep

from typing import List

from doi_request_fris import get_abstract_fris, get_author_fris, get_title_fris, get_year_fris, make_request_doi_fris

def make_request_orcid_fris(orcid: str, pageNumber: int = 0, pageSize: int = 2) -> zeep.AnyObject:
    """
    :param orcid: orcid from which to get xml response (example format: '0000-0003-4706-7950')
    :param pageNumber: requested page number
    :param pageSize: quantity of results returned in each page
    :return: xml response from orcid (zeep object) (contains info such as uuid, subject, keywords and profile name)
            - if doi is not found in FRIS -> returns xml response with 'person': [] and 'total': 0 (empty)
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
                    "authority": "ORCID",
                    "identifier": ""
                }
            }
        }
    }
    data['criteria']['window']['pageNumber'] = str(pageNumber)
    data['criteria']['window']['pageSize'] = str(pageSize)
    data['criteria']['sources']['source']['identifier'] = orcid
    wsdl = 'https://frisr4.researchportal.be/ws/PersonServiceFRIS?wsdl'
    settings = zeep.Settings(strict=False, xml_huge_tree=True)
    client = zeep.Client(wsdl=wsdl, settings=settings)
    soapResult = client.service.getPersons(**data)
    return soapResult


def make_request_uuid_fris(uuid: str, pageNumber: int = 0, pageSize: int = 15) -> zeep.AnyObject:
    """
    :param uuid: uuid from which to get xml response (example format: '1727939a-543a-4184-841f-944ee16db418')
    :param pageNumber: requested page number
    :param pageSize: quantity of results returned in each page
    :return: xml response of uuid (zeep object) (contains info such as research papers published)
            - if uuid is not found in FRIS -> returns xml response with '_value_1': {} and 'total': 0 (empty)
    """
    data2 = {
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
            "associatedPersons": {
                "identifier": ""
            }
        }
    }
    data2['criteria']['window']['pageNumber'] = str(pageNumber)
    data2['criteria']['window']['pageSize'] = str(pageSize)
    data2['criteria']['associatedPersons']['identifier'] = uuid
    wsdl = 'https://frisr4.researchportal.be/ws/ResearchOutputServiceFRIS?wsdl'
    settings = zeep.Settings(strict=False, xml_huge_tree=True)
    client = zeep.Client(wsdl=wsdl, settings=settings)
    soapResult2 = client.service.getResearchOutput(**data2)
    return soapResult2


def get_uuid_fris(soapResult: zeep.AnyObject) -> str:
    """
    :param soapResult: xml result of make_request_orcid_fris() function (zeep object)
    :return: uuid associated w the orcid used to generate xml result
            - if xml result has no uuid -> returns ''
    """
    try:
        return soapResult['person'][0]['uuid']
    except:
        return ''


def get_subject_fris(soapResult: zeep.AnyObject) -> str:
    """
    :param soapResult: xml result of make_request_orcid_fris() function (zeep object)
    :return: subject of research associated w the orcid id used to generate xml result
            - if xml result has no subject -> returns ''
    """
    try:
        return soapResult['person'][0]['personOrganisations']['personOrganisation'][0]['organisation']['name']['texts']['text'][0]['_value_1']
    except:
        return ''


def get_keywords_fris(soapResult: zeep.AnyObject) -> List[str]:
    """
    :param soapResult: xml result of make_request_orcid_fris() function (zeep object)
    :return: keywords associated w the orcid id used to generate xml result
            - if xml result has no keywords -> returns []
    """
    try:
        return [x["_value_1"] for x in soapResult['person'][0]['keywords']["keyword"]]
    except:
        return []


def get_profile_name_fris(soapResult: zeep.AnyObject):
    """
    :param soapResult: xml result of make_request_orcid_fris() function (zeep object)
    :return: name of researcher associated w the orcid id used to generate xml result
            - if xml result has no firstName and/or lastName -> returns ''
    """
    try:
        return soapResult['person'][0]['name']['firstName'] + " " + soapResult['person'][0]['name']['lastName']
    except:
        return ''


def get_publications_fris(soapResult: zeep.AnyObject) -> List[str]:
    """
    :param soapResult: xml result of make_request_uuid_fris() function (zeep object)
    :return: list of dois of all published research papers associated w the uuid used to generate xml result
            - if xml result includes no publications or no publication is a research paper -> returns []
    """
    data = soapResult['_value_1']
    journals = []
    for i in range(0, len(data)):
        try: # check if response is a research paper and, if it is, clean it and append it
            journals += [data[i]['journalContribution']['unpaywallDoi']
                         ['doiUrl'].replace('https://doi.org/', '')]
        except KeyError:
            pass # if it is not, then skip
    return journals


def get_publications_title_year_abstract_fris(orcid: str) -> List[dict]:
    """
    :param orcid: orcid from which to get research publications (example format: '0000-0003-4706-7950')
    :return: list of dictionaries with info from each published research paper by orcid id (title, author(s), year and abstract)
             - if any of conditions mentioned in any of the functions used take place -> returns []
    """
    soapResult = make_request_orcid_fris(orcid, 0, 2)
    uuid = get_uuid_fris(soapResult)
    soapResult2 = make_request_uuid_fris(uuid, 0, 30)
    dois = get_publications_fris(soapResult2)
    output = []
    for d in dois:
        soapResult2 = make_request_doi_fris(d, 0, 3)
        data = {}
        data["title"] = get_title_fris(soapResult2)
        data["year"] = get_year_fris(soapResult2)
        data["abstract"] = get_abstract_fris(soapResult2)
        data["author"] = get_author_fris(soapResult2)
        output.append(data)
    return output
