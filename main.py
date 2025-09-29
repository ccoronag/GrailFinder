from DiscogsFetch import Discogs
from EbayFetch import Ebay, EbayAuthTokenError
from flask import Flask, render_template, request,  jsonify
app = Flask(__name__)

discogs = Discogs()
ebay = Ebay()

cache = {}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    query = request.json.get("query").strip().lower()

    if query in cache:
        return jsonify(cache[query])
    
    
    discogs_results = discogs.fetch_result(query)
    ebay_results = ebay.fetch_result(query)

    cache[query] = {"discogs": discogs_results,
                    "ebay": ebay_results}

    print(ebay_results)
    return jsonify({
        "discogs": discogs_results,
        "ebay": ebay_results
    })

@app.route("/picks")
def weekly_picks():
    discogs_picks = discogs.fetch_picks()
    print(discogs_picks)
    return jsonify({
        "discogs": discogs_picks
    })

if __name__ == "__main__":
    app.run(debug=True)