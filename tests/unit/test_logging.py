import logging
default_logger = logging.getLogger(__package__)


def func_one(logger=default_logger):
    logger.info("one")

def func_two(logger=default_logger):
    logger.info("two")

def another():
    """dummy class to decorate"""


def test_one(caplog):

    with caplog.at_level(logging.INFO, logger=__package__):
        func_one(logger=default_logger)
    assert "one" in caplog.text

def test_two(caplog):
    """No logs are expected with this capture"""
    with caplog.at_level(logging.ERROR, logger="same"):
        func_two()
        func_two(logger=logging.getLogger("same"))
    assert caplog.record_tuples == []

def test_three(caplog):

    with caplog.at_level(logging.INFO, logger=__package__):
       func_one()
       func_two()
    assert len(caplog.record_tuples) == 2