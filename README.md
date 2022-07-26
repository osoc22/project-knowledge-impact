# project-the-power-of-sharing-knowledge

<div align="center">
  <img src=".Crest_KnowledgeImpact.svg" width="250px" />
</div>

project-the-power-of-sharing-knowledge consists of two parts:
- A front-end website
- A back-end Flask server 

## Quick start
- our server is running live at https://api.the-impact-of-sharing-knowledge.osoc.be/
- you can checkout the webpage at https://knowledge-impact.netlify.app/

## run locally

* clone this repository
* change your directory so you're in the repository
* build & start the container
```
git clone https://github.com/osoc22/project-the-power-of-sharing-knowledge.git
cd ./project-the-power-of-sharing-knowledge
docker build --tag final .
docker run -p 5000:5000 final
```
open index.html in your browser

check http://127.0.0.1:5000/api/docs/ for the Swagger UI docs



## Project structure
- In the main directory there is the app.py file, (+ which starts the Flask server), and the index.html file, which is the main page of our web application.
- [frontend/](/frontend) --> this directory contains all the html and css files for the front-end 
- [backend/](/backend) --> this directory contains the files used by the flask server
- [LICENSE](license.txt) --> License used by this project
- [README.md](README.md) --> this
The whole project is containerised and there is a Dockerfile available in the project. 


## License
Developed by [Miet Claes](https://github.com/mietcls), [Pieterjan Dendauw](https://github.com/dendpj), [Alba Lopez](https://github.com/alba-lopez), [Raman Talwar](https://github.com/rtalwar2), [Chanel Frederix](https://www.linkedin.com/in/chanel-frederix-0397b3221/), [Lyka Cabatay](https://www.linkedin.com/in/lykacabatay/) and [Ava Blanche](https://www.linkedin.com/in/avablanche/) for [Open Summer Of Code](https://osoc.be/) 2022.
This software is licensed under the [MIT license](LICENSE).
