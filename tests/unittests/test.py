import unittest
from unittest.mock import patch, Mock
import etls.etl as etl
import os
import etls.meta_data as meta
from etls import get_local_api


class TestETLTransformer(unittest.TestCase):

    def test_humidity_is_added(self):
        extracted_data = {
            "features": [
                {
                    'id': 14,
                    "properties": {
                        "parameterId": "humidity",
                        "stationId": "06124",
                        "observed": "2018-03-18T12:30:00Z",
                        "value": 80
                    }
                },

            ]
        }

        result = etl.transform(extracted_data)

        self.assertIn("humidity", result)
        return

    def test_humidity_stored(self):
        extracted_data = {
            "features": [
                {
                    'id' : 25,
                    "properties": {
                        "parameterId": "humidity",
                        "stationId": "06124",
                        "observed": "2018-03-18T12:30:00Z",
                        "value": 80
                    }
                },

            ]
        }

        result = etl.transform(extracted_data)
        self.assertEqual(result["humidity"][0], [25,
            "06124",
            "2018-03-18T12:30:00Z",
            80
        ]
        )
        return

    def test_value_0(self):
        extracted_data = {
            "features": [
                {
                    'id':'98845022-d7d1-1c18-a24f-3297f295634a',
                    "properties": {
                        "parameterId": "humidity",
                        "stationId": "06124",
                        "observed": "2018-03-18T12:30:00Z",
                        "value": 0
                    }
                },

            ]
        }

        result = etl.transform(extracted_data)
        self.assertEqual(result["humidity"][0], ['98845022-d7d1-1c18-a24f-3297f295634a',
            "06124",
            "2018-03-18T12:30:00Z",
            0
        ]
        )
        return



    def test_no_parameter(self):
        extracted_data = {
            "features": [
                {
                    'id': 1500,
                    "properties": {
                        "parameterId": "",
                        "stationId": "06124",
                        "observed": "2018-03-18T12:30:00Z",
                        "value": 80
                    }
                },

            ]
        }
        with self.assertRaises(ValueError) as context:
            etl.transform(extracted_data)
        self.assertIn("One of parameters not found.", str(context.exception))
        return



    def test_no_value(self):
        extracted_data = {
            "features": [
                {
                    'id':2500,
                    "properties": {
                        "parameterId": "humidity",
                        "stationId": "06124",
                        "observed": "2018-03-18T12:30:00Z",
                        "value": ""
                    }
                },

            ]
        }

        with self.assertRaises(ValueError) as context:
            etl.transform(extracted_data)
        self.assertIn("One of parameters not found.", str(context.exception))
        return

    def test_no_stationId(self):
        extracted_data = {
            "features": [
                {
                    'id': 5000,
                    "properties": {
                        "parameterId": "humidity",
                        "stationId": "",
                        "observed": "2018-03-18T12:30:00Z",
                        "value": 0.0
                    }
                },

            ]
        }

        with self.assertRaises(ValueError) as context:
            etl.transform(extracted_data)
        self.assertIn("One of parameters not found.", str(context.exception))
        return

    def test_no_observed_time(self):
        extracted_data = {
            "features": [
                {
                    'id': 7000,
                    "properties": {
                        "parameterId": "humidity",
                        "stationId": "06124",
                        "observed": "",
                        "value": 0.0
                    }
                },

            ]
        }

        with self.assertRaises(ValueError) as context:
            etl.transform(extracted_data)
        self.assertIn("One of parameters not found.", str(context.exception))
        return


    def test_standard_input(self):
        one_observation = {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'id': '2b55028a-aa90-6af2-3692-3a0855de24eb',
                                                        'geometry': {'type': 'Point',
                                                                     'coordinates': [10.1074, 57.5705]},
                                                        'properties': {'parameterId': 'precip_dur_past10min',
                                                                       'created': '2025-08-11T10:06:24.225346Z',
                                                                       'value': 0, 'observed': '2018-03-18T12:30:00Z',
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

        self.assertEqual(etl.transform(one_observation), {'precip_dur_past10min': [['2b55028a-aa90-6af2-3692-3a0855de24eb','05005', '2018-03-18T12:30:00Z', 0.0]]})
        self.assertEqual(etl.transform(two_observations), {'precip_dur_past10min': [['2b55028a-aa90-6af2-3692-3a0855de24eb','05005', '2018-03-18T12:30:00Z', 0.0]], 'precip_past10min': [['98845022-d7d1-1c18-a24f-3297f295634a','05005', '2018-03-18T12:30:00Z', 0.0]]})
        return

    def test_non_input(self):
        test_dict = {"greeting": "Hello, world!"}
        empty_dict = {}

        with self.assertRaises(KeyError) as context:
            etl.transform(test_dict)
        self.assertIn("Missing key in data.", str(context.exception))

        with self.assertRaises(ValueError) as context:
            etl.transform(empty_dict)
        self.assertIn("Trying to transform an empty dictionary.", str(context.exception))
        return

    def test_transform_empty_data(self):
        extracted_data = {
            "features": []
        }
        result = etl.transform(extracted_data)
        self.assertEqual(result, {})

    def test_dif_parmId_inputs(self):
        self.assertEqual(etl.transform({"features":[{'id': 12, 'properties': {'parameterId': 'temp_dry', 'value': -11.7,'observed': '2003-01-27T10:00:00Z', 'stationId': '04224'}},
                        {'id': 14, 'properties': {'parameterId': 'radia_glob_past1h', 'value': 40.0, 'observed': '2003-01-27T10:00:00Z','stationId': '06068'}}]})
                        ,{'temp_dry': [[12,'04224', '2003-01-27T10:00:00Z', -11.7]], 'radia_glob_past1h': [[14, '06068', '2003-01-27T10:00:00Z', 40.0]]})
    def test_same_parmId_inputs(self):
        self.assertEqual(etl.transform({"features":[{'id': 12,'properties': {'parameterId': 'temp_dry', 'value': -11.7, 'observed': '2003-01-27T10:00:00Z', 'stationId': '04224'}},
                        {'id': 14, 'properties': { 'parameterId': 'temp_dry', 'value': 40.0, 'observed': '2003-01-27T10:00:00Z','stationId': '06068'}}]})
                        ,{'temp_dry': [[12,'04224', '2003-01-27T10:00:00Z',-11.7],[14, '06068','2003-01-27T10:00:00Z',40.0]]})
    def test_notrel_data(self):
        self.assertEqual(etl.transform({"features":[{'id': 12,'properties': {'parameterId': 'temp_dry', 'created': '2025-08-25T17:00:16.827145Z', 'value': -11.7, 'observed': '2003-01-27T10:00:00Z', 'stationId': '04224'}},
                                {'id': 14,'properties': {'parameterId': 'temp_dry', 'created': '2025-08-25T17:00:16.827145Z', 'value': 40.0, 'observed':'2003-01-27T10:00:00Z','stationId': '06068',}}]})
                                ,{'temp_dry': [[12,'04224', '2003-01-27T10:00:00Z',-11.7],[14,'06068','2003-01-27T10:00:00Z',40.0]]})



class TestETLExtractor(unittest.TestCase):

    def test_random_datetime(self):
        temp_datetime = "2050102!"

        with self.assertRaises(ValueError) as context:
            etl.extract_weather_data_from_dmi(temp_datetime,1,0, "humidity" )
        self.assertIn("Input in extract outside of API scope.", str(context.exception))
        return

    def test_limit(self):
        temp_datetime = "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
        with self.assertRaises(ValueError) as context:
            etl.extract_weather_data_from_dmi(temp_datetime,300001,0,"humidity" )
        self.assertIn("Input in extract outside of API scope.", str(context.exception))

        return

    def test_offset(self):
        temp_datetime = "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
        with self.assertRaises(ValueError) as context:
            etl.extract_weather_data_from_dmi(temp_datetime,1,100000000,"humidity" )
        self.assertIn("Input in extract outside of API scope.", str(context.exception))
        return

    def test_parameter_id(self):
        temp_datetime = "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
        with self.assertRaises(ValueError) as context:
            etl.extract_weather_data_from_dmi(temp_datetime,1,0,"523flksatgq" )
        self.assertIn("Input in extract outside of API scope.", str(context.exception))
        return


    def test_bbox(self):
        temp_datetime = "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
        with self.assertRaises(ValueError) as context:
            etl.extract_weather_data_from_dmi(temp_datetime,100,0,"humidity", bbox = "1000,12,1500,58")
        self.assertIn("Input in extract outside of API scope.", str(context.exception))
        return

    @patch("etls.etl.requests.get") #erstatter request.get med en mock
    def test_extract_from_dmi(self, mock_get): #testen kontrollerer at det forventede json data returneres
        mock_get.return_value.ok = True #simulerer vellykket api kald
        mock_get.return_value.json.return_value = {"features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [10.1074, 57.5705]
                    },
                    "properties": {
                        "parameterId": "humidity",
                        "stationId": "06124",
                        "observed": "2018-03-18T12:30:00Z",
                        "created": "2018-03-18T12:31:00Z",
                        "value": 80
                    }
                }

            ]
        }

        result = etl.extract_weather_data_from_dmi("2018-02-12T00:00:00Z/2018-03-18T12:30:00Z", 1000, 0, "humidity")

        self.assertIn("features", result) #kontrollerer at features findes i resultatet
        self.assertEqual(len(result["features"]),1) #tjekker antallet af observationer
        properties = result["features"][0]["properties"]
        self.assertEqual(properties["parameterId"], "humidity") #tjekker at parameterid er humidity
        self.assertEqual(properties["stationId"], "06124")
        self.assertEqual(properties["created"], "2018-03-18T12:31:00Z")
        self.assertEqual(properties["observed"], "2018-03-18T12:30:00Z")
        self.assertEqual(properties["value"], 80) #Tjekker værdi af en observation
        return

