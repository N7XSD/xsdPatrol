"""
Sometimes we write things that we hope will go away.
Those things belong here.
"""

import common
import db_dispatch

class UglyHacks():
    """
    We're not even giving our ugly hacks real names
    """

    def __init__(self, cmn):
        self.cmn = cmn

    def hack_one(self):
        """
        Print a list of User_IDs and User_names usable for a Python
        dictonarey.
        """

        dispatch_db = db_dispatch.DispatchDB(cmn)
        rc = dispatch_db.open_dispatch_db()
        if not rc:
            print("Can't open DB")
            return
        sql_statement = """
            SELECT User_ID, User_Name
            FROM Users
            ORDER BY User_ID"""
        print(sql_statement)
        print()
        dispatch_db.curs_disp.execute(sql_statement)
        rows = dispatch_db.curs_disp.fetchall()
        for i in rows:
            u = "'" + i.User_ID + "',"
            print(f"999: {u:<16} # {i.User_Name}")
        return


if __name__ == '__main__':
    cmn = common.Common()
    ugly = UglyHacks(cmn)
    ugly.hack_one()
