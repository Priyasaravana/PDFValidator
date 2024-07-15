import logging

def setup_logging():
    """
    Setup basic logging configuration.
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def get_logger(name: str):
    """
    Get a logger instance with the specified name.
    
    Args:
    - name (str): Name of the logger.
    
    Returns:
    - logger (logging.Logger): Configured logger instance.
    """
    setup_logging()
    return logging.getLogger(name)
