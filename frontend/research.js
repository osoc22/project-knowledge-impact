let flask_hostname="https://api.knowledge-impact.osoc.be"
// let flask_hostname="http://127.0.0.1:5000"


function showPublications(data) {
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
    if(text==""){text="no publications available for this researcher in the application"}
    document.querySelector("#js_publications").innerHTML = text
}

const loadPublications = function (orcid) {
    fetch(flask_hostname+'/myresearch/publications/' + orcid)
        .then(function (response) {
            if (!response.ok) {
                throw Error(`Probleem bij de fetch(). Status Code: ${response.status}`);
            } else {
                console.info('Er is een response teruggekomen van de server');
                return response.json();
            }
        })
        .then(function (jsonObject) {
            console.info('json object is aangemaakt');
            console.info('verwerken data');
            showPublications(jsonObject)
        })
        .catch(function (error) {
            console.error(`fout bij verwerken json ` + error);
        });
}

function start() {
    console.log("started")
    ORCID=sessionStorage.getItem("ORCID");
    loadPublications(ORCID)
}

start()

