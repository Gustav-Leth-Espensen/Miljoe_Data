CREATE TABLE humidity (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE precip_past1min (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

/*
 timestamp med timezone
 stations id kotrere
 tjek float om byte størrelse

 */
CREATE TABLE pressure (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE wind_max (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE cloud_cover (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE radia_glob (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE precip_past10min (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE pressure_at_sea (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE precip_dur_past10min (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE temp_dry (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE wind_speed (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE temp_dew (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE leav_hum_dur_past10min (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE wind_dir (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE visibility (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE sun_last10min_glob (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE temp_soil (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE visib_mean_last10min (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE temp_grass (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE wind_min (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE cloud_height (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );

CREATE TABLE wind_gust_past10min (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    );