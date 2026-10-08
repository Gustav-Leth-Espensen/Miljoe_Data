import unittest
from etl import transform

class TestTransformer(unittest.TestCase):

    def test_humidity_is_added(self):
        extracted_data = {
            "features": [
                {
                    "properties": {
                        "parameterId": "humidity",
                        "stationId": "06124",
                        "observed": "2018-03-18T12:30:00Z",
                        "value": 80
                    }
                },

            ]
        }

        result = transform(extracted_data)

        self.assertIn("humidity", result)
        return

    def test_humidity_stored(self):
        extracted_data = {
            "features": [
                {
                    "properties": {
                        "parameterId": "humidity",
                        "stationId": "06124",
                        "observed": "2018-03-18T12:30:00Z",
                        "value": 80
                    }
                },

            ]
        }

        result = transform(extracted_data)

        self.assertEqual(result["humidity"][0], [
            "06124",
            "2018-03-18T12:30:00Z",
            80
        ]
        )
        return

    def test_skip_missing_data(self):
        extracted_data = {
            "features": [
                {
                    "properties": {
                        "parameterId": "",
                        "stationId": "06124",
                        "observed": "2018-03-18T12:30:00Z",
                        "value": 80
                    }
                },
                {

                    "properties": {
                        "parameterId": "temp_dry",
                        "stationId": "06124",
                        "observed": "2018-03-18T12:30:00Z",
                        "value": 18
                }
            },

            ]
        }

        result = transform(extracted_data)

        self.assertEqual(result["temp_dry"][0], [
            "06124",
            "2018-03-18T12:30:00Z",
            18
        ]
        )
        return