CREATE TABLE product (
    ASINid varchar(60) PRIMARY KEY,
    Picture varchar(60),
    Hazardous varchar(60),
    Oversized varchar(60),
    description varchar(200)
);

CREATE TABLE physicalLocation (
    Locationid SERIAL PRIMARY KEY,
    RackID INTEGER NOT NULL,
    ShelfID INTEGER NOT NULL
    );

CREATE TABLE bin (
    ContentID SERIAL PRIMARY KEY, 
    Locationid INTEGER REFERENCES physicalLocation(Locationid),
    ASINid varchar(60)REFERENCES product(ASINid),
    quantity INTEGER,
    dateReceived TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expirationDate varchar(60)
);

CREATE TABLE orders (
    Invid SERIAL PRIMARY KEY ,
    ASINid varchar(60) REFERENCES product(ASINid),
    datePurchased TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    buyPrice NUMERIC(7,2),
    sellPrice NUMERIC(7,2),
    store varchar(60),
    supplier varchar(60),
    quantity INTEGER,
    orderNumber varchar(60),
    fullfillment varchar(60),
    buyer varchar(60),
    description varchar(200) REFERENCES product (description)
    
);

CREATE TABLE tracking (
    id SERIAL PRIMARY KEY,
    TrackingID varchar(60), 
    invid INTEGER REFERENCES orders,
    received varchar(60)
);

CREATE TABLE trackingContents(
    trackeditem SERIAL PRIMARY KEY,
    TrackingID varchar(60),
    invid INTEGER,
    ASINid varchar(60) REFERENCES product(ASINid),
    quantity INTEGER
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY ,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);


CREATE TABLE users( 
    id SERIAL PRIMARY KEY,
    name varchar(100),
    email varchar(100),
    username varchar(30),
    userRole varchar(30),
    password varchar(100),
    register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
);
