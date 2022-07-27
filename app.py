from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from backend.profile_fris import get_keywords_fris, get_profile_name_fris, get_publications_fris, get_publications_title_year_abstract_fris, get_subject_fris, get_uuid_fris, make_request_orcid_fris, make_request_uuid_fris
from backend.recommendations_fris import get_all_recs_author, get_all_recs_title_author_year_abstract
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)


SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
# Our API url (can of course be a local resource)
API_URL = '/static/swagger.json'


# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    }
)

app.register_blueprint(swaggerui_blueprint)


@app.route("/")
def home():
    # print(df)
    return "Hello flask!"

@app.route('/myresearch/publications/<orcid>')
def getPublications(orcid):
    return jsonify(get_publications_title_year_abstract_fris(orcid))


@app.route("/profile/description/<orcid>")
def getDescription(orcid):
    soapResult = make_request_orcid_fris(orcid, 0, 2)
    output = {}
    output["name"] = get_profile_name_fris(soapResult)
    output["description"] = get_subject_fris(soapResult)
    output["keywords"] = get_keywords_fris(soapResult)
    return jsonify(output)


@app.route("/profile/network/<orcid>")
def getSuggestedConnections(orcid):
    return jsonify(get_all_recs_author(orcid))


@app.route("/profile/recommendations/<orcid>")
def getRecommendations(orcid):
    output = get_all_recs_title_author_year_abstract(orcid)
    return jsonify(output)  # to remove empty arrays


@app.route("/profile/dois/<orcid>")
def getAlldois(orcid):
    soapResult = make_request_orcid_fris(orcid, 0, 2)
    uuid = get_uuid_fris(soapResult)
    soapResult2 = make_request_uuid_fris(uuid, 0, 15)
    return jsonify(get_publications_fris(soapResult2))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
