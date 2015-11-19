import requests

class HabiticaObject:
    """Abstract class for custom HTTP requests commands for Habitica.

    Anything inherting from this class must have:
     - self.uuid
     - self.apikey.

    """

    def __init__(self):
        self.habitica_api = "https://habitica.com/api/v2"

    def _put_or_except(self, endpoint, data):
        """Return json from PUT request or raise an exception."""
        r = requests.put(
            self.habitica_api+endpoint,
            headers={
                'x-api-user':self.uuid,
                'x-api-key':self.apikey
            },
            json=data
        )

        r.raise_for_status()
        return r.json()

    def _get_or_except(self, endpoint):
        """Return json from GET request or raise an exception."""
        print self.habitica_api+endpoint
        r = requests.get(
            self.habitica_api+endpoint,
            headers={
                'x-api-user':self.uuid,
                'x-api-key':self.apikey
            }
        )

        r.raise_for_status()
        return r.json()

    def _post_or_except(self, endpoint, data):
        """Return json from POST request or raise an exception."""
        r = requests.post(
            self.habitica_api+endpoint,
            headers={
                'x-api-user':self.uuid,
                'x-api-key':self.apikey
            },
            json=data
        )

        r.raise_for_status()
        return r.json()
