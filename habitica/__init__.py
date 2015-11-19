import requests

habitica_api = "https://habitica.com/api/v2"

class HabiticaObject:
    """Abstract class for custom HTTP requests commands.

    Anything inherting from this class must have:
     - self.uuid
     - self.apikey.

    """
    
    def _put_or_except(self, endpoint, data):
        """Return json from PUT request or raise an exception."""
        r = requests.put(
            habitica_api+endpoint,
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
        print habitica_api+endpoint
        r = requests.get(
            habitica_api+endpoint,
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
            habitica_api+endpoint,
            headers={
                'x-api-user':self.uuid,
                'x-api-key':self.apikey
            },
            json=data
        )

        r.raise_for_status()
        return r.json()
    

class Task(HabiticaObject):
    """Simple class as a placeholder for tasks in Habitica.

    Set up so that getattr(Task, thing) is directly from task json, if the class member does not already exist."""

    def __init__(self, id_or_json, character):
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


class Character(HabiticaObject):
    def __init__(self, uuid, apikey):
        self.uuid = uuid
        self.apikey = apikey

        # Cache for tasks and user info
        # 
        # This leads to duplication, but keeping them separate is easier at this stage in development.
        self._tasks = []
        self._user = self._get_or_except("/user")

        self.name = self._user['profile']['name']


    def _pull_tasks(self):
        """Pull all tasks from the Habitica server to the character."""
        self._tasks = self._get_or_except("/user/tasks")

    def get_all_tasks(self, from_iterable=None, use_cached=False):
        """Get all tasks or all tasks from from_iterable."""

        if use_cached == False:
            self._pull_tasks()

        if from_iterable == None:
            return [Task(x, self) for x in self._tasks]
        elif callable(from_iterable):
            return [x for x in from_iterable([Task(x, self) for x in self._tasks])]

    def get_specific_tasks(self, tasks_iterable=None, use_cached=False, **kwargs):
        """Get tasks matching certain critera with keyword__contains.
        
        Get all tasks matching criteria given in kwargs. If no extra
        kwargs are given, return nothing. (If you want to return
        everything, use get_all_tasks())

        For example:
        >>> character.get_specific_tasks(text__contains="feats of daring do")
        [Task('Achieve feats of daring do'),
         Task('Watch feats of daring do on YouTube')]
        >>> character.get_specific_tasks(id__contains="asdfsd-asd-fasdg-asfdfasdgh-a-sdf")
        [Task('Understand how to be productive')]

        """

        if use_cached == False:
            self._pull_tasks()

        # If no generator is supplied, use all tasks
        if tasks_iterable == None:
            tasks = self.get_all_tasks(use_cached=True)
        elif callable(tasks_iterable):
            tasks = tasks_iterable(self.get_all_tasks(use_cached=True))
        else:
            assert False, "tasks_iterable must be None or a callable."
            
        return_list = []

        # TODO use regex to catch the _tmp_key and make sure
        # keyword__contains matches .*__contains$ (and implement __re
        # methods)
        for task in tasks:
            for k, v in kwargs.items():
                if "__contains" in k:
                    _tmp_key = k.replace("__contains", "")
                    if v in getattr(task, _tmp_key):
                        return_list.append(task)
                elif "__re" in k:
                    assert False, "Sorry, not implemented yet!"

        return return_list

    def _current_tasks_generator(self, tasks):
        """Generator for current tasks."""
        for task in tasks:
            try:
                if task.completed == False:
                    yield task
            except KeyError:
                if task.type == 'habit':
                    yield task

    def get_current_tasks(self):
        """Get all currently running tasks (not including rewards)."""
        return self.get_all_tasks(self._current_tasks_generator)
                            
    # TODO complete
    # def create_habit(self, **kwargs):
    #     template_task = {
    #         u'attribute': u'str',
    #         u'challenge': {},
    #         u'dateCreated': u'2015-10-22T15:00:57.083Z',
    #         u'down': True,
    #         u'history': [u'date', u'value', u'date', u'value', u'date', u'value'],
    #         u'id': u'd15a60c8-c345-44ca-9749-0831c8975097',
    #         u'notes': u'',
    #         u'priority': 1,
    #         u'tags': {},
    #         u'text': u'Fuzzy drinks',
    #         u'type': u'habit',
    #         u'up': True,
    #         u'value': 0.0}

    #     for i in kwargs:
    #         template
    

    def get_task(self, id):
        return Task(id, self)

    # def delete_task(self, id):
    #     pass

    # sort tasks?

    # clear completed

    # unlink

    # def get_purchasable_equipment(self):
    #     """Returns a list of equipment available to buy."""
    #     pass

    # # Consider merging equipment and other item types in api
    # def buy_equipment(self, key):
    #     pass

    # def sell_item(self, type, key):
    #     pass

    # def buy_item_with_gems(self, type, key):
    #     pass

    # def buy_item_with_hourglass(self, type, key):
    #     pass

    # def feed_pet(self, pet, food):
    #     pass

    # def feed_pet_best(self, pet):
    #     pass

    # def equip(self, type, equipment):
    #     pass

    # def hatch(self, egg, hatching_potion):
    #     pass

    # def revive(self):
    #     pass

    # def drink_fortify_potion(self):
    #     pass

    # # Reset account

    # # TODO make an explicit check_into_inn and check_out_of_inn methods
    # def toggle_sleep(self):
    #     pass

    # def class_change(self, cls):
    #     pass

    # def allocate_point(self, stat):
    #     pass

    # def cast(self, spell, target_type, target_id=None):
    #     pass

    # # TODO investigate how this function works (does it really allow you to cheat the system?)
    # def unlock(self, path):
    #     pass

    # # TODO figure out how to use batch update

    # def get_tag(self, id):
    #     pass

    # def create_tag(self, id):
    #     pass

    # def get_tags(self):
    #     pass

    # # sort tags?

    # def modify_tag(self, id, object):
    #     pass

    # def delete_tag(self, id):
    #     pass
