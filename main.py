from DiscogsFetch import Discogs
from EbayFetch import Ebay, EbayAuthTokenError
from flask import Flask, render_template, request,  jsonify
app = Flask(__name__)

discogs = Discogs()
ebay = Ebay()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    query = request.json.get("query")

    
    discogs_results = discogs.fetch_result(query)
    ebay_results = ebay.fetch_result(query)

    print(ebay_results)
    return jsonify({
        "discogs": discogs_results,
        "ebay": ebay_results
    })


if __name__ == "__main__":
    app.run(debug=True)