import json

from cappy import API

redcap_token = 'F53EA8B9D58456B722945F4B274E6B4C'
redcap_api_endpoint = 'http://redi2.dev/redcap/api/'
cappy_version = 'lineman.json'

api = API(redcap_token, redcap_api_endpoint, cappy_version)

# only gets the records for subjects with unique_field 1 and 2
res = api.export_records(records=[1,2])

cappy_version = 'master.yaml'
api = API(redcap_token, redcap_api_endpoint, cappy_version, requests_options={
    'verify': False,
    'headers': {
        'TEST': 'THIS IS A TEST'
    }
})

# exports in eav instead of flat
# resist the urge to use adhoc options
res = api.export_records(adhoc_redcap_options={
    'type': 'eav'
})

# we get back raw requests content
# print(res.content)
# cappy gives us more information about what was passed
print(res.cappy_data)
# we can alter the requests initialization
print(res.request.headers.get('TEST'))
