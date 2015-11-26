from habitica_object import HabiticaObject
from task import Task
from character import Character

class Content(HabiticaObject):
    """Simple object that holds *all* objects in Habitica.

    Create one of these objects and query it for information about
    objects for purchase etc. 

    """
    def __init__(self, uuid, apikey):
        super(Content, self).__init__(uuid, apikey, endpoint="/content")
    


