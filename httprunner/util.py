def diff_response(resp_obj, expected_resp_json):
    resp_info = parse_response_object(resp_obj)

    return diff_json(resp_info, expected_resp_json)


def parse_response_object(resp_obj):
    try:
        resp_body = resp_obj.json()
    except ValueError:
        resp_body = resp_obj.text

    return {
        'status_code': resp_obj.status_code,
        'headers': resp_obj.headers,
        'body': resp_body
    }


def diff_json(currect_json, expected_json):
    json_diff = {}

    for key, expected_value in expected_json.items():
        value = currect_json.get(key, None)
        if str(value) != str(expected_value):
            result, msg = _cmp_dict(dict(expected_value), dict(value))
            if result:
                continue
            json_diff[key] = {'value': value, 'expected': expected_value}

    return json_diff


def _cmp_dict(src_data, dst_data):
    if type(src_data) != type(dst_data):
        return False, f"type: '{type(src_data)}' != '{type(dst_data)}'"
    if isinstance(src_data, dict):
        for key in src_data:
            if key not in dst_data:
                return False, f'{key} not in {dst_data}'
            _cmp_dict(src_data[key], dst_data[key])
    elif isinstance(src_data, list):
        for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
            _cmp_dict(src_list, dst_list)
    else:
        if src_data != dst_data:
            return False, f"value '{src_data}' != '{dst_data}'"

    return True,""
