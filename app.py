from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # create an app_structure

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Niadatabase.db' #create database
app.config['SECRET_KEY'] = 'my super secret key' #secret Key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_SILENCE_UBER_WARNING'] = 1


db=SQLAlchemy(app) # initialize the databese
class Employee(db.Model): #inherete db.Model
    id = db.Column(db.Integer, primary_key = True) # primary key este intotdeauna unigue
    first_name = db.Column(db.String(50),nullable = False) # nullable = nu poate fi casuta goala in firstname
    last_name = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.Integer, unique = True)
    email = db.Column(db.String(50), nullable = False, unique = True)

    def __init__(self,first_name, last_name, phone, email):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email

class Services(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sub_service = db.Column(db.String(50),nullable = False)
    service = db.Column(db.String(50), nullable = False)
    price = db.Column(db.Integer, nullable = False)

    def __init__(self,sub_service, service, price):
        self.sub_service = sub_service
        self.service = service
        self.price = price

class Clients(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50),nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(1),nullable = False)
    phone = db.Column(db.Integer, nullable = False, unique = True)
    email = db.Column(db.String(50), nullable = False, unique = True)

    def __init__(self,first_name, last_name, age, gender,phone, email):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.email = email

class Appointments(db.Model):
    employee_name = db.Column(db.String(50),nullable = False)
    hour = db.Column(db.String(50), nullable=False)
    client_firstname = db.Column(db.String(50))
    client_lastname = db.Column(db.String(50))
    sub_service = db.Column(db.String(50))
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self,employee_name, hour, client_firstname, client_lastname , sub_service):
        self.employee_name = employee_name
        self.hour = hour
        self.client_firstname = client_firstname
        self.client_lastname = client_lastname
        self.sub_service = sub_service


with app.app_context():
    db.create_all()

@app.route('/') # create the home page (am creat pagina principala)
def index():
    return render_template('t1_index.html')

@app.route('/about') # o pagina secundare
def about():
    #return 'This is an about page!!!' # - test
    return render_template('t2_about.html')

# =======================================CLIENTS===============================================================

@app.route('/clients')
def clients():
    all_data = Clients.query.all()
    return render_template('t3_clients.html', clients = all_data)

@app.route('/insertc', methods = ['POST'])
def insertc():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']

        my_data = Clients(first_name, last_name,age, gender, phone, email)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('clients'))

@app.route('/updatec', methods = ['GET', 'POST'])
def updatec():
    if request.method == 'POST':
        mydata = Clients.query.get(request.form.get('id'))
        mydata.first_name = request.form['firstname']
        mydata.last_name = request.form['lastname']
        mydata.age = request.form['age']
        mydata.gender = request.form['gender']
        mydata.phone = request.form['phone']
        mydata.email = request.form['email']

        db.session.commit()

        return redirect(url_for('clients'))

@app.route('/deletec/<int:id>/', methods = ['GET', 'POST'])
def deletec(id):
    my_data = Clients.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('clients'))

# =======================================EMPLOYEES===============================================================

@app.route('/employees')
def employees():
    all_data = Employee.query.all()
    return render_template('t4_employees.html', employees = all_data)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']

        my_data = Employee(first_name, last_name, phone, email)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('employees'))

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        mydata = Employee.query.get(request.form.get('id'))
        mydata.first_name = request.form['firstname']
        mydata.last_name = request.form['lastname']
        mydata.phone = request.form['phone']
        mydata.email = request.form['email']

        db.session.commit()

        return redirect(url_for('employees'))

@app.route('/delete/<int:id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Employee.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('employees'))

# =====================================SERVICES=================================================================

@app.route('/services')
def services():
    all_data = Services.query.all()
    return render_template('t5_services.html', services = all_data)


@app.route('/inserte', methods = ['POST'])
def inserte():
    if request.method == 'POST':
        sub_service = request.form['subservice']
        service = request.form['service']
        price = request.form['price']

        my_data = Services(sub_service, service, price)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('services'))

@app.route('/updatee', methods = ['GET', 'POST'])
def updatee():
    if request.method == 'POST':
        mydata = Services.query.get(request.form.get('id'))
        mydata.sub_service = request.form['subservice']
        mydata.service = request.form['service']
        mydata.price = request.form['price']

        db.session.commit()

        return redirect(url_for('services'))

@app.route('/deletee/<int:id>/', methods = ['GET', 'POST'])
def deletee(id):
    my_data = Services.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('services'))

# ======================================================================================================

@app.route('/appointments')
def appointments():
    all_data = Appointments.query.all()
    return render_template('t6_appointments.html', appointments = all_data)


@app.route('/inserta', methods = ['POST'])
def inserta():
    if request.method == 'POST':
        employee_name = request.form['employeename']
        hour = request.form['hour']
        client_firstname = request.form['clientfirstname']
        client_lastname = request.form['clientlastname']
        sub_service = request.form['subservice']

        my_data = Appointments(employee_name, hour, client_firstname, client_lastname , sub_service)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('appointments'))

@app.route('/updatea', methods = ['GET', 'POST'])
def updatea():
    if request.method == 'POST':
        mydata = Appointments.query.get(request.form.get('id'))
        mydata.employee_name = request.form['employeename']
        mydata.hour = request.form['hour']
        mydata.client_firstname = request.form['clientfirstname']
        mydata.client_lastname = request.form['clientlastname']
        mydata.sub_service = request.form['subservice']

        db.session.commit()

        return redirect(url_for('appointments'))

# ======================================================================================================

if __name__ == '__main__':
    app.run()