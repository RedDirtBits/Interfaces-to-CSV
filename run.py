import time
import csv

from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from ntc_templates.parse import parse_output
from datetime import datetime

from helpers.constants import Constant
from helpers.validation import ip4_validate
from helpers.ping import ip4_ping
from helpers.open_file import open_device_list_file
from helpers.logs import logging
from helpers.commands import RunCommand
from credentials.credentials import GetCredentials


# Set a starting timer.  Mainly for initial testing
START_TIME = time.time()
TIMESTAMP = datetime.now().strftime("%m-%d-%Y_T%H:%M:%S")

# The first log entry when the application starts will deliniate when it
# has started and the root directory in which the script is running

logging.info("#" * 25 + " Application Starting " + "#" * 25 + "\n")
logging.info(f"Working Directory: {Constant.script_path()}\n")

# Loop through the file containg the devices to be connected to and create the connection
# profile
for device in open_device_list_file(Constant.devices_list() / "devices.txt"):

    # As a sanity check validate that the IP address is, in fact, a valid IP address then
    # ping it to see if it can be reached.  If either fails, abort the process
    if ip4_validate(device[0]) and ip4_ping(device[0]):

        device_ssh_connection = {
            "host": device[0],
            "device_type": device[1],
            "username": GetCredentials.netlab_user(),
            "password": GetCredentials.netlab_passwd(),
            "secret": GetCredentials.netlab_enable()
        }

        logging.info(f"Created SSH Connection profile for {device[0]}")

        try:

            # Only running a single command
            command = RunCommand.show_interfaces_all()

            # Connect to the device
            with ConnectHandler(**device_ssh_connection) as ssh_connection:
                
                # Activate enable mode
                ssh_connection.enable()
                # Grab the hostname.  Assumes the name at the command prompt is the hostname
                hostname = ssh_connection.find_prompt()[:-1]
                # Store the raw output of the command run in a variable
                raw_output = ssh_connection.send_command(command)

                logging.info(f"Console Output for {device[0]} running command: {command}\n\n{raw_output}")

                # Parse the command output into a format that is easier to work with
                formatted_output = parse_output(platform="cisco_ios", command="show ip interface brief", data=raw_output)

        except NetmikoAuthenticationException:
            logging.error(f"Authentication failed. Invalid username or password for {device[0]}. Please verify your credentials")
        except NetmikoTimeoutException:
            logging.error(f"Connection time out for {device[0]}")
        except ValueError:
            logging.error(f"Failed to enter privilege mode! Please check the enable password for device {device[0]}")

    else:
        logging.error(f"Failed to create a connection profile for {device[0]}")
        continue

try:
    # Open a CSV file whose filename is taken from the hostname
    with open(f"{hostname}_ifaces.csv", "w") as csv_file:

        logging.info(f"Created CSV file {hostname}_ifaces.csv")

        # Create the header row names
        field_names = ["INTERFACE", "IP ADDRESS", "STATUS", "PROTOCOL"]
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

        # Loop through the formatted output of the command.  The advantage of parsing the output
        # We can now loop through it.  Its a dictionary so grab the values and write them to the CSV
        # rows
        for interface in formatted_output:
            writer.writerow({
                "INTERFACE": interface["intf"],
                "IP ADDRESS": interface["ipaddr"],
                "STATUS": interface["status"],
                "PROTOCOL": interface["proto"]
                })
except ValueError:

    # If the field names don't match names in the writerow action, it will throw a ValueError
    logging.error(
        f"There was an error when trying to write to the CSV file.\n \
        If it contains only the header row, check the writerow field names"
        )


# for enum, interface in enumerate(formatted_output):
#     print(enum, interface)
# print(formatted_output[35]["intf"])

END_TIME = time.time()

logging.info("#" * 25 + " Application Finished " + "#" * 25 + "\n")
logging.info(f"Script Execution took {END_TIME - START_TIME} seconds")
