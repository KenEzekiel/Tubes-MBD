# Read Committed
1. Setting Up PostgreSQL with Docker
```shell
docker run --name postgres-demo -e POSTGRES_PASSWORD=mypassword -d -p 5432:5432 postgres
```

2. Connect to DB
```shell
docker exec -it postgres-demo psql -U postgres
```

3. Create a Sample Table and Insert Data
```shell
CREATE TABLE account_balances (
    id SERIAL PRIMARY KEY,
    balance DECIMAL NOT NULL
);

INSERT INTO account_balances (balance) VALUES (1000), (2000);
```

4. Demo Repeatable Read
```shell
-- Session 1
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT * FROM account_balances WHERE id = 1;
```
```shell
-- Session 2
BEGIN;
UPDATE account_balances SET balance = balance + 100 WHERE id = 1;
COMMIT;
```
```shell
-- Session 1
SELECT * FROM account_balances WHERE id = 1;
COMMIT;
```

5. Logs
```shell
docker logs postgres-demo
```