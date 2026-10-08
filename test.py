import unittest
from etl import transform
from etl import extract_from_dmi


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

    def test_standard_input(self):
        one_observation = {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'id': '2b55028a-aa90-6af2-3692-3a0855de24eb',
                                                        'geometry': {'type': 'Point',
                                                                     'coordinates': [10.1074, 57.5705]},
                                                        'properties': {'parameterId': 'precip_dur_past10min',
                                                                       'created': '2025-08-11T10:06:24.225346Z',
                                                                       'value': 0.0, 'observed': '2018-03-18T12:30:00Z',
                                                                       'stationId': '05005'}}],
             'timeStamp': '2026-10-08T08:50:31Z', 'numberReturned': 1, 'links': [{
                                                                                     'href': 'https://opendataapi.dmi.dk/v2/metObs/collections/observation/items?datetime=2018-02-12T00%3A00%3A00Z%2F2018-03-18T12%3A31%3A12Z&limit=1&offset=0&bbox=7%2C54%2C16%2C58',
                                                                                     'rel': 'self',
                                                                                     'type': 'application/geo+json',
                                                                                     'title': 'This document'}, {
                                                                                     'href': 'https://opendataapi.dmi.dk/v2/metObs/collections/observation/items?datetime=2018-02-12T00%3A00%3A00Z%2F2018-03-18T12%3A31%3A12Z&limit=1&bbox=7%2C54%2C16%2C58&offset=1',
                                                                                     'rel': 'next',
                                                                                     'type': 'application/geo+json',
                                                                                     'title': 'Next set of results'}]}
        two_observations = {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'id': '2b55028a-aa90-6af2-3692-3a0855de24eb',
                                                        'geometry': {'type': 'Point',
                                                                     'coordinates': [10.1074, 57.5705]},
                                                        'properties': {'parameterId': 'precip_dur_past10min',
                                                                       'created': '2025-08-11T10:06:24.225346Z',
                                                                       'value': 0.0, 'observed': '2018-03-18T12:30:00Z',
                                                                       'stationId': '05005'}},
                                                       {'type': 'Feature', 'id': '98845022-d7d1-1c18-a24f-3297f295634a',
                                                        'geometry': {'type': 'Point',
                                                                     'coordinates': [10.1074, 57.5705]},
                                                        'properties': {'parameterId': 'precip_past10min',
                                                                       'created': '2025-08-11T10:06:23.343744Z',
                                                                       'value': 0.0, 'observed': '2018-03-18T12:30:00Z',
                                                                       'stationId': '05005'}}],
             'timeStamp': '2026-10-08T08:47:36Z', 'numberReturned': 2, 'links': [{
                                                                                     'href': 'https://opendataapi.dmi.dk/v2/metObs/collections/observation/items?datetime=2018-02-12T00%3A00%3A00Z%2F2018-03-18T12%3A31%3A12Z&limit=2&offset=0&bbox=7%2C54%2C16%2C58',
                                                                                     'rel': 'self',
                                                                                     'type': 'application/geo+json',
                                                                                     'title': 'This document'}, {
                                                                                     'href': 'https://opendataapi.dmi.dk/v2/metObs/collections/observation/items?datetime=2018-02-12T00%3A00%3A00Z%2F2018-03-18T12%3A31%3A12Z&limit=2&bbox=7%2C54%2C16%2C58&offset=2',
                                                                                     'rel': 'next',
                                                                                     'type': 'application/geo+json',
                                                                                     'title': 'Next set of results'}]}

        self.assertEqual(transform(one_observation), {'precip_dur_past10min': [['05005', '2018-03-18T12:30:00Z', 0.0]]})
        self.assertEqual(transform(two_observations), {'precip_dur_past10min': [['05005', '2018-03-18T12:30:00Z', 0.0]], 'precip_past10min': [['05005', '2018-03-18T12:30:00Z', 0.0]]})
        return

    def test_non_input(self):
        test_dict = {"greeting": "Hello, world!"}
        empty_dict = {}
        api_fail = "Failed API response"

        self.assertEqual(transform(test_dict), "Called data from wrong API, try looking at \n https://www.dmi.dk/friedata/dokumentation/meteorological-observation-api")
        self.assertEqual(transform(empty_dict), "This is an empty dictionary")
        self.assertEqual(transform(api_fail), "Failed API response")
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

class TestExtractor(unittest.TestCase):

    def test_random_datetime(self):
        temp_datetime = "2050102!"

        function = extract_from_dmi(temp_datetime,1,0 )
        expected = "Failed API response"
        self.assertEqual(function, expected)
        return

    def test_limit(self):
        temp_datetime = "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"

        function = extract_from_dmi(temp_datetime,300001,0 )
        expected = "Failed API response"
        self.assertEqual(function, expected)
        return

    def test_offset(self):
        temp_datetime = "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"

        function = extract_from_dmi(temp_datetime,100,100000000 )
        expected = "Failed API response"
        self.assertEqual(function, expected)
        return