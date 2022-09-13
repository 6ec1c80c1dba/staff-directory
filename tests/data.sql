INSERT INTO user (username, password, staff_id, is_admin)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 12, 1),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', 13, 1);

INSERT INTO staff_member (title, first_name, last_name, preferred, job_role, email, extension_number, system_administrator, department_id)
VALUES
  ("Mr", "Johnathon", "Doe", 'John', 'Human Resources Manager', 'john@email.com', 12345, 1, 2)