class TestETLLoad(unittest.TestCase):

    @patch("etls.etl.psycopg.connect")
    def test_open_connection(self, mock_connect): #tester

        mock_connection = Mock()
        mock_connect.return_value = mock_connection #mock_connect return value skal være lig mock_connection
        result = etl.open_connection()
        url = str(os.getenv('DATABASE_URL'))
        mock_connect.assert_called_once_with(
            url) #kotrollerer at mock connect kaldes en gang med den definerede streng

        self.assertEqual(result, mock_connection) #kontrollerer at etl.open_connection returnerer det samme objekt som mock_connectiong


    def test_close_connection(self): #tjekker at close forsøger at lukke forbindelse og cursor

        cursor = Mock() # mock objekt
        conn = Mock() #mock objekt

        etl.close_connection(conn, cursor) #kalder funktion med mock objekter
        conn.close.assert_called_once()
        cursor.close.assert_called_once()

    @patch("etls.etl.open_connection")
    def test_load_humidity(self, mock_open_connection): #kontrolere om humidity data sendes til cursoren
        mock_conn = Mock() #mock objekt
        mock_cursor = Mock() #mock object

        mock_open_connection.return_value = mock_conn #mock_open_connection skal returnere mock_conn
        mock_conn.cursor.return_value = mock_cursor #mock_conn.cursor skal returnere mock cursor

        mock_transformed_data = {
            "humidity": [
                ["06124", "2018-03-18T12:30:00Z", 50, ],
                ["06126", "2018-03-18T12:30:00Z", 70, ],

            ]
                }

        etl.load_humidity(mock_transformed_data) #kører load med mock data

        mock_cursor.executemany.assert_called_once()
        #kontrollerer at de data der er sendt til executemany() er de samme som mock_transformed_data
        # call_args tager argumenter som sidste mock blev kaldet med, her er det insert_query og args[1] er vores mock data
        self.assertEqual(mock_cursor.executemany.call_args.args[1],
            mock_transformed_data["humidity"])

        self.assertEqual(mock_cursor.executemany.call_args.args[0],
                         """
                   INSERT INTO dmi_humidity(observation_id, station_id, observed_time, percent_humidity)
                   VALUES(%s, %s, %s, %s)
                   ON CONFLICT (observation_id) DO NOTHING;
                   """) #Antallet af mellemrum er vigtigt, do not touch!!


        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


    @patch("etls.etl.open_connection")
    def test_load_temp_dry(self, mock_open_connection):
        mock_conn = Mock()
        mock_cursor = Mock()

        mock_open_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_transformed_data = {
            "temp_dry": [
                ["06124", "2018-03-18T12:30:00Z", 15, ],
                ["06126", "2018-03-18T12:30:00Z", 20, ],

            ]
                }

        etl.load_temp_dry(mock_transformed_data)

        mock_cursor.executemany.assert_called_once()
        self.assertEqual(mock_cursor.executemany.call_args.args[1],
            mock_transformed_data["temp_dry"])

        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("etls.etl.open_connection")
    def test_load_pressure(self, mock_open_connection):
        mock_conn = Mock()
        mock_cursor = Mock()

        mock_open_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_transformed_data = {
            "pressure": [
                ["06124", "2018-03-18T12:30:00Z", 50, ],
                ["06126", "2018-03-18T12:30:00Z", 70, ],

            ]
        }

        etl.load_pressure(mock_transformed_data)

        mock_cursor.executemany.assert_called_once()

        self.assertEqual(mock_cursor.executemany.call_args.args[1],
                         mock_transformed_data["pressure"])

        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()




