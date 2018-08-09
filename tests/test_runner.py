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

    def setup_method(self):
        self.reset_all()

    def test_run_single_testcase_with_paramerror_json(self):
        path = 'tests/testcase/param_without_url.json'

        json_testcase = loader.load_json_file(path)

        with pytest.raises(expections.ParamsError):
            runner.run_single_testcase(json_testcase)

    def test_run_single_json_testcase_success(self):
        path = 'tests/testcase/smoke_test.json'

        json_testcase = loader.load_json_file(path)

        success, diff_content = runner.run_single_testcase(json_testcase)
        print(diff_content)
        assert success

    def test_run_single_yaml_testcase_success(self):
        path = 'tests/testcase/smoke_test.yml'

        json_testcase = loader.load_yaml_file(path)

        success, diff_content = runner.run_single_testcase(json_testcase)

        print(diff_content)
        assert success

    def reset_all(self):
        url = f'{self.host}/api/reset-all'
        return self.api_client.get(url)
