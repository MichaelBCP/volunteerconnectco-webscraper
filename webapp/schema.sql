DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS opportunity;
DROP TABLE IF EXISTS verification;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT DEFAULT 'verifier',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE opportunity (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  organization_name TEXT NOT NULL,
  volunteer_title TEXT NOT NULL,
  url TEXT NOT NULL,
  image TEXT,
  position_date TEXT NOT NULL,
  description TEXT NOT NULL,
  age_requirement TEXT,
  skill_requirement TEXT,
  address_virtual TEXT,
  passion_areas TEXT,
  specific_skills TEXT,
  filters TEXT,
  assigned_user_id INTEGER,
  verification_status TEXT DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (assigned_user_id) REFERENCES user (id)
);

CREATE TABLE verification (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  opportunity_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  status TEXT NOT NULL,
  notes TEXT,
  verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (opportunity_id) REFERENCES opportunity (id),
  FOREIGN KEY (user_id) REFERENCES user (id)
);