class TestMetaExtract(unittest.TestCase):
    def test_extract_bbox(self):
        with self.assertRaises(ValueError) as context:
            meta.extract_meta_data(limit = 1, station_id="", bbox = "10000, 12, 02, 15")
        self.assertIn("Input in extract outside of API scope.", str(context.exception))
        return



    @patch("etls.meta_data.requests.get") #erstatter request.get med en mock
    def test_extract_meta_from_dmi(self, mock_get): #testen kontrollerer at det forventede json data returneres
        mock_get.return_value.ok = True #simulerer vellykket api kald
        mock_get.return_value.json.return_value = {"features": [
    {
      "type": "Feature",
      "id": "92ca41f8-904f-0aaf-816a-06eb57b21332",
      "geometry": {
        "type": "Point",
        "coordinates": [10.3305, 55.4749]
      },
      "properties": {
        "owner": "DMI",
        "country": "DNK",
        "operationFrom": "2018-11-26T00:00:00Z",
        "parameterId": [
          "precip_dur_past10min",
          "precip_dur_past1h",
          "precip_past10min",
          "precip_past1h",
          "precip_past1min"
        ],
        "created": "2026-10-14T10:51:09Z",
        "validFrom": "2018-11-26T00:00:00Z",
        "type": "Pluvio",
        "stationHeight": 14,
        "regionId": "6",
        "name": "H. C. Andersen Airport",
        "stationId": "05408",
        "validTo": "2025-10-30T11:31:59Z",
        "status": "Active"
      }
    }
    ]}

        result = meta.extract_meta_data(limit=10, station_id="")

        self.assertIn("features", result) #kontrollerer at features findes i resultatet
        self.assertEqual(len(result["features"]),1) #tjekker antallet af observationer
        properties = result["features"][0]["properties"]
        self.assertEqual(properties["name"], "H. C. Andersen Airport") #tjekker at parameterid er humidity
        self.assertEqual(properties["stationId"], "05408")

        coordinates = result["features"][0]["geometry"]["coordinates"]
        self.assertEqual(coordinates[0], 10.3305)
        self.assertEqual(coordinates[1], 55.4749)
        return


