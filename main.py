import re
from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_mysqldb import MySQL , MySQLdb

app = Flask(__name__)

app.secret_key = "abdhghsbghddvbnbdsehjdghbsx"
 
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'webixer'
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password2 = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql1 = "SELECT * FROM signup WHERE email='"+email+"'"
        cursor.execute(sql1)
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if not account:
            flash("That email does not exist, please try again.") 
            return redirect(url_for('login'))
        elif not(account["password"] == password2):
            flash("Password is incorrect!")
            return redirect(url_for('login'))
        else:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['password'] = account['password']
            session['email'] = account['email']
            # Redirect to home page
            return redirect(url_for('dash1'))
        cursor.close()
    return render_template('login.html')


@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username = request.form["username"]
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM signup WHERE email='"+email+"'"
        if cursor.execute(sql):
            flash("You have already signed up with that email! LogIn instead")
            return redirect(url_for('login'))
        else:
            #executing sql statement
            cursor.execute("INSERT INTO signup(username,email,password) VALUES(%s,%s,%s) " , (username,email, password))
            #Saving the Actions performed on the DB
            mysql.connection.commit()
            #using session
            session['loggedin'] = True
            return redirect(url_for('dash1'))
    return render_template("signup.html")

@app.route("/gym-template")
def gym():
    return render_template("gym.html")

@app.route("/non-profit-1")
def np1():
    return render_template("non-profit1.html")

@app.route("/non-profit-2")
def np2():
    return render_template("non-profit2.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/dashboard1")
def dash1():
    return render_template("dashboard1.html")

@app.route("/gym-template-dashboard")
def gymdash():
    return render_template("gym-temp-dash.html")

@app.route("/gym-form")
def gymform():
    return render_template("gym-form.html")

@app.route("/nonprofit-form")
def nonprofit():
    return render_template("nonprofit-form.html")

@app.route("/portfolio-form")
def portfolioform():
    return render_template("portfolio-form.html")

@app.route("/np-dash")
def npdash():
    return render_template("np-dash.html")

@app.route("/portfolio-dash")
def portdash():
    return render_template("portfoliodash.html")

if __name__ == "__main__":
    app.run(debug=True)