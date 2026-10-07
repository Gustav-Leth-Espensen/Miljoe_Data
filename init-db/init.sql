CREATE TABLE humidity (
    station_id CHAR(5) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE,
    percent_humidity FLOAT NOT NULL
    );

CREATE TABLE temp_dry (
    station_id CHAR(5) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE,
    temperature FLOAT NOT NULL
    );

CREATE TABLE pressure (
    station_id CHAR(5) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE,
    mbar FLOAT NOT NULL
    );