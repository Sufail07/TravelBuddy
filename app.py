from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_sitemapper import Sitemapper
from geopy.geocoders import Nominatim
import requests
import datetime
import os
from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict

# Load the environment variables
load_dotenv()
api_key = os.environ.get("WEATHER_API_KEY")
secret_key = os.environ.get("SECRET_KEY")
places_api_key = "3ca4a31205a043f6b2b1f420e7c4987b"
geocoder = Nominatim(user_agent="Sufail")

# Initialize the app
app = Flask(__name__)
sitemapper = Sitemapper(app=app) # Create and initialize the sitemapper
app.secret_key = secret_key



# Weather Data 

def get_weather_data(api_key: str, location: str, start_date: str, end_date: str) -> dict:
    """
    Retrieves weather data from Visual Crossing Weather API for a given location and date range.

    Args:
        api_key (str): API key for Visual Crossing Weather API.
        location (str): Location for which weather data is to be retrieved.
        start_date (str): Start date of the date range in "MM/DD/YYYY" format.
        end_date (str): End date of the date range in "MM/DD/YYYY" format.

    Returns:
        dict: Weather data in JSON format.

    Raises:
        requests.exceptions.RequestException: If there is an error in making the API request.
    """
    # Date Formatting as per API "YYYY-MM-DD"

    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}?unitGroup=metric&include=days&key={api_key}&contentType=json"

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        data = response.json()
        # print(json.dumps(data, indent=4, sort_keys=True))
        return data
    except requests.exceptions.RequestException as e:
        print("Error:", e.__str__)
        


def get_places_of_interest(lon, lat, radius, categories):
    url = f"https://api.geoapify.com/v2/places?categories={categories}&filter=circle:{lon},{lat},{radius}&bias=proximity:{lon},{lat}&limit=10&apiKey={places_api_key}"
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        return response.json()["features"]  # Returns JSON response containing places of interest
    else:
        return None

@sitemapper.include() # Include the route in the sitemap
@app.route('/', methods=["GET", "POST"])
def index():
    """
    Renders the index.html template.

    Returns:
        The rendered index.html template.
    """
    if request.method == "POST":
        global source, destination, start_date, end_date
        source = request.form.get("source")
        destination = request.form.get("destination")
        start_date = request.form.get("date")
        end_date = request.form.get("return")
        # Calculating the number of days
        no_of_day = (datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.datetime.strptime(start_date, "%Y-%m-%d")).days
        # Process the route input here
        if no_of_day < 0:
            flash("Return date should be greater than the Travel date (Start date).", "danger")
            return redirect(url_for("index"))
        else:
            try:
                weather_data = get_weather_data(api_key, destination, start_date, end_date)
            except requests.exceptions.RequestException as e:
                flash("Error in retrieving weather data.{e.Error}", "danger")
                return redirect(url_for("index"))
        
        # getting coordinates
        
        origin_coords = [geocoder.geocode(source).latitude, geocoder.geocode(source).longitude]
        dest_coords = [geocoder.geocode(destination).latitude, geocoder.geocode(destination).longitude]
        
        # Getting the places of interest at the destination
        categories = "entertainment.culture,entertainment.museum,national_park,entertainment.zoo,entertainment.theme_park,entertainment.activity_park,national_park,beach,beach.beach_resort,natural,entertainment.water_park,catering.bar,heritage,natural"
        pois = get_places_of_interest(geocoder.geocode(destination).longitude, geocoder.geocode(destination).latitude, 10000, categories)
        
        places = []
        id = 0
        print(pois)
        for point in pois:
            if "name" in point["properties"]:
                name = point["properties"]["name"]
                if "lon" in point["properties"] and "lat" in point["properties"]:
                    coords = (point["properties"]["lon"], point["properties"]["lat"])
                    if "formatted" in point["properties"]:
                        info = point["properties"]["formatted"]
                        places.append({
                            'id': id,
                            'Name': name,
                            'Coordinates': coords,
                            'Information': info
                        })
            id += 1
        print(places)
        
        """Debugging"""
        # Json data format printing
        # print(json.dumps(weather_data, indent=4, sort_keys=True))
        if weather_data:
            # Render the weather information in the template
            return render_template("dashboard.html", weather_data=weather_data, origin=origin_coords, destination=dest_coords, location=destination, start_date=start_date, end_date=end_date, places=places)
    
    return render_template('index.html')

@sitemapper.include() # Include the route in the sitemap
@app.route("/about")
def about():
    """
    Renders the about.html template.

    Returns:
        The rendered about.html template.
    """
    return render_template("about.html")

@sitemapper.include() # Include the route in the sitemap
@app.route("/contact")
def contact():
    """
    Renders the contact.html template.

    Returns:
        The rendered contact.html template.
    """
    user_email = session.get('user_email', "Enter your email")
    user_name = session.get('user_name', "Enter your name")
    message = ''

    return render_template("contact.html", user_email=user_email, user_name=user_name, message=message)


# Robots.txt
@app.route('/robots.txt')
def robots():
    return render_template('robots.txt')

# Sitemap
@app.route("/sitemap.xml")
def r_sitemap():
    return sitemapper.generate()

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    """
    Renders the 404.html template.

    Returns:
        The rendered 404.html template.
    """
    return render_template('404.html'), 404

# Injecting current time into all templates for copyright year automatically updation
@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now()}


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()