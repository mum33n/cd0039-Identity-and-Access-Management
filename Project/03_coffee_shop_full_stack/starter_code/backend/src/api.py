import os
from turtle import title
from click import Abort
from flask import Flask, request, jsonify, abort
# from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.sort_by(Drink.id).all()
    formated = drinks.short()
    return jsonify({'success': True, 'drinks': formated})


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    drinks = Drink.query.sort_by(Drink.id).all()
    formated = drinks.long()
    return jsonify({'success': True, 'drinks': formated})


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks():
    data = request.get_json()
    id = data.get('id')
    title = data.get('title')
    recipe = data.get('recipe')
    if id and title and recipe:
        drink = Drink(id=id, title=title, recipe=recipe)
        drink.insert()
        formated = drink.long()
    else:
        Abort(422)

    return jsonify({'success': True, 'drinks': formated})


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(id):
    data = request.get_json()
    id = data.get('id')
    title = data.get('title')
    recipe = data.get('recipe')
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is not None:
        formated = drink.long()
        if id or title or recipe:
            if id:
                drink.id = id
                drink.update()
            if title:
                drink.title = title
                drink.update()
            if recipe:
                drink.recipe = recipe
                drink.update()
        else:
            Abort(422)
    else:
        Abort(404)

    return jsonify({'success': True, 'drinks': formated})


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('delete:drinks')
def delete_drinks(id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is not None:
        drink.delete()
    else:
        Abort(404)

    return jsonify({'success': True, 'delete': id})


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Not Processed'
    }), 422


@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500


@app.errorhandler(502)
def bad_gateway(error):
    return jsonify({
        'success': False,
        'error': 502,
        'message': 'bad gateway'
    }), 502


@app.errorhandler(501)
def not_implemented(error):
    return jsonify({
        'success': False,
        'error': 501,
        'message': 'not implemented'
    }), 501


@app.errorhandler(503)
def service_unavailable(error):
    return jsonify({
        'success': False,
        'error': 503,
        'message': 'service unavaailable'
    }), 503


@app.errorhandler(504)
def not_implemented(error):
    return jsonify({
        'success': False,
        'error': 504,
        'message': 'gateway timeout'
    }), 504


@app.errorhandler(505)
def not_supported(error):
    return jsonify({
        'success': False,
        'error': 505,
        'message': 'http version not supported'
    }), 501


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401