class TestMetaTransform(unittest.TestCase):
    def test_clean_input(self):
        data = {"features": [
            {
                "geometry": {
                    "type": "Point",
                    "coordinates": [10.3305, 55.4749]
                },
                "properties": {
                    "name": "H. C. Andersen Airport",
                    "stationId": "05408",
                }
            }
        ]}
        transformed_data = meta.transform_meta_data(data)
        self.assertEqual(transformed_data, [["05408", "H. C. Andersen Airport", 10.3305, 55.4749]])
        return

    def test_multiple_inputs(self):
        data = {"features": [
            {
              "geometry": {
                "type": "Point",
                "coordinates": [10.3305, 55.4749]
              },
              "properties": {
                "name": "H. C. Andersen Airport",
                "stationId": "05408",
              }
            },
            {
              "geometry": {
                "type": "Point",
                "coordinates": [8.1257, 56.4702]
              },
              "properties": {
                "name": "FJALTRING",
                "stationId": "24025",
              }
            }]}
        transformed_data = meta.transform_meta_data(data)
        self.assertEqual(transformed_data, [["05408", "H. C. Andersen Airport", 10.3305, 55.4749], ["24025", "FJALTRING", 8.1257, 56.4702]])
        return

    def test_standard_input(self):
        data = {
          "type": "FeatureCollection",
          "features": [
            {
              "type": "Feature",
              "id": "92ca41f8-904f-0aaf-816a-06eb57b21332",
              "geometry": {
                "type": "Point",
                "coordinates": [10.3305, 55.4749]
              },
              "properties": {
                "owner": "DMI",
                "country": "DNK",
                "anemometerHeight": None,
                "wmoCountryCode": None,
                "operationFrom": "2018-11-26T00:00:00Z",
                "parameterId": [
                  "precip_dur_past10min",
                  "precip_dur_past1h",
                  "precip_past10min",
                  "precip_past1h",
                  "precip_past1min"
                ],
                "created": "2026-10-14T10:51:09Z",
                "barometerHeight": None,
                "validFrom": "2018-11-26T00:00:00Z",
                "type": "Pluvio",
                "stationHeight": 14,
                "regionId": "6",
                "name": "H. C. Andersen Airport",
                "wmoStationId": None,
                "operationTo": None,
                "updated": None,
                "stationId": "05408",
                "validTo": "2025-10-30T11:31:59Z",
                "status": "Active"
              }
            }
          ],
          "timeStamp": "2026-10-19T12:31:24Z",
          "numberReturned": 1,
          "links": [
            {
              "href": "https://opendataapi.dmi.dk/v2/metObs/collections/station/items?bbox=7,54,16,58&limit=1",
              "rel": "self",
              "type": "application/geo+json",
              "title": "This document"
            },
            {
              "href": "https://opendataapi.dmi.dk/v2/metObs/collections/station/items?bbox=7,54,16,58&limit=1&offset=1",
              "rel": "next",
              "type": "application/geo+json",
              "title": "Next set of results"
            }
          ]
        }
        transformed_data = meta.transform_meta_data(data)
        self.assertEqual(transformed_data, [["05408", "H. C. Andersen Airport", 10.3305, 55.4749]])
        return

    def test_missing_station_id(self):
        data = {"features": [
            {
                "geometry": {
                    "type": "Point",
                    "coordinates": [10.3305, 55.4749]
                },
                "properties": {
                    "name": "H. C. Andersen Airport",
                    "stationId": "",
                }
            }
        ]}
        with self.assertRaises(ValueError) as context:
            meta.transform_meta_data(data)
        self.assertIn("One of parameters not found.", str(context.exception))
        return

    def test_missing_names(self):
        data = {"features": [
            {
                "geometry": {
                    "type": "Point",
                    "coordinates": [10.3305, 55.4749]
                },
                "properties": {
                    "name": "",
                    "stationId": "05408",
                }
            }
        ]}
        with self.assertRaises(ValueError) as context:
            meta.transform_meta_data(data)
        self.assertIn("One of parameters not found.", str(context.exception))
        return

    def test_missing_coordinate_long(self):
        data = {"features": [
            {
                "geometry": {
                    "type": "Point",
                    "coordinates": ["", 55.4749]
                },
                "properties": {
                    "name": "H. C. Andersen Airport",
                    "stationId": "05408",
                }
            }
        ]}
        with self.assertRaises(ValueError) as context:
            meta.transform_meta_data(data)
        self.assertIn("One of parameters not found.", str(context.exception))
        return

    def test_missing_coordinate_lat(self):
        data = {"features": [
            {
                "geometry": {
                    "type": "Point",
                    "coordinates": [10.3305, ""]
                },
                "properties": {
                    "name": "H. C. Andersen Airport",
                    "stationId": "05408",
                }
            }
        ]}
        with self.assertRaises(ValueError) as context:
            meta.transform_meta_data(data)
        self.assertIn("One of parameters not found.", str(context.exception))
        return

    def test_coordinate_long_0(self):
        data = {"features": [
            {
                "geometry": {
                    "type": "Point",
                    "coordinates": [0, 55.4749]
                },
                "properties": {
                    "name": "H. C. Andersen Airport",
                    "stationId": "05408",
                }
            }
        ]}
        transformed_data = meta.transform_meta_data(data)
        self.assertEqual(transformed_data, [["05408", "H. C. Andersen Airport", 0, 55.4749]])
        return

    def test_coordinate_lat_0(self):
        data = {"features": [
            {
                "geometry": {
                    "type": "Point",
                    "coordinates": [10.3305, 0]
                },
                "properties": {
                    "name": "H. C. Andersen Airport",
                    "stationId": "05408",
                }
            }
        ]}
        transformed_data = meta.transform_meta_data(data)
        self.assertEqual(transformed_data, [["05408", "H. C. Andersen Airport", 10.3305, 0]])
        return

    def test_wrong_input_meta_data(self):
        test_dict = {"greeting": "Hello, world!"}

        with self.assertRaises(KeyError) as context:
            meta.transform_meta_data(test_dict)
        self.assertIn("Missing key in data.", str(context.exception))
        return

class TestMetaLoad(unittest.TestCase):
    @patch("etls.meta_data.open_connection")
    def test_load_meta_data(self, mock_open_connection): #kontrolere om meta data sendes til cursor
        mock_conn = Mock() #mock objekt
        mock_cursor = Mock() #mock object

        mock_open_connection.return_value = mock_conn #mock_open_connection skal returnere mock_conn
        mock_conn.cursor.return_value = mock_cursor #mock_conn.cursor skal returnere mock cursor

        mock_transformed_data = ["05408", "H. C. Andersen Airport", 10.3305, 55.0522]

        meta.load_meta_data(mock_transformed_data) #kører load med mock data

        mock_cursor.executemany.assert_called_once()
        #kontrollerer at de data der er sendt til executemany() er de samme som mock_transformed_data
        # call_args tager argumenter som sidste mock blev kaldet med, her er det insert_query og args[1] er vores mock data
        self.assertEqual(mock_cursor.executemany.call_args.args[1],mock_transformed_data)

        self.assertEqual(mock_cursor.executemany.call_args.args[0],
                         """
                   INSERT INTO meta_data(station_id, name, coordinates_longitude, coordinates_latitude)
                   VALUES(%s, %s, %s, %s);
                   """) #Antallet af mellemrum er vigtigt, do not touch!!

        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        return

