
let ORCID = "0000-0001-8390-6171"
let JCR;
let DOWNLOADS={}
let i=0;

function saveJCR(data){
    JCR=data
    console.log("jcr data is saved")
    console.log(JCR)
    loadBiblioDownloads();
}
function saveFullDownloads(data){
    // DOWNLOADS=data
    console.log("full page downloads saved")
    // let i=0;
    
    for(let line of data.split('\n')){
        let linesplit=line.split(',')
        DOWNLOADS[linesplit[1]]=linesplit[2].replace("\r","")
        // i++
        // if(i==5){
        //     console.log(DOWNLOADS)
        //     break;
        // }
    }
    // loadAllData();
}


function verwerkData(data) {
    // console.log(data.hits)
    // let body=document.querySelector("body")
    // body.innerText=JSON.stringify(data)
    //from this i can extract the biblio id
    //I can use the biblio id to get the number of full tect downloads for the specific paper
    //show  biblio metrics
    for( let publication of data.hits){
        console.log(publication.biblio_id)
        console.log(publication)
        // console.log(JCRData)
        // console.log(JCR.id)
        let tekst;
            tekst=`\ntitle = ${publication.title},
            subject: ${publication.subject},
            author:`
            for(let a of publication.author){
                console.log(a)
                tekst+=a.name_last_first+" "
                tekst+=`ORCID: ${a.orcid_id} \n`
            }
        tekst+=`full text downloads= ${DOWNLOADS[publication.biblio_id]}\n`
        tekst+=`vabb ID=${publication.vabb_id}\n`
        tekst+=`doi =${publication.doi}\n`
        for(let id in JCR.id){
            // console.log(id)
            if(publication.biblio_id==JCR.id[id]){
                tekst+=`'jcr_eigenfactor' = ${JCR.jcr_eigenfactor[id]},
                    'jcr_immediacy_index'=${JCR.jcr_immediacy_index[id]}, 
                    'jcr_impact_factor'=${JCR.jcr_impact_factor[id]}, 
                    'jcr_impact_factor_5year'=${JCR.jcr_impact_factor_5year[id]},
                    'jcr_total_cites'=${JCR.jcr_total_cites[id]}, 
                    'jcr_category_quartile'=${JCR.jcr_category_quartile[id]}, 
                    'jcr_prev_impact_factor'=${JCR.jcr_prev_impact_factor[id]},
                    'jcr_prev_category_quartile'=${JCR.jcr_prev_category_quartile[id]}`
                
            }
        }
        div=document.createElement("div")
                div.innerText=tekst
                document.querySelector("body").appendChild(div)
        // console.log(JCR.id.map((obj)=>{console.log(obj)}))
        // console.log(JCR.id.map(function (obj) { return obj.id.value; }).indexOf(publication.biblio_id))
        // loadBiblioMetrics(publication.biblio_id)
    }
}

const loadBiblioMetrics = function () {
    fetch(`biblio_jcr_metrics.json`)
        .then(function (response) {
            if (!response.ok) {
                throw Error(`Problem with the fetch(). Status Code: ${response.status}`);
            } else {
                console.info('There is a response from the server');
                return response.json();
            }
        })
        .then(function (jsonObject) {
            console.info('a json object has been made');
            console.info('processing data');
            saveJCR(jsonObject)
        })
        .catch(function (error) {
            console.error(`error with processing json ${error}`);
        });
};

const loadBiblioDownloads = function () {
    fetch(`full_page_downloads_biblio.csv`)
        .then(function (response) {
            if (!response.ok) {
                throw Error(`Problem with the fetch(). Status Code: ${response.status}`);
            } else {
                console.info('There is a response from the server');
                return response.text();
            }
        })
        .then(function (jsonObject) {
            console.info('a json object has been made');
            console.info('processing data');
            saveFullDownloads(jsonObject)
        })
        .catch(function (error) {
            console.error(`error with processing json ${error}`);
        });
};

const loadAllData = function () {
    fetch(`https://biblio.ugent.be/publication?q=author%20exact%20${ORCID}&format=json`)
        .then(function (response) {
            if (!response.ok) {
                throw Error(`Problem with the fetch(). Status Code: ${response.status}`);
            } else {
                console.info('There is a response from the server');
                return response.json();
            }
        })
        .then(function (jsonObject) {
            console.info('a json object has been made');
            console.info('percessing data');
            verwerkData(jsonObject)
        })
        .catch(function (error) {
            console.error(`error with processing json ${error}`);
        });
};


start = () => {
    console.log("started")
    loadBiblioMetrics()
}



start();

function searchORCID(e){
    ORCID=document.querySelector("#orcid").value
    loadAllData()
}

document.querySelector("#searchbtn").addEventListener("click",searchORCID)