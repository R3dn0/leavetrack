INSERT INTO department (name) VALUES ('Test');

INSERT INTO employee (first_name, last_name, email, department_id, manager_id, hire_date)
VALUES
    ('Alice', 'Martin',  'alice.martin@leavetrack.dev',  1, NULL, '2019-03-15'),
    ('Bob',   'Dupont',  'bob.dupont@leavetrack.dev',    1, 1,    '2020-06-01'),
    ('Clara', 'Leclerc', 'clara.leclerc@leavetrack.dev', 1, 1,    '2021-09-10'),
    ('David', 'Moreau',  'david.moreau@leavetrack.dev',  1, 1,    '2022-01-20'),
    ('Emma',  'Bernard', 'emma.bernard@leavetrack.dev',  1, 1,    '2023-04-05');

INSERT INTO absence_type (label, max_day_per_year, is_paid)
VALUES
    ('Paid Leave',   25, TRUE),
    ('Sick Leave',   NULL, FALSE),
    ('Unpaid Leave', NULL, FALSE);

INSERT INTO leave_balance (employee_id, type_id, year, total_days, used_days)
VALUES
    (1, 1, 2025, 25, 5),
    (2, 1, 2025, 25, 10),
    (3, 1, 2025, 25, 0),
    (4, 1, 2025, 25, 15),
    (5, 1, 2025, 25, 3);

INSERT INTO absence (employee_id, type_id, start_date, end_date, status, reason)
VALUES
    (1, 1, '2025-02-10', '2025-02-14', 'approved',  'Winter holidays'),
    (2, 1, '2025-03-03', '2025-03-14', 'approved',  'Spring break'),
    (3, 2, '2025-04-07', '2025-04-08', 'approved',  'Flu'),
    (4, 1, '2025-05-01', '2025-05-16', 'approved',  'May holidays'),
    (5, 1, '2025-06-23', '2025-06-25', 'pending',   'Long weekend'),
    (2, 2, '2025-07-15', '2025-07-15', 'approved',  'Medical appointment'),
    (1, 3, '2025-08-01', '2025-08-03', 'rejected',  'Unpaid leave request denied'),
    (3, 1, '2025-09-22', '2025-09-26', 'pending',   'Autumn holidays');
