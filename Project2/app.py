import os

import pandas as pd
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import select

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

from pprint import pprint
from operator import itemgetter
app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/MigrationData.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Mydata = Base.classes.mydata


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/maps")
def maps():
    # print()
    return data_for_plugin_2015.json


if __name__ == "__main__":
    app.run()