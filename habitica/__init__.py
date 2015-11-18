import requests
import json

# TODO come back to this idea
def task_lister(gen):
    def new_f(self, use_cached=False):
        if use_cached == False:
            self._tasks = self.get_tasks()

        return list(gen(self, self._tasks))
    return new_f

habitica_api = "https://habitica.com/api/v2"

def get_or_except(endpoint, uuid, apikey):
    """Return json from request or raise an exception."""
    print habitica_api+endpoint
    r = requests.get(
        habitica_api+endpoint,
        headers={
            'x-api-user':uuid,
            'x-api-key':apikey
        }
    )

    r.raise_for_status()
    return r.json()

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
        return get_or_except(endpoint, self.uuid, self.apikey)

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
        assert direction == "up" or direction == "down",\
            "direction must be \"up\" or \"down\""
        
        habit = self._post_or_except(
            "/user/tasks/{}/{}".format(self.id, direction),
            self._json
            )

        # Should probably return something useful here
        return habit
                            

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

    # TODO change the name of this

    def get_tasks(self):
        tasks_json = self._get_or_except("/user/tasks")

        return [Task(x, self) for x in tasks_json]


    # Task lister changes these generators into functions with a 'use_cached' keyword argument
    @task_lister
    def get_current_tasks(self, tasks):
        """Generator for current tasks."""
        for task in tasks:
            try:
                if task.completed == False:
                    yield task
            except KeyError:
                if task.type == 'habit':
                    yield task
                            
    @task_lister
    def get_current_habits(self, tasks):
        """Generator for all habits on Habitica."""
        for task in tasks:
            if task.type == 'habit':
                yield task

    @task_lister
    def get_current_rewards(self, tasks):
        """Generator for all custom rewards on Habitica."""
        for task in tasks:
            if task.type == 'reward':
                yield task

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
