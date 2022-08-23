DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS staff_member;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS locations;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL, 
  staff_id INTEGER NOT NULL,
  FOREIGN KEY (staff_id) references staff_member (id)
);

CREATE TABLE staff_member (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  full_name TEXT,
  preferred TEXT NOT NULL,
  job_role TEXT NOT NULL,
  email TEXT NOT NULL,
  extension_number VARCHAR (20), 
  manager_id INTEGER,
  system_administrator INTEGER NOT NULL,
  department_id INTEGER NOT NULL,
  FOREIGN KEY (department_id) REFERENCES department (id)
  FOREIGN KEY (manager_id) REFERENCES staff_member (id)
);

CREATE TABLE department (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  department_name TEXT,
  location_id TEXT,
  FOREIGN KEY (id) REFERENCES locations (id)
);

CREATE TABLE locations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  street_address VARCHAR (40),
  postal_code VARCHAR (12) NOT NULL,
  FOREIGN KEY (id) REFERENCES staff_member (id)
);

