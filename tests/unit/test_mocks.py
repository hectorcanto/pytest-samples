import requests

import pytest

@pytest.mark.current
def test_with_spy(mocker):
    url = "https://2021.es.pycon.org/"
    spy = mocker.patch.object(requests, "get", wraps=requests.get)
    response = requests.get(url)
    assert response.status_code == 200
    spy.assert_called_once(), spy.mock_calls
    spy.assert_called_with(url)