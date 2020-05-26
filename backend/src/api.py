import os
from flask import (Flask, request, jsonify, abort)
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import (db_drop_and_create_all, setup_db, Drink)
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


#db_drop_and_create_all()

## ROUTES

@app.route('/drinks' , methods=['GET'])
def get_drinks():

    drink_list = Drink.query.all()
    if len(drink_list) == 0:
        abort(404)
    drinks = [drink.short() for drink in drink_list]
    return jsonify({
        "success": True, 
        "drinks": drinks
        }),200
    


@app.route('/drinks-detail' , methods = ['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(token):

    drinks = []
    try:
        data = Drink.query.all()
        if len(data) == 0:
            abort(404)
        
        for drink in data:
            drinks.append(drink.long())
        return jsonify({
            "success": True,
            "drinks": drinks
            }), 200
    except:
        abort(422)



@app.route('/drinks' , methods = ['POST'])
@requires_auth('post:drinks')
def creat_drink(token):
    
    form = request.get_json()
    title =form.get('title')
    recipe = form.get('recipe')
    try:
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
        drink.long()
        return jsonify({
                "success": True,
                "drinks": drink
                }), 200
    except:
        abort(404)


@app.route('/drinks/<int:drink_id>' , methods = ['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(token, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404)
        try:
            form = request.get_json()
            drink.title = form.get('title')
            drink.recipe =form.get('recipe')
            drink.update()
            drink.long()
            return jsonify({
                "success": True,
                "drinks": drink
                }) ,200
        except:
            abort(422)




@app.route('/drinks/<int:drink_id>' , methods = ['DELETE'])
@requires_auth('delete:drinks')
def delet_drink(token, drink_id):
     try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404)
        try:
            drink.delete()
            return jsonify({
                "success": True,
                "delete": drink_id
                }) ,200
        except:
            abort(422)

## Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

@app.errorhandler(AuthError)
def authentification_failed(ex):
    return jsonify({
        "success": False,
        "error": ex.status_code,
        "message": get_error_message(ex.error, "authentification fails")
                    }), ex.status_code