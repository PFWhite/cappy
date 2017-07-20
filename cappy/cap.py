import copy

import requests as req
import yaml

import cappy.utils as utils

class API(object):
    """
    The only class in the library. Dynamically adds methods to itself
    on initialization from a json or yaml file in the "versions" directory
    """

    def __init__(self, token, endpoint, version_file, requests_options={}):
        """
        Given:
        - a token for a project
        - an endpoint to query
        - a filename for a version file
        - an optional dictionary of options for requests

        Result:
        An instance of API that has each top level key as a method.
        These methods will return a requests response object when called
        and will generally do what you expect when calling them with and
        without arguments. Any variadic fields are passed as keyword parameters

        The requests options will be applied to all calls made with the
        auto generated API functions
        """
        version_path = utils.path_for_version(version_file)
        self.requests_options = requests_options or {}
        with open(version_path, 'r') as api_def:
            version_data = yaml.load(api_def.read())
            self.api_definition = version_data.get('api_def') or version_data
        for key in self.api_definition:
            setattr(self, key, self._redcap_call_from_def(token, endpoint, key))


    def _redcap_call_from_def(self, token, endpoint, key):
        """
        Private function that is used to create the method calls on the
        API instance. The token and enpoint are bound up in the closure
        so if you need to change them, delete the instance you are using
        and make a new one.
        """
        def run_call(data=None, **kwargs):
            """
            The methods on the API instance you will call have this signature.

            Example usage (assuming export_metadata is in the version file):
            api.export_metadata(forms=['my_redcap_instrument_name'])

            This will call the redcap api with the form arguments filled in correctly
            """
            call_definition = self.api_definition[key]
            call_def_copy = copy.copy(call_definition)
            body = self._build_post_body(token, data, call_def_copy, **kwargs)
            res = req.post(endpoint, body, **self.requests_options)
            return self._enhance_response(res, key, copy.copy(call_definition), kwargs, body)
        return run_call

    def _build_post_body(self, token, data, post_body_template, **kwargs):
        """
        Constructs a post body for a redcap api call based on what is in
        the versioned api definition json, and optionally in the
        'adhoc_redcap_options' kwarg
        """
        post_copy = copy.copy(post_body_template)
        post_copy['token'] = token
        if data:
            post_copy['data'] = data
            # We dont want to allow readonly methods to write
            if not post_body_template['data']:
                del post_copy['data']

        # Usually you should edit the version file to add another option to a call
        # to redcap. There are times that this takes a prohibitive amount of time,
        # so when calling a API function one can pass key value pairs of options
        # to add by passing 'adhoc_redcap_options' as a kwarg to the function
        # any iterable keys passed in this manner need to have their contents
        # passed the usual way as a kwarg
        for key, val in kwargs.items():
            if key == 'adhoc_redcap_options':
                for k, v in val.items():
                    # we done want people to make readonly functions write
                    if not k == 'data':
                        # if we have an iterable
                        if type(v) == type([]):
                            post_body_template[k] = []
                        # we just have some option like rawOrLabel
                        else:
                            post_copy[k] = v

        # add iterable things to the post_copy which will be POSTed to redcap
        for key in post_body_template:
            if type(kwargs.get(key)) == type([]):
                iterable_name = key
                post_copy = self._add_iterable(kwargs[key], iterable_name, post_copy)
            if type(post_copy.get(key)) == type([]):
                del post_copy[key]

        return post_copy

    def _add_iterable(self, iterable, name, post_body):
        """
        Redcap has odd behavior when submitting arrays. Instead of
        submitting an array, it prefers that one put field[i] for the
        i-th item. This method fills out the post body appropriately
        """
        for index, item in enumerate(iterable):
            post_body['{}[{}]'.format(name, index)] = item
        return post_body

    def _enhance_response(self, response, call_name, call_def, kwargs, body):
        """
        This function exists to expose to the end user more information about
        the way in which the request was called. For instance, they may want
        to know what the format of the file returned is.
        """
        if body.get('data'):
            del body['data']
        response.cappy_data = {
            'call_name': call_name,
            'file_format': call_def.get('format'),
            'error_format': call_def.get('returnFormat'),
            'kwargs_passed': kwargs,
            'post_body_minus_data': body
        }
        return response
