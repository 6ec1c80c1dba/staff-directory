DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS staff_member;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS location;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  password TEXT NOT NULL, 
  staff_id INTEGER NOT NULL,
  is_admin INTEGER NOT NULL,
  FOREIGN KEY (username) references staff_member (email),
  FOREIGN KEY (staff_id) references staff_member (id),
  FOREIGN KEY (is_admin) references staff_member (system_administrator)
);

CREATE TABLE staff_member (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  preferred TEXT NOT NULL,
  job_role TEXT NOT NULL,
  email TEXT NOT NULL,
  extension_number VARCHAR (20), 
  system_administrator INTEGER NOT NULL,
  department_id INTEGER NOT NULL,
  FOREIGN KEY (department_id) REFERENCES department (id)
);

CREATE TABLE department (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  department_name TEXT,
  location_id TEXT,
  FOREIGN KEY (id) REFERENCES locations (id)
);

CREATE TABLE location (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  street_address VARCHAR (40),
  postal_code VARCHAR (12) NOT NULL
);

DELETE FROM user;

INSERT INTO location (street_address, postal_code)
VALUES
('Oxford Street', 'W1D 1BS'),
('Shoreditch High Street', 'E1 6JE'),
('Soho Street', 'W1D 3AD');

INSERT INTO department (department_name, location_id)
VALUES
('Advertising', 1),
('Recruitment', 2),
('Marketing', 3);

INSERT INTO staff_member (title, first_name, last_name, preferred, job_role, email, extension_number, system_administrator, department_id)
VALUES
  ("Mr", "Johnathon", "Dove", "John", 'Human Resources Administrator', 'johnathondove@mediacentral.com', 12652, 1, 2),
  ("Mrs", "Sam", "Park", 'Sammie', 'Advertising Executive', 'sampark@mediacentral.com', 79513, 0, 1),
  ("Mr", "Stewart", "Thomas", "Stew", 'Marketing Advisor', 'stewartthomas@mediacentral.com', 87623, 0, 3),
  ("Miss", "Brenda", "Serrano", 'Brenda', 'Training and Development Advisor', 'sampark@mediacentral.com', 28367, 0, 2),
  ("Mr", "Anthony", "Sharp", 'Tony', 'Advertising Manager', 'anthonysharp@mediacentral.com', 92945, 0, 1),
  ("Miss", "Jasmin", "Powers", 'Jaz', 'Marketing Executive', 'jasminpowers@mediacentral.com', 66805, 0, 2);

INSERT INTO user (username, password, staff_id, is_admin)
VALUES
('johnathondove@mediacentral.com', 'pbkdf2:sha256:260000$SIrUaDlbHO4ONj1A$a3e63528815b537a9f75fc7394a8ecf6cbf2578570d89ceafd9d5c1d3cee2b20', 1, 1),
('jasminpowers@mediacentral.com', 'pbkdf2:sha256:260000$SIrUaDlbHO4ONj1A$a3e63528815b537a9f75fc7394a8ecf6cbf2578570d89ceafd9d5c1d3cee2b20', 6, 0);





