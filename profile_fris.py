
import zeep

from doi_request_fris import get_author_fris, make_request_doi_fris
from doi_request_fris import get_title_fris
from doi_request_fris import get_year_fris
from doi_request_fris import get_abstract_fris


def make_request_orcid_fris(orcid: str, pageNumber: int, pageSize: int, publicationNumber):
    """
    :param orcid: '0000-0003-4706-7950' (example format)
    :param pageNumber:
    :param pageSize:
    :param publicationNumber:
    :return: xml response of orcid (zeep object)
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
    data['criteria']['window']['pageNumber'] = pageNumber
    data['criteria']['window']['pageSize'] = pageSize
    data['criteria']['sources']['source']['identifier'] = orcid
    wsdl = 'https://frisr4.researchportal.be/ws/PersonServiceFRIS?wsdl'
    settings = zeep.Settings(strict=False, xml_huge_tree=True)
    client = zeep.Client(wsdl=wsdl, settings=settings)
    soapResult = client.service.getPersons(**data)
    return soapResult


def make_request_uuid_fris(uuid: str, pageNumber: int, pageSize: int, publicationNumber):
    """
    :param uuid: '1727939a-543a-4184-841f-944ee16db418' (example format)
    :param pageNumber:
    :param pageSize:
    :param publicationNumber:
    :return: xml result of uuid (zeep object)
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
    data2['criteria']['window']['pageNumber'] = pageNumber
    data2['criteria']['window']['pageSize'] = pageSize
    data2['criteria']['associatedPersons']['identifier'] = uuid
    # 'https://app-testing.r4.researchportal.be/ws/ResearchOutputServiceFRIS?wsdl'
    wsdl = 'https://frisr4.researchportal.be/ws/ResearchOutputServiceFRIS?wsdl'
    settings = zeep.Settings(strict=False, xml_huge_tree=True)
    client = zeep.Client(wsdl=wsdl, settings=settings)
    soapResult2 = client.service.getResearchOutput(**data2)
    return soapResult2


def get_subject_fris(soapResult):
    """
    :param soapResult: xml result of orcid (zeep object) (result of fun make_request_orcid_fris())
    :return: subject of research associated w orcid id (str)
    """
    return soapResult['person'][0]['personOrganisations']['personOrganisation'][0]['organisation']['name']['texts']['text'][0]['_value_1']


def get_keywords_fris(soapResult):
    """
    :param soapResult: xml result of orcid (zeep object) (result of fun make_request_orcid_fris())
    :return: keywords associated to orcid id (str)
    """
    try:
        return [x["_value_1"] for x in soapResult['person'][0]['keywords']["keyword"] ]
    except TypeError:
        return []


def get_profile_name_fris(soapResult):
    """
    :param soapResult: xml result of orcid (zeep object) (result of fun make_request_orcid_fris())
    :return: name of researcher associated w orcid id (str)
    """
    return soapResult['person'][0]['name']['firstName']+" "+soapResult['person'][0]['name']['lastName']


def get_uuid_fris(soapResult):
    """
    :param soapResult: xml result of orcid (zeep object) (result of fun make_request_orcid_fris())
    :return: uuid associated w an orcid id (str)
    """
    # print(soapResult['person'])
    # print("hallo")
    # print(soapResult['person'][0]["uuid"])
    # print(soapResult['person'][1]["uuid"])
    # print(soapResult['person'][0]["uuid"])
    # print("hallo")
    return soapResult['person'][0]['uuid']


def get_publications_fris(soapResult):
    """
    :param soapResult: xml result of uuid (zeep object) (result of fun make_request_uuid_fris())
    :return: list of doi of all publications (list(str))
    """
    # returns dois of all author´s publications from the soapResult
    data = soapResult['_value_1']
    print(len(data))
    journals = []
    for i in range(0, len(data)):
        try:
            journals += [data[i]['journalContribution']['unpaywallDoi']
                         ['doiUrl'].replace('https://doi.org/', '')]
        except Exception as e:
            print(e)
            journals = journals
    return journals

# data1 = make_request_orcid_fris('0000-0003-4706-7950', 0, 10, 0)
# uuid = get_uuid_fris(data1)
# print(uuid)
# print(get_subject_fris(data1))
# data2 = make_request_uuid_fris(uuid, 0, 10, 0)
# print(get_publications_fris(data2))


def get_publications_title_year_abstract_fris(orcid):
    """
    :param orcid: '0000-0003-4706-7950' (example format)
    :return: lists of dois, titles, years and abstracts from all research papers published by orcid id
    """
    soapResult = make_request_orcid_fris(orcid, 0, 2, 0)
    uuid = get_uuid_fris(soapResult)
    soapResult2 = make_request_uuid_fris(uuid, 0, 30, 0)
    # print(soapResult2)
    dois = get_publications_fris(soapResult2)
    output = {}
    output["doi"] = dois
    output["title"] = []
    output["year"] = []
    output["abstract"] = []
    output["author"] = []
    for d in dois:
        soapResult2 = make_request_doi_fris(d, 0, 3, 0)
        output["title"] += [get_title_fris(soapResult2)]
        output["year"] += [get_year_fris(soapResult2)]
        output["abstract"] += [get_abstract_fris(soapResult2)]
        output["author"] += [get_author_fris(soapResult2)]
    return output


# dois, fris_titles, fris_years, fris_abstracts = get_publications_title_year_abstract_fris('0000-0003-4706-7950')
# print(fris_titles)
# print(fris_years)
# print(fris_abstracts)
# print(dois)
