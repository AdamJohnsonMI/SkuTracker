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
    dateReceived varchar(60),
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
    buyer varchar(60)
);

CREATE TABLE tracking (
    TrackingID varchar(60) PRIMARY KEY, 
    invid INTEGER REFERENCES orders,
    received varchar(60)
);

--Can add trackingContents to match tracking to
CREATE TABLE trackingContents(
    trackeditem SERIAL PRIMARY KEY,
    TrackingID varchar(60) REFERENCES tracking(TrackingID),
    ASINid varchar(60) REFERENCES product(ASINid),
    quantity INTEGER
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY ,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);


--The sections below are onyl for remembering privilege access


CREATE USER readonly  WITH ENCRYPTED PASSWORD '(password here)';
GRANT USAGE ON SCHEMA public to adam;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO adam;

GRANT CONNECT ON DATABASE inventory to adam;
\c foo
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO adam; --- this grants privileges on new tables generated in new database "foo"
GRANT USAGE ON SCHEMA public to adam; 
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO adam;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO adam;


GRANT ALL PRIVILEGES ON DATABASE inventory TO adam;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO adam;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO adam;