from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd

from profile_fris import get_publications_title_year_abstract_fris
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


@app.route('/publications/<orcid>')
def getPublications(orcid):
    x, dois, fris_titles, fris_years, fris_abstracts = get_publications_title_year_abstract_fris(
        '0000-0003-4706-7950')
    print(fris_titles)
    print(fris_years)
    print(fris_abstracts)
    print(dois)
    return jsonify(get_publications_title_year_abstract_fris(orcid))


if __name__ == "__main__":
    app.run()
