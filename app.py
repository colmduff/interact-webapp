from cs50 import SQL
from flask import flash, redirect, render_template, request, session
from flask_session import Session
import connexion
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
import json
import plotly
import plotly.express as px

from helpers import password_validation, apology, login_required, temperature_lookup, emission_lookup, country_lookup, carbon_dioxide_lookup, sea_ice_lookup, gen_map

# Configure application
app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")
#app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
application = app.app
application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
Session(application)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@application.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@application.route("/")
def index():
    """Show A Welcome message and ask to register/login"""

    return render_template(
        "index.html"
    )

@application.route("/map", methods=["GET"])
@login_required
def data_mapping():

    gen_map()

    return render_template("map.html")

@application.route("/api_route", methods=["GET"])
@login_required
def api_route():
    return render_template("docs.html")

@application.route("/world_emissions", methods=["GET"])
def world_emissions():
    """get global emissions"""

    temperature_df = temperature_lookup()
    carbon_dioxide_df = carbon_dioxide_lookup()
    sea_ice_df = sea_ice_lookup()

    fig = px.line(temperature_df, x="time", y="temperature",template="plotly_white",  markers=True,
        labels=dict(time="Year", temperature=f"Degrees Celcius"))

    fig.update_traces(line_color='red', line_width=.5)

    fig1 = px.line(carbon_dioxide_df, x="year", y="CO2",template="plotly_white", markers=True,
                   labels=dict(x="Year", CO2=f"Carbon Dioxide parts per million"))

    fig2 = px.line(sea_ice_df, x="time", y="extent",template="plotly_white",  markers=True,
    labels=dict(time="Year", extent=f"Million km2"))

    fig2.update_traces(line_color='green', line_width=.5)


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("world.html",  graphJSON=graphJSON, graphJSON1=graphJSON1, graphJSON2=graphJSON2)


@application.route("/national_emissions", methods=["GET", "POST"])
def national_emissions():
    """Show emissoins for selected country"""
    #get country names and codes
    countries = country_lookup()
    gas = ['Aggregate_GHGs', 'CH4', 'CO', 'CO2', 'NMVOC', 'NOx', 'N2O', 'SO2'
                    'Aggregate_F-gases', 'HFCs', 'SF6']

    if request.method == "POST":
        #https://towardsdatascience.com/web-visualization-with-plotly-and-flask-3660abf9c946

        country_name = request.form.get("country")
        country_code = countries["code"].loc[(countries["name"] == country_name)].values[0]


        gas_selection = request.form.get("gas").replace("_", " ")

        country_df = emission_lookup(country_code, gas_selection)

        unit = country_df.unit.unique()

        fig = px.line(country_df, x="year", y="numberValue", color="category",template="plotly_white",  markers=True,
                      labels=dict(year="Year", numberValue=f"{gas_selection} in {unit[0]}", category="Category"))


        graphJSON3 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template("national_emissions.html",
                               graphJSON3=graphJSON3,
                               country_name =country_name,
                               unit=unit[0],
                               gas_selection=gas_selection)

    else:

        return render_template("national_emissions_request.html", countries = countries["name"], gas=gas)


@application.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@application.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@application.route("/survey", methods=["GET", "POST"])
@login_required
def survey():
    """input survey data"""
    if request.method == "POST":

        survey_flag = db.execute("SELECT survey_complete FROM users WHERE id = (?)", session["user_id"])

        print(survey_flag[0]["survey_complete"])

        if survey_flag[0]["survey_complete"] == 1:

            return apology("Survey already registered")

        else:
            row = [session["user_id"],
                    request.form.get("gender"),
                    request.form.get("age"),
                    request.form.get("education"),
                    request.form.get("knowledge"),
                    request.form.get("sources"),
                    request.form.get("causes"),
                    request.form.get("anxiety"),
                    request.form.get("personal"),
                    request.form.get("government"),
                    request.form.get("politics"),
                    request.form.get("country"),
                    date.today()]

            db.execute("INSERT INTO survey_results (user_id, gender, age, education, climate_k_rating, climate_info_source, climate_causes, anxiety, personal, government_action, politics, country, date) VALUES(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?)",
                        *row,
                    )

            db.execute("UPDATE users SET survey_complete = 1 WHERE id = (?)", session["user_id"])


            flash("Survey Registered!")

            return redirect("/survey_history")

    else:

        gender = db.execute("SELECT response1, response2, response3, response4, response5 FROM survey_questions WHERE question = 'gender'")
        age = db.execute("SELECT response1, response2, response3, response4, response5 FROM survey_questions WHERE question = 'age'")
        education = db.execute("SELECT response1, response2, response3, response4, response5 FROM survey_questions WHERE question = 'education'")
        climate_k_rating = db.execute("SELECT response1, response2, response3, response4, response5 FROM survey_questions WHERE question = 'climate_k_rating'")
        climate_info_source = db.execute("SELECT response1, response2, response3, response4, response5 FROM survey_questions WHERE question = 'climate_info_source'")
        climate_causes = db.execute("SELECT response1, response2, response3, response4, response5 FROM survey_questions WHERE question = 'climate_causes'")
        anxiety = db.execute("SELECT response1, response2, response3, response4, response5 FROM survey_questions WHERE question = 'anxiety'")
        personal = db.execute("SELECT response1, response2, response3, response4, response5 FROM survey_questions WHERE question = 'personal'")
        government_action = db.execute("SELECT response1, response2, response3, response4, response5 FROM survey_questions WHERE question = 'government_action'")
        politics = db.execute("SELECT response1, response2, response3, response4, response5 FROM survey_questions WHERE question = 'politics'")
        countries =db.execute("SELECT Country FROM countries_codes_and_coordinates")

        return render_template("survey.html",
                               gender=gender,
                               age=age,
                               education=education,
                               climate_k_rating=climate_k_rating,
                               climate_info_source=climate_info_source,
                               climate_causes=climate_causes,
                               anxiety=anxiety,
                               personal=personal,
                               government_action=government_action,
                               politics=politics,
                               countries = countries)


@application.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("Username or Password cannot be empty")

        elif not password_validation(password):
            return apology("Invalid Password")

        elif password != confirmation:
            return apology("Password matching error")

        else:
            password_hash = generate_password_hash(password)

            if db.execute("SELECT username FROM users WHERE username = ?", username):
                return apology("User already exists")

            db.execute(
                "INSERT INTO users (username, hash) VALUES(?, ?)",
                username,
                password_hash,
            )

        return redirect("/login")
    else:
        return render_template("register.html")


@application.route("/survey_history", methods=["GET"])
@login_required
def survey_history():
    """Show survey responses"""
    result = db.execute(
        "SELECT * FROM survey_results WHERE user_id = (?)", session["user_id"]
    )

    return render_template("history.html", result=result)



