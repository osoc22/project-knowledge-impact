
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
    return soapResult

def get_publications_fris(soapResult):
    # returns dois of all author´s publications from the soapResult
    return

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