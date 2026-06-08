INSERT INTO
    department (name)
VALUES ('Engineering'),
    ('Human Resources'),
    ('Sales'),
    ('Marketing'),
    ('Finance');

INSERT INTO
    employee (
        first_name,
        last_name,
        email,
        department_id,
        manager_id,
        hire_date
    )
VALUES (
        'Alice',
        'Martin',
        'alice.martin@leavetrack.dev',
        1,
        NULL,
        '2019-03-15'
    ),
    (
        'Bob',
        'Dupont',
        'bob.dupont@leavetrack.dev',
        1,
        1,
        '2020-06-01'
    ),
    (
        'David',
        'Moreau',
        'david.moreau@leavetrack.dev',
        1,
        1,
        '2022-01-20'
    ),
    (
        'Clara',
        'Leclerc',
        'clara.leclerc@leavetrack.dev',
        2,
        NULL,
        '2021-09-10'
    ),
    (
        'Emma',
        'Bernard',
        'emma.bernard@leavetrack.dev',
        2,
        4,
        '2023-04-05'
    ),
    (
        'Francois',
        'Petit',
        'francois.petit@leavetrack.dev',
        3,
        NULL,
        '2018-11-01'
    ),
    (
        'Julie',
        'Renard',
        'julie.renard@leavetrack.dev',
        3,
        6,
        '2021-02-15'
    ),
    (
        'Hugo',
        'Lambert',
        'hugo.lambert@leavetrack.dev',
        4,
        NULL,
        '2020-09-01'
    ),
    (
        'Sarah',
        'Cohen',
        'sarah.cohen@leavetrack.dev',
        4,
        8,
        '2022-06-15'
    ),
    (
        'Isabelle',
        'Morel',
        'isabelle.morel@leavetrack.dev',
        5,
        NULL,
        '2021-01-10'
    );

INSERT INTO
    absence_type (
        label,
        code,
        max_days_per_year,
        is_paid
    )
VALUES (
        'Paid Leave',
        'paid',
        25,
        TRUE
    ),
    (
        'Sick Leave',
        'sick',
        NULL,
        FALSE
    ),
    (
        'Unpaid Leave',
        'unpaid',
        NULL,
        FALSE
    );

INSERT INTO
    leave_balance (
        employee_id,
        type_id,
        year,
        total_days,
        used_days
    )
VALUES (1, 1, 2024, 25, 22),
    (1, 1, 2025, 25, 5),
    (1, 1, 2026, 25, 0),
    (2, 1, 2024, 25, 18),
    (2, 1, 2025, 25, 10),
    (2, 1, 2026, 25, 0),
    (3, 1, 2024, 25, 20),
    (3, 1, 2025, 25, 15),
    (3, 1, 2026, 25, 0),
    (4, 1, 2024, 25, 12),
    (4, 1, 2025, 25, 0),
    (4, 1, 2026, 25, 0),
    (5, 1, 2024, 25, 8),
    (5, 1, 2025, 25, 3),
    (5, 1, 2026, 25, 0),
    (6, 1, 2024, 25, 25),
    (6, 1, 2025, 25, 8),
    (6, 1, 2026, 25, 0),
    (7, 1, 2024, 25, 15),
    (7, 1, 2025, 25, 4),
    (7, 1, 2026, 25, 0),
    (8, 1, 2024, 25, 10),
    (8, 1, 2025, 25, 6),
    (8, 1, 2026, 25, 0),
    (9, 1, 2024, 25, 5),
    (9, 1, 2025, 25, 2),
    (9, 1, 2026, 25, 0),
    (10, 1, 2024, 25, 20),
    (10, 1, 2025, 25, 12),
    (10, 1, 2026, 25, 0),
    (1, 2, 2024, NULL, 2),
    (2, 2, 2024, NULL, 1),
    (3, 2, 2024, NULL, 3),
    (4, 2, 2024, NULL, 0),
    (5, 2, 2024, NULL, 1),
    (6, 2, 2024, NULL, 0),
    (7, 2, 2024, NULL, 2),
    (8, 2, 2024, NULL, 0),
    (9, 2, 2024, NULL, 1),
    (10, 2, 2024, NULL, 0),
    (1, 2, 2025, NULL, 0),
    (2, 2, 2025, NULL, 1),
    (3, 2, 2025, NULL, 5),
    (4, 2, 2025, NULL, 0),
    (5, 2, 2025, NULL, 1),
    (6, 2, 2025, NULL, 0),
    (7, 2, 2025, NULL, 1),
    (8, 2, 2025, NULL, 0),
    (9, 2, 2025, NULL, 0),
    (10, 2, 2025, NULL, 0),
    (1, 3, 2025, NULL, 0),
    (10, 3, 2025, NULL, 0);

