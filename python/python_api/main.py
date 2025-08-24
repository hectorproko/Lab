from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# creating app, or app object
app = Flask(__name__) # as in name of the flask app is going to be app

# Create Databse
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"

db = SQLAlchemy(app)

#building a model
class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    
    #he wants to turn the above into json
    def to_dict(self):
        return {
            "id" : self.id,
            "destination" : self.destination,
            "country" : self.country,
            "rating" : self.rating
        }

# create context manager
with app.app_context():
    db.create_all()


# Create Routes
@app.route("/")
def home():
    return "Hello!"



#to constantly keep you application running
#contastly be refreshing anytime you makes changes
if __name__ == "__main__":
    app.run(debug=True)

