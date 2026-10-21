import unittest
from unittest.mock import patch, Mock
import etl
import os
import meta_data as meta

class Test_etl_Transformer(unittest.TestCase):

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

        result = etl.transform(extracted_data)

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

        result = etl.transform(extracted_data)
        self.assertEqual(result["humidity"][0], [
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
        self.assertEqual(result["humidity"][0], [
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

        self.assertEqual(etl.transform(one_observation), {'precip_dur_past10min': [['05005', '2018-03-18T12:30:00Z', 0.0]]})
        self.assertEqual(etl.transform(two_observations), {'precip_dur_past10min': [['05005', '2018-03-18T12:30:00Z', 0.0]], 'precip_past10min': [['05005', '2018-03-18T12:30:00Z', 0.0]]})
        return

    def test_non_input(self):
        test_dict = {"greeting": "Hello, world!"}
        empty_dict = {}

        with self.assertRaises(AttributeError) as context:
            etl.transform(test_dict)
        self.assertIn("Called data from wrong API, try looking at \n https://www.dmi.dk/friedata/dokumentation/meteorological-observation-api", str(context.exception))

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
        self.assertEqual(etl.transform({"features":[{'properties': {'parameterId': 'temp_dry', 'value': -11.7,'observed': '2003-01-27T10:00:00Z', 'stationId': '04224'}},
                        {'properties': {'parameterId': 'radia_glob_past1h', 'value': 40.0, 'observed': '2003-01-27T10:00:00Z','stationId': '06068'}}]})
                        ,{'temp_dry': [['04224', '2003-01-27T10:00:00Z', -11.7]], 'radia_glob_past1h': [['06068', '2003-01-27T10:00:00Z', 40.0]]})
    def test_same_parmId_inputs(self):
        self.assertEqual(etl.transform({"features":[{'properties': {'parameterId': 'temp_dry', 'value': -11.7, 'observed': '2003-01-27T10:00:00Z', 'stationId': '04224'}},
                        {'properties': {'parameterId': 'temp_dry', 'value': 40.0, 'observed': '2003-01-27T10:00:00Z','stationId': '06068'}}]})
                        ,{'temp_dry': [['04224', '2003-01-27T10:00:00Z',-11.7],['06068','2003-01-27T10:00:00Z',40.0]]})
    def test_notrel_data(self):
        self.assertEqual(etl.transform({"features":[{'properties': {'parameterId': 'temp_dry', 'created': '2025-08-25T17:00:16.827145Z', 'value': -11.7, 'observed': '2003-01-27T10:00:00Z', 'stationId': '04224'}},
                                {'properties': {'parameterId': 'temp_dry', 'created': '2025-08-25T17:00:16.827145Z', 'value': 40.0, 'observed':'2003-01-27T10:00:00Z','stationId': '06068',}}]})
                                ,{'temp_dry': [['04224', '2003-01-27T10:00:00Z',-11.7],['06068','2003-01-27T10:00:00Z',40.0]]})



class Test_etl_Extractor(unittest.TestCase):

    def test_random_datetime(self):
        temp_datetime = "2050102!"

        with self.assertRaises(ValueError) as context:
            etl.extract_from_dmi(temp_datetime,1,0 )
        self.assertIn("Input in extract outside of API scope.", str(context.exception))
        return

    def test_limit(self):
        temp_datetime = "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
        with self.assertRaises(ValueError) as context:
            etl.extract_from_dmi(temp_datetime,300001,0 )
        self.assertIn("Input in extract outside of API scope.", str(context.exception))

        return

    def test_offset(self):
        temp_datetime = "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
        with self.assertRaises(ValueError) as context:
            etl.extract_from_dmi(temp_datetime,1,100000000 )
        self.assertIn("Input in extract outside of API scope.", str(context.exception))
        return


    def test_bbox(self):
        temp_datetime = "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z"
        with self.assertRaises(ValueError) as context:
            etl.extract_from_dmi(temp_datetime,100,0, bbox = "1000,12,1500,58" )
        self.assertIn("Input in extract outside of API scope.", str(context.exception))
        return

    @patch("etl.requests.get") #erstatter request.get med en mock
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

        result = etl.extract_from_dmi("2018-02-12T00:00:00Z/2018-03-18T12:30:00Z", 1000, 0)

        self.assertIn("features", result) #kontrollerer at features findes i resultatet
        self.assertEqual(len(result["features"]),1) #tjekker antallet af observationer
        properties = result["features"][0]["properties"]
        self.assertEqual(properties["parameterId"], "humidity") #tjekker at parameterid er humidity
        self.assertEqual(properties["stationId"], "06124")
        self.assertEqual(properties["created"], "2018-03-18T12:31:00Z")
        self.assertEqual(properties["observed"], "2018-03-18T12:30:00Z")
        self.assertEqual(properties["value"], 80) #Tjekker værdi af en observation
        return

class Test_etl_Load(unittest.TestCase):

    @patch("etl.psycopg.connect")
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

    @patch("etl.open_connection")
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
            mock_transformed_data["humidity"]) #

        self.assertEqual(mock_cursor.executemany.call_args.args[0],
                         """
                   INSERT INTO humidity(station_id, observed_time, percent_humidity)
                   VALUES(%s, %s, %s);
                   """) #Antallet af mellemrum er vigtigt, do not touch!!


        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


    @patch("etl.open_connection")
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

    @patch("etl.open_connection")
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




class Test_meta_extract(unittest.TestCase):
    def test_extract_bbox(self):
        with self.assertRaises(ValueError) as context:
            meta.extract_meta_data(bbox = "10000, 12, 02, 15")
        self.assertIn("Input in extract outside of API scope.", str(context.exception))
        return



    @patch("meta_data.requests.get") #erstatter request.get med en mock
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

        result = meta.extract_meta_data()

        self.assertIn("features", result) #kontrollerer at features findes i resultatet
        self.assertEqual(len(result["features"]),1) #tjekker antallet af observationer
        properties = result["features"][0]["properties"]
        self.assertEqual(properties["name"], "H. C. Andersen Airport") #tjekker at parameterid er humidity
        self.assertEqual(properties["stationId"], "05408")

        coordinates = result["features"][0]["geometry"]["coordinates"]
        self.assertEqual(coordinates[0], 10.3305)
        self.assertEqual(coordinates[1], 55.4749)
        return


class Test_meta_transform(unittest.TestCase):
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

    def test_missing_stationid(self):
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



class Test_meta_load(unittest.TestCase):
    @patch("meta_data.open_connection")
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




#Mangler at teste:





if __name__ == '__main__':
    unittest.main()