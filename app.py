
from flask import (
    Flask,
    render_template,
    request,
    send_file,
    redirect,
    url_for,
    session
)

import os
import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from src.model_utils import columns, preprocess
from src.report import create_pdf
from src.excel_report import create_excel

from src.database import (
    create_table,
    insert_detection,
    get_all,
    delete_detection,
    delete_all
)


# ======================================================
# Flask App
# ======================================================

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)


# ======================================================
# Session Configuration
# ======================================================

app.secret_key = "ids_project_2026_secret"

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"



# ======================================================
# Paths
# ======================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "app",
    "static",
    "uploads"
)


REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "reports"
)


MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "random_forest.pkl"
)


TEST_DATASET = os.path.join(
    BASE_DIR,
    "dataset",
    "KDDTest+.txt"
)



# ======================================================
# Create folders
# ======================================================

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



# ======================================================
# Load Machine Learning Model
# ======================================================

model = joblib.load(
    MODEL_PATH
)



# ======================================================
# Database
# ======================================================

create_table()



# ======================================================
# Login
# ======================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:

            session.clear()
            session["user"] = username

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Please enter both username and password."
        )

    return render_template("login.html")


# ======================================================
# Logout
# ======================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )



# ======================================================
# Home
# ======================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )



# ======================================================
# Upload Page
# ======================================================

@app.route("/upload")
def upload():

    print(
        "Upload Session:",
        session
    )


    if "user" not in session:

        return redirect(
            url_for("login")
        )


    return render_template(
        "upload.html"
    )



# ======================================================
# Dashboard
# ======================================================

@app.route("/dashboard")
def dashboard():

    print(
        "Dashboard Session:",
        session
    )


    if "user" not in session:

        return redirect(
            url_for("login")
        )


    try:

        df = pd.read_csv(
            TEST_DATASET,
            names=columns
        )


        X, y_true = preprocess(df)


        predictions = model.predict(X)


        total = len(
            predictions
        )


        normal = int(
            (predictions == 1).sum()
        )


        attack = int(
            (predictions == 0).sum()
        )


        accuracy = round(
            accuracy_score(
                y_true,
                predictions
            ) * 100,
            2
        )
        precision = round(
            precision_score(
                y_true,
                predictions,
                zero_division=0
            ) * 100,
            2
        )


        recall = round(
            recall_score(
            y_true,
            predictions,
            zero_division=0
            ) * 100,
            2
        )


        f1 = round(
            f1_score(
            y_true,
            predictions,
            zero_division=0
            ) * 100,
            2
        )


        matrix = confusion_matrix(
            y_true,
            predictions
        )


        insert_detection(
            "KDDTest+.txt",
            total,
            normal,
            attack,
            accuracy
        )


        results=[]


        for i in range(
            min(20,total)
        ):

            results.append(
                {
                    "id":i+1,
                    "prediction":
                    "Normal"
                    if predictions[i]==1
                    else "Attack"
                }
            )


        return render_template(
        "dashboard.html",

        total=total,

        normal=normal,

        attack=attack,

        accuracy=accuracy,

        precision=precision,

        recall=recall,

        f1=f1,

        matrix=matrix,

        results=results
    )


    except Exception as e:

        return f"""
        <h2>Dashboard Error</h2>
        <p>{e}</p>
        """



# ======================================================
# Predict Uploaded File
# ======================================================

@app.route("/predict", methods=["POST"])
def predict():

    if "user" not in session:

        return redirect(
            url_for("login")
        )


    file = request.files.get(
        "file"
    )


    if not file:

        return "No file uploaded"


    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )


    file.save(
        filepath
    )


    try:

        df = pd.read_csv(
            filepath,
            names=columns
        )


        X,y_true = preprocess(df)


        predictions=model.predict(X)


        total=len(predictions)


        normal=int(
            (predictions==1).sum()
        )


        attack=int(
            (predictions==0).sum()
        )


        accuracy = round(
        accuracy_score(
        y_true,
        predictions
        ) * 100,
        2
        )


        precision = round(
        precision_score(
        y_true,
        predictions,
        zero_division=0
        ) * 100,
        2
        )


        recall = round(
        recall_score(
        y_true,
        predictions,
        zero_division=0
        ) * 100,
        2
        )


        f1 = round(
        f1_score(
        y_true,
        predictions,
        zero_division=0
        ) * 100,
        2
        )


        matrix = confusion_matrix(
            y_true,
            predictions
        )


        insert_detection(
            file.filename,
            total,
            normal,
            attack,
            accuracy
        )
        session["report"] = {

        "total": total,

        "normal": normal,

        "attack": attack,

        "accuracy": accuracy

        }
        insert_detection(
            "KDDTest+.txt",
            total,
            normal,
            attack,
            accuracy
        )
        session["report"] = {

            "total": total,

            "normal": normal,

            "attack": attack,

            "accuracy": accuracy
        }
        results=[]


        for i in range(min(20,total)):

            results.append(
                {
                "id":i+1,
                "prediction":
                "Normal"
                if predictions[i]==1
                else "Attack"
                }
            )


        return render_template(
        "dashboard.html",

        total=total,

        normal=normal,

        attack=attack,

        accuracy=accuracy,

        precision=precision,

        recall=recall,

        f1=f1,

        matrix=matrix,

        results=results
    )


    except Exception as e:

        return f"Prediction Error: {e}"



# ======================================================
# History
# ======================================================

@app.route("/history")
def history():

    if "user" not in session:
        return redirect(url_for("login"))

    records = get_all()

    return render_template(
        "history.html",
        records=records
    )
# ==========================================
# Delete One History Record
# ==========================================

@app.route("/delete/<int:record_id>")
def delete(record_id):

    if "user" not in session:
        return redirect(url_for("login"))

    delete_detection(record_id)

    return redirect(url_for("history"))


# ==========================================
# Clear All History
# ==========================================

@app.route("/clear-history")
def clear_history():

    if "user" not in session:
        return redirect(url_for("login"))

    delete_all()

    return redirect(url_for("history"))
# ======================================================
# PDF Download
# ======================================================

@app.route("/download/pdf")
def download_pdf():

    if "user" not in session:
        return redirect(url_for("login"))


    data = session.get("report")


    if not data:
        return "No prediction report available"


    filename = os.path.join(
        REPORT_FOLDER,
        "IDS_Report.pdf"
    )


    create_pdf(
        filename,
        data["total"],
        data["normal"],
        data["attack"],
        data["accuracy"]
    )


    return send_file(
        filename,
        as_attachment=True
    )

# ======================================================
# Excel Download
# ======================================================

@app.route("/download/excel")
def download_excel():

    if "user" not in session:
        return redirect(
            url_for("login")
        )


    data = session.get("report")


    if not data:
        return "No prediction report available"


    filename = os.path.join(
        REPORT_FOLDER,
        "IDS_Report.xlsx"
    )


    create_excel(
        filename,
        data["total"],
        data["normal"],
        data["attack"],
        data["accuracy"]
    )


    return send_file(
        filename,
        as_attachment=True
    )
# ======================================================
# About
# ======================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )



# ======================================================
# Run
# ======================================================

if __name__=="__main__":

    app.run(
        debug=True
    )
# =====================================
# Custom Error Pages
# =====================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500