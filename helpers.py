import requests
import pandas as pd
import unfccc_di_api
from cs50 import SQL
from flask import redirect, render_template, request, session
from functools import wraps
import folium
import re

def password_validation(password):

    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*)[A-Za-z\d]{6,20}$"

    # compiling regex
    pattern = re.compile(reg)

    # searching regex
    match = re.search(pattern, password)

    # validating conditions
    if match:
        return True
    else:
        False

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def temperature_lookup():
    """Look up monthly tempterature."""

    # Contact API
    try:
        url = f"https://global-warming.org/api/temperature-api"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        data = response.json()

        climate_dict ={
            "time":[],
            "temperature":[]
        }

        for item in range(len(data["result"])):
            climate_dict["time"].append(data["result"][item]["time"])
            climate_dict["temperature"].append(data["result"][item]["land"])

        temperature_df = pd.DataFrame.from_dict(climate_dict)

        return temperature_df

    except (KeyError, TypeError, ValueError):
        return None

def sea_ice_lookup():
    """Look up global sea ice."""

    # Contact API
    try:
        url = f"https://global-warming.org/api/arctic-api"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        data = response.json()

        sea_ice_dict ={
            "time":[],
            "extent":[]
        }

        for item in range(len(data["arcticData"])):
            sea_ice_dict["time"].append(data["arcticData"][item]["year"])
            sea_ice_dict["extent"].append(data["arcticData"][item]["extent"])

        sea_ice_df = pd.DataFrame.from_dict(sea_ice_dict)

        return sea_ice_df

    except (KeyError, TypeError, ValueError):
        return None



def carbon_dioxide_lookup():
    """Look up carbon dioxide."""

    # Contact API
    try:
        url = f"https://global-warming.org/api/co2-api"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        data = response.json()

        climate_dict ={
            "year":[],
            "month":[],
            "CO2":[]
        }

        for item in range(len(data["co2"])):
            climate_dict["year"].append(data["co2"][item]["year"])
            climate_dict["month"].append(data["co2"][item]["month"])
            climate_dict["CO2"].append(data["co2"][item]["trend"])

        co2_df = pd.DataFrame.from_dict(climate_dict)
        co2_df["CO2"]= pd.to_numeric(co2_df["CO2"], errors='coerce')
        co2_df =co2_df.groupby("year")["CO2"].mean()
        co2_df = pd.DataFrame(co2_df)
        co2_df["year"] = co2_df.index

        return co2_df

    except (KeyError, TypeError, ValueError):
        return None

def emission_lookup(country, gas):
    reader = unfccc_di_api.UNFCCCApiReader()
    country_df = reader.query(party_code=country)

    mask = ((country_df["year"] != "Base year") & (country_df["gas"]== gas) & (country_df["measure"] == 'Net emissions/removals') & (country_df["stringValue"] != "NO") & ((country_df["category"] == 'Total GHG emissions without LULUCF') | (country_df["category"] == 'Total GHG emissions with LULUCF')))


    return country_df.loc[mask, ["year", "category","numberValue","gas", "unit"]]


def country_lookup():
    reader = unfccc_di_api.UNFCCCApiReader()

    country_names_and_codes = reader.parties[["code", "name"]]

    return country_names_and_codes



def gen_map():
    db = SQL("sqlite:///project.db")

    survey_data = db.execute("SELECT * FROM survey_results")
    country_data = db.execute("SELECT Country, [Latitude (average)],  [Longitude (average)] FROM countries_codes_and_coordinates")
    country_data = pd.DataFrame(country_data)
    survey_data = pd.DataFrame(survey_data)

    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")

    feature_group = folium.FeatureGroup(name="Survey Data", show=False)

    for (index, row) in country_data.iterrows():
        if row["Country"] in survey_data["country"].values:
            gender_dict= db.execute("SELECT gender, COUNT(*) as count FROM survey_results WHERE country = (?) GROUP BY gender", row["Country"])
            age_dict= db.execute("SELECT age, COUNT(*) as count FROM survey_results WHERE country = (?) GROUP BY age", row["Country"])
            education_dict= db.execute("SELECT education, COUNT(*) as count FROM survey_results WHERE country = (?) GROUP BY education", row["Country"])
            climate_k_rating_dict= db.execute("SELECT climate_k_rating, COUNT(*) as count FROM survey_results WHERE country = (?) GROUP BY climate_k_rating", row["Country"])
            climate_info_source_dict = db.execute("SELECT climate_info_source, COUNT(*) as count FROM survey_results WHERE country = (?) GROUP BY climate_info_source", row["Country"])
            climate_info_source_dict = db.execute("SELECT climate_info_source, COUNT(*) as count FROM survey_results WHERE country = (?) GROUP BY climate_info_source", row["Country"])
            climate_causes_dict = db.execute("SELECT climate_causes, COUNT(*) as count FROM survey_results WHERE country = (?) GROUP BY climate_causes", row["Country"])
            anxiety_dict = db.execute("SELECT anxiety, COUNT(*) as count FROM survey_results WHERE country = (?) GROUP BY anxiety", row["Country"])
            personal_dict= db.execute("SELECT personal, COUNT(*) as count FROM survey_results WHERE country = (?) GROUP BY personal", row["Country"])
            government_action_dict= db.execute("SELECT government_action, COUNT(*) as count FROM survey_results WHERE country = (?) GROUP BY government_action", row["Country"])
            politics_dict= db.execute("SELECT politics, COUNT(*) as count FROM survey_results WHERE country = (?) GROUP BY politics", row["Country"])

            html="""
            <h2> Survey Data</h2><br>

            <strong>Name: </strong> {name}<br>
            <strong>Gender: </strong> {gender}<br>
            <strong>Age: </strong> {age}<br>
            <strong>Education: </strong> {education}<br>
            <strong>Climate Change Knowledge: </strong> {climate_k_rating}<br>
            <strong>Information Sources: </strong> {climate_info_source}<br>
            <p>

            """.format(name=row["Country"],
                        age=string_return(age_dict, "age"),
                        gender=string_return(gender_dict, "gender"),
                        education=string_return(education_dict, "education"),
                        climate_k_rating= string_return(climate_k_rating_dict, "climate_k_rating"),
                        climate_info_source= string_return(climate_info_source_dict, "climate_info_source"),
                        climate_causes = string_return(climate_causes_dict, "climate_causes"),
                        anxiety = string_return(anxiety_dict, "anxiety"),
                        personal=string_return(personal_dict, "personal"),
                        government_action=string_return(government_action_dict, "government_action"),
                        politics=string_return(politics_dict,"politics"))

            popup = folium.Popup(html, max_width=2650)

            folium.Marker(location=[row.loc['Latitude (average)'], row.loc['Longitude (average)']],
                            popup=popup,icon=folium.Icon(color='blue', icon_color='white', icon='info-sign', angle=0, prefix='glyphicon')).add_to(feature_group)


    feature_group.add_to(m)
    m.save("templates/map.html")


def string_return(_dict, column):

    _text =""

    for i in range(len(_dict)):
        cat = _dict[i][column]
        count = str(_dict[i]['count'])
        line =[cat, ": ", count, ", "]
        _text +="".join(line)

    return _text

