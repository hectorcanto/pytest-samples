import requests
from delayed_assert import assert_expectations, expect


def test_delayed_response(requests_mock):
    url = "http://tests.com"
    requests_mock.get(url, json={"key": "value"})

    response = requests.get(url)

    expect(response.status_code == 200, response.status_code)
    expect(response.json() == {}, response.text)
    assert_expectations()
