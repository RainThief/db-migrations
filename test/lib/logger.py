"""logging wrapper module"""

from robot_support.logger import Logger


def set_level(level: str) -> None:
    """set logging level

    Args:
        level: logging level description
    """
    Logger.get_instance().set_level(level)



def set_file_path(path: str) -> None:
    """set logging level

    Args:
        level: logging level description
    """
    Logger.get_instance().set_file_log(path)
