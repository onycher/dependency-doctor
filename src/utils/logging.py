import structlog
import logging

# Configure structlog for console output with timestamps and log levels
logging.basicConfig(
    format="%(message)s",
    stream=None,
    level=logging.INFO,
)

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.dev.ConsoleRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

def get_logger(name: str = None):
    """
    Returns a structlog logger instance.
    Args:
        name (str): Optional logger name.
    Returns:
        structlog.BoundLogger
    """
    return structlog.get_logger(name) if name else structlog.get_logger() 