from flask import Flask, render_template, request, current_app
import mysql.connector
import os
import json

app = Flask(__name__)

cnx = mysql.connector.connect(user='puser', password='securepw',
                              host='localhost', database='cop4710')

cursor = cnx.cursor()

#our sql queries
query = ("SELECT * FROM County WHERE county_name = %s")
query2 = ("SELECT * FROM City WHERE City.name = %s")
query3 = ("SELECT * FROM zip_code WHERE zip_code = %s")
#total cases in a given city
total_cases = ("SELECT SUM(num_cases) AS cases FROM City," 
          "zip_code WHERE city = name AND name = %s")

#all the cities and counties in our DB, will use to check input and 
#for autocomplete
cursor.execute("SELECT county_name FROM County")
county_list = [i[0].lower() for i in cursor.fetchall()]
cursor.execute("SELECT name FROM City")
city_list = [i[0].lower() for i in cursor.fetchall()]

@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")


@app.route("/stats", methods=['GET', 'POST'])
def stats():
    if request.method == "POST":
        search_text = (request.form["city/county/zip"]).lower()
 
        #if its a county request
        if search_text in county_list:
            cursor.execute(query,(search_text,))
            results = cursor.fetchone()
            fields = ['County Name','Total Cases','Ages 0-4','Ages 15-24',
                      'Ages 25-34','Ages 35-44', 'Ages 45-54','Ages 5-14',
                      'Ages 55-64','Ages 65-74','Ages 75-84','Ages 85+',
                      'Median Age','New Cases','Deaths','Men','Women', 
                      'White','Black','Hispanic','Non Hispanic']

            data = dict(zip(fields, results))
            return render_template('stats2.html', data=data)

        #if its a city request
        elif search_text in city_list:
            cursor.execute(query2,(search_text,))
            results = cursor.fetchone()
            results_list = list(results)
            cursor.execute(total_cases,(search_text,))
            total = cursor.fetchone()[0]
            results_list.append(total)
            fields = ['City','County','Total Cases']

            data = dict(zip(fields, results_list))
            return render_template('stats2.html', data=data)

        #if its a zipcode
        elif search_text.isdigit():
            cursor.execute(query3,(search_text,))
            results = cursor.fetchone()
            fields = ['Zip-code', 'Total Cases', 'City', 'County']

            data = dict(zip(fields, results))
            return render_template('stats2.html', data=data)

        #if its anything else that is not in our DB 
        else:
            return render_template('error.html')

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/county.geojson", methods=['GET'])
def map_render():
    root = os.path.realpath(os.path.dirname(__file__)) 
    json_url = os.path.join(root, "static", "county.geojson")
    data = json.load(open(json_url))
    return data

if __name__ == "__main__":
    app.run(debug=True)

    cursor.close()
    cnx.close()
