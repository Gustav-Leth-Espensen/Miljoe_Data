CREATE TABLE IF NOT EXISTS humidity (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS precip_past1min (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS pressure (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS wind_max (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS cloud_cover (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS radia_glob (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS precip_past10min (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS pressure_at_sea (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS precip_dur_past10min (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS temp_dry (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS wind_speed (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS temp_dew (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS leav_hum_dur_past10min (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS wind_dir (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS visibility (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS sun_last10min_glob (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS temp_soil (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS visib_mean_last10min (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS temp_grass (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS wind_min (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS cloud_height (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )

CREATE TABLE IF NOT EXISTS wind_gust_past10min (
    station_ID VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    value_d FLOAT NOT NULL
    )