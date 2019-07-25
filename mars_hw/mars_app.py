# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo 
# import mars_scraping

#from mars_scraping.py import init_browser
# create instance of Flask app


#------------------------------------------------------------------------------------#
# Flask Setup #
#------------------------------------------------------------------------------------#
app = Flask(__name__,template_folder="templates")

# Use PyMongo to set up mongo connection; define db and collection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
#mongo = PyMongo(app)
#------------------------------------------------------------------------------------#
# Local MongoDB connection #
#------------------------------------------------------------------------------------#
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)
## create / Use database
db = client.mars_db
## create/use collection. 
coll = db.mars_data_coll

#------------------------------------------------------------------------------------#
# MLab MongoDB connection #
#------------------------------------------------------------------------------------#
#client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)
##Database connection
#db = client.get_default_database()
###db = client.get_database('healthi_db')

# create route that renders index.html template and finds documents from mongo
# mars_db is the database; mars_data is the collection
@app.route("/")
def index():
    # Get the data from mongodb.
    #scrape()
    mars_mission_data = coll.find_one()
    #mars_mission_data = mars_scrape()
    if mars_mission_data is None:
         mars_mission_data =  {
            "News_Title": "",
            "News_Summary": "",
            "Featured_Image" : "",
            "Weather_Tweet" : "",
            "Facts" : "",
            "Hemisphere_Image_urls": [
                {"img_url":"","title":""},
                {"img_url":"","title":""},
                {"img_url":"","title":""},
                {"img_url":"","title":""}],
            "Date" : "",
        }

    #return template and data
    return render_template("index.html", mars_mission_data=mars_mission_data)
    #return render_template("index.html")

#import python function from mars_scraping.py
from mars_scraping import mars_scrape
# Route that will trigger scrape function.
@app.route("/scrape")
def scrape():
    # Run scrape function.
    mars_mission_data = mars_scrape()
    #print (f'in scrape function. will take a few min to  execute  - {type(mars_mission_data)}')
    #print (f'printing {mars_mission_data}')  

    # Insert mars_mission_data into database
    coll.update({"id": 1}, {"$set": mars_mission_data}, upsert = True)

    # Redirect back to home page
    #return redirect("/", code=302)
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)