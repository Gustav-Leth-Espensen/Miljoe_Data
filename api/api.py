import os
from fastapi import FastAPI, Query, param_functions
from sqlalchemy import create_engine, text


app = FastAPI()

engine = create_engine(os.environ["DATABASE_URL"])

@app.get("/")
def home():
    return {"message": "API is working"}

@app.get("/stations")
def stations(
        station_id: str | None = None,
        limit: int = Query(default=1000, ge=1, le=10000),
):
    query = """ SELECT * 
                FROM meta_data
                WHERE (CAST(:stationid AS CHAR(5)) IS NULL OR station_id = CAST(:station_id AS CHAR(5)))
                ORDER BY observed_time DESC
                LIMIT :limit"""


    with engine.connect() as conn:
        result = conn.execute(
            text(query),
            {"station_id": station_id,
                        "limit": limit,
             },
        )
        return [dict(row) for row in result.mappings()]

@app.get("/humidity")
def humidity(
    station_id: str | None = None,
    limit: int = Query(default=1000, ge=1, le=1000),

):
    query = """ SELECT * 
                FROM humidity 
                WHERE (CAST(:station_id AS CHAR(5)) IS NULL OR station_id = CAST(:station_id AS CHAR(5)))
                ORDER BY observed_time DESC
                LIMIT :limit
            """
    with engine.connect() as conn:
        result = conn.execute(
            text(query),
            { "station_id": station_id,
                "limit": limit,
            },
            )
        return [dict(row) for row in result.mappings()]


@app.get("/temperature")
def temperature(
    station_id: str | None = None,
    limit: int = Query(default=1000, ge=1, le=10000),

    ):
    query = """ SELECT * 
                FROM temp_dry 
                WHERE (CAST(:station_id AS CHAR(5)) IS NULL OR station_id = CAST(:station_id AS CHAR(5)))
                ORDER BY observed_time DESC
                LIMIT :limit
            """
    with engine.connect() as conn:
        result = conn.execute(
            text(query),
            { "station_id": station_id,
                "limit": limit,
            },
            )
        return [dict(row) for row in result.mappings()]

@app.get("/pressure")
def pressure(
    station_id: str | None = None,
    limit: int = Query(default=1000, ge=1, le=1000),
    ):

    query = """ SELECT * 
                FROM pressure
                WHERE (CAST(:station_id AS CHAR(5)) IS NULL OR station_id = CAST(:station_id AS CHAR(5)))
                ORDER BY observed_time DESC
                LIMIT :limit OR LIMIT = int
            """
    with engine.connect() as conn:
        result = conn.execute(
            text(query),
            { "station_id": station_id,
                "limit": limit,
            },
            )
        return [dict(row) for row in result.mappings()]





