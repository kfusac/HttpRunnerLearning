import os
import pytest

from httprunner import expections, runner, loader
from tests.base import TestApiServerBase


class TestRunner(TestApiServerBase):
    @classmethod
    def setup_class(cls):
        super().setup_class()

    @classmethod
    def teardown_class(cls):
        super().teardown_class()

    def test_run_single_json_testcase(self):
        path = 'tests/testcase/smoke_test.json'

        json_testcase = loader.load_json_file(path)

        success, diff_content = runner.run_single_testcase(json_testcase)

        print(diff_content)
        assert success