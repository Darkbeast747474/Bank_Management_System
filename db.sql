CREATE DATABASE BankingSystem;
USE BankingSystem;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
);

CREATE TABLE Customer (
    Cust_ID CHAR(5) PRIMARY KEY,
    Cust_Name VARCHAR(100) NOT NULL,
    Cust_Address VARCHAR(150)
);

CREATE TABLE Branch (
    Branch_ID CHAR(5) PRIMARY KEY,
    Branch_Name VARCHAR(100) NOT NULL
);

CREATE TABLE Account (
    Account_No CHAR(10) PRIMARY KEY,
    Cust_ID CHAR(5),
    Branch_ID CHAR(5),
    Account_Type VARCHAR(20),
    Balance DECIMAL(12,2),

    FOREIGN KEY (Cust_ID) REFERENCES Customer(Cust_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (Branch_ID) REFERENCES Branch(Branch_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Loan (
    Loan_ID CHAR(5) PRIMARY KEY,
    Cust_ID CHAR(5),
    Loan_Amount DECIMAL(12,2),

    FOREIGN KEY (Cust_ID) REFERENCES Customer(Cust_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Transaction (
    Transaction_ID CHAR(6) PRIMARY KEY,
    Account_No CHAR(10),
    Transaction_Date DATE,
    Transaction_Type VARCHAR(20),
    Transaction_Amount DECIMAL(10,2),

    FOREIGN KEY (Account_No) REFERENCES Account(Account_No)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- User Data
INSERT INTO users (username, password) VALUES
('admin', 'admin123'),

-- Customer Data
INSERT INTO Customer VALUES
('C001', 'Rahul Sharma', 'Delhi'),
('C002', 'Neha Verma', 'Mumbai'),
('C003', 'Amit Singh', 'Chandigarh');

-- Branch Data
INSERT INTO Branch VALUES
('B01', 'Connaught'),
('B02', 'Andheri'),
('B03', 'Sector 17');

-- Account Data
INSERT INTO Account VALUES
('A101', 'C001', 'B01', 'Savings', 25000.00),
('A102', 'C002', 'B02', 'Current', 40000.00),
('A103', 'C003', 'B03', 'Savings', 30000.00);

-- Loan Data
INSERT INTO Loan VALUES
('L01', 'C001', 100000.00),
('L02', 'C002', 150000.00);

-- Transaction Data
INSERT INTO Transaction VALUES
('T9001', 'A101', '2025-11-01', 'Deposit', 5000.00),
('T9002', 'A101', '2025-11-03', 'Withdraw', 2000.00),
('T9003', 'A102', '2025-11-02', 'Deposit', 10000.00),
('T9004', 'A103', '2025-11-04', 'Deposit', 8000.00);
