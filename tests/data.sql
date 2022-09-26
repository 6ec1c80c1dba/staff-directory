INSERT INTO user (id, username, password, staff_id, department_id)
VALUES
  (3, 'test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 12, 2),
  (4, 'john@email.com', 'pbkdf2:sha256:260000$SIrUaDlbHO4ONj1A$a3e63528815b537a9f75fc7394a8ecf6cbf2578570d89ceafd9d5c1d3cee2b20', 13, 1);

INSERT INTO staff_member (id, title, first_name, last_name, preferred, job_role, email, extension_number, system_administrator, in_department)
VALUES
  (12, "Miss", "Jane", "Doe", 'test', 'Team Lead', 'test', 25436, 1, 2),
  (13, "Mr", "Johnathon", "Doe", 'John', 'Human Resources Manager', 'john@email.com', 12345, 1, 2);


INSERT INTO post ( title, body, created_by, department_collection, posted_on)
VALUES 
  ("Test Title", "My Test Body", 3, 2, '2022-09-13 22:24:59'),
  ("My new post", "Contents of my post", 4, 1, '2022-09-24 20:30:00');