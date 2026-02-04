
#1 import the libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


#2 initialize the Flask application
app = Flask(__name__)

#3 Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#4 create a user model
class User(db.Model): #Model definition (User)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"
    #5 initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to the usr management app! Go to /add_user to add a user or /users to see all users."

#6 add users manualy by via url ******
@app.route('/add_user')
def add_user():
    name = request.args.get('name')
    email = request.args.get('email')
    if not name or not email:
        return "Provide name and email in URL like ?name=John&email=john@example.com"

    new_user = User(name=name, email=email)

# these two lines are important to add data to database like sql writes the data into userdb file 
    db.session.add(new_user) #stage it to be added to database
    db.session.commit() #actually save it to database
    return f"User {name} added successfully!"
#7 display all users*******
@app.route('/users')
def get_users():
    users = User.query.all()
    users_list = [{"id": u.id, "name": u.name, "email": u.email} for u in users]
    return jsonify(users_list)
# User.query.all() → SQLAlchemy fetches all rows from the User table.
# We convert it into a list of dictionaries to make it readable.
# jsonify(users_list) → turns it into JSON (browser-friendly).
# Open in browser: http://127.0.0.1:5000/users

#8 run the app 
if __name__ == "__main__":
    app.run(debug=True)
