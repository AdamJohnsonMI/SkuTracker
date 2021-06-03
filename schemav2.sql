CREATE TABLE product (
    ASINid varchar(60) PRIMARY KEY,
    Picture varchar(60),
    Hazardous varchar(60),
    Oversized varchar(60),
    desription varchar(60)
);

CREATE TABLE physicalLocation (
    Locationid SERIAL PRIMARY KEY,
    RackID INTEGER NOT NULL,
    ShelfID INTEGER NOT NULL
    );

CREATE TABLE bin (
    ContentID SERIAL PRIMARY KEY, 
    Locationid INTEGER REFERENCES physicalLocation(Locationid),
    ASINid varchar(60)REFERENCES product,
    quantity INTEGER,
    dateReceived varchar(60),
    expirationDate varchar(60)
);

CREATE TABLE orders (
    Invid SERIAL PRIMARY KEY ,
    ASINid varchar(60) REFERENCES product,
    datePurchased TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    buyPrice NUMERIC(7,2),
    sellPrice NUMERIC(7,2),
    store varchar(60),
    supplier varchar(60),
    quantity INTEGER,
    orderNumber varchar(60),
    fullfillment varchar(60),
    buyer varchar(60)
);

CREATE TABLE tracking (
    TrackingID SERIAL PRIMARY KEY, 
    invid INTEGER REFERENCES orders,
    received varchar(60)
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY ,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);