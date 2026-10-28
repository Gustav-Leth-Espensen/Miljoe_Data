CREATE TABLE meta_data (
    id SERIAL PRIMARY KEY,
    station_id CHAR(5) NOT NULL,
    name VARCHAR(50),
    coordinates_longitude FLOAT NOT NULL,
    coordinates_latitude FLOAT NOT NULL
    );

CREATE TABLE dmi_humidity (
    id SERIAL NOT NULL,
    observation_id CHAR(36) PRIMARY KEY,
    station_id CHAR(5) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE,
    percent_humidity FLOAT NOT NULL
    );

CREATE TABLE dmi_temp_dry (
    id SERIAL NOT NULL,
    observation_id CHAR(36) PRIMARY KEY,
    station_id CHAR(5) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE,
    celsius FLOAT NOT NULL
    );

CREATE TABLE dmi_pressure (
    id SERIAL NOT NULL,
    observation_id CHAR(36) PRIMARY KEY,
    station_id CHAR(5) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE,
    hPa FLOAT NOT NULL
    );


CREATE TABLE local_temperature (
    id SERIAL NOT NULL,
    observation_id CHAR(36) PRIMARY KEY,
    instrument_model CHAR(7) NOT NULL,
    station_id CHAR(5) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE,
    celsius FLOAT NOT NULL
    );

CREATE TABLE local_humidity (
    id SERIAL NOT NULL,
    observation_id CHAR(36) PRIMARY KEY,
    instrument_model CHAR(7) NOT NULL,
    station_id CHAR(5) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE,
    percent_humidity FLOAT NOT NULL
    );


CREATE TABLE local_pressure (
    id SERIAL NOT NULL,
    observation_id CHAR(36) PRIMARY KEY,
    instrument_model CHAR(7) NOT NULL,
    station_id CHAR(5) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE,
    pascal FLOAT NOT NULL
    );

CREATE TABLE local_CO2 (
    id SERIAL NOT NULL,
    observation_id CHAR(36) PRIMARY KEY,
    instrument_model CHAR(7) NOT NULL,
    station_id CHAR(5) NOT NULL,
    observed_time TIMESTAMP WITH TIME ZONE,
    ppm FLOAT NOT NULL
    );

