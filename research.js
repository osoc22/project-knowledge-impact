function showPublications(data) {
    console.log(data)
    let text = ""
    for (let i = 0; i < data.title.length; i++) {
        if (data.abstract[i] == "") { data.abstract[i] = "---" }
        text += `<div class="row">
        <div class="col-11">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">${data.title[i]}</h5>
              <h6 class="card-subtitle mb-2 text-muted">${data.year[i]}</h6>
              <p class="card-text"><h6>Abstract</h6>
                ${data.abstract[i]}
                </p>
              <p class="card-text"><small class="text-muted">${data.author[i]}</small></p>

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
    fetch('http://127.0.0.1:5000/myresearch/publications/' + orcid)
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

