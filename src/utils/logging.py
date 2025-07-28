import logging
import sys

# Fallback logging setup when structlog is not available
def setup_fallback_logging():
    """Setup basic logging when structlog is not available."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger()

try:
    import structlog
    
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

except ImportError:
    # Fallback to standard logging if structlog is not available
    setup_fallback_logging()
    
    def get_logger(name: str = None):
        """
        Returns a standard logger when structlog is not available.
        Args:
            name (str): Optional logger name.
        Returns:
            logging.Logger
        """
        return logging.getLogger(name) if name else logging.getLogger() 