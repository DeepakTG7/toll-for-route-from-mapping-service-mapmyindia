# [MapmyIndia](https://www.mapmyindia.com/api/)

### Get API key to access MapmyIndia (if you have an API key skip this)
#### Step 1: Get API Key
* Create an account to access [MapmyIndia API Dashboard](https://www.mapmyindia.com/api/dashboard)
* go to [signup/login](https://www.mapmyindia.com/api/login)

#### Step 2: Getting you key
* Once you are logged in, go to [MapmyIndia API Dashboard](https://www.mapmyindia.com/api/dashboard)
* You will be presented with different keys, the key that we are looking
  for is `REST API Key for Web/Android/iOS`

With this in place, make a GET request:='https://apis.mapmyindia.com/advancedmaps/v1/{a}/route_adv/driving/{b},{c};{d},{e}?geometries=polyline&overview=full'.format(a=key,b=source_longitude,c=source_latitude,d=destination_longitude,e=destination_latitude)
### Note:
* REQUEST should include `geometries` as `polyline` and `overview` as `full`.
* Setting overview as full sends us complete route. Default value for `overview` is `simplified`, which is an approximate (smoothed) path of the resulting directions.
* MapmyIndia accepts source and destination, as semicolon seperated

```python
def get_polyline_from_mapmyindia(source_longitude, source_latitude, destination_longitude, destination_latitude, key):
    url = f'https://apis.mapmyindia.com/advancedmaps/v1/{key}/route_adv/driving/{source_longitude},{source_latitude};{destination_longitude},{destination_latitude}?geometries=polyline&overview=full'
    response = requests.get(url).json()
    if 'message' in response:
        raise Exception(f"{response['code']}: {response['message']}")
    return response["routes"][0]['geometry']
```

Note:

We extracted the polyline for a route from MapmyIndia API

We need to send this route polyline to TollGuru API to receive toll information

## [TollGuru API](https://tollguru.com/developers/docs/)

### Get key to access TollGuru polyline API
* create a dev account to [receive a free key from TollGuru](https://tollguru.com/developers/get-api-key)
* suggest adding `vehicleType` parameter. Tolls for cars are different than trucks and therefore if `vehicleType` is not specified, may not receive accurate tolls. For example, tolls are generally higher for trucks than cars. If `vehicleType` is not specified, by default tolls are returned for 2-axle cars. 
* Similarly, `departure_time` is important for locations where tolls change based on time-of-the-day.

the last line can be changed to following

```python
def get_rates_from_tollguru(polyline, tolls_key):
    url = 'https://dev.tollguru.com/v1/calc/route'
    headers = {
        'Content-type': 'application/json',
        'x-api-key': tolls_key
    }
    params = {
        'source': "mapmyindia",
        'polyline': polyline,
        'vehicleType': '2AxlesAuto',
        'departure_time': "2021-01-05T09:46:08Z"
    }
    response = requests.post(url, json=params, headers=headers).json()
    if 'message' in response:
        raise Exception(response['message'])
    return response['route']['costs']
```

The working code can be found in mapmyindia.py file.

## License
ISC License (ISC). Copyright 2020 &copy;TollGuru. https://tollguru.com/

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
