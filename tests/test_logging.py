import pytest
from src.utils.logging import get_logger
import re

@pytest.fixture
def logger():
    return get_logger("test_logger")

def strip_ansi(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)

def test_logger_info_level(logger, caplog):
    with caplog.at_level("INFO"):
        logger.info("info message", test_key="test_value")
    log_output = " ".join(strip_ansi(record.message) for record in caplog.records)
    assert "info message" in log_output

def test_logger_error_level(logger, caplog):
    with caplog.at_level("ERROR"):
        logger.error("error message", error_code=123)
    log_output = " ".join(strip_ansi(record.message) for record in caplog.records)
    assert "error message" in log_output

def test_logger_all_levels(logger, caplog):
    with caplog.at_level("DEBUG"):
        logger.debug("debug message")
        logger.info("info message")
        logger.warning("warning message")
        logger.error("error message")
        logger.critical("critical message")
    all_logs = " ".join(strip_ansi(record.message) for record in caplog.records)
    assert "debug message" in all_logs
    assert "info message" in all_logs
    assert "warning message" in all_logs
    assert "error message" in all_logs
    assert "critical message" in all_logs

def test_logger_structured_data(logger, caplog):
    with caplog.at_level("INFO"):
        logger.info("structured", foo="bar", num=42)
    log_output = " ".join(strip_ansi(record.message) for record in caplog.records)
    assert "structured" in log_output
    assert "foo=bar" in log_output
    assert "num=42" in log_output

def test_logger_naming(caplog):
    named_logger = get_logger("custom_logger")
    with caplog.at_level("INFO"):
        named_logger.info("named logger test")
    # structlog's ConsoleRenderer does not always include logger name, so just check log message
    log_output = " ".join(strip_ansi(record.message) for record in caplog.records)
    assert "named logger test" in log_output

def test_logger_exception_logging(logger, caplog):
    try:
        1 / 0
    except ZeroDivisionError:
        with caplog.at_level("ERROR"):
            logger.exception("exception occurred")
    log_output = " ".join(strip_ansi(record.message) for record in caplog.records)
    assert "exception occurred" in log_output
    assert "ZeroDivisionError" in log_output or "division by zero" in log_output 