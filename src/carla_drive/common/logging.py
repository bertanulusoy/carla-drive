import logging

def get_logger(name: str):
    """Create and return a logger with the given name."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


if __name__ == "__main__":
    logger = get_logger("test")
    logger.info("Logging modülü çalışıyor!")
    logger.debug("Bu bir debug mesajı")
    logger.warning("Bu bir uyarı mesajı")