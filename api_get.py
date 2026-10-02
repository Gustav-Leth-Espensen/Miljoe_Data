import requests


## https://opendataapi.dmi.dk/v2/metObs/collections/station/items?type=Pluvio&datetime=2020-11-01T00:00:00Z/2020-12-01T00:00:00Z&status=Active&bbox=7,54,16,58 
## Vis stations ID og hvilke målere de har



def extract_from_dmi(url: str, date_start:str, date_end:str, observations:int, offset:int, bbox = "7,54,16,58"):
    r"https://opendataapi.dmi.dk/v2/metObs/collections/observation/items?"
    nye_url = url + "datetime" + date_start

url = r"https://opendataapi.dmi.dk/v2/metObs/collections/observation/items?datetime=2018-02-12T00:00:00Z/2018-03-18T12:31:12Z&limit=1000&offset=0&bbox=7,54,16,58"

response = requests.get(url)
# if response.status_code == 200:
#     print("Succesful retrive")
data = response.json()

# print(data)
# print(data['features'][0]['geometry']['coordinates'])
# print(data['features'][0]['properties'])
# print(len(data['features']))

outer_dict = {}

# print(outer_dict.keys())
# print(outer_dict[first_dict_layer].keys())

for i in range(len(data['features'])):
    date_and_time = data['features'][i]['properties']['observed'][:-1]
    first_dict_layer = data['features'][i]['properties']['parameterId']
    second_dict_layer = data['features'][i]['properties']['stationId']
    if data['features'][i]['properties']['parameterId'] not in outer_dict.keys():
        first_dict_layer = data['features'][i]['properties']['parameterId']
        outer_dict[first_dict_layer] = {}
        if  data['features'][i]['properties']['stationId'] not in outer_dict[first_dict_layer].keys():
            second_dict_layer = data['features'][i]['properties']['stationId']
            outer_dict[first_dict_layer][second_dict_layer ] = {}
            outer_dict[first_dict_layer][second_dict_layer ][date_and_time] = data['features'][i]['properties']['value']
        else:
            outer_dict[first_dict_layer][second_dict_layer ][date_and_time] = data['features'][i]['properties']['value']
    elif data['features'][i]['properties']['stationId'] not in outer_dict[first_dict_layer].keys():
        second_dict_layer = data['features'][i]['properties']['stationId']
        outer_dict[first_dict_layer][second_dict_layer ] = {}
        outer_dict[first_dict_layer][second_dict_layer ][date_and_time] = data['features'][i]['properties']['value']
    else:
        outer_dict[first_dict_layer][second_dict_layer][date_and_time] = data['features'][i]['properties']['value']

# print(outer_dict)
print(outer_dict['pressure'])
