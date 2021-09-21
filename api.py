from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Employee API',
)

ns = api.namespace('employees', description='Employees Crud operations')

#region Employer
employer = api.model('Employer', {
    'EmployerID': fields.Integer(readonly=True, description='The task unique identifier'),
    'CompanyName': fields.String(required=True),
    'Address': fields.String(required=True),
    'City': fields.String(required=True),
    'State': fields.String(required=True)
})

class EmployerDAO(object):
    def __init__(self):
        self.counter = 0
        self.employers = []

    def get(self, id):
        for employer in self.employers:
            if employer['EmployerID'] == id:
                return employer
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        employer = data
        employer['EmployerID'] = self.counter = self.counter + 1
        self.employers.append(employer)
        return employer



DAO = EmployerDAO()
DAO.create({'CompanyName': 'Analiza', 'Address': 'SS', 'City' : 'Escalon','State': 'ESA'})

@ns.route('/')
class EmployerList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @api.marshal_list_with(employer)
    def get(self):
        '''List all tasks'''
        return DAO.employers

    @api.doc('create_todo')
    @api.expect(employer)
    @api.marshal_with(employer, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201

#endregion

#region Employee
employee = api.model('Employee', {
    'EmployeeID': fields.Integer(readonly=True, description='The task unique identifier'),
    'EmployerID': fields.Integer(description='The task unique identifier'),
    'FirstName': fields.String(required=True),
    'LastName': fields.String(required=True),
    'Address': fields.String(required=True),
    'City': fields.String(required=True),
    'State': fields.String(required=True)
})

class EmployeeDAO(object):
    def __init__(self):
        self.counter = 0
        self.employees = []

    def get(self, id):
        for employee in self.employees:
            if employee['EmployeeID'] == id:
                return employer
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        employee = data
        employee['EmployeeID'] = self.counter = self.counter + 1
        self.employees.append(employee)
        return employee


DAOEmployee = EmployeeDAO()
DAOEmployee.create({'EmployerID': '1', 'FirstName': 'Rob', 'LastName' : 'Escalon','Address': 'ESA','City': 'SS','State': 'ESA'})

@ns.route('/employee')
class EmployeeList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @api.marshal_list_with(employee)
    def get(self):
        '''List all tasks'''
        return DAOEmployee.employees

    @api.doc('create_todo')
    @api.expect(employee)
    @api.marshal_with(employee, code=201)
    def post(self):
        '''Create a new task'''
        return DAOEmployee.create(api.payload), 201

#endregion

#region Client
client = api.model('Client', {
    'ClientID': fields.Integer(readonly=True, description='The task unique identifier'),
    'EmployeeID': fields.Integer(description='The task unique identifier'),
    'ClientName': fields.String(required=True),
    'Address': fields.String(required=True),
    'City': fields.String(required=True),
    'State': fields.String(required=True)
})

class ClientDAO(object):
    def __init__(self):
        self.counter = 0
        self.clients = []

    def get(self, id):
        for client in self.clients:
            if client['ClientID'] == id:
                return client
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        client = data
        client['ClientID'] = self.counter = self.counter + 1
        self.clients.append(client)
        return client

    def update(self, id, data):
        client = self.get(id)
        client.update(data)
        return client


DAOClient = ClientDAO()
DAOClient.create({'EmployeeID': '1', 'ClientName': 'Rob','Address': 'ESA','City': 'SS','State': 'ESA'})

@ns.route('/client')
class ClientList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @api.marshal_list_with(client)
    def get(self):
        '''List all tasks'''
        return DAOClient.clients

    @api.doc('create_todo')
    @api.expect(client)
    @api.marshal_with(client, code=201)
    def post(self):
        '''Create a new task'''
        return DAOClient.create(api.payload), 201

    @ns.expect(client)
    @ns.marshal_with(client)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)
#endregion

if __name__ == '__main__':
    app.run(debug=True)