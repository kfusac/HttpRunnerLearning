import multiprocessing
import time
import pytest

import requests
from tests.api_server import app as flask_app

FLASK_APP_PORT=5000

def run_flask():
    flask_app.run(port=FLASK_APP_PORT)

class TestApiServerBase:
    @classmethod
    def setup_class(cls):
        cls.host=f'http://127.0.0.1:{FLASK_APP_PORT}'
        cls.flask_process=multiprocessing.Process(
            target=run_flask
        )
        cls.flask_process.start()
        time.sleep(1)
        cls.api_client=requests.Session()
    
    @classmethod
    def teardown_class(cls):
        cls.flask_process.terminate()