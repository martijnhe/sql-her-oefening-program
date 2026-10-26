CREATE TABLE department (
    id serial PRIMARY KEY NOT NULL,
    name character varying(15) NOT NULL,
    managerstart date,
    manager integer
);
ALTER TABLE ONLY department ADD CONSTRAINT department_name_key UNIQUE (name);

CREATE TABLE department_location (
    department integer NOT NULL,
    location character varying(15) NOT NULL
);
ALTER TABLE department_location ADD CONSTRAINT department_location_department_fkey FOREIGN KEY (department) REFERENCES department(id);

CREATE TABLE employee (
    id serial PRIMARY KEY NOT NULL,
    firstname character varying(15) NOT NULL,
    middlename character(1),
    lastname character varying(15) NOT NULL,
    ssn character(9) NOT NULL,
    birthdate date,
    address character varying(30),
    sex character(1),
    salary numeric(10,2),
    supervisor integer,
    department integer NOT NULL
);
ALTER TABLE employee ADD CONSTRAINT employee_ssn_key UNIQUE (ssn);

CREATE TABLE dependent (
    employee integer NOT NULL,
    name character varying(15) NOT NULL,
    sex character(1),
    birthdate date,
    relationship character varying(8)
);
ALTER TABLE dependent ADD CONSTRAINT dependent_employee_fkey FOREIGN KEY (employee) REFERENCES employee(id);

CREATE TABLE project (
    id serial PRIMARY KEY NOT NULL,
    name character varying(15) NOT NULL,
    location character varying(15),
    department integer NOT NULL
);
ALTER TABLE project ADD CONSTRAINT project_name_key UNIQUE (name);
ALTER TABLE project ADD CONSTRAINT project_department_fkey FOREIGN KEY (department) REFERENCES department(id);

CREATE TABLE works_on (
    employee integer NOT NULL,
    project integer NOT NULL,
    hours numeric(3,1) NOT NULL
);
ALTER TABLE works_on ADD CONSTRAINT works_on_employee_project_key UNIQUE (employee, project);
ALTER TABLE works_on ADD CONSTRAINT works_on_employee_fkey FOREIGN KEY (employee) REFERENCES employee(id);
ALTER TABLE works_on ADD CONSTRAINT works_on_project_fkey FOREIGN KEY (project) REFERENCES project(id);

INSERT INTO department (id, name, managerstart, manager) VALUES (1, 'Headquarters', '1971-06-19', 5);
INSERT INTO department (id, name, managerstart, manager) VALUES (4, 'Administration', '1985-01-01', 8);
INSERT INTO department (id, name, managerstart, manager) VALUES (5, 'Research', '1978-05-22', 9);
INSERT INTO department (id, name, managerstart, manager) VALUES (6, 'Software', '1999-05-15', 2);
INSERT INTO department (id, name, managerstart, manager) VALUES (7, 'Hardware', '1998-05-15', 4);
INSERT INTO department (id, name, managerstart, manager) VALUES (8, 'Sales', '1997-01-01', 3);
SELECT pg_catalog.setval('department_id_seq', 8, true);

INSERT INTO department_location (department, location) VALUES (1, 'Houston');
INSERT INTO department_location (department, location) VALUES (4, 'Stafford');
INSERT INTO department_location (department, location) VALUES (5, 'Bellaire');
INSERT INTO department_location (department, location) VALUES (5, 'Houston');
INSERT INTO department_location (department, location) VALUES (5, 'Sugarland');
INSERT INTO department_location (department, location) VALUES (6, 'Atlanta');
INSERT INTO department_location (department, location) VALUES (6, 'Sacramento');
INSERT INTO department_location (department, location) VALUES (7, 'Milwaukee');
INSERT INTO department_location (department, location) VALUES (8, 'Chicago');
INSERT INTO department_location (department, location) VALUES (8, 'Dallas');
INSERT INTO department_location (department, location) VALUES (8, 'Miami');
INSERT INTO department_location (department, location) VALUES (8, 'Philadephia');
INSERT INTO department_location (department, location) VALUES (8, 'Seattle');

INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (1, 'Evan', 'E', 'Wallis', '222222200', '1958-01-16', '134 Pelham Milwaukee WI', 'M', 92000.00, NULL, 7);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (2, 'Jared', 'D', 'James', '111111100', '1966-10-10', '123 Peachtree Atlanta GA', 'M', 85000.00, NULL, 6);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (3, 'John', 'C', 'James', '555555500', '1975-06-30', '7676 Bloomington Sacramento CA', 'M', 81000.00, NULL, 6);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (4, 'Alex', 'D', 'Freed', '444444400', '1950-10-09', '4333 Pillsbury Milwaukee WI', 'M', 89000.00, NULL, 7);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (5, 'James', 'E', 'Borg', '888665555', '1927-11-10', '450 Stone Houston TX', 'M', 55000.00, NULL, 1);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (6, 'Kim', 'C', 'Grace', '333333300', '1970-10-23', '6677 Mills Ave Sacramento CA', 'F', 79000.00, NULL, 6);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (7, 'Bob', 'B', 'Bender', '666666600', '1968-04-17', '8794 Garfield Chicago IL', 'M', 96000.00, NULL, 8);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (8, 'Jennifer', 'S', 'Wallace', '987654321', '1931-06-20', '291 Berry Bellaire TX', 'F', 43000.00, 5, 4);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (9, 'Franklin', 'T', 'Wong', '333445555', '1945-12-08', '638 Voss Houston TX', 'M', 40000.00, 5, 5);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (10, 'Andy', 'C', 'Vile', '222222202', '1944-06-21', '1967 Jordan Milwaukee WI', 'M', 53000.00, 1, 7);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (11, 'Brad', 'C', 'Knight', '111111103', '1968-02-13', '176 Main St. Atlanta GA', 'M', 44000.00, 2, 6);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department)
     VALUES (12, 'Josh', 'U', 'Zell', '222222201', '1954-05-22', '266 McGrady Milwaukee WI', 'M', 56000.00, 1, 7);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (13, 'Justin', 'n', 'Mark', '111111102', '1966-01-12', '2342 May Atlanta GA', 'M', 40000.00, 2, 6);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (14, 'Jon', 'C', 'Jones', '111111101', '1967-11-14', '111 Allgood Atlanta GA', 'M', 45000.00, 2, 6);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (15, 'Ahmad', 'V', 'Jabbar', '987987987', '1959-03-29', '980 Dallas Houston TX', 'M', 25000.00, 8, 4);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (16, 'Joyce', 'A', 'English', '453453453', '1962-07-31', '5631 Rice Houston TX', 'F', 25000.00, 9, 5);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (17, 'Ramesh', 'K', 'Narayan', '666884444', '1952-09-15', '971 Fire Oak Humble TX', 'M', 38000.00, 9, 5);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (18, 'Alicia', 'J', 'Zelaya', '999887777', '1958-07-19', '3321 Castle Spring TX', 'F', 25000.00, 8, 4);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (19, 'John', 'B', 'Smith', '123456789', '1955-01-09', '731 Fondren Houston TX', 'M', 30000.00, 9, 5);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (20, 'Tom', 'G', 'Brand', '222222203', '1966-12-16', '112 Third St Milwaukee WI', 'M', 62500.00, 1, 7);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (21, 'Jenny', 'F', 'Vos', '222222204', '1967-11-11', '263 Mayberry Milwaukee WI', 'F', 61000.00, 12, 7);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (22, 'Chris', 'A', 'Carter', '222222205', '1960-03-21', '565 Jordan Milwaukee WI', 'F', 43000.00, 12, 7);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (23, 'Jeff', 'H', 'Chase', '333333301', '1970-01-07', '145 Bradbury Sacramento CA', 'M', 44000.00, 6, 6);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (24, 'Bonnie', 'S', 'Bays', '444444401', '1956-06-19', '111 Hollow Milwaukee WI', 'F', 70000.00, 4, 7);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (25, 'Alec', 'C', 'Best', '444444402', '1966-06-18', '233 Solid Milwaukee WI', 'M', 60000.00, 4, 7);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (26, 'Sam', 'S', 'Snedden', '444444403', '1977-07-31', '987 Windy St Milwaukee WI', 'M', 48000.00, 4, 7);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (27, 'Nandita', 'K', 'Ball', '555555501', '1969-04-16', '222 Howard  Sacramento CA', 'M', 62000.00, 3, 6);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (28, 'Jill', 'J', 'Jarvis', '666666601', '1966-01-14', '6234 Lincoln Chicago IL', 'F', 36000.00, 7, 8);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (29, 'Kate', 'W', 'King', '666666602', '1966-04-16', '1976 Boone Trace Chicago IL', 'F', 44000.00, 7, 8);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (30, 'Lyle', 'G', 'Leslie', '666666603', '1963-06-09', '417 Hancock Ave Chicago IL', 'M', 41000.00, 28, 8);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (31, 'Billie', 'J', 'King', '666666604', '1960-01-01', '556 Washington Chicago IL', 'F', 38000.00, 30, 8);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (32, 'Jon', 'A', 'Kramer', '666666605', '1964-08-22', '1988 Windy Creek Seattle WA', 'M', 41500.00, 30, 8);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (33, 'Ray', 'H', 'King', '666666606', '1949-08-16', '213 Delk Road Seattle WA', 'M', 44500.00, 31, 8);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (34, 'Gerald', 'D', 'Small', '666666607', '1962-05-15', '122 Ball Street Dallas TX', 'M', 29000.00, 29, 8);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (35, 'Arnold', 'A', 'Head', '666666608', '1967-05-19', '233 Spring St Dallas TX', 'M', 33000.00, 29, 8);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (36, 'Helga', 'C', 'Pataki', '666666609', '1969-03-11', '101 Holyoke St Dallas TX', 'F', 32000.00, 29, 8);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (37, 'Naveen', 'B', 'Drew', '666666610', '1970-05-23', '198 Elm St Philadelphia PA', 'M', 34000.00, 34, 8);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (38, 'Carl', 'E', 'Reedy', '666666611', '1977-06-21', '213 Ball St Philadelphia PA', 'M', 32000.00, 37, 8);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (39, 'Sammy', 'G', 'Hall', '666666612', '1970-01-11', '433 Main Street Miami FL', 'M', 37000.00, 38, 8);
