'''
steps to take:

1. change directory into the chalice project and run chalice deploy 

2. stdout will return the api_gateway url, copy and paste it into the variable below:
$api_url = ''
api_url=''

3. execute the command in powershell\bash for your convience 
'''

import sys
from chalice import Chalice
from chalice import BadRequestError
from chalice import UnauthorizedError
from chalice import NotFoundError
from chalice import Chalice
from urllib.parse import urlparse, parse_qs

app = Chalice(app_name='helloworld')

# required for more specific errors
app.debug = True

CITIES_TO_STATE = {
    'seattle': 'WA',
    'portland': 'OR',
}

OBJECTS = {
}


# @app.route('/')
# def index():
#     return {'hello': 'world'}

@app.route('/cities/{city}')
def state_of_city(city):
    try:
        return {'state': CITIES_TO_STATE[city]}
    except KeyError:
        raise BadRequestError("Unknown city '%s', valid choices are: %s" % (
            city, ', '.join(CITIES_TO_STATE.keys())))

@app.route('/resource/{value}', methods=['PUT'])
def put_test(value):
    return {"value": value}

@app.route('/myview', methods=['POST', 'PUT'])
def myview():
    pass

####################################################################################################
# request metadata
####################################################################################################

@app.route('/objects/{key}', methods=['GET', 'PUT'])
def myobject(key):
    request = app.current_request
    if request.method == 'PUT':
        OBJECTS[key] = request.json_body
    elif request.method == 'GET':
        try:
            return {key: OBJECTS[key]}
        except KeyError:
            raise NotFoundError(key)
# echo '{"foo": "bar"}' | http PUT $api_url/api/objects/mykey  
# http GET $api_url/api/objects/mykey


@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()
# chalice deploy
# http '$api_url/api/introspect?query1=value1&query2=value2' 'X-TestHeader: Foo'

####################################################################################################
# request content types
####################################################################################################


@app.route('/', methods=['POST'],
           content_types=['application/x-www-form-urlencoded'])
def index():
    parsed = parse_qs(app.current_request.raw_body.decode())
    return {
        'states': parsed.get('states', [])
    }
# http POST $api_url/api/ states=WA states=CA --debug 
# http --form POST $api_url/api/formtest states=WA states=CA --debug

# http POST $api_url/api/ states=WA states=CA --debug 
# http --form POST $api_url/api/formtest states=WA states=CA --debug

#