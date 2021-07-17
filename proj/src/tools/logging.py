"""app logging"""
import logging


class Loging:
    """class Loging"""

    @staticmethod
    def debug(name, message):
        """write logfile of winners"""
        logging.basicConfig(
            format="%(asctime)s:%(levelname)s:%(name)s - %(message)s",
            level=logging.DEBUG,
            filename="./src/logs/logs.log",
        )
        logger = logging.getLogger(__name__)
        logger.debug(f"{message} : {name}")

    @staticmethod
    def info(name, message):
        """write logfile of winners"""
        logging.basicConfig(
            format="%(asctime)s:%(levelname)s:%(name)s - %(message)s",
            level=logging.INFO,
            filename="./src/logs/logs.log",
        )
        logger = logging.getLogger(__name__)
        logger.info(f"{message} : {name}")

    @staticmethod
    def exept(message):
        """write logfile of winners"""
        logging.basicConfig(
            format="%(asctime)s:%(levelname)s:%(name)s - %(message)s",
            level=logging.DEBUG,
            filename="./src/logs/logs.log",
        )
        logger = logging.getLogger(__name__)
        logger.exception(message)


loging = Loging()
