# Import libraries

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)                                                            # Initialize the app
app.config["SECRET_KEY"] = "5791628bb0b13ce0c6f6dfde280ba245"                    # Set the secret key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"                      # Initialize the database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True                            # Set it False for production environment
db = SQLAlchemy(app)                                                             # Initialize database variable
bcrypt = Bcrypt(app)                                                             # Initialize bycryption variable


# Routes file is called here so that we can work with different funtions
from main import routes