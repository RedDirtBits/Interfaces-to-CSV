
class RunCommand():
    """
    RunCommand A simple class similar to the one used for credentials.  Static methods to return commands
    to be run on Cisco devices

    Returns:
        show_routes str: show ip route
        show_routes_minimal str: show ip route | b Gateway
        show_interfaces_all str: show ip interface brief
        show_up_interfaces str: show ip interface brief | i up
    """

    @staticmethod
    def show_routes():
        return "show ip route"

    @staticmethod
    def show_routes_minimal():
        return "show ip route | b Gateway"

    @staticmethod
    def show_interfaces_all():
        return "show ip interface brief"

    @staticmethod
    def show_up_interfaces():
        return "show ip interface brief | i up"