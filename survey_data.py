from cs50 import SQL

def read_all():
    db = SQL("sqlite:///project.db")
    SURVEY = db.execute("SELECT * FROM survey_results")

    return SURVEY