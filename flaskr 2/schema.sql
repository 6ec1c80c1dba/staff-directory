DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS staff_member;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username CHAR(50) NOT NULL,
  password CHAR(30) NOT NULL, 
  staff_id INTEGER NOT NULL,
  is_admin INTEGER NOT NULL,
  department_id INTEGER NOT NULL,
  FOREIGN KEY (username) references staff_member (email),
  FOREIGN KEY (staff_id) references staff_member (id),
  FOREIGN KEY (is_admin) references staff_member (system_administrator),
  FOREIGN KEY (department_id) references staff_member (department_id)
);

CREATE TABLE staff_member (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title CHAR (20) NOT NULL,
  first_name CHAR (40) NOT NULL,
  last_name VARCHAR NOT NULL,
  preferred CHAR (50) NOT NULL,
  job_role CHAR (30) NOT NULL,
  email CHAR (40) NOT NULL,
  extension_number CHAR (20) DEFAULT NULL, 
  system_administrator INTEGER NOT NULL,
  in_department INTEGER NOT NULL,
  FOREIGN KEY (in_department) REFERENCES department (id)
);

CREATE TABLE department (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  department_name CHAR (20)
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title CHAR (40) NOT NULL,
  body TEXT NOT NULL,
  created_by CHAR (40) NOT NULL, 
  department_collection CHAR (20),
  posted_on DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES user (username),
  FOREIGN KEY (department_collection) REFERENCES department (id)
);


INSERT INTO department (id, department_name)
VALUES
(1, 'Advertising'),
(2, 'Recruitment'),
(3, 'Marketing');

INSERT INTO staff_member (title, first_name, last_name, preferred, job_role, email, extension_number, system_administrator, in_department)
VALUES
  ("Mr", "Johnathon", "Dove", "John", 'Human Resources Administrator', 'johnathondove@mediacentral.com', 12652, 1, 2),
  ("Miss", "Jasmin", "Powers", 'Jaz', 'Marketing Executive', 'jasminpowers@mediacentral.com', 66805, 0, 2),
  ("Mrs", "Sam", "Park", 'Sammie', 'Advertising Executive', 'sampark@mediacentral.com', 79513, 0, 1),
  ("Mr", "Stewart", "Thomas", "Stew", 'Marketing Advisor', 'stewartthomas@mediacentral.com', 87623, 0, 3),
  ("Miss", "Brenda", "Serrano", 'Brenda', 'Training and Development Advisor', 'brendaserrano@mediacentral.com', 28367, 0, 2),
  ("Mr", "Anthony", "Sharp", 'Tony', 'Advertising Manager', 'anthonysharp@mediacentral.com', 92945, 0, 1);

INSERT INTO user (username, password, staff_id, is_admin, department_id)
VALUES
('johnathondove@mediacentral.com', 'pbkdf2:sha256:260000$SIrUaDlbHO4ONj1A$a3e63528815b537a9f75fc7394a8ecf6cbf2578570d89ceafd9d5c1d3cee2b20', 1, 1, 2),
('jasminpowers@mediacentral.com', 'pbkdf2:sha256:260000$SIrUaDlbHO4ONj1A$a3e63528815b537a9f75fc7394a8ecf6cbf2578570d89ceafd9d5c1d3cee2b20', 2, 0, 2);




