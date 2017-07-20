# cappy v1.1.1
The Redcap API library that you build yourself.

## Ideology ##

A module should do one thing and do it well. Cappy calls the redcap API. It does not rate limit, it does not
tell you how to organize the data you get back, it does not handle errors nor declare any new exception types.

## Usage ##

The redcap API requires a token, and an endpoint. Also Cappy uses a version file that specifies the API
calls you want to support. You pass all three of these into the API constructor to get an instance of the 
api. This instance has methods corresponding to the definitions in the json file.

Any API call that pushes data takes the data object as the first parameter. This would be calls like `import_record`
and the like. Any iterable thing other than data is passed by a keyword param. More information can be found in the
doc strings of cap.py

Happy redcapping!

