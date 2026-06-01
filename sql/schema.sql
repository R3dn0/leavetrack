DROP TABLE IF EXISTS department, employee, absence_type, absence, leave_balance CASCADE;

CREATE TABLE department (
    id                      SERIAL PRIMARY KEY,
    name                    VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE employee (
    id                      SERIAL PRIMARY KEY,
    first_name              varchar(100) NOT NULL,
    last_name               varchar(100) NOT NULL,
    email                   varchar(100) NOT NULL UNIQUE,
    department_id           int REFERENCES department(id) ON DELETE SET NULL,
    manager_id              int REFERENCES employee(id) ON DELETE SET NULL,
    hire_date               date NOT NULL,
    is_active               boolean NOT NULL DEFAULT TRUE
);

CREATE TABLE absence_type (
    id                      SERIAL PRIMARY KEY,
    label                   VARCHAR(100) NOT NULL,
    max_day_per_year        int,
    is_paid                 boolean
);

CREATE TABLE absence (
    id                      SERIAL PRIMARY KEY,
    employee_id             int REFERENCES employee(id),
    type_id                 int REFERENCES absence_type(id),
    start_date              date NOT NULL,
    end_date                date NOT NULL,
    status                  VARCHAR(20) CHECK (status IN ('pending', 'approved', 'rejected')) DEFAULT 'pending',
    reason                  text
);

CREATE TABLE leave_balance (
    id                      SERIAL PRIMARY KEY,
    employee_id             int REFERENCES employee(id),
    type_id                 int REFERENCES absence_type(id),
    year                    int NOT NULL,
    total_days              int NOT NULL,
    used_days               int DEFAULT 0
);


CREATE INDEX ON absence(employee_id);
CREATE INDEX ON leave_balance(employee_id, year);
CREATE INDEX ON employee(department_id);
