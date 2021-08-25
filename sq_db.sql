create table if not exists menu (
id integer primary key autoincrement,
title text not null,
url text not null
);

CREATE TABLE IF NOT EXISTS posts (
id integer PRIMARY KEY AUTOINCREMENT,
article text NOT NULL,
book text NOT NULL,
author text NOT NULL,
post text NOT NULL,
time integer NOT NULL
);