from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
with open('./mock.json', 'r') as file:  # Adjust the path as necessary
    mock_ads = json.load(file)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///real_estate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incremented primary key
    link = db.Column(db.String, nullable=True)
    source = db.Column(db.String, nullable=True)
    scraper_id = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=True)
    properties = db.Column(db.Text, nullable=True)  # Stored as JSON string
    images = db.Column(db.Text, nullable=True)  # Stored as JSON string
    phone = db.Column(db.String, nullable=True)
    user = db.Column(db.String, nullable=True)
    publish_date = db.Column(db.String, nullable=True)

with app.app_context():
    db.create_all()

@app.route('/api/property', methods=['POST'])
def create_properties():
    data = request.json  # Expects a list of property data
    for property_data in data:
        new_property = Property(
            link=property_data.get("Link"),
            source=property_data.get("Source"),
            scraper_id=property_data.get("Id"),
            description=property_data.get("Description"),
            properties=json.dumps(property_data.get("Properties", {})),  # Convert to JSON string
            images=json.dumps(property_data.get("Images", [])),  # Convert to JSON string
            phone=property_data.get("Phone"),
            user=property_data.get("User"),
            publish_date=property_data.get("Publish Date"),
        )
        db.session.add(new_property)
    db.session.commit()

    return jsonify({
        "message": "All property data saved successfully",
        "saved_count": len(data)
    }), 201

@app.route('/api/property', methods=['GET'])
def get_properties():
    properties = Property.query.all()
    property_list = []
    for prop in properties:
        property_dict = {
            "id": prop.id,
            "link": prop.link,
            "source": prop.source,
            "scraper_id": prop.scraper_id,
            "description": prop.description,
            "properties": prop.properties if prop.properties else {},
            "images": prop.images if prop.images else [],
            "phone": prop.phone,
            "user": prop.user,
            "publish_date": prop.publish_date
        }
        property_list.append(property_dict)

    return jsonify(property_list), 200

@app.route('/api/property/mock', methods=['GET'])
def get_mock_properties():
    return mock_ads, 200

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "API is running!"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')