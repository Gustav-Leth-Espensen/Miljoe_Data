import os
from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text, bindparam, DateTime, String, Integer
from datetime import datetime


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
    query = text(""" SELECT * 
                FROM meta_data
                WHERE (:station_id IS NULL OR station_id = :station_id)
                ORDER BY id ASC 
                LIMIT :limit""").bindparams(
                    bindparam("station_id", type_=String(5)),
                    )
    with engine.connect() as conn:
        result = conn.execute(query,
    { "station_id": station_id,
                "limit": limit,
            },
    )

        return [dict(row) for row in result.mappings()]

@app.get("/humidity")
def humidity(
    station_id: str | None = None,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    limit: int = Query(default=1000, ge=1, le=10000),

):
    query = text("""SELECT *
                FROM dmi_humidity
                WHERE (:station_id IS NULL OR station_id = :station_id)
                AND (:start_datetime IS NULL OR observed_time >= :start_datetime)
                AND (:end_datetime IS NULL OR observed_time <= :end_datetime)
                ORDER BY id ASC
                LIMIT :limit
            """).bindparams(
                    bindparam("station_id", type_=String(5)),
                    bindparam("start_datetime", type_=DateTime(timezone=True)),
                    bindparam("end_datetime", type_=DateTime(timezone=True)),)
    with engine.connect() as conn:
        result = conn.execute(query,
                {"station_id": station_id,
                "start_datetime": start_datetime,
                "end_datetime": end_datetime,
                "limit": limit,
            },
            )
        return [dict(row) for row in result.mappings()]
@app.get("/local_humidity")
def local_humidity(
    station_id: str | None = None,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    limit: int = Query(default=1000, ge=1, le=10000),

):
    query = text("""SELECT *
                FROM local_humidity
                WHERE (:station_id IS NULL OR station_id = :station_id)
                AND (:start_datetime IS NULL OR observed_time >= :start_datetime)
                AND (:end_datetime IS NULL OR observed_time <= :end_datetime)
                ORDER BY id ASC
                LIMIT :limit
            """).bindparams(
                    bindparam("station_id", type_=String(5)),
                    bindparam("start_datetime", type_=DateTime(timezone=True)),
                    bindparam("end_datetime", type_=DateTime(timezone=True)),)
    with engine.connect() as conn:
        result = conn.execute(query,
                {"station_id": station_id,
                "start_datetime": start_datetime,
                "end_datetime": end_datetime,
                "limit": limit,
            },
            )
        return [dict(row) for row in result.mappings()]

@app.get("/temperature")
def temperature(
    station_id: str | None = None,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    limit: int = Query(default=1000, ge=1, le=10000),

    ):
    query = text(""" SELECT * 
                FROM dmi_temp_dry 
                WHERE (:station_id IS NULL OR station_id = :station_id)
                AND (:start_datetime IS NULL OR observed_time >= :start_datetime)
                AND (:end_datetime IS NULL OR observed_time <= :end_datetime)
                ORDER BY id ASC
                LIMIT :limit
            """).bindparams(
                    bindparam("station_id", type_=String(5)),
                    bindparam("start_datetime", type_=DateTime(timezone=True)),
                    bindparam("end_datetime", type_=DateTime(timezone=True)),)
    with engine.connect() as conn:
        result = conn.execute(query,
                {"station_id": station_id,
                "start_datetime": start_datetime,
                "end_datetime": end_datetime,
                "limit": limit,
            },
            )
        return [dict(row) for row in result.mappings()]

@app.get("/local_temperature")
def local_temperature(
    station_id: str | None = None,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    limit: int = Query(default=1000, ge=1, le=10000),

    ):
    query = text(""" SELECT * 
                FROM local_temperature
                WHERE (:station_id IS NULL OR station_id = :station_id)
                AND (:start_datetime IS NULL OR observed_time >= :start_datetime)
                AND (:end_datetime IS NULL OR observed_time <= :end_datetime)
                ORDER BY id ASC
                LIMIT :limit
            """).bindparams(
                    bindparam("station_id", type_=String(5)),
                    bindparam("start_datetime", type_=DateTime(timezone=True)),
                    bindparam("end_datetime", type_=DateTime(timezone=True)),)
    with engine.connect() as conn:
        result = conn.execute(query,
                {"station_id": station_id,
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

    query = text("""SELECT * 
                FROM pressure
                WHERE (:station_id IS NULL OR station_id = :station_id)
                AND (:start_datetime IS NULL OR observed_time >= :start_datetime)
                AND (:end_datetime IS NULL OR observed_time <= :end_datetime)
                ORDER BY id ASC
                LIMIT :limit
            """).bindparams(
                    bindparam("station_id", type_=String(5)),
                    bindparam("start_datetime", type_=DateTime(timezone=True)),
                    bindparam("end_datetime", type_=DateTime(timezone=True)),)
    with engine.connect() as conn:
        result = conn.execute(query,
                {"station_id": station_id,
                "start_datetime": start_datetime,
                "end_datetime": end_datetime,
                "limit": limit,
            },
            )
        return [dict(row) for row in result.mappings()]

@app.get("/local_pressure")
def local_pressure(
    station_id: str | None = None,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    limit: int = Query(default=1000, ge=1, le=10000),

    ):
    query = text(""" SELECT * 
                FROM local_pressure 
                WHERE (:station_id IS NULL OR station_id = :station_id)
                AND (:start_datetime IS NULL OR observed_time >= :start_datetime)
                AND (:end_datetime IS NULL OR observed_time <= :end_datetime)
                ORDER BY id ASC
                LIMIT :limit
            """).bindparams(
                    bindparam("station_id", type_=String(5)),
                    bindparam("start_datetime", type_=DateTime(timezone=True)),
                    bindparam("end_datetime", type_=DateTime(timezone=True)),)
    with engine.connect() as conn:
        result = conn.execute(query,
                {"station_id": station_id,
                "start_datetime": start_datetime,
                "end_datetime": end_datetime,
                "limit": limit,
            },
            )
        return [dict(row) for row in result.mappings()]

@app.get("/local_CO2")
def local_co2(
    station_id: str | None = None,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    limit: int = Query(default=1000, ge=1, le=10000),

    ):
    query = text(""" SELECT * 
                FROM local_CO2 
                WHERE (:station_id IS NULL OR station_id = :station_id)
                AND (:start_datetime IS NULL OR observed_time >= :start_datetime)
                AND (:end_datetime IS NULL OR observed_time <= :end_datetime)
                ORDER BY id ASC
                LIMIT :limit
            """).bindparams(
                    bindparam("station_id", type_=String(5)),
                    bindparam("start_datetime", type_=DateTime(timezone=True)),
                    bindparam("end_datetime", type_=DateTime(timezone=True)),)
    with engine.connect() as conn:
        result = conn.execute(query,
                {"station_id": station_id,
                "start_datetime": start_datetime,
                "end_datetime": end_datetime,
                "limit": limit,
            },
            )
        return [dict(row) for row in result.mappings()]



