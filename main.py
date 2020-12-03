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

        results = ('Leon', 15253, 241, 6869, 2307, 1640, 1372, 536, 1166, 634, 287, 192, 24, 243, 141, 6809, 8410, 6187, 4161, 1383, 9314)
        description = [('county_name', 253, None, None, None, None, 0, 20483), ('cases', 3, None, None, None, None, 1, 32768), ('age_0_4', 3, None, None, None, None, 1, 32768),
                       ('age_15_24', 3, None, None, None, None, 1, 32768), ('age_25_34', 3, None, None, None, None, 1, 32768), ('age_35_44', 3, None, None, None, None, 1, 32768),
                       ('age_45_54', 3, None, None, None, None, 1, 32768), ('age_5_14', 3, None, None, None, None, 1, 32768), ('age_55_64', 3, None, None, None, None, 1, 32768),
                       ('age_65_74', 3, None, None, None, None, 1, 32768), ('age_75_84', 3, None, None, None, None, 1, 32768), ('age_85_plus', 3, None, None, None, None, 1, 32768),
                       ('age_median', 3, None, None, None, None, 1, 32768), ('new_cases', 3, None, None, None, None, 1, 32768), ('deaths', 3, None, None, None, None, 1, 32768),
                       ('men', 3, None, None, None, None, 1, 32768), ('women', 3, None, None, None, None, 1, 32768), ('race_white', 3, None, None, None, None, 1, 32768),
                       ('race_black', 3, None, None, None, None, 1, 32768), ('race_hispanic_yes', 3, None, None, None, None, 1, 32768), ('race_hispanic_no', 3, None, None, None, None, 1, 32768)]
        fields = [i[0] for i in description]
        data = dict(zip(fields, results))
        
        print(data)
        return render_template('stats2.html', data=data)

@app.route("/map")
def map():
    return render_template("map.html")

if __name__ == "__main__":
    app.run(debug=True)

    cursor.close()
    cnx.close()