INSERT INTO
    absence (
        employee_id,
        type_id,
        start_date,
        end_date,
        status,
        reason
    )
VALUES (
        1,
        1,
        '2024-07-22',
        '2024-08-16',
        'approved',
        'Summer holidays'
    ),
    (
        1,
        2,
        '2024-11-11',
        '2024-11-12',
        'approved',
        'Food poisoning'
    ),
    (
        1,
        1,
        '2025-02-10',
        '2025-02-14',
        'approved',
        'Winter holidays'
    ),
    (
        1,
        3,
        '2025-08-01',
        '2025-08-03',
        'rejected',
        'Unpaid leave request denied'
    ),
    (
        2,
        1,
        '2024-05-13',
        '2024-05-17',
        'approved',
        'Spring break'
    ),
    (
        2,
        1,
        '2025-03-03',
        '2025-03-14',
        'approved',
        'Spring break'
    ),
    (
        2,
        2,
        '2025-07-15',
        '2025-07-15',
        'approved',
        'Medical appointment'
    ),
    (
        2,
        1,
        '2025-10-20',
        '2025-10-21',
        'approved',
        'Docker workshop'
    ),
    (
        3,
        1,
        '2024-01-02',
        '2024-01-26',
        'approved',
        'Extended new year break'
    ),
    (
        3,
        1,
        '2025-09-22',
        '2025-09-26',
        'pending',
        'Autumn holidays'
    ),
    (
        3,
        2,
        '2025-12-01',
        '2025-12-05',
        'approved',
        'Flu'
    ),
    (
        4,
        1,
        '2025-06-01',
        '2025-09-01',
        'approved',
        'Maternity leave'
    ),
    (
        4,
        1,
        '2026-01-12',
        '2026-01-16',
        'pending',
        'Ski trip'
    ),
    (
        5,
        1,
        '2025-06-23',
        '2025-06-25',
        'pending',
        'Long weekend'
    ),
    (
        5,
        2,
        '2025-11-10',
        '2025-11-10',
        'approved',
        'Child sick at home'
    ),
    (
        6,
        1,
        '2024-12-23',
        '2025-01-03',
        'approved',
        'Christmas holidays'
    ),
    (
        6,
        1,
        '2025-07-07',
        '2025-07-18',
        'approved',
        'Summer break'
    ),
    (
        6,
        1,
        '2025-04-10',
        '2025-04-11',
        'approved',
        'Kubernetes conference'
    ),
    (
        7,
        1,
        '2025-05-01',
        '2025-05-16',
        'approved',
        'May holidays'
    ),
    (
        7,
        2,
        '2025-09-15',
        '2025-09-16',
        'approved',
        'Migraine'
    ),
    (
        8,
        1,
        '2025-08-11',
        '2025-08-22',
        'approved',
        'Summer break'
    ),
    (
        8,
        3,
        '2025-03-17',
        '2025-03-17',
        'approved',
        'Family event'
    ),
    (
        9,
        1,
        '2025-04-21',
        '2025-04-23',
        'approved',
        'Staycation'
    ),
    (
        9,
        1,
        '2026-02-02',
        '2026-02-06',
        'pending',
        'Winter break'
    ),
    (
        10,
        1,
        '2024-08-05',
        '2024-08-30',
        'approved',
        'Summer holidays'
    ),
    (
        10,
        1,
        '2025-04-14',
        '2025-04-25',
        'approved',
        'Easter break'
    ),
    (
        10,
        3,
        '2025-12-22',
        '2025-12-31',
        'pending',
        'Unpaid extra holidays'
    ),
    (
        3,
        1,
        '2026-06-15',
        '2026-06-19',
        'pending',
        'Team building'
    ),
    (
        5,
        3,
        '2026-05-01',
        '2026-05-10',
        'pending',
        'Paternity leave'
    ),
    (
        2,
        2,
        '2026-04-06',
        '2026-04-06',
        'pending',
        'Family obligation'
    );