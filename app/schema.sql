CREATE TABLE user (
    username VARCHAR(20) UNIQUE NOT NULL PRIMARY KEY,
    password VARCHAR(255),
    role VARCHAR(1) default 0,
    created TEXT,
    modified TEXT NULL
);

CREATE TABLE customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(35) NOT NULL,
    addr TEXT NULL,
    pic_name VARCHAR(35) NULL,
    pic_hp VARCHAR(35) NULL,
    pic_email VARCHAR(35) NULL,
    created TEXT,
    modified TEXT NULL
);

CREATE TABLE shipment (
    
);