class TestLocalExtract(unittest.TestCase):


    @patch("etls.get_local_api.requests.get")
    def test_local_limit_patch(self, mock_get):
        mock_get.return_value.ok = False
        mock_get.return_value.status_code = 400

        with self.assertRaises(ValueError) as context:
            get_local_api.extract_data_from_local_api()

        self.assertIn("Input in extract outside of API scope.", str(context.exception))

        return

    def test_local_limit(self):
        get_local_api.URL = "https://herodot.spac.dk/api/v1/observations?limit=5001"

        with self.assertRaises(ValueError) as context:
            get_local_api.extract_data_from_local_api()
        self.assertIn("Input in extract outside of API scope.", str(context.exception))

        return


    #
    # def test_offset(self):
    #     temp_datetime = "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
    #     with self.assertRaises(ValueError) as context:
    #         etl.extract_weather_data_from_dmi(temp_datetime, 1, 100000000, "humidity")
    #     self.assertIn("Input in extract outside of API scope.", str(context.exception))
    #     return
    #
    # def test_parameter_id(self):
    #     temp_datetime = "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
    #     with self.assertRaises(ValueError) as context:
    #         etl.extract_weather_data_from_dmi(temp_datetime, 1, 0, "523flksatgq")
    #     self.assertIn("Input in extract outside of API scope.", str(context.exception))
    #     return
    #
    # def test_bbox(self):
    #     temp_datetime = "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
    #     with self.assertRaises(ValueError) as context:
    #         etl.extract_weather_data_from_dmi(temp_datetime, 100, 0, "humidity", bbox="1000,12,1500,58")
    #     self.assertIn("Input in extract outside of API scope.", str(context.exception))
    #     return

    @patch("etls.get_local_api.requests.get")
    def test_extract_from_local_api(self, mock_get):  # testen kontrollerer at det forventede json data returneres
        mock_get.return_value.ok = True  # simulerer vellykket api kald
        mock_get.return_value.json.return_value = {"observations": [
            {'observationId': 'f7064fe3-0e3c-4d0d-81c6-620213ae5dc2',
             'nodeId': '2c47284d-777b-44f0-bdeb-3d442f6a31b1',
             'instrumentId': 'BME280:75E99D2B',
             'instrumentModel': 'BME280',
             'sensor': 'pressure',
             'readingId': 'c3e7eecf-1ff8-4323-b849-625e894968f3',
             'value': 101954.6171875,
             'timestamp': '2026-10-28T12:24:33.408625Z'}
        ]
        }

        result = get_local_api.extract_data_from_local_api()

        self.assertIn("observations", result)  # kontrollerer at features findes i resultatet
        self.assertEqual(len(result["observations"]), 1)  # tjekker antallet af observationer
        parameters = result["observations"][0]
        self.assertEqual(parameters["observationId"], "f7064fe3-0e3c-4d0d-81c6-620213ae5dc2")
        self.assertEqual(parameters["nodeId"], "2c47284d-777b-44f0-bdeb-3d442f6a31b1") # tjekker at parameterid er humidity
        self.assertEqual(parameters["instrumentId"], "BME280:75E99D2B")
        self.assertEqual(parameters["instrumentModel"], "BME280")
        self.assertEqual(parameters["sensor"], "pressure")
        self.assertEqual(parameters["timestamp"], "2026-10-28T12:24:33.408625Z")
        self.assertEqual(parameters["value"], 101954.6171875)  # Tjekker værdi af en observation
        return

