CREATE TABLE email_password (
  email TEXT PRIMARY KEY,
  password TEXT NOT NULL,
  role TEXT NOT NULL
);

CREATE TABLE teacher (
  name TEXT NOT NULL,
  email TEXT PRIMARY KEY UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL,
  role TEXT NOT NULL
);

CREATE TABLE student (
  name TEXT NOT NULL,
  email TEXT PRIMARY KEY UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL,
  role TEXT NOT NULL
);

CREATE TABLE teacher_students (
  teacher_email TEXT,
  student_email TEXT,
  PRIMARY KEY(teacher_email, student_email),
  FOREIGN KEY(teacher_email) REFERENCES teacher(email),
  FOREIGN KEY(student_email) REFERENCES student(email)
);

CREATE TABLE theme (
  name TEXT NOT NULL,
  teacher_email TEXT NOT NULL,
  materials BLOB, 
  homework BLOB,
  PRIMARY KEY(teacher_email, name),
  FOREIGN KEY(teacher_email) REFERENCES teacher(email)
);

CREATE TABLE lesson (
  teacher_email TEXT,
  student_email TEXT,
  lesDate TEXT,
  theme_name TEXT,
  link TEXT,
  note TEXT,
  passed TEXT,
  PRIMARY KEY(teacher_email, lesDate),
  FOREIGN KEY(teacher_email, student_email) REFERENCES teacher_students(teacher_email, student_email),
  -- FOREIGN KEY(student_email) REFERENCES teacher_students(student_email),
  FOREIGN KEY(theme_name) REFERENCES theme(name)
);