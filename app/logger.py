import structlog


def configure_structlog():
    """
    Configures structlog which will be used through the entire code.
    """
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )


def wrap_async(logger) -> structlog.stdlib.AsyncBoundLogger:
    """
    Wraps the log to allow async calls. This will cause overhead for each logging but log calls will not block other threads from running.
    """
    return structlog.wrap_logger(logger, wrapper_class=structlog.stdlib.AsyncBoundLogger)
