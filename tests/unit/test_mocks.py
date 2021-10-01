import os.path

import pytest
import requests

from source import SystemUnderTest

def test_stubbing(monkeypatch):

    def mock_exist(value):
        print(f"{value} exists")
        return True

    monkeypatch.setattr(os.path, 'exists', mock_exist)
    assert os.path.exists("/believe/me/I/exist")


def test_mock_patching(mocker):
    url = "https://2021.es.pycon.org/"
    mocked = mocker.patch.object(requests, "get", return_value="intercepted")

    response = requests.get(url)
    assert response == "intercepted"
    assert mocked.called_once()


def test_mock_side_effect(mocker):
    mocked = mocker.patch.object(requests, "get", side_effect=KeyError("coconut"))

    with pytest.raises(KeyError) as exc_info:
        requests.get("does not matter")
    assert exc_info.value.args[0] == "coconut"
    assert exc_info.typename == "keyError"
    assert mocked.called_once()


def test_mock_magic_method(mocker):
    one_dict = {"key": 1}
    mock = mocker.patch("source.SystemUnderTest.function")
    mock.__str__.return_value = "foo_bar"
    assert str(SystemUnderTest.function) == "foo_bar"


def test_with_spy(mocker):
    url = "https://2021.es.pycon.org/"
    spy = mocker.patch.object(requests, "get", wraps=requests.get)
    response = requests.get(url)
    assert response.status_code == 200
    spy.assert_called_once(), spy.mock_calls
    spy.assert_called_with(url)


def test_with_better_spy(mocker):
    url = "https://2021.es.pycon.org/"
    spy = mocker.spy(requests, "get")
    response = requests.get(url)
    assert response.status_code == 200
    spy.assert_called_once(), spy.mock_calls
    spy.assert_called_with(url)