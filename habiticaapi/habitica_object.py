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
        self.__dict__["habitica_api"] = "https://habitica.com/api/v2"

        if json:
            self.__dict__["_json"] = attrdict.AttrMap(json)
        elif endpoint:
            self.__dict__["_json"] = self._get_or_except(endpoint)
        else:
            self.__dict__["_json"] = attrdict.AttrMap()



    def _put_or_except(self, endpoint, data):
        """Return json from PUT request or raise an exception."""
        r = requests.put(
            self.habitica_api+endpoint,
            headers={
                'x-api-user':self.uuid,
                'x-api-key':self.apikey
            },
            json=dict(data)
        )

        r.raise_for_status()
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
            json=dict(data)
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

    def __getattr__(self, name):
        try:
            return getattr(self.__dict__["_json"], name)
        except KeyError:
            return self.__dict__[name]

    def __setattr__(self, name, value):
        if name in self._json.keys():
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
