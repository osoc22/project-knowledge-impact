
const loadPeopleWhoCitedMe = function () {//get publications from fris, 
    fetch("")//seding a request with my doi and getting the persons as a reposnse
        .then(function (response) {
            if (!response.ok) {
                throw Error(`Problem with the fetch(). Status Code: ${response.status}`);
            } else {
                // console.info('There is a response from the server');
                return response.json();
            }
        })
        .then(function (jsonObject) {
            // console.info('a json object has been made');
            // console.info('percessing data');
            verwerkData(jsonObject)
        })
        .catch(function (error) {
            console.error(`error with processing json ${error}`);
        });
};

const loadPublications = function () {//get publications from fris, 
    fetch("")
        .then(function (response) {
            if (!response.ok) {
                throw Error(`Problem with the fetch(). Status Code: ${response.status}`);
            } else {
                // console.info('There is a response from the server');
                return response.json();
            }
        })
        .then(function (jsonObject) {
            // console.info('a json object has been made');
            // console.info('percessing data');
            verwerkData(jsonObject)
        })
        .catch(function (error) {
            console.error(`error with processing json ${error}`);
        });
};



function searchORCID(e){
    ORCID=document.querySelector("#orcid").value
    loadPublications()
}

start()


function start(){
    console.log("started")
}