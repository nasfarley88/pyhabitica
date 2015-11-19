from habitica_object import HabiticaObject

def _create_task_on_server(uuid, apikey):
    """Create a task on the Habitica server and return a Task()."""
    assert False, "Sorry, this function is not made yet!"

# TODO consider changing _json to something less confusing
class Task(HabiticaObject):
    """Simple class as a placeholder for tasks in Habitica.

    Automatically fetches task information from the Habitica
    servers.

    Set up so that __getattr__ and __setattr__ is directly from task
    json, if the class member does not already exist.

    """

    def __init__(self, id_or_json, character):
        HabiticaObject.__init__(self)

        # TODO consider what happens when a task needs to be created
        if type(id_or_json) == str:
            self._json = get_or_except("/user/tasks/{}".format(id), character.uuid, character.apikey)
        elif type(id_or_json) == dict:
            # WARNING little checking is done that this is a valid task. Programmer beware!
            self._json = id_or_json
            assert self._json.has_key("id"), "No id found in dict, was a valid task json passed?"
        else:
            assert False, "id_or_json must be str or dict."
            
        self.uuid = character.uuid
        self.apikey = character.apikey

    def __getattr__(self, name):
        try:
            return self.__dict__["_json"][name]
        except KeyError:
            return self.__dict__[name]

    def __setattr__(self, name, value):
        try:
            self._json[name] = value
        except KeyError:
            self.__dict__[name] = value

    def __repr__(self):
        return "Task('"+self.text+"')"

    # TODO repr and str methods

    def pull(self):
        """Update the task from the server, squashing any local changes."""
        self._json = get_or_except("/user/tasks/{}".format(id), self.uuid, self.apikey)

    def push(self):
        """Push updates to the task (via the HTTP PUT method)."""
            
        return self._put_or_except(
            "/user/tasks/{}".format(self.id),
            self._json
            )

    # def modify_habit(self, id, direction):
    def _task_direction(self, direction):
        """Move the task in a "direction" (allowed values: "up" and "down").

        The internal Habitica API inteprets "up" and "down"
        differently for different types of tasks. Habits are obvious
        ("up" is positive, "down" is negative). Dailies and Todos are
        complete and not completed by "up" and "down".

        TODO figure out what happens to rewards.

        """
        assert direction == "up" or direction == "down",\
            "direction must be \"up\" or \"down\""
        
        # Returns information on XP gained, items etc.
        result = self._post_or_except(
            "/user/tasks/{}/{}".format(self.id, direction),
            self._json
            )

        return result
                            

    # TODO think about better naming scheme
    def up(self):
        return self._task_direction("up")

    def down(self):
        return self._task_direction("down")

    def complete(self):
        return self.up()

    def uncomplete(self):
        return self.down()
