CREATE TABLE humidity (
    station_ID CHAR(7) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE
    percent_humidity FLOAT NOT NULL
    );

CREATE TABLE temp_dry (
    station_ID CHAR(7) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE
    temperature FLOAT NOT NULL
    );

/*
 timestamp med timezone
 stations id kotrere
 tjek float om byte størrelse

 */
CREATE TABLE pressure (
    station_ID CHAR(7) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE
    mbar FLOAT NOT NULL
    );