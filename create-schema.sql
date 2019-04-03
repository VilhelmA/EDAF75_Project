PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS recipes;
CREATE TABLE recipes(
    bar_code    INT,
    name        TEXT,
    PRIMARY KEY (bar_code)
);

DROP TABLE IF EXISTS customers;
CREATE TABLE customers(
    customer_name   TEXT,
    address         TEXT,
    PRIMARY KEY (customer_name)
);

DROP TABLE IF EXISTS raw_materials;
CREATE TABLE raw_materials(
    ingredient_name TEXT,
    balance         INT,
    unit            TEXT,
    update_date     DATE,
    update_amount   INT,
    PRIMARY KEY (ingredient_name)
);

DROP TABLE IF EXISTS recipe_entries;
CREATE TABLE recipe_entries(
    amount          INT,
    bar_code        INT,
    ingredient_name TEXT,
    PRIMARY KEY (bar_code, ingredient_name),
    FOREIGN KEY (bar_code) REFERENCES recipes (bar_code),
    FOREIGN KEY (ingredient_name) REFERENCES raw_materials(ingredient_name)
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders(
    order_id        INT,
    order_date      DATE,
    delivered       INT,
    customer_name   TEXT,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_name) REFERENCES customers(customer_name)
);

DROP TABLE IF EXISTS pallets;
CREATE TABLE pallets(
    pallet_nbr  INT,
    bar_code    INT,
    time        TIME,
    date        DATE,
    is_blocked  INT,
    order_id    INT,
    PRIMARY KEY (pallet_nbr),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (bar_code)  REFERENCES recipes(bar_code)
);

DROP TABLE IF EXISTS order_spec;
CREATE TABLE order_spec(
    bar_code    INT,
    order_id    INT,
    quantity    INT,
    PRIMARY KEY (bar_code, order_id),
    FOREIGN KEY (bar_code) REFERENCES recipes (bar_code),
    FOREIGN KEY (order_id) REFERENCES orders (order_id)
);
