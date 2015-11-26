# This is a user supplied file with user credentials
import config

import habiticaapi
import unittest2
import logger
import copy

class TestCharacter(unittest2.TestCase):
    def setUp(self):
        """Setup character."""
        self.character = habiticaapi.Character(
            config.USERID,
            config.APIKEY
        )

        # This *must* be an independent copy
        self.character_to_restore = copy.deepcopy(self.character)

    def tearDown(self):
        """Tear down character."""
        print self.character_to_restore
        self.character_to_restore.push()

    def test_push_character_return_None(self):
        self.character.push()

    def test_pickling_character_return_None(self):
        import pickle
        import os
        pickle_filename = "test_char_pickle.p"
        if os.path.exists(pickle_filename):
            os.remove(pickle_filename)
        pickle.dump(self.character, open(pickle_filename, "wb"))
        unpickled_character = pickle.load(open(pickle_filename, "rb"))
        os.remove(pickle_filename)

        assert self.character._json == unpickled_character._json
        assert self.character.__dict__ == unpickled_character.__dict__

    def test_yaml_character_return_None(self):
        import yaml
        import os
        yaml_filename = "test_char.yaml"
        if os.path.exists(yaml_filename):
            os.remove(yaml_filename)
        yaml.dump(self.character, open(yaml_filename, "wb"))
        unyamld_character = yaml.load(open(yaml_filename, "rb"))
        os.remove(yaml_filename)

        assert self.character._json == unyamld_character._json
        try:
            assert self.character.__dict__ == unyamld_character.__dict__
        except AssertionError as e:
            print set(self.character.__dict__).symmetric_difference(set(unyamld_character.__dict__))
            raise e

        
    def test_assert_character_exists_return_None(self):
        assert self.character

    def test_pull_tasks_return_None(self):
        self.character._pull_tasks()

    def test_get_all_tasks_simple_return_None(self):
        tasks = self.character.get_all_tasks()
        assert len(tasks) != 0
        for i in tasks:
            assert type(i) is habiticaapi.Task


    def test_get_specific_tasks_return_None(self):
        tasks = self.character.get_specific_tasks()

        # Should be 0 as no conditions are given
        assert len(tasks) == 0

    def test_get_specific_tasks_kw__contains_return_None(self):
        tasks = self.character.get_specific_tasks(text__contains="e")
        assert len(tasks) != 0,\
                             """If this test has failed, it's possible that there are no tasks with the letter 'e' on Habitica ... or the function really is broken."""
        
    @staticmethod
    def dummy_generator(tasks):
        for task in tasks:
            yield task

    def test_get_specific_tasks_simple_generator_return_None(self):
        self.character._pull_tasks()
        tasks = self.character.get_specific_tasks(
            task_iterable=self.dummy_generator,
            text__contains="e",
            use_cached=True,
            )
        assert len(tasks) != 0

        all_tasks_containing_e = self.character.get_specific_tasks(
            text__contains="e",
            use_cached=True,
        )

        assert len(tasks) == len(all_tasks_containing_e)

    def test_get_current_tasks_return_None(self):
        tasks = self.character.get_current_tasks()
        assert len(tasks) != 0


    def test_get_task_from_get_all_tasks_return_None(self):
        tasks = self.character.get_all_tasks()
        task = self.character.get_task(tasks[0].id)

    def test_get_items_can_buy(self):
        items = self.character.get_items_can_buy()
        # Not sure what i can test here, assignment should be enough.

    # TODO figure out how to test this safely
    # def test_buy_equipment(self):
    #     assert False,\
    #         "Not sure how to test this one yet, can't create items." 

    # TODO figure out how to test selling item

    # TODO figure out how to test buying items with gems
