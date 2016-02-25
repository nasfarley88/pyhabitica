# User provided config file
import config

import requests
import attrdict

def attrdict_or_list(thing):

    if type(thing) == dict:
        return attrdict.AttrMap(thing)
    elif type(thing) == list:
        return thing
    else:
        assert False, "DON'T PANIC. Something that wasn't a list or dict."


class HabiticaObject(object):
    """Abstract class for custom HTTP requests commands for Habitica. """

    def __init__(self, uuid, apikey, json=None, endpoint=None):
        # _json must be created with __dict__ to avoid referencing itself in __setattr__
        # self.__dict__["_json"] = attrdict.AttrMap()

        self.__dict__["uuid"] = uuid
        self.__dict__["apikey"] = apikey
        self.__dict__["habitica_api"] = config.HABITICA_URL+"/api/v2"

        if json:
            self.__dict__["_json"] = attrdict.AttrMap(json)
        elif endpoint:
            self.__dict__["_json"] = self._get_or_except(endpoint)
        else:
            self.__dict__["_json"] = attrdict.AttrMap()


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
                self.habitica_api+endpoint,
                headers={
                    'x-api-user':self.uuid,
                    'x-api-key':self.apikey
                },
                json=dict(json)
            )
        else:
            r = requests.put(
                self.habitica_api+endpoint,
                headers={
                    'x-api-user':self.uuid,
                    'x-api-key':self.apikey
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
            self.habitica_api+endpoint,
            headers={
                'x-api-user':self.uuid,
                'x-api-key':self.apikey
            }
        )

        r.raise_for_status()
        return attrdict_or_list(r.json())

    def _post_or_except(self, endpoint, json={}, query={}):
        """Return json from POST request or raise an exception."""
        r = requests.post(
            self.habitica_api+endpoint,
            headers={
                'x-api-user':self.uuid,
                'x-api-key':self.apikey
            },
            json=dict(json),
            params=query
        )

        r.raise_for_status()
        return attrdict_or_list(r.json())

    def _delete_or_except(self, endpoint):
        """Return json from POST request or raise an exception."""
        r = requests.delete(
            self.habitica_api+endpoint,
            headers={
                'x-api-user':self.uuid,
                'x-api-key':self.apikey
            }
        )

        r.raise_for_status()
        return attrdict_or_list(r.json())

    # This is a problem. Trying to yaml or pickle stuff, this getattr
    # gets in the way and causes the emmitter to simply take
    # self._json.thing and call it self.thing. Which is what I want
    # the programmer to see. But not what I want the emmitter to see
    # (since it's hella confusing __getattr__(self, name):
    def __getattr__(self, name):
        # If other methods fail, try
        try:
            return getattr(self.__dict__["_json"], name)
        except KeyError:
            # Sometimes _json doesn't exist yet, so create it and
            # recall the function
            self.__dict__["_json"] = attrdict.AttrMap()
            return getattr(self, name)


    def __setattr__(self, name, value):
        if name in self.__dict__["_json"].keys():
            # TODO ensure that the same types are put into place
            # (Maybe consider on the fly checking for different types)
            assert type(self.__dict__["_json"]) == type(value),\
                ("Types must be kept consistent with json variables."
                 " To repair broken json structures, see self._repair_json.")
            setattr(self.__dict__["_json"], name, value)
        else:
            self.__dict__[name] = value

    def _repair_json(self, name, value):
        """Sets attributes of self._json without checking for type. """
        setattr(self.__dict__["_json"], name, value)

        # Allow the user to check the change was sucessful
        return self._json
