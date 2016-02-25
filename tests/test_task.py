# This is a user supplied file with user credentials
import config

import habiticaapi
import unittest2
import logger
import copy

class TestTask(unittest2.TestCase):
    def setUp(self):
        """Setup character."""
        self.character = habiticaapi.Character(
            config.USERID,
            config.APIKEY
        )
        # TODO set this up to create a task for testing on
        self.task = self.character.get_all_tasks()[0]
        self.habit = self.character.get_specific_tasks(
            type__contains = "habit"
            )[0]

        # This *must* be an independent copy otherwise when it is changed, and
        # I push it back, it will be the changed character
        self.character_to_restore = copy.deepcopy(self.character)

    def tearDown(self):
        """Tear down character."""
        self.character_to_restore.push()

    def test_task___init___return_None(self):
        assert self.task

    def test_pull_return_None(self):
        task = self.task.pull()

    def test_push_return_None(self):
        task = self.task.push()

    def test__task_direction_return_None(self):
        task_up = self.habit._task_direction("up")
        task_down = self.habit._task_direction("down")

    def test_up_return_None(self):
        task = self.habit.up()

    def test_down_return_None(self):
        task = self.habit.down()

    # TODO set up a test for delete once I have a working create
