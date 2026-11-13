CREATE TABLE raw_credit_clients (
    client_id INT PRIMARY KEY,
    limit_bal NUMERIC(12, 2),
    sex INT,
    education INT,
    marriage INT,
    age INT,
    pay_0 INT, pay_2 INT, pay_3 INT, pay_4 INT, pay_5 INT, pay_6 INT,
    bill_amt1 NUMERIC(12, 2), bill_amt2 NUMERIC(12, 2), bill_amt3 NUMERIC(12, 2),
    bill_amt4 NUMERIC(12, 2), bill_amt5 NUMERIC(12, 2), bill_amt6 NUMERIC(12, 2),
    pay_amt1 NUMERIC(12, 2), pay_amt2 NUMERIC(12, 2), pay_amt3 NUMERIC(12, 2),
    pay_amt4 NUMERIC(12, 2), pay_amt5 NUMERIC(12, 2), pay_amt6 NUMERIC(12, 2),
    default_next_month INT
);