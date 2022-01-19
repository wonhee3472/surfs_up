# Import the Flask Dependency
from flask import Flask

# Create a New Flask App Instance
# "Instance" is a general term in programming to refer to a singular version of something
# The __name__ variable denotes the name of the function
# Variables with underscores before and after them are called magic methods in Python
app = Flask(__name__)

# Create Flask Routes
# Define the stating point or root
# The foward slash denotates that we want to put our data at the root of our routes
@app.route('/')
def hello_world():
    return 'Hello world'