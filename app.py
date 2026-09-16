from flask import Flask,render_template,request ,session , redirect, url_for
import mysql.connector

app=Flask(__name__)
app.secret_key="bank-management-system-key"
con=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abhishek@2611",
    database="bank_db"
    )
cursor=con.cursor()
@app.route("/")
def home():
    return render_template("login.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
     username=request.form["username"]
     password=request.form["password"]
     test_cursor=con.cursor(buffered=True)
     test_cursor.execute("SELECT id,username,password FROM admin WHERE" \
                  "  username=%s AND password=%s",
                         (username,password))
     admin=test_cursor.fetchone()
     test_cursor.close()
     if admin:
          session["admin_logged_in"]=True
          session["admin_username"]=admin[1]
          return redirect(url_for("dashboard"))
# <----------- Customres login page ------------------->
     test_cursor=con.cursor(buffered=True)
     test_cursor.execute(""" 
                          SELECT account_no,username,password
            FROM customers WHERE username=%s AND password=%s  
                         """, (username,password)
                         )
     customer=test_cursor.fetchone()
     test_cursor.close()
     if customer:
         session["customer_logged_in"]=True
         session["customer_account_no"]=customer[0]
         session["customer_username"]=customer[1]
         return redirect(url_for("customer_dashboard"))
     # --------------Invalid login ------------->
         return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

@app.route("/add_customer", methods=["GET","POST"])
def add_customer():
    if not session.get("admin_logged_in"):
           return redirect(url_for("login"))
    if request.method=="POST":
        account_no=request.form["account_no"]
        name=request.form["name"]
        phone=request.form["phone"]
        address=request.form["address"]
        username=request.form["username"]
        balance=request.form["balance"]
        cursor.execute(""" INSERT INTO accounts(account_no,name,phone,address,balance,username)
        VALUES (%s,%s,%s,%s,%s,%s) """,
        (account_no,name,phone,address,balance))
        con.commit()
        return render_template("success.html")
    return render_template("add_customer.html") 

@app.route("/view_customer",methods=["GET","POST"])
def view_customer():
    if not session.get("admin_logged_in"):
       return redirect(url_for("login"))
    cursor.execute("SELECT * FROM accounts")
    customers=cursor.fetchall()
    return render_template("view_customer.html", customers=customers)

@app.route("/dashboard")
def dashboard():

    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    cursor.execute(" SELECT COUNT(*) FROM accounts")
    accounts_count=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM customers")
    customers_count = cursor.fetchone()[0]
    total_customers=accounts_count+customers_count

    cursor.execute("SELECT COALESCE(SUM(balance), 0) FROM customers")
    total_balance = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = cursor.fetchone()[0]

    return render_template(
        "dashboard.html",
        total_customers=total_customers,
        total_balance=total_balance,
        total_transactions=total_transactions
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/deposit_success")
def deposit_success():
    return render_template("/deposit_success.html")

# <------------Deposit money------------>
@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            account_no = request.form["account_no"]
            amount = request.form["amount"]

            if not account_no or not amount:
                return render_template(
                    "deposit.html",
                    error="Please enter account number and amount"
                )

            amount = int(amount)

            if amount <= 0:
                return render_template(
                    "deposit.html",
                    error="Amount must be greater than 0"
                )

            cursor.execute(
                "UPDATE accounts SET balance = balance + %s WHERE account_no = %s",
                (amount, account_no)
            )
            if cursor.rowcount==0:
                return render_template("deposit.html",error="Account number not found")
            mysql.connection.commit()
            cursor.close()
            return render_template("deposit.html",success="Amount is successfully deposit into your account.")

            con.commit()

            return render_template (
                "deposit.html",
                success="Money deposited successfully")

        except ValueError:
            return render_template(
                "deposit.html",
                error="Please enter a valid amount"
            )

        except mysql.connector.Error as e:
            con.rollback()
            return render_template(
                "deposit.html",
                error="Database error occurred"
            )

        except Exception as e:
            con.rollback()
            return render_template(
                "deposit.html",
                error="Something went wrong"
            )
    return render_template("deposit.html")
# <------------Sign up ------------->
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        
        full_name = request.form["full_name"]
        username = request.form["username"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        address = request.form["address"]

        # Check password
        if password != confirm_password:
            return render_template(
                "signup.html",
                error="Passwords do not match"
            )

        # Check username already exists
        test_cursor = con.cursor(buffered=True)

        test_cursor.execute(
            "SELECT username FROM customers WHERE username=%s",
            (username,)
        )
        existing_admin = test_cursor.fetchone()
        test_cursor.close()

        if existing_admin:
            return render_template(
                "signup.html",
                error="Username already exists"
            )
      #  print("successfully")
        insert_cursor = con.cursor()
        # Insert admin data
        insert_cursor.execute(
            """
            INSERT INTO customers
            (full_name, username, email, mobile, password, address)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                full_name,
                username,
                email,
                mobile,
                password,
                address
            )
        )
       # print("insert execute")
        con.commit()
       # print("DATA INSERTED successfully")
        insert_cursor.close()
        #print("DATA INSERTED successfully",username)


        return render_template("signup_success.html")

    return render_template("signup.html")
#<---------------Customer Dashboard--------------->
@app.route("/customer_dashboard")
def customer_dashboard():

    if not session.get("customer_logged_in"):
        return redirect(url_for("login"))

    account_no = session.get("customer_account_no")

    cursor.execute(
        """
        SELECT account_no, full_name, email, mobile, address, balance
        FROM customers
        WHERE account_no=%s
        """,
        (account_no,)
    )

    customer_data = cursor.fetchone()

    if not customer_data:
        return "Customer not found"

    customer = {
        "account_no": customer_data[0],
        "full_name": customer_data[1],
        "email": customer_data[2],
        "mobile": customer_data[3],
        "address": customer_data[4],
        "balance": customer_data[5]
    }

    return render_template(
        "customer_dashboard.html",
        customer=customer
    )
#   <----------Withdraw money---------->
@app.route("/withdraw", methods=["GET","POST"])
def withdraw():

    if request.method=="POST":

        account_no=request.form.get("account_no")
        amount=request.form.get("amount")

        if not account_no or not amount:
            return "please enter account number and amount"

        amount=int(amount)

        cursor=con.cursor()

        cursor.execute("SELECT balance FROM accounts WHERE account_no =%s",
                       (account_no,))

        customer=cursor.fetchone()
        if customer is None:
            cursor.close()
            return "Account not found"
        balance=customer[0]

        if amount<=0:
            cursor.close()
            return "Invalid amount"
        if amount>balance:
            cursor.close()
            return "Insufficient balance"
        new_balance = balance-amount

        cursor.execute("UPDATE accounts SET balance=%s WHERE account_no=%s",
                       (new_balance,account_no))

        con.commit()
        cursor.close()

        return render_template("withdraw_success.html")

    return render_template("withdraw.html")


@app.route("/delete_customer",methods=["GET","POST"])
def delete_customer():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    if request.method=="POST":
        account_no=request.form["account_no"]
        cursor.execute (f"DELETE  FROM accounts WHERE account_no={account_no}")
        con.commit()
        return render_template("delete_success.html")    
    return render_template("delete_customer.html")
@app.route("/transfer", methods=["GET", "POST"])
def transfer():

    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("transfer.html")

    sender_account = request.form["sender_account"]
    receiver_account = request.form["receiver_account"]
    amount = request.form["amount"]

    # Convert amount to integer
    try:
        amount = int(amount)
    except ValueError:
        return "Invalid amount"

    # Basic validation
    if amount <= 0:
        return "Amount must be greater than 0"

    if sender_account == receiver_account:
        return "Sender and receiver account cannot be same"

    try:

        # Start database transaction
        con.start_transaction()

        # Check sender account and lock row
        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_no = %s
            FOR UPDATE
            """,
            (sender_account,)
        )

        sender = cursor.fetchone()

        if not sender:
            con.rollback()
            return "Sender account not found"

        sender_balance = sender[0]

        # Check receiver account
        cursor.execute(
            """
            SELECT account_no
            FROM accounts
            WHERE account_no = %s
            FOR UPDATE
            """,
            (receiver_account,)
        )

        receiver = cursor.fetchone()

        if not receiver:
            con.rollback()
            return "Receiver account not found"

        # Check sufficient balance
        if sender_balance < amount:
            con.rollback()
            return "Insufficient balance"

        # Deduct money from sender
        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance - %s
            WHERE account_no = %s
            """,
            (amount, sender_account)
        )

        # Add money to receiver
        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance + %s
            WHERE account_no = %s
            """,
            (amount, receiver_account)
        )

        # Sender transaction
        cursor.execute(
            """
            INSERT INTO transactions
            (account_no, transaction_type, amount)
            VALUES (%s, %s, %s)
            """,
            (sender_account, "TRANSFER OUT", amount)
        )

        # Receiver transaction
        cursor.execute(
            """
            INSERT INTO transactions
            (account_no, transaction_type, amount)
            VALUES (%s, %s, %s)
            """,
            (receiver_account, "TRANSFER IN", amount)
        )

        # Save all changes
        con.commit()

        return redirect(url_for("dashboard"))

    except Exception as e:

        con.rollback()

        return f"Transfer failed: {e}"
if __name__ == "__main__":
    app.run(debug=True)