INSERT INTO employee (id, firstname, middlename, lastname, ssn, birthdate, address, sex, salary, supervisor, department) 
     VALUES (40, 'Red', 'A', 'Bacher', '666666613', '1980-05-21', '196 Elm Street Miami FL', 'M', 33500.00, 39, 8);
SELECT pg_catalog.setval('employee_id_seq', 40, true);

INSERT INTO dependent (employee, name, sex, birthdate, relationship) VALUES (9, 'Alice', 'F', '1976-04-05', 'Daughter');
INSERT INTO dependent (employee, name, sex, birthdate, relationship) VALUES (9, 'Theodore', 'M', '1973-10-25', 'Son');
INSERT INTO dependent (employee, name, sex, birthdate, relationship) VALUES (9, 'Joy', 'F', '1948-05-03', 'Spouse');
INSERT INTO dependent (employee, name, sex, birthdate, relationship) VALUES (8, 'Abner', 'M', '1932-02-29', 'Spouse');
INSERT INTO dependent (employee, name, sex, birthdate, relationship) VALUES (19, 'Michael', 'M', '1978-01-01', 'Son');
INSERT INTO dependent (employee, name, sex, birthdate, relationship) VALUES (19, 'Alice', 'F', '1978-12-31', 'Daughter');
INSERT INTO dependent (employee, name, sex, birthdate, relationship) VALUES (19, 'Elizabeth', 'F', NULL, 'Spouse');
INSERT INTO dependent (employee, name, sex, birthdate, relationship) VALUES (4, 'Johnny', 'M', '1997-04-04', 'Son');
INSERT INTO dependent (employee, name, sex, birthdate, relationship) VALUES (4, 'Tommy', 'M', '1999-06-07', 'Son');
INSERT INTO dependent (employee, name, sex, birthdate, relationship) VALUES (24, 'Chris', 'M', '1969-04-19', 'Spouse');
INSERT INTO dependent (employee, name, sex, birthdate, relationship) VALUES (25, 'Sam', 'M', '1964-02-14', 'Spouse');

