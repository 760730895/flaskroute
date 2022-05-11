DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  password TEXT NOT NULL
);

INSERT INTO users (name, password) VALUES ('visit', '111');
INSERT INTO users (name, password) VALUES ('admin', '123');