from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# creating app, or app object
app = Flask(__name__) # as in name of the flask app is going to be app

# Create Databse
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"

db = SQLAlchemy(app) #creatin SQLAlchemy obecjt binding it to flask app, we telling it to use config from app.config

#building a model
# The destination model defines the structure of the destination table, in travel.db
class Destination(db.Model): #this class inherits from db.Model and becomes a SQLAlchemy model, maps to a database table named destination,
    #each instance of this class is a row
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    
    #he wants to turn the above into json
    #It converts a Destination object (a row in the database) into a 
    # Python dictionary, which is useful for serializing the data to JSON
    def to_dict(self):
        return {
            "id" : self.id,
            "destination" : self.destination,
            "country" : self.country,
            "rating" : self.rating
        }

# create context manager
with app.app_context(): #Flask-SQLAlchemy relies on the Flask application context to know which app’s configuration to use
    db.create_all() #knows the config and creates


# Create Routes

# home directory ex: www.hectorprokos.com
@app.route("/")
def home():
    #return jsonify({"message":"Welcome to the Travel API"})
    return jsonify([destination.to_dict()] for destination in destinations)

#www.hectorprokos.com/destinations
@app.route("/destinations", methods=["GET"])
def get_destinations():
    destinations = Destination.query.all()

    return jsonify([Destination.to_dict()] for destination in destinations)

#www.hectorprokos.com/destinations/2
@app.route("/destinations/<int:destination_id>", methods=["GET"])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error":"Destination not found!"}), 404


#POST
@app.route("/destinations",methods=["POST"])
def add_destination():
    data = request.get_json()
    new_destination = Destination(destination=data["destination"],
                                  country=data["country"],
                                  rating=data["rating"])

db.session.add(new_destination)
db.session.commit()

return jsonify(new_destination.to_dict), 201


# PUT -> Update
@app.route("/destinations/<int:destination_id>",methods=["PUT"])
def update_destination(destination_id):
    data = request.get_json()

    destination = Destination.query.get(destination_id)
    if destination: #if there is a match                  #second parameter is the default value, keeps existing value
        destination.destination = data.get("destination", destination.destination) #object destination, attribute destination
        destination.country = data.get("country", destination.country)
        destination.rating = data.get("rating", destination.rating)

        db.session.commit()

        return jsonify(destination.to_dict())
    
    else:
        return jsonify({"error":"Destination not found!"}), 404

# DELETE
@app.route("/destinations/<int:destination_id>", methods=["DELETE"]
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        db.session.delete(destination)
        db.session.commit()
        return jsonify({"message":"Destination deleted successfully!"})
    else:
        return jsonify({"error":"Destination not found!"}), 404

#to constantly keep you application running
#contastly be refreshing anytime you makes changes
if __name__ == "__main__":
    app.run(debug=True)

