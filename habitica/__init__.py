import requests

habitica_api = "https://habitica.com/api/v2"

class Character:

    def _get_or_except(self, endpoint):
        """Return json from request or raise an exception."""
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

    def _post_or_except(self, endpoint, params):
        """Return json from request or raise an exception."""
        r = requests.post(
            habitica_api+endpoint,
            headers={
                'x-api-user':self.uuid,
                'x-api-key':self.apikey
            },
            params=params
        )

        r.raise_for_status()
        return r.json()

    def _put_or_except(self, endpoint, data):
        """Return json from request or raise an exception."""
        r = requests.put(
            habitica_api+endpoint,
            headers={
                'x-api-user':self.uuid,
                'x-api-key':self.apikey
            },
            data=data
        )

        print "Status for put is {}".format(r.status_code)
        r.raise_for_status()
        return r.json()

    def __init__(self, uuid, apikey):
        self.uuid = uuid
        self.apikey = apikey

        # Cache for tasks and user info
        # 
        # This leads to duplication, but keeping them separate is easier at this stage in development.
        self._tasks = []
        self._user = self._get_or_except("/user")

        self.name = self._user['profile']['name']

    def modify_habit(self, id, direction):
        assert direction == "up" or direction == "down",\
            "direction must be \"up\" or \"down\""
        
        habit = self._post_or_except(
            "/user/tasks/{}/{}".format(id, direction),
            params={'id': id,
                    'direction': direction,
            })

        # Should probably return something useful here
        return habit
                            

    def positive_habit(self, id):
        return self.modify_habit(id, "up")

    def negative_habit(self, id):
        return self.modify_habit(id, "down")

    def get_tasks(self):
        return self._get_or_except("/user/tasks")

    def _process_tasks(self, include_generator, use_cached=False):
        """Gets tasks with a given generator

        TODO more documentation here.

        """

        if use_cached == False:
            self._tasks = self.get_tasks()

        tasks_to_return = []

        for task in include_generator(self._tasks):
            tasks_to_return.append(task)

        return tasks_to_return

    # It's pattern time
    # TODO consider using **kwargs to pass along the arguments
    def _current_tasks_generator(self, tasks):
        """Generator for current tasks."""
        for task in tasks:
            try:
                if task['completed'] == False:
                    yield task
            except KeyError:
                if task['type'] == 'habit':
                    yield task

    def get_current_tasks(self, use_cached=False):
        """Gets the list of tasks currently not completed (including inactive dailies)."""
        return self._process_tasks(self._current_tasks_generator, use_cached)
                            
    def _current_habits_generator(self, tasks):
        """Generator for all habits on Habitica."""
        for task in tasks:
            if task['type'] == 'habit':
                yield task

    def get_current_habits(self, use_cached=False):
        return self._process_tasks(self._current_habits_generator, use_cached)


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
        return self._get_or_except("/user/tasks/{}".format(id))

    def modify_task(self, id, to_modify):
        task = self.get_task(id)

        for k in to_modify.keys():
            task[k] = to_modify[k]
            
        return self._put_or_except(
            "/user/tasks/{}".format(id),
            task
            )




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
