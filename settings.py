"""
xsdPatrol settings
"""

#pylint: disable=too-few-public-methods
#pylint: disable=too-many-instance-attributes

import configparser
import datetime
import logging

ID_NAME = "xsdPatrol"
ID_VER = "0.0"
ID_CONF_VER = "1"

#Logging levels are: CRITICAL, ERROR, WARNING, INFO, and DEBUG.
LOGGING_LEVEL = logging.DEBUG
LOGGING_FILE = 'xsdPatrol.log'


class Settings():
    """
    Manage application Settings
    """
    def __init__(self):
        logging.debug("Init settings.Settings")

        # Someday we'll read in a file and not have to
        # depend on the defaults.
        self.config = configparser.ConfigParser()
        self.config['xsdPatrol'] = {}
        self.config.set('xsdPatrol', 'name', ID_NAME)
        self.config.set('xsdPatrol', 'version', ID_VER)
        self.config.set('xsdPatrol', 'config-file-version', ID_CONF_VER)

    def _get(self, sect, key, def_val, val_type=None):
        try:
            section = self.config[str(sect)]
            val = section.get(str(key), str(def_val))
            # This is where we should test to see if our value should be
            # a list and do the conversion.  Tuples may also need some love.
        except KeyError:
            val = def_val
        if val_type == 'int':
            val = int(val)
        elif val_type == 'date':
            val = datetime.datetime.fromisoformat(val)
        elif val_type == 'list':
            val = val.split()
        return val

    def get_first_watch(self):
        return self._get('date', 'first-watch', '2009-08-14', 'date')

    def get_format_date(self):
        """Return date format"""
        return self._get('format', 'date', '%Y-%m-%d')

    def get_format_time(self):
        """Return time format"""
        return self._get('format', 'time', '%H:%M')

    def get_format_datetime(self):
        """Return datetime format"""
        return self._get('format', 'datetime', '%Y-%m-%d %H:%M')

    def get_gear(self):
        return self._get('resources', "gear", [
            "Radio-A", "Radio-B", "Radio-C",
            "Radio-D", "Radio-E", "Radio-F",
            "Radio-R", "Radio-S", "Radio-T",
            "Flashlight-1", "Flashlight-2", "Flashlight-3",
            "Flashlight-4", "Flashlight-5", "Flashlight-6"])

    def get_names_shift(self):
        # Watches are divided into named shifts of equal length
        return self._get('resources', 'shift-names', "1 2 3", "list")

    def get_names_watch(self):
        # Days are divided into named watches of equal length
        return self._get('resources', 'watch-names', "1 2", "list")

    def get_pathname_dispatch_db(self):
        """Return full pathname for Dispatcher/WC log DB"""
#       default = r"//SERVER/SecurityLogDB2/SecurityLog.mdb"
        default = r"/Users/josep/SCS-Patrol-data/SecurityLogDB2/SecurityLog.mdb"
        return self._get('data', 'dispatch-db', default)

    def get_pathname_member_db(self):
        """Return full pathname for member DB"""
        return self._get('data', 'member-db',
            r"/Users/josep/SCS-Patrol-data/MemberDB/"
            + r"SPMemberDB.accdb")

    def get_window_pos_time(self):
        return self._get('window', 'time-window-position', (32, 32))

    def get_window_size_time(self):
        return self._get('window', 'time-window-size', (600, 200))

    def get_widget_border_size(self):
        return self._get('window', 'widget-border-size', 8,
            val_type='int')

    def write_ini(self):
        with open('xsdPatrol.ini', 'w') as configfile:
            self.config.write(configfile)


if __name__ == '__main__':
    stns = Settings()

    print(stns.get_first_watch())
    print(stns.get_format_date())
    print(stns.get_format_datetime())
    print(stns.get_format_time())
    print(stns.get_gear())
    print(stns.get_names_shift())
    print(stns.get_names_watch())
    print(stns.get_pathname_dispatch_db())
    print(stns.get_widget_border_size())
    print(stns.get_window_pos_time())
    print(stns.get_window_size_time())
    print()
    stns.write_ini()
