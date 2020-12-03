from flask import Flask, render_template, request
from flask_table import Table, Col

app = Flask(__name__)



@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")


@app.route("/stats", methods=['GET', 'POST'])
def stats():
    if request.method == "POST":
        search_text = (request.form["city/county/zip"]).lower()
        #send to db and get back tuple, then return to stats page

        results = ('Leon', 15253, 0, 241, 6869, 2307, 1640, 1372, 536, 1166, 634, 287, 192, 24, 243, 141, 6809, 8410, 6187, 4161, 1383, 9314)

        fields = ['County Name', 'Total Cases', 'Population', 'Cases (Age 0-4)', 'Cases (Age 15-24)','Cases (Age 25-34)',
                  'Cases (Age 35-44)', 'Cases (Age 45-54)', 'Cases (Age 5-14)', 'Cases (Age 55-64)', 'Cases (Age 65-74)',
                  'Cases (Age 75-84)','Cases (Age 85+)', 'Age Median', 'New Cases', 'Deaths',
                  'Men', 'Women', 'White', 'Black', 'Hispanic', 'Non Hispanic']
        data = dict(zip(fields, results))
        return render_template('stats2.html', data=data)

@app.route("/map")
def map():
    return render_template("map.html")

if __name__ == "__main__":
    app.run(debug=True)

    cursor.close()
    cnx.close()