CREATE TABLE data (
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    price INT NOT NULL,
    code TEXT UNIQUE
     /* required so the form can't be submitted without the entry having something in it .*/

);