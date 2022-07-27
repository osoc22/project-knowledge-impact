let DOWNLOADS = ""
let flask_hostname="https://api.knowledge-impact.osoc.be"
// let flask_hostname="http://127.0.0.1:5000"
/////show data/////////////////

function addTimeline(workcounts,citations, years) {
    let tekst = ""
    for (let i = years.length - 1; i >= 0; i--) {
        tekst += `<li>
        <p class="diplome">${workcounts[i]} publications <br> ${citations[i]} citations</p>
        <p class="year">${years[i]}</p>
            <span class="point"></span>
            
          </li>`
    }
    document.querySelector("#js_timeline").innerHTML = tekst
}
function showCitationsAndWorkCount(data) {
    let years = []
    let workcounts = []
    let citations = []
    for (let obj of data.counts_by_year) {
        years.push(obj.year)
        workcounts.push(obj.works_count)
        citations.push(obj.cited_by_count)
    }


    let plot = [
        {
            x: years,
            y: workcounts,
            type: 'scatter',
            line: {
                color: 'rgb(101, 88, 245)',
            }
        }
    ];

    Plotly.newPlot('js_workCount', plot,
        {
            xaxis: { tickformat: '.0f' },
            title: {
                text: 'publications per year'
            }
        });

    plot[0].y = citations
    Plotly.newPlot('js_citations', plot, {
        xaxis: { tickformat: '.0f' },
        yaxis: { rangemode: 'tozero'},
        title: {
            text: 'citations per year'
        }
    });
    addTimeline(workcounts,citations, years)

}

function showDescription(data) {
    // console.log(data)
    document.querySelector("#js_profile_desc").innerText = data.description
    document.querySelector("#js_name").innerText = data.name
    if (data.keywords.length > 0) {
        loadTools(data.keywords[Math.floor(Math.random() * data.keywords.length)])
    }
    else {
        document.querySelector("#js_tools").innerText = "no tools available"
    }
}

function showConnections(data) {
    let i = 0;
    console.log(data)
    let text = ""
    for (let name of data) {
        text += `
        <div class="col-2">
            <h3>${name}</h3>

            <a href="#" class="circle">
              <img height="128" width="128" src="placeholder.png" alt="picture of researcher" />
            </a>
          </div>
        `
        i++
    }
    if (text == "") { text = "no connections available" }
    document.querySelector("#js_connections").classList.add('row')

    document.querySelector("#js_connections").innerHTML = text
}

function showRecommendations(data) {
    console.log(data)
    let text = ""
    for (let obj of data) {
        if (obj.abstract == "") { obj.abstract = "---" }
        text += `<div class="row">
        <div class="col-11 mb-10">
          <div class="card">
            <div class="card-body">
              <h3 class="card-title">${obj.title}</h3>
              <h4 class="card-subtitle mb-2 text-muted">${obj.year}</h4>
              <p class="card-text"><h6>Abstract</h6>
                ${obj.abstract}
                </p>
              <p class="card-text"><small class="text-muted">${obj.author}</small></p>

              <a href="#" class="btn btn-primary disabled">details</a>
            </div>
          </div>
        </div>
      </div>`
    }
    if (text == "") { text = "no recommendations available" }
    document.querySelector("#js_recommendation").innerHTML = text
}



function showDownloads(data) {
    // console.log(data)
    let downloadcount = { 2020: 0, 2021: 0, 2022: 0 }
    for (let doi of data) {
        console.log(doi)
        for (let i in DOWNLOADS[doi]) {
            // console.log(DOWNLOADS[doi][i])
            downloadcount[i] += DOWNLOADS[doi][i]
        }
    }
    console.log(downloadcount)
    // console.log(downloadcount.keys())
    // console.log(downloadcount.values())
    let years = []
    let downloads = []
    for (let i in downloadcount) {
        years.push(i)
        downloads.push(downloadcount[i])
    }

    let plot = [
        {
            x: years,
            y: downloads,
            type: 'scatter',
            line: {
                color: 'rgb(101, 88, 245)',
            }
        }
    ];

    Plotly.newPlot('js_downloads', plot,
        {
            xaxis: { tickformat: '.0f' },
            yaxis: { rangemode: 'tozero'},
            title: {
                text: 'biblio downloads per year'
            }
        });

}

