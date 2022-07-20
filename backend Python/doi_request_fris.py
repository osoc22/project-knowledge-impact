
import zeep

def make_request_doi_fris(pageNumber: int, pageSize: int, publicationNumber, doi: str):
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

    data['criteria']['window']['pageNumber'] = pageNumber
    data['criteria']['window']['pageSize'] = pageSize
    data['criteria']['sources']['source']['identifier'] = "https://doi.org/" + doi
    wsdl = 'https://frisr4.researchportal.be/ws/ResearchOutputServiceFRIS?wsdl'
    settings = zeep.Settings(strict=False, xml_huge_tree=True)
    client = zeep.Client(wsdl=wsdl, settings=settings)
    soapResult = client.service.getResearchOutput(**data)
    return soapResult

def get_title_fris(soapResult):
    return soapResult['_value_1'][0]['journalContribution']['title']['texts']['text'][0]['_value_1']

def get_author_fris(soapResult):
    return soapResult['_value_1'][0]['journalContribution']['participants']['participant'][0]['name']['firstName'] + ' ' + \
           soapResult['_value_1'][0]['journalContribution']['participants']['participant'][0]['name']['lastName']

def get_year_fris(soapResult):
    return soapResult['_value_1'][0]['journalContribution']['publicationYear']

def get_abstract_fris(soapResult):
    return soapResult['_value_1'][0]['journalContribution']['researchAbstract']['texts']['text'][0]['_value_1']