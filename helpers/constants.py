import pathlib
import random
import string
from datetime import datetime


class Constant():
    """
    Constant A class with simple static methods to return paths to various parts
    of the environment, and a timestamp

    Returns:
        root_path str: Project root path
        script_path str: file path
        devices_list str: Path to file that contains the device(s) list
        timestamp str: timestamp in month-day-Year_Hour:Minutes:Seconds format
        create_id str: ID created from a random selection of ascii characters
    """

    @staticmethod
    def root_path():
        return pathlib.Path(__file__).parent

    @staticmethod
    def script_path():
        return pathlib.Path(__file__).parent.parent

    @staticmethod
    def devices_list():
        file_path = pathlib.Path(Constant.script_path())
        return file_path

    @staticmethod
    def timestamp():
        return datetime.now().strftime("%m-%d-%Y_T%H:%M:%S")

    @staticmethod
    def create_id():
        return "".join(random.choices(string.ascii_letters, k=12))


