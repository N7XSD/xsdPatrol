"""
wxPython (GUI) for accessing MemberDB
"""

import logging
import wx

import common
import commonwx

class Import(commonwx.CommonFrame):
    """
    Frame for importing data from MemberDB
    """

    def __init__(self, parent, cmn):
        title = "Import from MemberDB"
        commonwx.CommonFrame.__init__(self, parent, cmn, title)
        logging.debug("Init wx_member.Import")

        members = self.cmn.member_db.get_members()
        print(len(members))

#       active_members = self.cmn.member_db.get_active_members()
#       sorted_members = dict(sorted(active_members.items()))
#       for i_key, i_value in sorted_members.items():
#           print(f"{i_key}: {i_value}")

        self.Show()
