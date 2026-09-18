# 🏦 NOVA BANK — Bank Management System

**A Web-Based Banking Management Application using Flask, Python & MySQL**

---

## 📌 Project Overview

NOVA BANK is a web-based **Bank Management System** developed as a BCA academic project. It provides a secure and user-friendly interface for managing customer accounts, deposits, withdrawals, fund transfers, transaction history, and role-based login for Admin and Customer.

---

## 🚀 Features

* Admin Login Authentication
* Customer Signup & Login
* Add Customer Account
* View Customer Details
* Deposit Money
* Withdraw Money
* Transfer Money
* Transaction History
* Dashboard Statistics
* Session-based Logout
* Input Validation

---

## 🛠 Technology Stack

| Layer           | Technology               |
| --------------- | ------------------------ |
| Frontend        | HTML5, CSS3, Bootstrap 5 |
| Backend         | Python, Flask            |
| Database        | MySQL                    |
| Template Engine | Jinja2                   |
| IDE             | VS Code / PyCharm        |

---

## 📁 Project Structure

```text
NOVA_BANK/
│
├── app.py
├── templates/
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── customer_dashboard.html
│   ├── add_customer.html
│   ├── view_customer.html
│   ├── deposit.html
│   ├── withdraw.html
│   ├── transfer.html
│   ├── transaction_history.html
│   ├── success.html
│   └── transfer_success.html
│
├── static/
│   ├── css/
│   └── images/
│
└── database/
    └── bank_db.sql
```

---

## 🗄 Database Tables

### 1. admin

Stores administrator login credentials.

| Column   | Type    |
| -------- | ------- |
| id       | INT     |
| username | VARCHAR |
| password | VARCHAR |

### 2. customers

Stores customer registration information.

| Column   | Type    |
| -------- | ------- |
| id       | INT     |
| username | VARCHAR |
| password | VARCHAR |

### 3. accounts

Stores actual bank account details.

| Column     | Type    |
| ---------- | ------- |
| account_no | BIGINT  |
| name       | VARCHAR |
| phone      | VARCHAR |
| address    | VARCHAR |
| balance    | INT     |
| username   | VARCHAR |

### 4. transactions

Stores deposit, withdrawal and transfer records.

| Column           | Type     |
| ---------------- | -------- |
| id               | INT      |
| account_no       | BIGINT   |
| transaction_type | VARCHAR  |
| amount           | INT      |
| transaction_date | DATETIME |

---

## 🔐 Authentication Flow

```text
Admin Login
      │
      ▼
Username & Password Verification
      │
      ▼
Session Created
      │
      ▼
Admin Dashboard
```

Flask Session Example:

```python
session["admin_logged_in"] = True
```

Protected Modules:

* Dashboard
* Add Customer
* Deposit
* Withdraw
* Transfer
* Delete Customer

---

## 💳 Modules

### Admin Module

* Login
* Dashboard
* Add Customer
* View Customer
* Delete Customer
* Deposit
* Withdraw
* Transfer Money
* View Transactions
* Logout

### Customer Module

* Signup
* Login
* View Profile
* View Balance
* Transaction History
* Logout

---

## 📊 Dashboard

The Admin Dashboard displays:

* Total Customers
* Total Balance
* Total Transactions
* Banking Operations

---

## ✅ Validation Used

| Module       | Validation                       |
| ------------ | -------------------------------- |
| Login        | Username & Password Required     |
| Signup       | Username Unique                  |
| Add Customer | Account Unique, Phone Validation |
| Deposit      | Amount > 0                       |
| Withdraw     | Sufficient Balance               |
| Transfer     | Sender ≠ Receiver                |
| Transfer     | Receiver Exists                  |
| Transfer     | Amount Greater Than 0            |

Example:

```python
if sender_balance < amount:
    return "Insufficient Balance"
```

---

## 🔄 Transfer Money Workflow

```text
Sender Account
      │
      ▼
Check Balance
      │
      ▼
Deduct Amount
      │
      ▼
Receiver Account
      │
      ▼
Add Amount
      │
      ▼
Save Transaction
      │
      ▼
Transfer Successful
```

Two transaction records are created:

* TRANSFER OUT
* TRANSFER IN

---

## ⚙ Installation

### Step 1

```bash
git clone https://github.com/yourusername/nova-bank.git
```

### Step 2

```bash
pip install flask mysql-connector-python
```

### Step 3

Create Database:

```sql
CREATE DATABASE bank_db;
```

Import **bank_db.sql**

### Step 4

Run Project:

```bash
python app.py
```

Open Browser:

```text
http://127.0.0.1:5000
```

---

## 🎯 Future Scope

* REST API Integration
* Password Hashing
* OTP Verification
* PDF Statement
* Email Notification
* Charts & Analytics
* Cloud Deployment

---

## 👨‍💻 Developer

**Abhishek Pal**

Bachelor of Computer Applications (BCA)

Kashi Institute of Technology, Varanasi

Academic Session: **2026–27**

---

## 📄 License

This project is developed for **academic and educational purposes only**.