#class TestLocalETLTransformer(unittest.TestCase):
    #
    # def test_local_pressure_is_added(self):
    #     extracted_data = {
    #             "observations": [
    #             {'observationId': 'f7064fe3-0e3c-4d0d-81c6-620213ae5dc2',
    #              'nodeId': '2c47284d-777b-44f0-bdeb-3d442f6a31b1',
    #              'instrumentId': 'BME280:75E99D2B',
    #              'instrumentModel': 'BME280',
    #              'sensor': 'pressure',
    #              'readingId': 'c3e7eecf-1ff8-4323-b849-625e894968f3',
    #              'value': 101954.6171875,
    #              'timestamp': '2026-10-28T12:24:33.408625Z'}
    #         ]
    #         }
    #
    #     result = get_local_api.transform_local_data(extracted_data)
    #
    #     self.assertIn("pressure", result)
    #     return

        # def test_humidity_stored(self):
        #     extracted_data = {
        #         "features": [
        #             {
        #                 "properties": {
        #                     "parameterId": "humidity",
        #                     "stationId": "06124",
        #                     "observed": "2018-03-18T12:30:00Z",
        #                     "value": 80
        #                 }
        #             },
        #
        #         ]
        #     }
        #
        #     result = etl.transform(extracted_data)
        #     self.assertEqual(result["humidity"][0], [
        #         "06124",
        #         "2018-03-18T12:30:00Z",
        #         80
        #     ]
        #                      )
        #     return
        #
        # def test_value_0(self):
        #     extracted_data = {
        #         "features": [
        #             {
        #                 "properties": {
        #                     "parameterId": "humidity",
        #                     "stationId": "06124",
        #                     "observed": "2018-03-18T12:30:00Z",
        #                     "value": 0
        #                 }
        #             },
        #
        #         ]
        #     }
        #
        #     result = etl.transform(extracted_data)
        #     self.assertEqual(result["humidity"][0], [
        #         "06124",
        #         "2018-03-18T12:30:00Z",
        #         0
        #     ]
        #                      )
        #     return
        #
        # def test_no_parameter(self):
        #     extracted_data = {
        #         "features": [
        #             {
        #                 "properties": {
        #                     "parameterId": "",
        #                     "stationId": "06124",
        #                     "observed": "2018-03-18T12:30:00Z",
        #                     "value": 80
        #                 }
        #             },
        #
        #         ]
        #     }
        #     with self.assertRaises(ValueError) as context:
        #         etl.transform(extracted_data)
        #     self.assertIn("One of parameters not found.", str(context.exception))
        #     return
        #
        # def test_no_value(self):
        #     extracted_data = {
        #         "features": [
        #             {
        #                 "properties": {
        #                     "parameterId": "humidity",
        #                     "stationId": "06124",
        #                     "observed": "2018-03-18T12:30:00Z",
        #                     "value": ""
        #                 }
        #             },
        #
        #         ]
        #     }
        #
        #     with self.assertRaises(ValueError) as context:
        #         etl.transform(extracted_data)
        #     self.assertIn("One of parameters not found.", str(context.exception))
        #     return
        #
        # def test_no_stationId(self):
        #     extracted_data = {
        #         "features": [
        #             {
        #                 "properties": {
        #                     "parameterId": "humidity",
        #                     "stationId": "",
        #                     "observed": "2018-03-18T12:30:00Z",
        #                     "value": 0.0
        #                 }
        #             },
        #
        #         ]
        #     }
        #
        #     with self.assertRaises(ValueError) as context:
        #         etl.transform(extracted_data)
        #     self.assertIn("One of parameters not found.", str(context.exception))
        #     return
        #
        # def test_no_observed_time(self):
        #     extracted_data = {
        #         "features": [
        #             {
        #                 "properties": {
        #                     "parameterId": "humidity",
        #                     "stationId": "06124",
        #                     "observed": "",
        #                     "value": 0.0
        #                 }
        #             },
        #
        #         ]
        #     }
        #
        #     with self.assertRaises(ValueError) as context:
        #         etl.transform(extracted_data)
        #     self.assertIn("One of parameters not found.", str(context.exception))
        #     return
        #
        # def test_standard_input(self):
        #     one_observation = {'type': 'FeatureCollection',
        #                        'features': [{'type': 'Feature', 'id': '2b55028a-aa90-6af2-3692-3a0855de24eb',
        #                                      'geometry': {'type': 'Point',
        #                                                   'coordinates': [10.1074, 57.5705]},
        #                                      'properties': {'parameterId': 'precip_dur_past10min',
        #                                                     'created': '2025-08-11T10:06:24.225346Z',
        #                                                     'value': 0, 'observed': '2018-03-18T12:30:00Z',
        #                                                     'stationId': '05005'}}],
        #                        'timeStamp': '2026-10-08T08:50:31Z', 'numberReturned': 1, 'links': [{
        #             'href': 'https://opendataapi.dmi.dk/v2/metObs/collections/observation/items?datetime=2018-02-12T00%3A00%3A00Z%2F2018-03-18T12%3A31%3A12Z&limit=1&offset=0&bbox=7%2C54%2C16%2C58',
        #             'rel': 'self',
        #             'type': 'application/geo+json',
        #             'title': 'This document'}, {
        #             'href': 'https://opendataapi.dmi.dk/v2/metObs/collections/observation/items?datetime=2018-02-12T00%3A00%3A00Z%2F2018-03-18T12%3A31%3A12Z&limit=1&bbox=7%2C54%2C16%2C58&offset=1',
        #             'rel': 'next',
        #             'type': 'application/geo+json',
        #             'title': 'Next set of results'}]}
        #     two_observations = {'type': 'FeatureCollection',
        #                         'features': [{'type': 'Feature', 'id': '2b55028a-aa90-6af2-3692-3a0855de24eb',
        #                                       'geometry': {'type': 'Point',
        #                                                    'coordinates': [10.1074, 57.5705]},
        #                                       'properties': {'parameterId': 'precip_dur_past10min',
        #                                                      'created': '2025-08-11T10:06:24.225346Z',
        #                                                      'value': 0.0, 'observed': '2018-03-18T12:30:00Z',
        #                                                      'stationId': '05005'}},
        #                                      {'type': 'Feature', 'id': '98845022-d7d1-1c18-a24f-3297f295634a',
        #                                       'geometry': {'type': 'Point',
        #                                                    'coordinates': [10.1074, 57.5705]},
        #                                       'properties': {'parameterId': 'precip_past10min',
        #                                                      'created': '2025-08-11T10:06:23.343744Z',
        #                                                      'value': 0.0, 'observed': '2018-03-18T12:30:00Z',
        #                                                      'stationId': '05005'}}],
        #                         'timeStamp': '2026-10-08T08:47:36Z', 'numberReturned': 2, 'links': [{
        #             'href': 'https://opendataapi.dmi.dk/v2/metObs/collections/observation/items?datetime=2018-02-12T00%3A00%3A00Z%2F2018-03-18T12%3A31%3A12Z&limit=2&offset=0&bbox=7%2C54%2C16%2C58',
        #             'rel': 'self',
        #             'type': 'application/geo+json',
        #             'title': 'This document'}, {
        #             'href': 'https://opendataapi.dmi.dk/v2/metObs/collections/observation/items?datetime=2018-02-12T00%3A00%3A00Z%2F2018-03-18T12%3A31%3A12Z&limit=2&bbox=7%2C54%2C16%2C58&offset=2',
        #             'rel': 'next',
        #             'type': 'application/geo+json',
        #             'title': 'Next set of results'}]}
        #
        #     self.assertEqual(etl.transform(one_observation),
        #                      {'precip_dur_past10min': [['05005', '2018-03-18T12:30:00Z', 0.0]]})
        #     self.assertEqual(etl.transform(two_observations),
        #                      {'precip_dur_past10min': [['05005', '2018-03-18T12:30:00Z', 0.0]],
        #                       'precip_past10min': [['05005', '2018-03-18T12:30:00Z', 0.0]]})
        #     return
        #
        # def test_non_input(self):
        #     test_dict = {"greeting": "Hello, world!"}
        #     empty_dict = {}
        #
        #     with self.assertRaises(KeyError) as context:
        #         etl.transform(test_dict)
        #     self.assertIn("Missing key in data.", str(context.exception))
        #
        #     with self.assertRaises(ValueError) as context:
        #         etl.transform(empty_dict)
        #     self.assertIn("Trying to transform an empty dictionary.", str(context.exception))
        #     return
        #
        # def test_transform_empty_data(self):
        #     extracted_data = {
        #         "features": []
        #     }
        #     result = etl.transform(extracted_data)
        #     self.assertEqual(result, {})
        #
        # def test_dif_parmId_inputs(self):
        #     self.assertEqual(etl.transform({"features": [{'properties': {'parameterId': 'temp_dry', 'value': -11.7,
        #                                                                  'observed': '2003-01-27T10:00:00Z',
        #                                                                  'stationId': '04224'}},
        #                                                  {'properties': {'parameterId': 'radia_glob_past1h',
        #                                                                  'value': 40.0,
        #                                                                  'observed': '2003-01-27T10:00:00Z',
        #                                                                  'stationId': '06068'}}]})
        #                      , {'temp_dry': [['04224', '2003-01-27T10:00:00Z', -11.7]],
        #                         'radia_glob_past1h': [['06068', '2003-01-27T10:00:00Z', 40.0]]})
        #
        # def test_same_parmId_inputs(self):
        #     self.assertEqual(etl.transform({"features": [{'properties': {'parameterId': 'temp_dry', 'value': -11.7,
        #                                                                  'observed': '2003-01-27T10:00:00Z',
        #                                                                  'stationId': '04224'}},
        #                                                  {'properties': {'parameterId': 'temp_dry', 'value': 40.0,
        #                                                                  'observed': '2003-01-27T10:00:00Z',
        #                                                                  'stationId': '06068'}}]})
        #                      , {'temp_dry': [['04224', '2003-01-27T10:00:00Z', -11.7],
        #                                      ['06068', '2003-01-27T10:00:00Z', 40.0]]})
        #
        # def test_notrel_data(self):
        #     self.assertEqual(etl.transform({"features": [{'properties': {'parameterId': 'temp_dry',
        #                                                                  'created': '2025-08-25T17:00:16.827145Z',
        #                                                                  'value': -11.7,
        #                                                                  'observed': '2003-01-27T10:00:00Z',
        #                                                                  'stationId': '04224'}},
        #                                                  {'properties': {'parameterId': 'temp_dry',
        #                                                                  'created': '2025-08-25T17:00:16.827145Z',
        #                                                                  'value': 40.0,
        #                                                                  'observed': '2003-01-27T10:00:00Z',
        #                                                                  'stationId': '06068', }}]})
        #                      , {'temp_dry': [['04224', '2003-01-27T10:00:00Z', -11.7],
        #                                      ['06068', '2003-01-27T10:00:00Z', 40.0]]})


