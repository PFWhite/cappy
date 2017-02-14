# Purpose of these files #

These json files define different ways to produce API instances.

Every top level key is a method on the API instance and the object corresponding to that key
is the post body that is given when viewed on the API playground screen in RedCap.

The forms and fields keys do not hold arrays for their fields but instead hold a truthy or falsy
value. This is used to determine if the api call accepts those variadic parameters.

### What makes a version? ###

Good question. It is not an accident that versions are so closely tied to how the developer will
consume the API. Basically, any time your use case changes, add a new version.

Do you want read-only? Don't put any import calls in the json.

Only want csv's? Make an api version that has all csv calls for the format.

Find some workaround that needs to be done for your project? Make another version file.

