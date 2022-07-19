
// const loadPeopleWhoCitedMe = function () {//get publications from fris, 
//     fetch("")//seding a request with my doi and getting the persons as a reposnse
//         .then(function (response) {
//             if (!response.ok) {
//                 throw Error(`Problem with the fetch(). Status Code: ${response.status}`);
//             } else {
//                 // console.info('There is a response from the server');
//                 return response.json();
//             }
//         })
//         .then(function (jsonObject) {
//             // console.info('a json object has been made');
//             // console.info('percessing data');
//             verwerkData(jsonObject)
//         })
//         .catch(function (error) {
//             console.error(`error with processing json ${error}`);
//         });
// };

// const loadPublications = function () {//get publications from fris, 
//     fetch("")
//         .then(function (response) {
//             if (!response.ok) {
//                 throw Error(`Problem with the fetch(). Status Code: ${response.status}`);
//             } else {
//                 // console.info('There is a response from the server');
//                 return response.json();
//             }
//         })
//         .then(function (jsonObject) {
//             // console.info('a json object has been made');
//             // console.info('percessing data');
//             verwerkData(jsonObject)
//         })
//         .catch(function (error) {
//             console.error(`error with processing json ${error}`);
//         });
// };


function addTimeline(workcounts,years){
    console.log(workcounts)
    console.log(years)
    let tekst=""
    for(let i=years.length-1;i>=0;i--){
        tekst+=`<li>
            <p class="diplome">${workcounts[i]} publications</p>
            <p class="year">${years[i]}</p>
            <span class="point"></span>
            <p class="description">
              you have written ${workcounts[i]} publications in that department
            </p>
          </li>`
    }
    document.querySelector("#js_timeline").innerHTML=tekst

}
function showCitationsAndWorkCount(data){
    console.log(data)
    let years=[]
    let workcounts=[]
    let citations=[]
    for(let obj of data.counts_by_year){
        // console.log(obj)
        years.push(obj.year)
        workcounts.push(obj.works_count)
        citations.push(obj.cited_by_count)
    }
    let plot = [
        {
          x: years,
          y: workcounts,
          type: 'scatter'
        }
      ];
      
      Plotly.newPlot('js_workCount', plot,{
        xaxis: { tickformat: '.0f'}
      });
      plot[0].y=citations
      Plotly.newPlot('js_citations', plot,{
        xaxis: { tickformat: '.0f'}
      });
    
    addTimeline(workcounts,years)

}


const loadCitationsAndWorkCount = function(orcid) {
    fetch('http://api.openalex.org/authors/orcid:'+orcid)
        .then(function(response) {
            if (!response.ok) {
                throw Error(`Probleem bij de fetch(). Status Code: ${response.status}`);
            } else {
                console.info('Er is een response teruggekomen van de server');
                return response.json();
            }
        })
        .then(function(jsonObject) {
            console.info('json object is aangemaakt');
            console.info('verwerken data');
            showCitationsAndWorkCount(jsonObject)
        })
        .catch(function(error) {
            console.error(`fout bij verwerken json ${error}`);
        });
};


function searchORCID(e){
    ORCID=document.querySelector("#orcid").value
    // loadPublications()
    loadCitationsAndWorkCount(ORCID)
}


document.querySelector("#searchbtn").addEventListener("click",searchORCID)


start()


function start(){
    console.log("started")    
    // loadCitationsAndWorkCount("0000-0003-0248-0987")
}
