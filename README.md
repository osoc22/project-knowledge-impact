# project-the-power-of-sharing-knowledge

<div align="center">
  <img src="Crest_KnowledgeImpact.svg" width="250px" />
</div>

project-the-power-of-sharing-knowledge consists of two parts:
- A front-end website
- A back-end Flask server 

## Quick start
- Our server is running live at https://api.knowledge-impact.osoc.be
- You can checkout the webpage at https://knowledge-impact.netlify.app/

## Run locally

* clone this repository
* change your directory so you're in the repository
* build & start the container
```
git clone https://github.com/osoc22/project-the-power-of-sharing-knowledge.git
cd ./project-the-power-of-sharing-knowledge
docker build --tag final .
docker run -p 5000:5000 final
```
open index.html in your browser, enter the desired researcher´s orcid id, and press the ‘search’ button.

check http://127.0.0.1:5000/api/docs/ for the Swagger UI docs



## Project structure
- In the main directory there is the app.py file, (+ which starts the Flask server), and the index.html file, which is the main page of our web application.
- [frontend/](/frontend) --> this directory contains all the html and css files for the front-end 
- [backend/](/backend) --> this directory contains the files used by the flask server
- [LICENSE](license.txt) --> License used by this project
- [README.md](README.md) --> this
- The whole project is containerised and there is a [Dockerfile](Dockerfile) available in the project. 

## Notice
- The Biblio full-text downloads data is only available for researchers from Ghent University and only from the last 2.5 years, so it may not be representative of the researcher´s career.
- Currently, only 15 “research outputs” at a time are retrieved from FRIS so the web application loads relatively quickly. Therefore, shown results are limited.
- Only research papers (JournalContributions) are retrieved so that results remain relevant. Therefore, shown results are limited.
- Recommendations only include research papers/researchers that are available in FRIS. Therefore, shown results are limited.
- There are missing metadata about publications, so results may not always be available or complete. More information about missing metadata from biblio can be found on https://drive.google.com/file/d/1LMpakm6wecEST0f34oyVjc2cL2Hgxx1-/view?usp=sharing and https://drive.google.com/file/d/148_gY3iDnVcf8cqyvEgYRcCz0bVemFok/view?usp=sharing

## License
Developed by [Miet Claes](https://github.com/mietcls), [Pieterjan Dendauw](https://github.com/dendpj), [Alba Lopez](https://github.com/alba-lopez), [Fien Goeman](https://github.com/FienGoeman), [Raman Talwar](https://github.com/rtalwar2), [Chanel Frederix](https://www.linkedin.com/in/chanel-frederix-0397b3221/), [Lyka Cabatay](https://www.linkedin.com/in/lykacabatay/) and [Ava Blanche](https://www.blinge.design) for [Open Summer Of Code](https://osoc.be/) 2022.
This software is licensed under the [MIT license](license.txt).
