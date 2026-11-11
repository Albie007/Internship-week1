
CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);

CREATE TABLE employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    salary DECIMAL(10,2),
    department_id INT,
    FOREIGN KEY (department_id)
    REFERENCES departments(department_id)
);

INSERT INTO departments (department_name, location)
VALUES
('HR', 'Kochi'),
('IT', 'Bangalore'),
('Finance', 'Chennai'),
('Marketing', 'Trivandrum'),
('Sales', 'Kochi');


INSERT INTO employees
(employee_name, email, salary, department_id)
VALUES
('Arun', 'arun@gmail.com', 30000, 1),
('Priya', 'priya@gmail.com', 45000, 2),
('Rahul', 'rahul@gmail.com', 35000, 3),
('Anjali', 'anjali@gmail.com', 50000, 2),
('Vishnu', 'vishnu@gmail.com', 28000, 4),
('Meera', 'meera@gmail.com', 40000, 1);

SELECT * FROM employees;
SELECT * FROM departments;

INSERT INTO employees
(employee_name, email, salary, department_id)
VALUES
('Kiran', 'kiran@gmail.com', 32000, 5);

INSERT INTO employees
(employee_name, email, salary, department_id)
VALUES
('Kiran', 'kiran@gmail.com', 32000, 5);


SELECT employee_name, salary
FROM employees;


SELECT *
FROM employees
WHERE salary > 35000;

UPDATE employees
SET salary = 35000
WHERE employee_name = 'Arun';

UPDATE employees
SET email = 'priya123@gmail.com'
WHERE employee_id = 2;


DELETE FROM employees
WHERE employee_id = 7;


SELECT
    employees.employee_name,
    departments.department_name
FROM employees
INNER JOIN departments
ON employees.department_id = departments.department_id;


SELECT
    departments.department_name,
    employees.employee_name
FROM departments
LEFT JOIN employees
ON departments.department_id = employees.department_id;


SELECT
    employees.employee_name,
    departments.department_name
FROM employees
RIGHT JOIN departments
ON employees.department_id = departments.department_id;


SELECT COUNT(*) AS total_employees
FROM employees;


SELECT SUM(salary) AS total_salary
FROM employees;


SELECT MAX(salary) AS highest_salary
FROM employees;


SELECT
    department_id,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department_id;

