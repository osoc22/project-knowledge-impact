
function searchORCID(e) {
    ORCID = document.querySelector("#orcid").value
    sessionStorage.setItem("ORCID", ORCID);
    window.open("./profile.html","_self")
}


document.querySelector("#searchbtn").addEventListener("click", searchORCID)


start()


function start() {
    console.log("started")
}
