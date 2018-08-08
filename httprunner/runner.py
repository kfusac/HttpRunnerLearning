import requests

from httprunner import util,expections


def run_single_testcase(testcase):
    req_kwargs = testcase['request']

    try:
        url = req_kwargs.pop('url')
        method = req_kwargs.pop('method')
    except KeyError:
        raise expections.ParamsError('Params Error')

    resp_obj = requests.request(url=url, method=method, **req_kwargs)
    diff_content = util.diff_response(resp_obj, testcase['response'])
    success = False if diff_content else True
    return success, diff_content
