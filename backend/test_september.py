import zeep

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



soapResult = make_request_orcid_fris("0000-0003-0575-5894", 0, 2)
print(soapResult)
# output = {}
# output["name"] = get_profile_name_fris(soapResult)
# output["description"] = get_subject_fris(soapResult)
# output["keywords"] = get_keywords_fris(soapResult)
# return jsonify(output)
