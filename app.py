from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd

from profile_fris import get_keywords_fris, get_profile_name_fris, get_publications_fris, get_publications_title_year_abstract_fris, get_subject_fris, get_uuid_fris, make_request_orcid_fris, make_request_uuid_fris
from recommendations_fris import get_all_recs_author, get_all_seggested_papers
app = Flask(__name__)
CORS(app)

# total_downloads=pd.read_csv("full_page_downloads_biblio.csv")

# df = pd.read_csv("publications.csv",low_memory=False)
# df=df[['id','jcr_eigenfactor',
#        'jcr_immediacy_index', 'jcr_impact_factor', 'jcr_impact_factor_5year',
#        'jcr_total_cites', 'jcr_category_quartile', 'jcr_prev_impact_factor',
#        'jcr_prev_category_quartile']]


@app.route("/")
def home():
    # print(df)
    return "Hello flask!"


@app.route("/biblioMetrics/<bibid>")
def getBiblioMetrics(bibid):
    # return df[df['id']==int(bibid)].set_index("id").to_json()
    return "hello"


@app.route("/biblioDownloads/<bibid>")
def getBiblioDownloads(bibid):
    # return total_downloads[total_downloads['id']==bibid].set_index("id").to_json()

    # return total_downloads.loc[[bibid]].to_json()
    return "THis works"


@app.route('/myresearch/publications/<orcid>')
def getPublications(orcid):
    # x, dois, fris_titles, fris_years, fris_abstracts = get_publications_title_year_abstract_fris(
    #     '0000-0003-4706-7950')
    # print(fris_titles)
    # print(fris_years)
    # print(fris_abstracts)
    # print("ik voer uit")
    return jsonify(get_publications_title_year_abstract_fris(orcid))


@app.route("/profile/description/<orcid>")
def getDescription(orcid):
    soapResult = make_request_orcid_fris(orcid, 0, 25, 0)
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
    output = get_all_seggested_papers(orcid)
    return jsonify([x for x in output if x != []])  # to remove empty arrays
    # return jsonify(get_all_seggested_papers(orcid))


@app.route("/profile/dois/<orcid>")
def getAlldois(orcid):
    soapResult = make_request_orcid_fris(orcid, 0, 2, 0)
    uuid = get_uuid_fris(soapResult)
    soapResult2 = make_request_uuid_fris(uuid, 0, 15, 0)
    return jsonify(get_publications_fris(soapResult2))


if __name__ == "__main__":
    app.run()
