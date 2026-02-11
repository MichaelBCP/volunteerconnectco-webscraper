DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE opportunity (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  organization_name TEXT NOT NULL,
  volunteer_title TEXT NOT NULL,
  url TEXT NOT NULL,
  image TEXT NOT NULL,
  position_date TEXT NOT NULL,
  description TEXT NOT NULL,
  age_requirement TEXT NOT NULL,
  skill_requirement TEXT NOT NULL,
  address_virtual TEXT NOT NULL,
  passion_areas TEXT NOT NULL,
  specific_skills TEXT NOT NULL,
  filters TEXT NOT NULL,
  assigned_user INTEGER,
  verification_status
);
