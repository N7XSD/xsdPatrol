"""
wxPython (GUI) interface for xsdPatrol personnel module
"""

# This is not a serious attempt at writing the personnel module but
# I needed a place for a quick and dirty report.

import datetime
import logging

import common
#import data
#import settings


# Someday this wil be simple CLI for a Timekeeping module.
# Today it's a place to keep a Q+D report I needed.
if __name__ == '__main__':
    common.init_logging()
    cmn = common.Common()

    # Header
    print("Compare Users In Dispatch DB And Member DB")
    print("==========================================")
    print()

    cmn.dat.open_dispatch_db()
    users_dis_dict = cmn.dat.get_active_disp_users()
    print(f"Active Dispatch Users:  {len(users_dis_dict)}")

    cmn.dat.open_member_db()
#   users_member_dict = cmn.dat.get_active_members_users()
#   print(f"Active Members:  {len(users_member_dict)}")
#   print()
    print()

#   print("### Active Members in Dispatch DB not active in Member DB")
    print("### Active Members in Dispatch DB")
    print()
    for i in sorted(users_dis_dict, key=users_dis_dict.get):
        print(f"{i:16} {users_dis_dict[i]}")
