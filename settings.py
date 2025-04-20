"""
xsdPatrol settings
"""

#pylint: disable=too-few-public-methods
#pylint: disable=too-many-instance-attributes

import configparser
import datetime
import logging

ID_NAME = "xsdPatrol"
ID_VER = "Very early development"

#Logging levels are: CRITICAL, ERROR, WARNING, INFO, and DEBUG.
LOGGING_LEVEL = logging.DEBUG
LOGGING_FILE = 'xsdPatrol.log'


class Settings():
    """
    Manage application Settings
    """
    def __init__(self):
        logging.debug("Init settings.Settings")

        self.config = configparser.ConfigParser()

        # Defaults to access data
        self.config['data'] = {'dispatch_db':
            r"/Users/josep/SCS Patrol server copies/SecurityLogDB2/SecurityLog.mdb"}

        self.config['date'] =  {'first_watch': '2009-04-12'}

        # Time formatting variables
        self.config['format'] = {
            'date': '%%Y-%%m-%%d',
            'time': '%%H:%%M',
            'datetime': '%%Y-%%m-%%d %%H:%%M'}

        self.gear_default = ["Radio-A", "Radio-B", "Radio-C",
                "Radio-D", "Radio-E", "Radio-F",
                "Radio-R", "Radio-S", "Radio-T",
                "Flashlight-1", "Flashlight-2", "Flashlight-3",
                "Flashlight-4", "Flashlight-5", "Flashlight-6"]
        self.shift_names = ["1", "2", "3"]
        self.watch_names = ["1", "2"]

        self.initial_window_position = (32, 32)
        self.initial_window_size = (600, 200)

        # Don't allow users to edit these fields
        self.table_users_fixed_fields = ["User_ID"]

        # Don't show users these fields
        self.table_users_hidden_fields = ["Password",
            "Last_Change_Date", "Last_Change_By",
            "Rec_Version"]

        self.widget_border = 8
        
        with open('xsdPatrol.ini', 'w') as configfile:
            self.config.write(configfile)
            
    def get_pathname_dispatch_db(self):
        return self.config['data']['dispatch_db']

    def get_format_date(self):
        """Return date format"""
        return self.config['format']['date']

    def get_format_time(self):
        """Return time format"""
        return self.config['format']['time']

    def get_format_datetime(self):
        """Return datetime format"""
        return self.config['format']['datetime']

if __name__ == '__main__':
    stns = Settings()
