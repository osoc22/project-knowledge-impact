
import zeep

def make_request_doi_fris(doi: str, pageNumber: int = 0, pageSize: int = 10, publicationNumber: int = 0):
    """
    :param doi: '10.1016/j.foodchem.2022.132915' (example format)
    :param pageNumber:
    :param pageSize:
    :param publicationNumber:
    :return: xml response (zeep object)
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

    data['criteria']['window']['pageNumber'] = pageNumber
    data['criteria']['window']['pageSize'] = pageSize
    data['criteria']['sources']['source']['identifier'] = 'https://doi.org/' + str(doi)
    wsdl = 'https://frisr4.researchportal.be/ws/ResearchOutputServiceFRIS?wsdl'
    settings = zeep.Settings(strict=False, xml_huge_tree=True)
    client = zeep.Client(wsdl=wsdl, settings=settings)
    soapResult = client.service.getResearchOutput(**data)
    return soapResult

def get_title_fris(soapResult):
    """
    :param soapResult: xml response (zeep object)
    :return: title of publication (str)
    """
    return soapResult['_value_1'][0]['journalContribution']['title']['texts']['text'][0]['_value_1']

def get_author_fris(soapResult):
    """
    :param soapResult: xml response (zeep object)
    :return: author(s) of publication (list[str])
    """
    data = soapResult['_value_1'][0]['journalContribution']['unpaywallDoi']['ZAuthors']
    list_names = []
    for i in range(0, len(data)):
        list_names += [data[i]['given'] + ' ' + data[i]['family']]  # THE GOOD WAY
    return list_names

def get_year_fris(soapResult):
    """
    :param soapResult: xml response (zeep object)
    :return: year of publication (int)
    """
    return soapResult['_value_1'][0]['journalContribution']['publicationYear']

def get_abstract_fris(soapResult):
    """
    :param soapResult: xml response (zeep object)
    :return: abstract of publication (str)
    """
    if soapResult['_value_1'][0]['journalContribution']['researchAbstract'] is not None:
        return soapResult['_value_1'][0]['journalContribution']['researchAbstract']['texts']['text'][0]['_value_1']
    else:
        return ''


#r = make_request_doi_fris(0, 10, 0, '10.1016/j.foodchem.2022.132915')
#r = make_request_doi_fris(0, 10, 0, '10.1186/s11689-022-09423-3')
#r = make_request_doi_fris(0, 10, 0, '10.1080/15325008.2012.749554')

#print(get_author_fris(r))

