# what is the meaning of jason here : # Route /list: JSON list of all tasks.
# and when do we use repr__function 
# why didn't we include id and is_completed variables while passing them at the time of object creation 
# why did you import os 
# sometimes you write request.args.get and sometimes request.form.get what is the difference
# sometimes you write app.app_context() and create_all() inside a with block and sometimes you don't why , when actually will we use it 
# I don't know what's the reason of writing this :  def to_dict(self):
#         """Helper to convert the model to a dictionary for JSON response"""
#         return {
#             "id": self.id,
#             "content": self.content,
#             "is_completed": self.is_completed
#         }


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the app and database configuration
app = Flask(__name__)
# This creates a file named 'tasks.db' in your project folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db = SQLAlchemy(app)

# --- MODEL DEFINITION ---
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
# before creating the model we will just convert the complex object into a dictionary 
    def to_dict(self):
        """Helper to convert the model to a dictionary for JSON response"""
        # in simple words this function is written just inside the class to give the object an ability which is used to convert the Task object into a dictionary format 
        return {
            "id": self.id,
            "content": self.content,
            "is_completed": self.is_completed
        }
    
# here is the difference of the scope of writing this function inside the class and outside: 
# If you put it OUTSIDE: You would have to write a separate function and pass the task to it: convert_to_dict(my_task).

# By putting it INSIDE: The task knows how to convert itself: my_task.to_dict(). It makes the code much cleaner later on.

# --- DATABASE SETUP ---
# We use the app context to ensure the DB is created before the app starts
# basically this block of code is used to create the schema of the database on the hard drive, the model is actually created now 
with app.app_context():
    db.create_all()
    print("Database initialized and 'tasks.db' created!")

# --- ROUTES ---

# Route 1: Add a new task
# Usage: POST /add?content=Buy Milk
@app.route('/add', methods=['POST'])
def add_task():
    # Get content from query parameters  or JSON body
    content = request.args.get('content') 
    
    if not content:
        return jsonify({"error": "Content is required"}), 400

    new_task = Task(content=content) #We converted the input data to an object of Task class to store in databse as record 
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"message": "Task created", "task": new_task.to_dict()}), 201

# Route 2: List all tasks
# Usage: GET /list
@app.route('/list', methods=['GET'])
def list_tasks():
    tasks = Task.query.all()
    # Convert list of objects to list of dictionaries
    return jsonify([task.to_dict() for task in tasks]) #You are performing a "double conversion":
# Object -> Dictionary (So Python knows how to read the data).
# Dictionary -> JSON String (So the Internet knows how to transport the data).

# Route 3: Complete a task
# Usage: PATCH /complete/<id>
@app.route('/complete/<int:id>', methods=['PATCH'])
def complete_task(id):
    task = Task.query.get(id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
        
    task.is_completed = True
    db.session.commit()
    return jsonify({"message": f"Task {id} marked as complete", "task": task.to_dict()})

# Route 4: Delete a task
# Usage: DELETE /delete/<id>
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
        
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": f"Task {id} deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)

# How to run this program  to check the outputs : 
#You cannot add a task using the browser's address bar. You must use the terminal (or a special tool like Postman) to send the POST signal.

# Step 1: Run the Server (Window A)
# Open your terminal.
# Activate your virtual environment (venv\Scripts\activate or source venv/bin/activate).
# Run the app:

# LEAVE THIS WINDOW ALONE. Do not close it. It should say "Running on http://127.0.0.1:5000".
# Step 2: Send Commands (Window B)
# Open a New, Second Terminal Window.
# Add a Task (The POST Request): Copy and paste this command exactly:

# curl -X POST http://127.0.0.1:5000/add?content=Buy_Milk

# If you are on Windows PowerShell and that fails, try this format: curl -X POST "http://127.0.0.1:5000/add?content=Buy_Milk"
# Output: You should see a JSON string like {"message": "Task created", ...}.
# Check the List (The GET Request): Now you can use curl OR your Browser.

# curl http://127.0.0.1:5000/list

# Output: You will see [{"id": 1, "content": "Buy_Milk", ...}].
# Complete the Task (The PATCH Request):

# curl -X PATCH http://127.0.0.1:5000/complete/1

# Delete the Task (The DELETE Request):

# curl -X DELETE http://127.0.0.1:5000/delete/1
