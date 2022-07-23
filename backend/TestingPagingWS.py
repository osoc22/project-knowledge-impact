import zeep # RC: needed to make wsdl soap requests. https://docs.python-zeep.org/en/master/

pageNumber = 0 # RC: pageNumber start value 
pageSize = 10 # RC: pageSize
publicationNumber = 0  # RC: if we get 'pageSize' publications, we print the 'publicationNumber'th to the file/console. 
                        # E.g. publicationNumber = 10 and pageSize = 50 means that after every request, we print the 10th publication out of 50 publications

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
      "sources":{
        "source":{
        "authority": "DOI",
        "identifier": ""
        }
      }
    }
}

data['criteria']['window']['pageNumber'] = pageNumber
data['criteria']['window']['pageSize'] = pageSize
data['criteria']['sources']['source']['identifier'] = "https://doi.org/10.1080/15325008.2012.749554"

# RC: setup soap and do a request to get the total number of publications 
wsdl = 'https://frisr4.researchportal.be/ws/ResearchOutputServiceFRIS?wsdl' #'https://app-testing.r4.researchportal.be/ws/ResearchOutputServiceFRIS?wsdl' 
settings = zeep.Settings(strict=False, xml_huge_tree=True)
client = zeep.Client(wsdl=wsdl, settings=settings)
soapResult = client.service.getResearchOutput(**data)
total = soapResult['total']
print(soapResult)
soapResult = client.service.getResearchOutput(**data) # RC: do the actual request
title = soapResult['_value_1'][publicationNumber]['journalContribution']['title']['texts']['text'][0]['_value_1'] # RC: get title from result
currentPublicationNumber = pageNumber * pageSize + publicationNumber # RC: get the number of the publication that we print to the file/console
output = str(currentPublicationNumber) + ' - ' + title
print(output) # RC: print to console

# RC: get the total number of requests
# #total = 75000 # RC: due to a crash around 81.000 publications, we limit the total to this number. I didn't look into the reason of the crash.
# totalRequests = int(total / pageSize) + 1

# # RC: do all the requests
# print('Trying to dowload ' + str(total) + ' publications.')
# for pageNumber in range(totalRequests):
#     try:
#         data['criteria']['window']['pageNumber'] = pageNumber # RC: change the pageNumber in the xml 
#         soapResult = client.service.getResearchOutput(**data) # RC: do the actual request
#         title = soapResult['_value_1'][publicationNumber]['journalContribution']['title']['texts']['text'][0]['_value_1'] # RC: get title from result
#         currentPublicationNumber = pageNumber * 200 + publicationNumber # RC: get the number of the publication that we print to the file/console
#         output = str(currentPublicationNumber) + ' - ' + title
#         print(output) # RC: print to console
#         pageNumber = pageNumber + 1
#     except(RuntimeError, TypeError, NameError):
#         print('RuntimeError ' + RuntimeError)
#         print('TypeError ' + TypeError)
#         print('NameError ' + NameError)        
