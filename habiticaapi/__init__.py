from habitica_object import HabiticaObject
from task import Task
from character import Character

# TODO build test for this and make it return True or False
def server_is_up():
    return requests.get("https://habitica.com/api/v2/status")

class Content(HabiticaObject):
    """Simple object that holds *all* objects in Habitica.

    Create one of these objects and query it for information about
    objects for purchase etc. 

    """
    def __init__(self, uuid, apikey):
        super(Content, self).__init__(uuid, apikey, endpoint="/content")
    


