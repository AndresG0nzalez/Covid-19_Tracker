from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")

@app.route("/stats", methods=['GET', 'POST'])
def stats():
    if request.method == "POST":
        search_text = (request.form["city/county/zip"]).lower()
        #send to db and get back tuple, then return to stats page
        return render_template('stats2.html', CityTable=CityTable[0])

@app.route("/map")
def map():
    return render_template("map.html")

if __name__ == "__main__":
    app.run(debug=True)