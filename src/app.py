"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/members', methods=['POST'])
def add_member():
    member_data = request.get_json()
    # Validar campos obligatorios
    required_fields = ["first_name", "age", "lucky_numbers"]
    for field in required_fields:
        if field not in member_data:
            return jsonify({"error": f"Falta el campo obligatorio: {field}"}), 400
    jackson_family.add_member(member_data)
    return jsonify(member_data), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        filtered_member = {
            "first_name": member["first_name"],
            "id": member["id"],
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }
        return jsonify(filtered_member), 200
    return jsonify({"error": "Miembro no encontrado"}), 404

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    result = jackson_family.delete_member(id)
    if result:
        return jsonify({"done": True}), 200
    return jsonify({"done": False}), 404

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
