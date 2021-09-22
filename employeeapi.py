from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Información Employer/Employee/Client API',
)

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

ns = api.namespace('venta', description='Employer/Employee/Client Crud operations')

#region Models
class Employer(db.Model):
    employerID = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(100), unique=True)
    address =  db.Column(db.String(200))
    city =  db.Column(db.String(200))
    state =  db.Column(db.String(200))

    def __init__(self, companyName, address, city, state):
        self.companyName = companyName
        self.address = address
        self.city = city
        self.state = state

class Employee(db.Model):
    employeeID = db.Column(db.Integer, primary_key=True)
    employerID = db.Column(db.String(100))
    firstName =  db.Column(db.String(200))
    lastName =  db.Column(db.String(200))
    address =  db.Column(db.String(200))
    city =  db.Column(db.String(200))
    state =  db.Column(db.String(200))

    def __init__(self, employerID, firstName, lastName, address, city, state):
        self.employerID = employerID
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.city = city
        self.state = state

class Client(db.Model):
    clientID = db.Column(db.Integer, primary_key=True)
    employeeID = db.Column(db.String(100))
    clientName =  db.Column(db.String(200))
    address =  db.Column(db.String(200))
    city =  db.Column(db.String(200))
    state =  db.Column(db.String(200))

    def __init__(self, employeeID, clientName, address, city, state):
        self.employeeID = employeeID
        self.clientName = clientName
        self.address = address
        self.city = city
        self.state = state
#endregion

#region Schemas
class EmployerSchema(ma.Schema):
  class Meta:
    fields = ('employerID','companyName','address','city','state')

class EmployeeSchema(ma.Schema):
  class Meta:
    fields = ('employeeID','employerID','firstName','lastName','address','city','state')

class ClientSchema(ma.Schema):
  class Meta:
    fields = ('clientID','employeeID','clientName','address','city','state')
#endregion

#region Init schema
employer_schema = EmployerSchema()
employers_schema = EmployerSchema(many=True)
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)
#endregion

#region Employer
# Create a Employer
@app.route('/venta/employer', methods=['POST'])
def addEmployer():
    companyName = request.json['companyName']
    address =  request.json['address']
    city = request.json['city']
    state = request.json['state']

    new_employer = Employer(companyName,address,city,state)

    db.session.add(new_employer)
    db.session.commit()

    return employer_schema.jsonify(new_employer)

# Get All Employers
@app.route('/venta/employer', methods=['GET'])
def getEmployers():
    all_employers = Employer.query.all()
    result = employers_schema.dump(all_employers)
    return jsonify(result)

employer = api.model('Employer', {
    'employerID': fields.Integer(readonly=True, description='The task unique identifier'),
    'companyName': fields.String(required=True),
    'address': fields.String(required=True),
    'city': fields.String(required=True),
    'state': fields.String(required=True)
})


@ns.route('/employer')
class EmployerListAndCreate(Resource):
    
    @ns.doc('list_employers')
    @api.marshal_list_with(employer)
    def get(self):
        '''List all employers'''
        return getEmployers()

    @api.doc('create_employer')
    @api.expect(employer)
    @api.marshal_with(employer, code=201)
    def post(self):
        '''Create a new employer'''
        return addEmployer()
#endregion

#region Employee
# Create a Employee
@app.route('/venta/employee', methods=['POST'])
def addEmployee():
    employerID = request.json['employerID']
    firstName =  request.json['firstName']
    lastName = request.json['lastName']
    address =  request.json['address']
    city =  request.json['city']
    state =  request.json['state']

    new_employee = Employee(employerID,firstName,lastName,address,city,state)

    db.session.add(new_employee)
    db.session.commit()

    return employee_schema.jsonify(new_employee)

# Get Single Employee
@app.route('/venta/employee/<id>', methods=['GET'])
def getEmployeeByid(id):
  employee = Employee.query.get(id)
  return employee_schema.jsonify(employee)

employee = api.model('Employee', {
    'employeeID': fields.Integer(readonly=True, description='The task unique identifier'),
    'employerID': fields.Integer(description='The task unique identifier'),
    'firstName': fields.String(required=True),
    'lastName': fields.String(required=True),
    'address': fields.String(required=True),
    'city': fields.String(required=True),
    'state': fields.String(required=True)
})

@ns.route('/employee/<id>')
@api.doc(params={'id': 'employeeID'})
class EmployeeByid(Resource):
    @ns.doc('list_employees')
    @api.marshal_with(employee)
    def get(self,id):
        '''List employee by id'''
        return getEmployeeByid(id)

@ns.route('/employee')
class EmployeeCreate(Resource):
    @api.doc('create_employee')
    @api.expect(employee)
    @api.marshal_with(employee, code=201)
    def post(self):
        '''Create a new employee'''
        return addEmployee()
#endregion

#region Client
# Create a Client
@app.route('/venta/client', methods=['POST'])
def addClient():
    employeeID = request.json['employeeID']
    clientName =  request.json['clientName']
    address =  request.json['address']
    city =  request.json['city']
    state =  request.json['state']

    new_client= Client(employeeID,clientName,address,city,state)

    db.session.add(new_client)
    db.session.commit()

    return client_schema.jsonify(new_client)

# Get All Client
@app.route('/venta/client', methods=['GET'])
def getClients():
    all_clients = Client.query.all()
    result = clients_schema.dump(all_clients)
    return jsonify(result)


# Update a Client
@app.route('/venta/client/<id>', methods=['PUT'])
def updateClient(id):
    client = Client.query.get(id)
    employeeID = request.json['employeeID']
    clientName =  request.json['clientName']
    address =  request.json['address']
    city =  request.json['city']
    state =  request.json['state']

    client.employeeID = employeeID
    client.clientName = clientName
    client.address = address
    client.city = city
    client.state = state

    db.session.commit()

    return client_schema.jsonify(client)

client = api.model('Client', {
    'clientID': fields.Integer(readonly=True, description='The task unique identifier'),
    'employeeID': fields.Integer(description='The task unique identifier'),
    'clientName': fields.String(required=True),
    'address': fields.String(required=True),
    'city': fields.String(required=True),
    'state': fields.String(required=True)
})

@ns.route('/client')
class clientListAndCreate(Resource):
    @api.doc('create_client')
    @api.expect(client)
    @api.marshal_with(client, code=201)
    def post(self):
        '''Create a new client'''
        return addClient()

    @ns.doc('list_clients')
    @api.marshal_list_with(client)
    def get(self):
        '''List all clients'''
        return getClients()

@ns.route('/client/<id>')
@api.doc(params={'id': 'clientID'})
class clientUpdate(Resource):
    @ns.doc('list_employees')
    @api.expect(client)
    def put(self,id):
        '''Update a client given its identifier'''
        return updateClient(id)
#endregion

if __name__ == '__main__':
    app.run(debug=True)