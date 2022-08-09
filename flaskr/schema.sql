DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS staff_member;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE staff_member (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  staff_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  full_name TEXT ,
  preferred TEXT NOT NULL,
  job_role TEXT NOT NULL,
  email TEXT,
  FOREIGN KEY (staff_id) REFERENCES staff_member (id)
);