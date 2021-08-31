create table if not exists menu (
id integer primary key autoincrement,
title text not null,
url text not null
);

CREATE TABLE IF NOT EXISTS posts (
id integer PRIMARY KEY AUTOINCREMENT,
id_user integer NOT NULL,
article text NOT NULL,
book text NOT NULL,
author text NOT NULL,
post text NOT NULL,
time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
email text NOT NULL,
psw text NOT NULL,
time integer NOT NULL
);