class TestETLLoadLocal(unittest.TestCase):


    @patch("etls.etl.open_connection")
    def test_load_local_humidity_data(self, mock_open_connection): #kontrolere om humidity data sendes til cursoren
        mock_conn = Mock() #mock objekt
        mock_cursor = Mock() #mock object

        mock_open_connection.return_value = mock_conn #mock_open_connection skal returnere mock_conn
        mock_conn.cursor.return_value = mock_cursor #mock_conn.cursor skal returnere mock cursor

        mock_transformed_local_data_humidity = [["BME280", "BAL01", "2026-10-28T12:24:33.408625Z", 50, ],
                ["BME280", "BAL02", "2026-10-28T12:24:33.408625Z", 70, ],]

#instrument_model, station_id, observed_time, percent_humidity

        # mock_get.return_value.json.return_value = {"observations": [
        #     {'observationId': 'f7064fe3-0e3c-4d0d-81c6-620213ae5dc2',
        #      'nodeId': '2c47284d-777b-44f0-bdeb-3d442f6a31b1',
        #      'instrumentId': 'BME280:75E99D2B',
        #      'instrumentModel': 'BME280',
        #      'sensor': 'pressure',
        #      'readingId': 'c3e7eecf-1ff8-4323-b849-625e894968f3',
        #      'value': 101954.6171875,
        #      'timestamp': '2026-10-28T12:24:33.408625Z'}
        # ]
        # }
        get_local_api.load_local_humidity_data(mock_transformed_local_data_humidity) #kører load med mock data

        mock_cursor.executemany.assert_called_once()
        #kontrollerer at de data der er sendt til executemany() er de samme som mock_transformed_data
        # call_args tager argumenter som sidste mock blev kaldet med, her er det insert_query og args[1] er vores mock data
        self.assertEqual(mock_cursor.executemany.call_args.args[1],
            mock_transformed_local_data_humidity)

        self.assertEqual(mock_cursor.executemany.call_args.args[0],
                          """
                   INSERT INTO local_humidity(instrument_model, station_id, observed_time, percent_humidity)
                   VALUES (%s, %s, %s, %s);
                   """)


        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("etls.etl.open_connection")
    def test_load_local_pressure_data(self,mock_open_connection):  # kontrolere om humidity data sendes til cursoren
        mock_conn = Mock()  # mock objekt
        mock_cursor = Mock()  # mock object

        mock_open_connection.return_value = mock_conn  # mock_open_connection skal returnere mock_conn
        mock_conn.cursor.return_value = mock_cursor  # mock_conn.cursor skal returnere mock cursor

        mock_transformed_local_data_pressure = [["BME280", "BAL01", "2026-10-28T12:24:33.408625Z", 101954.6171875, ],
                                                    ["BME280", "BAL02", "2026-10-28T12:24:33.408625Z", 101955.6171875, ], ]

        get_local_api.load_local_pressure_data(mock_transformed_local_data_pressure)  # kører load med mock data

        mock_cursor.executemany.assert_called_once()
            # kontrollerer at de data der er sendt til executemany() er de samme som mock_transformed_data
            # call_args tager argumenter som sidste mock blev kaldet med, her er det insert_query og args[1] er vores mock data
        self.assertEqual(mock_cursor.executemany.call_args.args[1],
                            mock_transformed_local_data_pressure)

        self.assertEqual(mock_cursor.executemany.call_args.args[0],
                          """
                   INSERT INTO local_pressure(instrument_model, station_id, observed_time, pascal)
                   VALUES (%s, %s, %s, %s);
                   """)
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("etls.etl.open_connection")
    def test_load_local_temperature_data(self,mock_open_connection):  # kontrolere om humidity data sendes til cursoren
        mock_conn = Mock()  # mock objekt
        mock_cursor = Mock()  # mock object

        mock_open_connection.return_value = mock_conn  # mock_open_connection skal returnere mock_conn
        mock_conn.cursor.return_value = mock_cursor  # mock_conn.cursor skal returnere mock cursor

        mock_transformed_local_data_temperature = [["BME280", "BAL01", "2026-10-28T12:24:33.408625Z", 21, ],
                                                    ["BME280", "BAL02", "2026-10-28T12:24:33.408625Z", 19, ], ]

        get_local_api.load_local_temperature_data(mock_transformed_local_data_temperature)  # kører load med mock data

        mock_cursor.executemany.assert_called_once()
            # kontrollerer at de data der er sendt til executemany() er de samme som mock_transformed_data
            # call_args tager argumenter som sidste mock blev kaldet med, her er det insert_query og args[1] er vores mock data
        self.assertEqual(mock_cursor.executemany.call_args.args[1],
                            mock_transformed_local_data_temperature)

        self.assertEqual(mock_cursor.executemany.call_args.args[0],
                          """
                   INSERT INTO local_temperature(instrument_model, station_id, observed_time, celsius)
                   VALUES (%s, %s, %s, %s);
                   """)
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


    @patch("etls.etl.open_connection")
    def test_load_local_co2_data(self,mock_open_connection):  # kontrolere om humidity data sendes til cursoren
        mock_conn = Mock()  # mock objekt
        mock_cursor = Mock()  # mock object

        mock_open_connection.return_value = mock_conn  # mock_open_connection skal returnere mock_conn
        mock_conn.cursor.return_value = mock_cursor  # mock_conn.cursor skal returnere mock cursor

        mock_transformed_local_data_co2 = [["BME280", "BAL01", "2026-10-28T12:24:33.408625Z", 0.2, ],
                                                    ["BME280", "BAL02", "2026-10-28T12:24:33.408625Z", 0.2, ], ]

        get_local_api.load_local_co2_data(mock_transformed_local_data_co2)  # kører load med mock data

        mock_cursor.executemany.assert_called_once()
            # kontrollerer at de data der er sendt til executemany() er de samme som mock_transformed_data
            # call_args tager argumenter som sidste mock blev kaldet med, her er det insert_query og args[1] er vores mock data
        self.assertEqual(mock_cursor.executemany.call_args.args[1],
                            mock_transformed_local_data_co2)

        self.assertEqual(mock_cursor.executemany.call_args.args[0],
                          """
                   INSERT INTO local_CO2(instrument_model, station_id, observed_time, ppm)
                   VALUES (%s, %s, %s, %s);
                   """)
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("etls.etl.open_connection")
    def test_load_local_temperature(self, mock_open_connection):
        mock_conn = Mock()
        mock_cursor = Mock()

        mock_open_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_transformed_data =[
                ["BAL01", "2018-03-18T12:30:00Z", 15, ],
                ["ODE01", "2018-03-18T12:30:00Z", 20, ],

            ]


        get_local_api.load_local_temperature_data(mock_transformed_data)

        mock_cursor.executemany.assert_called_once()
        self.assertEqual(mock_cursor.executemany.call_args.args[1],
            mock_transformed_data)

        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("etls.etl.open_connection")
    def test_load_local_pressure(self, mock_open_connection):
        mock_conn = Mock()
        mock_cursor = Mock()

        mock_open_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_transformed_data =[
                ["06124", "2018-03-18T12:30:00Z", 50, ],
                ["06126", "2018-03-18T12:30:00Z", 70, ],

            ]


        get_local_api.load_local_pressure_data(mock_transformed_data)

        mock_cursor.executemany.assert_called_once()

        self.assertEqual(mock_cursor.executemany.call_args.args[1],
                         mock_transformed_data)

        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()