INSERT INTO project (id, name, location, department) VALUES (1, 'ProductX', 'Bellaire', 5);
INSERT INTO project (id, name, location, department) VALUES (2, 'ProductY', 'Sugarland', 5);
INSERT INTO project (id, name, location, department) VALUES (3, 'ProductZ', 'Houston', 5);
INSERT INTO project (id, name, location, department) VALUES (10, 'Computerization', 'Stafford', 4);
INSERT INTO project (id, name, location, department) VALUES (20, 'Reorganization', 'Houston', 1);
INSERT INTO project (id, name, location, department) VALUES (30, 'Newbenefits', 'Stafford', 4);
INSERT INTO project (id, name, location, department) VALUES (61, 'OperatingSystem', 'Jacksonville', 6);
INSERT INTO project (id, name, location, department) VALUES (62, 'DatabaseSystem', 'Birmingham', 6);
INSERT INTO project (id, name, location, department) VALUES (63, 'Middleware', 'Jackson', 6);
INSERT INTO project (id, name, location, department) VALUES (91, 'InkjetPrinters', 'Phoenix', 7);
INSERT INTO project (id, name, location, department) VALUES (92, 'LaserPrinters', 'LasVegas', 7);
SELECT pg_catalog.setval('project_id_seq', 92, true);

INSERT INTO works_on (employee, project, hours) VALUES (19, 1, 32.5);
INSERT INTO works_on (employee, project, hours) VALUES (19, 2, 7.5);
INSERT INTO works_on (employee, project, hours) VALUES (17, 3, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (16, 1, 20.0);
INSERT INTO works_on (employee, project, hours) VALUES (16, 2, 20.0);
INSERT INTO works_on (employee, project, hours) VALUES (9, 2, 10.0);
INSERT INTO works_on (employee, project, hours) VALUES (9, 3, 10.0);
INSERT INTO works_on (employee, project, hours) VALUES (9, 10, 10.0);
INSERT INTO works_on (employee, project, hours) VALUES (9, 20, 10.0);
INSERT INTO works_on (employee, project, hours) VALUES (18, 30, 30.0);
INSERT INTO works_on (employee, project, hours) VALUES (18, 10, 10.0);
INSERT INTO works_on (employee, project, hours) VALUES (15, 10, 35.0);
INSERT INTO works_on (employee, project, hours) VALUES (15, 30, 5.0);
INSERT INTO works_on (employee, project, hours) VALUES (8, 30, 20.0);
INSERT INTO works_on (employee, project, hours) VALUES (8, 20, 15.0);
INSERT INTO works_on (employee, project, hours) VALUES (5, 20, 0.0);
INSERT INTO works_on (employee, project, hours) VALUES (2, 61, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (14, 61, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (13, 61, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (11, 61, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (1, 62, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (12, 62, 48.0);
INSERT INTO works_on (employee, project, hours) VALUES (10, 62, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (20, 62, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (21, 62, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (22, 62, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (6, 63, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (23, 63, 46.0);
INSERT INTO works_on (employee, project, hours) VALUES (4, 91, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (24, 91, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (25, 91, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (26, 91, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (3, 92, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (27, 92, 44.0);
INSERT INTO works_on (employee, project, hours) VALUES (28, 91, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (30, 91, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (31, 91, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (32, 92, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (33, 91, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (34, 61, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (35, 62, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (36, 63, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (37, 61, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (38, 61, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (39, 61, 40.0);
INSERT INTO works_on (employee, project, hours) VALUES (40, 61, 30.0);
INSERT INTO works_on (employee, project, hours) VALUES (40, 62, 10.0);
INSERT INTO works_on (employee, project, hours) VALUES (40, 63, 10.0);

ALTER TABLE department ADD CONSTRAINT department_manager_fkey FOREIGN KEY (manager) REFERENCES employee(id);
ALTER TABLE employee ADD CONSTRAINT employee_department_fkey FOREIGN KEY (department) REFERENCES department(id);
ALTER TABLE employee ADD CONSTRAINT employee_supervisor_fkey FOREIGN KEY (supervisor) REFERENCES employee(id);

