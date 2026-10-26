import os
from fastapi import FastAPI, Query, param_functions
from sqlalchemy import create_engine, text, bindparam, DateTime
from datetime import datetime, timezone


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
                FROM dmi_meta_data
                WHERE (CAST(:station_id AS CHAR(5)) IS NULL OR station_id = CAST(:station_id AS CHAR(5)))
                ORDER BY id ASC 
                LIMIT :limit"""
    with engine.connect() as conn:
        result = conn.execute(
            text(query),
            {"station_id": station_id,
                        "limit": limit,
             },
        )
        return [dict(row) for row in result.mappings()]

# @main_app.get("/humidity")
# def humidity(
#     station_id: str | None = None,
#     start_datetime: datetime | None = None,
#     end_datetime: datetime | None = None,
#     limit: int = Query(default=1000, ge=1, le=10000),
#
# ):
#     query = """ SELECT *
#                 FROM humidity
#                 WHERE (:station_id AS CHAR(5) IS NULL OR station_id = :station_id AS CHAR(5))
#                 AND (:start_datetime AS TIMESTAMP WITH TIME ZONE IS NULL OR observed_time >= :start_datetime AS TIMESTAMP WITH TIME ZONE)
#                 AND (:end_datetime AS TIMESTAMP WITH TIME ZONE IS NULL OR observed_time <= :end_datetime AS TIMESTAMP WITH TIME ZONE)
#                 ORDER BY id ASC
#                 LIMIT :limit
#             """).bindparams(
#                 bindparam("station_id", type_=String(5)),
#                 bindparam("start_datetime", type_=DateTime(timezone=True)),
#                 bindparam("end_datetime", type_=DateTime(timezone=True)),)
#     with engine.connect() as conn:
#         result = conn.execute(query,
#                 {"station_id": station_id,
#                 "start_datetime": start_datetime,
#                 "end_datetime": end_datetime,
#                 "limit": limit,
#             },
#             )
#         return [dict(row) for row in result.mappings()]


@app.get("/temperature")
def temperature(
    station_id: str | None = None,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    limit: int = Query(default=1000, ge=1, le=10000),

    ):
    query = """ SELECT * 
                FROM dmi_temp_dry 
                WHERE (CAST(:station_id AS CHAR(5)) IS NULL OR station_id = CAST(:station_id AS CHAR(5)))
                AND (CAST(:start_datetime AS TIMESTAMP WITH TIME ZONE) IS NULL OR observed_time >= CAST(:start_datetime AS TIMESTAMP WITH TIME ZONE)) 
                AND (CAST(:end_datetime AS TIMESTAMP WITH TIME ZONE) IS NULL OR observed_time <= CAST(:end_datetime AS TIMESTAMP WITH TIME ZONE)) 
                ORDER BY id ASC
                LIMIT :limit
            """
    with engine.connect() as conn:
        result = conn.execute(
            text(query),
            { "station_id": station_id,
              "start_datetime": start_datetime,
              "end_datetime": end_datetime,
                "limit": limit,
            },
            )
        return [dict(row) for row in result.mappings()]

@app.get("/pressure")
def pressure(
    station_id: str | None = None,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    limit: int = Query(default=1000, ge=1, le=10000),
    ):

    query = """ SELECT * 
                FROM dmi_pressure
                WHERE (CAST(:station_id AS CHAR(5)) IS NULL OR station_id = CAST(:station_id AS CHAR(5)))
                AND (CAST(:start_datetime AS TIMESTAMP WITH TIME ZONE) IS NULL OR observed_time >= CAST(:start_datetime AS TIMESTAMP WITH TIME ZONE)) 
                AND (CAST(:end_datetime AS TIMESTAMP WITH TIME ZONE) IS NULL OR observed_time <= CAST(:end_datetime AS TIMESTAMP WITH TIME ZONE)) 
                ORDER BY id ASC
                LIMIT :limit
            """
    with engine.connect() as conn:
        result = conn.execute(
            text(query),
            { "station_id": station_id,
                        "start_datetime": start_datetime,
                        "end_datetime": end_datetime,
                        "limit": limit,
            },
            )
        return [dict(row) for row in result.mappings()]





