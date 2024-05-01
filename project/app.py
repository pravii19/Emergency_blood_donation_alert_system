from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from werkzeug.exceptions import BadRequestKeyError
from chat import get_response
from twilio.rest import Client  


app = Flask(__name__, template_folder='templates')

# Database connection for user registration
conn_user_registration = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="logindb"
)

# Database connection for blood donation
conn_blood_donation = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="blood_donation",

)

account_sid = ''
auth_token = ''

# Initialize Twilio Client
client = Client(account_sid, auth_token)

# Route for the home page
@app.route('/')
def index():
    return render_template('index1.html')

# Route for user signup
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user_type = request.form['user_type']

    cursor = conn_user_registration.cursor()
    cursor.execute("INSERT INTO users (username, email, password, user_type) VALUES (%s, %s, %s, %s)",
                   (username, email, password, user_type))
    conn_user_registration.commit()
    cursor.close()  # Close the cursor after executing the query

    return redirect(url_for('index'))  # Redirect to the index page

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']

        cursor = conn_user_registration.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            if user['password'] == password:
                if user['user_type'] == 'admin':
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('user'))
            else:
                return "Incorrect password"
        else:
            return "User not found"
    except BadRequestKeyError as e:
        return f"Bad request: {e}"

# Route for admin dashboard
@app.route('/admin')
def admin():
    return render_template('base.html')

# Route for user dashboard
@app.route('/user')
def user():
    return render_template('register.html')

# Route for user registration form


# Route for user registration
@app.route("/register", methods=["POST"])
def register():
    # Get form data
    name = request.form.get("name")
    email = request.form.get("email")
    phone_no = request.form.get("phone_no")
    gender = request.form.get("gender")
    age = request.form.get("age")
    blood_group = request.form.get("blood_group")
    location = request.form.get("location")
    address = request.form.get("address")

    # Check if the phone number or email already exists in the database
    cursor = conn_blood_donation.cursor(dictionary=True)
    check_query = "SELECT * FROM registration WHERE phone_no = %s OR email = %s"
    check_values = (phone_no, email)
    cursor.execute(check_query, check_values)
    existing_record = cursor.fetchall()

    if existing_record:
        return redirect(url_for('exists'))
    else:
        # Insert data into MySQL database
        sql = "INSERT INTO registration (name, email, phone_no, gender, age, blood_group, location, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, email, phone_no, gender, age, blood_group, location, address)
        cursor = conn_blood_donation.cursor()
        cursor.execute(sql, values)
        conn_blood_donation.commit()
        cursor.close()
        # Return success message
        return redirect(url_for('thank'))

# Route for existing user page
@app.route("/exists")
def exists():
    return render_template("exists.html")  

# Route for thank you page
@app.route("/thank")
def thank():
    return render_template("thank.html")

# Route for index1 page
@app.route('/index1')
def index1():
    return render_template('index1.html')

# Route for contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for about page
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/donor')
def donor():
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="blood_donation"
    )

    # Create a cursor object to execute queries
    cursor = conn.cursor(dictionary=True)

    # Query the database for all registered users
    query = "SELECT * FROM registration"
    cursor.execute(query)
    registered_users = cursor.fetchall()

    # Close cursor and database connection
    cursor.close()
    conn.close()

    # Pass the list of registered users to the base.html template
    return render_template('donor.html', users=registered_users)



@app.route("/predict", methods=["POST"])
def predict():
    text = request.json.get("message")
    if text is None:
        return jsonify({"error": "No message provided"}), 400

    response = get_response(text)
    message = {"answer": response}
    
    return jsonify(message)


def get_blood_group(blood_group):
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="blood_donation"
    )

    # Create a cursor object to execute queries
    cursor = conn.cursor(dictionary=True)

    # Query the database for the specified blood group
    query = "SELECT * FROM registration WHERE blood_group = %s"
    cursor.execute(query, (blood_group,))
    result = cursor.fetchall()

    # Close cursor and database connection
    cursor.close()
    conn.close()

    # Check if there are any results
    if result:
        # If there are results, return them as JSON
        return jsonify(result)
    else:
        # If no results found, return a message
        return jsonify({"message": "No records found for the specified blood group."}), 404
    
@app.route("/display_blood_group", methods=["POST"])
def display_blood_group():
    # Get the blood group from the request data
    data = request.get_json()
    blood_group = data.get("blood_group")

    # Call the get_blood_group function to retrieve data from the database
    result = get_blood_group(blood_group)
    
    return result



    
if __name__ == "__main__":
    app.run(debug=True)