function showTools(data) {
    console.log(data)
    //show max 2 tools
    let text = ""
    for (let i = 0; i < data.results.length; i++) {
        console.log(data)
        text += `
        <div class="card" style="width: 18rem;">
        <img src="${data.results[i].logo}" class="card-img-top" alt="${data.results[i].abbreviation}">
        <div class="card-body">
          <h3 class="card-title">${data.results[i].name}</h3>
          <h4 class="card-subtitle mb-2 text-muted">organisation: ${data.facets[1].values[i].label}</h4>
          <p class="card-text">${data.results[i].description.substr(0, 105) + '...'}</p>
          <a href="${data.results[i].webpage}" class="btn btn-primary">learn More</a>
      </div>
    </div>
    `
    }
    if (text == "") { text = "no tools available. refresh, sometimes it helps ;)" }
    document.querySelector("#js_tools").classList.add('row')
    document.querySelector("#js_tools").innerHTML = text
}

//////////load data////////////////////
const loadCitationsAndWorkCount = function (orcid) {
    fetch('https://api.openalex.org/authors/orcid:' + orcid)
        .then(function (response) {
            if (!response.ok) {
                throw Error(`Probleem bij de fetch(). Status Code: ${response.status}`);
            } else {
                console.info('load citations and workcount successful');
                return response.json();
            }
        })
        .then(function (jsonObject) {
            showCitationsAndWorkCount(jsonObject)
        })
        .catch(function (error) {
            console.error(`fout bij verwerken json ${error}`);
        });
};



const loadProfileDescription = function (orcid) {
    fetch(flask_hostname+'/profile/description/' + orcid)
        .then(function (response) {
            if (!response.ok) {
                throw Error(`Probleem bij de fetch(). Status Code: ${response.status}`);
            } else {
                console.info('load profile description successful');
                return response.json();
            }
        })
        .then(function (jsonObject) {
            showDescription(jsonObject)
        })
        .catch(function (error) {
            console.error(`fout bij verwerken json ${error}`);
        });
};

const loadSuggestedConections = function (orcid) {
    fetch(flask_hostname+'/profile/network/' + orcid)
        .then(function (response) {
            if (!response.ok) {
                throw Error(`Probleem bij de fetch(). Status Code: ${response.status}`);
            } else {
                console.info('load suggested Connections successful');
                return response.json();
            }
        })
        .then(function (jsonObject) {
            showConnections(jsonObject)
        })
        .catch(function (error) {
            console.error(`error with parsing json ${error}`);
        });
};

const loadRecommendations = function (orcid) {
    fetch(flask_hostname+'/profile/recommendations/' + orcid)
        .then(function (response) {
            if (!response.ok) {
                throw Error(`Probleem bij de fetch(). Status Code: ${response.status}`);
            } else {
                console.info('load recommended papers successful');
                return response.json();
            }
        })
        .then(function (jsonObject) {
            showRecommendations(jsonObject)
        })
        .catch(function (error) {
            console.error(`error with parsing json ${error}`);
        });
};

const loadDois = function (orcid) {
    fetch(flask_hostname+'/profile/dois/' + orcid)
        .then(function (response) {
            if (!response.ok) {
                throw Error(`Probleem bij de fetch(). Status Code: ${response.status}`);
            } else {
                console.info('load Dois  successful');
                return response.json();
            }
        })
        .then(function (jsonObject) {
            showDownloads(jsonObject)
        })
        .catch(function (error) {
            console.error(`error with parsing json ${error}`);
        });
};

const loadDownloads = function () {
    fetch('./table_doi_downloads.json')
        .then(function (response) {
            if (!response.ok) {
                throw Error(`Probleem bij de fetch(). Status Code: ${response.status}`);
            } else {
                console.info('load downloads successful');
                return response.json();
            }
        })
        .then(function (jsonObject) {
            DOWNLOADS = jsonObject
        })
        .catch(function (error) {
            console.error(`error with parsing json ${error}`);
        });
};

const loadTools = function (keyword) {
    console.log('https://api.eosc-portal.eu/resource/all?catalogue_id=eosc&query=' + keyword)
    fetch('https://api.eosc-portal.eu/resource/all?catalogue_id=eosc&' + new URLSearchParams({
        query: keyword
    }))
        .then(function (response) {
            if (!response.ok) {
                throw Error(`Probleem bij de fetch(). Status Code: ${response.status}`);
            } else {
                console.info('load Tools successful');
                return response.json();
            }
        })
        .then(function (jsonObject) {
            showTools(jsonObject)
        })
        .catch(function (error) {
            console.error(`error with parsing json ${error}`);
        });
};


///////////start//////////
start()


function start() {
    console.log("started")
    loadDownloads()
    ORCID = sessionStorage.getItem("ORCID");
    loadDois(ORCID)
    loadCitationsAndWorkCount(ORCID)
    loadProfileDescription(ORCID)
    loadSuggestedConections(ORCID)
    loadRecommendations(ORCID)
}
