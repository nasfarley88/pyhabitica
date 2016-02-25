# User provided config file
import config

import requests
import attrdict
import logging

def attrdict_or_list(thing):

    if type(thing) == dict:
        return attrdict.AttrMap(thing)
    elif type(thing) == list:
        return thing
    else:
        assert False, "DON'T PANIC. Something that wasn't a list or dict."

class NotInHabiticaObject(Exception):
    pass


class HabiticaObject(object):
    """Abstract class for custom HTTP requests commands for Habitica. """

    def __init__(self, uuid, apikey, json=None, endpoint=None):
        # json must be created with __dict__ to avoid referencing itself in __setattr__
        # self.__dict__["json"] = attrdict.AttrMap()

        self.__dict__["_uuid"] = uuid
        self.__dict__["_apikey"] = apikey
        self.__dict__["_habitica_api"] = config.HABITICA_URL+"/api/v2"

        if json:
            self.__dict__["json"] = attrdict.AttrMap(json)
        elif endpoint:
            self.__dict__["json"] = self._get_or_except(endpoint)
        else:
            self.__dict__["json"] = attrdict.AttrMap()


    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        # Use the ordinary, plain, boring, normal setattr so that
        # pickle doesn't freak out.
        super(HabiticaObject, self).__setattr__("__dict__", d)

    def _put_or_except(self, endpoint, json=None):
        """Return json from PUT request or raise an exception."""
        if json:
            r = requests.put(
                self._habitica_api+endpoint,
                headers={
                    'x-api-user':self._uuid,
                    'x-api-key':self._apikey
                },
                json=dict(json)
            )
        else:
            r = requests.put(
                self._habitica_api+endpoint,
                headers={
                    'x-api-user':self._uuid,
                    'x-api-key':self._apikey
                },
            )

        try:
            r.raise_for_status()
        except Exception as e:
            print(r)
            raise(e)
        return attrdict_or_list(r.json())

    def _get_or_except(self, endpoint):
        """Return json from GET request or raise an exception."""
        r = requests.get(
            self._habitica_api+endpoint,
            headers={
                'x-api-user':self._uuid,
                'x-api-key':self._apikey
            }
        )

        r.raise_for_status()
        return attrdict_or_list(r.json())

    def _post_or_except(self, endpoint, json={}, query={}):
        """Return json from POST request or raise an exception."""
        r = requests.post(
            self._habitica_api+endpoint,
            headers={
                'x-api-user':self._uuid,
                'x-api-key':self._apikey
            },
            json=dict(json),
            params=query
        )

        r.raise_for_status()
        return attrdict_or_list(r.json())

    def _delete_or_except(self, endpoint):
        """Return json from POST request or raise an exception."""
        r = requests.delete(
            self._habitica_api+endpoint,
            headers={
                'x-api-user':self._uuid,
                'x-api-key':self._apikey
            }
        )

        r.raise_for_status()
        return attrdict_or_list(r.json())

    def __str__(self):
        return "HabiticaObject: \n"+str(self.__dict__)
