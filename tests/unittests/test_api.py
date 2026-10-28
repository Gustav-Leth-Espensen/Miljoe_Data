import unittest
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parents[2] / ".env"
load_dotenv(env_path, override=True)

if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = "postgresql://user:pass@localhost/dummy"

import api.api as api


#engine = create_engine(os.environ["DATABASE_URL"])
class TestStartAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(api.app)


    @patch("api.api.engine")
    def test_stations_returns_data(self, mock_engine):

        mock_conn = MagicMock()
        mock_result = MagicMock()

        mock_result.mappings.return_value = [
            {"Api is working": True},
        ]

        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        mock_conn.execute.return_value = mock_result

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), 1)

        self.assertEqual(response.json()['message'], "API is working")


class TestStationsAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(api.app)


    @patch("api.api.engine")
    def test_stations_returns_data(self, mock_engine):

        mock_conn = MagicMock()
        mock_result = MagicMock()

        mock_result.mappings.return_value = [
            {"id": 1, "station_id": "05435", "name": "Bøjden"}
        ]


        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        mock_conn.execute.return_value = mock_result


        response = self.client.get("/stations?station_id=05435&limit=10")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        params = mock_conn.execute.call_args.args[1]
        self.assertEqual(params["station_id"], "05435")
        self.assertEqual(params["limit"],10)


class TestHumidityAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(api.app)


    @patch("api.api.engine")
    def test_humidity_returns_data(self, mock_engine):

        mock_conn = MagicMock()
        mock_result = MagicMock()

        mock_result.mappings.return_value = [
            {"id": 1, "station_id": "06180", "percent_humidity": 75.0}
        ]


        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        mock_conn.execute.return_value = mock_result


        response = self.client.get("/humidity?station_id=06180&limit=10")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["percent_humidity"], 75.0)

        params = mock_conn.execute.call_args.args[1]
        self.assertEqual(params["station_id"], "06180")
        self.assertEqual(params["limit"],10)



class TestTemperatureAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(api.app)


    @patch("api.api.engine")
    def test_temperature_returns_data(self, mock_engine):

        mock_conn = MagicMock()
        mock_result = MagicMock()

        mock_result.mappings.return_value = [
            {"id": 1, "station_id": "06019", "temp_dry": -0.4}
        ]


        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        mock_conn.execute.return_value = mock_result


        response = self.client.get("/temperature?station_id=06019&limit=10")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["temp_dry"], -0.4)

        params = mock_conn.execute.call_args.args[1]
        self.assertEqual(params["station_id"], "06019")
        self.assertEqual(params["limit"],10)

class TestPressureAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(api.app)


    @patch("api.api.engine")
    def test_pressure_returns_data(self, mock_engine):

        mock_conn = MagicMock()
        mock_result = MagicMock()

        mock_result.mappings.return_value = [
            {"id": 1, "station_id": "06019", "pressure": 1014.1}
        ]


        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        mock_conn.execute.return_value = mock_result


        response = self.client.get("/pressure?station_id=06019&limit=10")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["pressure"], 1014.1)

        params = mock_conn.execute.call_args.args[1]
        self.assertEqual(params["station_id"], "06019")
        self.assertEqual(params["limit"],10)





if __name__ == "__main__":
    unittest.main()