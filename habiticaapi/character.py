from habitica_object import HabiticaObject
from task import Task
from item import InventoryItem
import attrdict

# TODO consider having all HabiticaObjects do the _json and __getattr__ and __setattr__ thing
class Character(HabiticaObject):
    def __init__(self, uuid, apikey):
        super(Character, self).__init__(uuid, apikey)

        # Cache for tasks and user info
        # 
        # This leads to duplication, but keeping them separate is easier at this stage in development.
        self.__dict__["_tasks"] = []
        self._json = attrdict.AttrMap(self._get_or_except("/user"))

    # overriding __setattr__ to prevent users modifying values without functions
    # def __setattr__(self, name, value):
    #     assert False, "__setattr__ has been disabled for the Character class. If you *really* need to edit a member variable, use self.__dict__[name] = value."
        

    def _pull_tasks(self):
        """Pull all tasks from the Habitica server to the character."""
        self.__dict__["_tasks"] = self._get_or_except("/user/tasks")

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
            except AttributeError:
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
    #         u'text': u'Some text',
    #         u'type': u'habit',
    #         u'up': True,
    #         u'value': 0.0}

    #     for i in kwargs:
    #         template
    

    def get_task(self, id):
        # When a Task recieves only an ID, it fetches the task from online.
        return Task(id, self)


    # sort tasks?

    # clear completed

    # unlink

    def get_items_can_buy(self):
        """Returns a list of items available to buy."""
        return [InventoryItem(i) for i in self._get_or_except("/user/inventory/buy")]

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
