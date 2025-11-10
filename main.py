from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = "your secret key"

db = mysql.connector.connect(
    host="localhost", user="rex", password="2225", database="BankingSystem"
)

if not db.is_connected():
    print("Database connection failed")
    exit(1)
else:
    print("Database connected successfully")


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password),
        )
        account = cursor.fetchone()
        if account:
            session["loggedin"] = True
            session["username"] = account["username"]
            return redirect(url_for("home"))
        else:
            msg = "Incorrect username or password!"
        cursor.close()
    return render_template("login.html", msg=msg)


@app.route("/home")
def home():
    if "loggedin" in session:
        return render_template("home.html", username=session["username"])
    return redirect(url_for("/login"))


@app.route("/api/dashboard-data")
def get_dashboard_data():
    cursor = db.cursor(dictionary=True)

    # ✅ Fetch Transaction
    cursor.execute(
        """
        SELECT t.transaction_id AS id,
               t.transaction_date AS date,
               t.transaction_type AS type,
               t.Account_No AS account,
               t.transaction_Amount AS amount
        FROM Transaction t
        ORDER BY t.transaction_date DESC
        LIMIT 10
    """
    )
    transactions = cursor.fetchall()

    # ✅ Fetch Total Deposits
    cursor.execute(
        """
        SELECT IFNULL(SUM(transaction_Amount),0) AS total_deposits
        FROM Transaction
        WHERE LOWER(transaction_type) = 'deposit'
    """
    )
    total_deposits = cursor.fetchone()["total_deposits"]

    # ✅ Fetch Total Loans
    cursor.execute(
        """
        SELECT IFNULL(SUM(Loan_Amount),0) AS total_loans
        FROM Loan
    """
    )
    total_loans = cursor.fetchone()["total_loans"]

    cursor.execute(
        """
        SELECT 
            B.Branch_ID,
            B.Branch_Name, 
            SUM(A.Balance) AS Total_Balance
        FROM Branch B
        JOIN Account A ON B.Branch_ID = A.Branch_ID
        GROUP BY B.Branch_ID,B.Branch_Name;
    """
    )
    branch_balances = cursor.fetchall()

    # ✅ Calculate Deficit
    deficit = max(0, total_loans - total_deposits)

    cursor.close()

    return jsonify(
        {
            "total_deposits": total_deposits,
            "total_loans": total_loans,
            "deficit": deficit,
            "transactions": transactions,
            "branch_balances": branch_balances,
        }
    )


@app.route("/dashboard")
def dashboard():
    if "loggedin" in session:
        get_dashboard_data()
        return render_template("dashboard.html", username=session["username"])
    return redirect(url_for("/login"))


@app.route("/show_accounts")
def show_accounts():
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT 
            A.Account_No, 
            C.Cust_Name, 
            C.Cust_Address, 
            B.Branch_Name, 
            A.Account_Type, 
            A.Balance
        FROM Account A
        JOIN Customer C ON A.Cust_ID = C.Cust_ID
        JOIN Branch B ON A.Branch_ID = B.Branch_ID;
    """
    )
    accounts = cursor.fetchall()
    cursor.close()
    return render_template("show_accounts.html", accounts=accounts)


@app.route("/loans")
def show_loans():
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT 
            L.Loan_ID, 
            C.Cust_Name, 
            L.Loan_Amount
        FROM Loan L
        JOIN Customer C ON L.Cust_ID = C.Cust_ID;
    """
    cursor.execute(query)
    loans = cursor.fetchall()
    cursor.close()
    return render_template("show_loans.html", loans=loans)


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
