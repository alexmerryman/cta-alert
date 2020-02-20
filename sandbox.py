import os
import json
import requests
from datetime import datetime
import math
from twilio.rest import Client


def get_env_vars():
    cta_api_key = str(os.environ.get('cta-api-key'))
    twilio_sid = str(os.environ.get('twilio-sid'))
    twilio_auth_token = str(os.environ.get('twilio-auth-token'))
    twilio_phone_number = str(os.environ.get('twilio-phone-number'))
    my_phone_number = str(os.environ.get('my-phone-number'))

    return cta_api_key, twilio_sid, twilio_auth_token, twilio_phone_number, my_phone_number


cta_api_key, twilio_sid, twilio_auth_token, twilio_phone_number, my_phone_number = get_env_vars()

cta_mapid = '40670'
api_call = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={KEY}&mapid={MAPID}&outputType=JSON".format(KEY=cta_api_key, MAPID=cta_mapid)

response = requests.get(api_call)
api_json = json.loads(response.text)

next_trains = []
for t in api_json['ctatt']['eta']:
    eta = datetime.strptime(t['arrT'], "%Y-%m-%dT%H:%M:%S")
    diff = eta - datetime.now()
    diff_rounded = math.floor(diff.seconds / 60.)
    next_trains.append(diff_rounded)

    # TODO: If time < X mins, exclude (too soon, won't make it)
    # TODO: Include actual time
    # print(eta)
    # print(datetime.now())
    # print(diff)
    # print(diff_rounded)


next_trains_message = \
    '''
    The next train is in: {} min(s)
    Other trains in:
    {}
    '''.format(next_trains[0], next_trains[1:])

print(next_trains_message)

# print("The next train is in: {} min(s)".format(next_trains[0]))
# print("Other trains in:")
# for n in next_trains[1:]:
#     print(n, "min(s)")


client = Client(twilio_sid, twilio_auth_token)

message = client.messages.create(
    to=my_phone_number,
    from_=twilio_phone_number,
    body=next_trains_message)

print(message.sid)
