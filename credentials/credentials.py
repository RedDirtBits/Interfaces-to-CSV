from dotenv import load_dotenv
import os

load_dotenv()

class GetCredentials():

    """
     GetCredentials A simple class that creates static methods that returns credentials to be
     used for logging into a network device.  Mainly to abstract away from the 
     .env file a bit more

    Returns:
        netlab_user str: SSH username
        netlab_passwd str: SSH password
        netlab_enable str: enable password
    """

    @staticmethod
    def netlab_user():
        return os.environ.get("NETLAB_USER")

    @staticmethod
    def netlab_passwd():
        return os.environ.get("NETLAB_PASSWD")

    @staticmethod
    def netlab_enable():
        return os.environ.get("NETLAB_ENABLE")

