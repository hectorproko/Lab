from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# creating app, or app object
app = Flask(__name__) # as in name of the flask app is going to be app

# Create Databse


# Create Routes
@app.route("/")
def home():
    return "Hello!"



#to constantly keep you application running
#contastly be refreshing anytime you makes changes
if __name__ == "__main__":
    app.run(debug=True)

