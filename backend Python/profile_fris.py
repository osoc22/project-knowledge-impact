
import zeep

from doi_request_fris import make_request_doi_fris
from doi_request_fris import get_title_fris
from doi_request_fris import get_year_fris
from doi_request_fris import get_abstract_fris

def make_request_orcid_fris(pageNumber: int, pageSize: int, publicationNumber, orcid: str):
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

    uuid = soapResult['person'][0]['uuid']

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
    wsdl = 'https://frisr4.researchportal.be/ws/ResearchOutputServiceFRIS?wsdl'  # 'https://app-testing.r4.researchportal.be/ws/ResearchOutputServiceFRIS?wsdl'
    settings = zeep.Settings(strict=False, xml_huge_tree=True)
    client = zeep.Client(wsdl=wsdl, settings=settings)
    soapResult2 = client.service.getResearchOutput(**data2)

    return soapResult2

def get_publications_fris(soapResult):
    # returns dois of all author´s publications from the soapResult
    data = soapResult['_value_1']
    journals = []
    for i in range(0, len(data)):
        try:
            journals += [data[i]['journalContribution']['unpaywallDoi']['doiUrl'].replace('https://doi.org/', '')]
        except KeyError:
            journals = journals

    return journals

#data = make_request_orcid_fris(0, 10, 0, '0000-0003-4706-7950')
#print(get_publications_fris(data))

def get_publications_title_year_abstract_fris(orcid):
    soapResult = make_request_orcid_fris(0, 10, 0, orcid)
    dois = get_publications_fris(soapResult)
    fris_titles = []
    fris_years = []
    fris_abstracts = []
    for d in dois:
        soapResult = make_request_doi_fris(0, 10, 0, d)
        fris_titles += [get_title_fris(soapResult)]
        fris_years += [get_year_fris(soapResult)]
        fris_abstracts += [get_abstract_fris(soapResult)]
    return fris_titles, fris_years, fris_abstracts

# fris_titles, fris_years, fris_abstracts = get_publications_title_year_abstract_fris('0000-0003-4706-7950')
# print(fris_titles)
# print(fris_years)
# print(fris_abstracts)
