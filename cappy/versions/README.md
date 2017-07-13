# Purpose of these files #

These yaml and json files define different ways to produce API instances.

Every top level key or api_def level key is a method on the API instance and the object corresponding to that key
is the post body that is given when viewed on the API playground screen in RedCap.

Any iterable / list-like argument (i.e. forms, fields) should have an array as its value in the 
version file. This signals that this is a variadic arguement and lets the API class know how to
do its thing.

### What makes a version? ###

Good question. It is not an accident that versions are so closely tied to how the developer will
consume the API. Basically, any time your use case changes, add a new version.

Do you want read-only? Don't put any import calls in the json.

Only want csv's? Make an api version that has all csv calls for the format.

Find some workaround that needs to be done for your project? Make another version file.

