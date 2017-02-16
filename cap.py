import json
import copy

import requests as req

import utils as utils

class API(object):
    """
    The only class in the library. Dynamically adds methods to itself
    on initialization from a json file in the "versions" directory
    """

    def __init__(self, token, endpoint, version_file):
        """
        Given:
        - a token for a project
        - an endpoint to query
        - a filename for a version file

        Result:
        An instance of API that has each top level key as a method.
        These methods will return a requests response object when called
        and will generally do what you expect when calling them with and
        without arguments.
        """
        version_path = utils.path_for_version(version_file)
        with open(version_path, 'r') as api_def:
            self.api_definition = json.loads(api_def.read())
        for key in self.api_definition:
            setattr(self, key, self._redcap_call_from_def(token, endpoint, key))

    def _redcap_call_from_def(self, token, endpoint, key):
        """
        Private function that is used to create the method calls on the
        API instance. The token and enpoint are bound up in the closure
        so if you need to change them, delete the instance you are using
        and make a new one.
        """
        def run_call(data=None, forms=[], fields=[]):
            data_copy = copy.copy(self.api_definition[key])
            body = self._build_post_body(token, data, forms, fields, data_copy)
            return req.post(endpoint, body)
        return run_call

    def _build_post_body(self, token, data, forms, fields, post_body):
        """
        Constructs a post body for a redcap api call based on what is in
        the versioned api definition json.
        """
        post_body['token'] = token
        if data:
            post_body['data'] = data
        if post_body.get('fields'):
            del post_body['fields']
            post_body = self._add_iterable(fields, 'fields', post_body)
        if post_body.get('forms'):
            del post_body['forms']
            post_body = self._add_iterable(forms, 'forms', post_body)
        return post_body

    def _add_iterable(self, iterable, name, post_body):
        """
        Redcap has odd behavior when submitting arrays. Instead of
        submitting an array, it prefers that one put field[i] for the
        i-th item. This method fills out the post body appropriately
        """
        for index, item in enumerate(iterable):
            post_body['{}[{}]'.format(name, index)] = item
        return post_body
