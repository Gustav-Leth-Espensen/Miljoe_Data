CREATE TABLE meta_data (
    id SERIAL PRIMARY KEY,
    station_id CHAR(5) NOT NULL,
    name VARCHAR(50),
    coordinates_longitude FLOAT NOT NULL,
    coordinates_latitude FLOAT NOT NULL
    );

CREATE TABLE humidity (
    id SERIAL PRIMARY KEY,
    station_id CHAR(5) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE,
    percent_humidity FLOAT NOT NULL
    );

CREATE TABLE temp_dry (
    id SERIAL PRIMARY KEY,
    station_id CHAR(5) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE,
    temperature FLOAT NOT NULL
    );

CREATE TABLE pressure (
    id SERIAL PRIMARY KEY,
    station_id CHAR(5) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE,
    mbar FLOAT NOT NULL
    );