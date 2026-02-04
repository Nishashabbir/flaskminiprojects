from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model): #here class and its objects will become the table and rows in database that we don't need to write in sql sqlalchemy will convert our code to it 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# Home page you ccan see all the contacts here 
@app.route('/')
def index():
    contacts = Contact.query.all() #selects all the records and puts in contacts object then render to index page with the contacts object with all the columns 
    return render_template('index.html', contacts=contacts)

# Add contact form submission
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    new_contact = Contact(name=name, phone=phone, email=email) #here we created the object/a full record  of the class Contact and passed the 3 columns in it 
    db.session.add(new_contact) #here we added the object to the database 
    db.session.commit() #officially added to database
    return redirect(url_for('index'))

# Delete contact
@app.route('/delete/<int:id>')
def delete(id):
    contact = Contact.query.get(id) #this is same to saying : SELECT * FROM contact WHERE id = 5; so it gives the full record of that id 
    db.session.delete(contact) #this object is deleted with full record 
    db.session.commit()
    return redirect(url_for('index'))

# Update contact form
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    contact = Contact.query.get(id) #here we took the record and stored it in object then we manually update the columns in it 
    contact.name = request.form.get('name')
    contact.phone = request.form.get('phone')
    contact.email = request.form('email')
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

# submit is  a must due to which the form data is sent to the server or browser from the inputs
# action decides or tells the browser where the data goes next , it chooses the url to which the data is rendered
# method just decides that how the data is sent GET or POST ?  GET simply read and view , while POST for the request 
