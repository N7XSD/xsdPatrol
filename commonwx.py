"""
wxPython (GUI) frame for xsdPatrol
"""

#pylint: disable=too-many-locals
#pylint: disable=too-many-statements

#import datetime
import logging
import wx
import wx.html

import common


class ShowHTML(wx.Frame):
    """
    Class for simple HTML viewer
    """

    def __init__(self, parent, cmn, html_content, title):
        wx.Frame.__init__(self, parent, title=title)
        html_window = wx.html.HtmlWindow(self)
        html_window.SetPage(html_content.read())
        self.SetSize(wx.Size(512, 512))


class CommonFrame(wx.Frame):
    """
    Base class for xsdPatrol frames
    """

    def __init__(self, parent, cmn):
        self.cmn = cmn
        wx.Frame.__init__(self, parent)
        self.pnl = wx.Panel(self)

        # Create the menubar
        menu_bar = self.create_menu_bar()
        self.SetMenuBar(menu_bar)

        # Layout sizers
        sizer_main = self.create_sizer_main()
        self.pnl.SetSizer(sizer_main)
        self.pnl.SetAutoLayout(1)
        sizer_main.Fit(self)

        self.SetTitle("Your Message Here")
        self.SetMinSize(wx.Size(256, 256))
        self.Show()

    def create_file_menu(self):
        """Create the File menu"""

        # Note: Exit is moved to the application menu in macOS
        exit_mitem = wx.MenuItem(None, wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_mitem)

        this_menu = wx.Menu()
        this_menu.Append(exit_mitem)
        return this_menu

    def create_help_menu(self):
        """Create the Help menu"""

        # Note: About is moved to the application menu in macOS
        about_mitem = wx.MenuItem(None, wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.on_about, about_mitem)

        this_menu = wx.Menu()
        this_menu.Append(about_mitem)
        return this_menu

    def create_menu_bar(self):
        """Create the menu bar"""

        menu_bar = wx.MenuBar()
        menu_bar.Append(self.create_file_menu(), "&File")
        menu_bar.Append(self.create_help_menu(), "&Help")

        return menu_bar

    def create_sizer_bottom_buttons(self):
        """Create a sizer to hold the buttons"""

        # Static text

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.
        cancel_button = wx.Button(self.pnl, wx.ID_CANCEL)
        exit_button = wx.Button(self.pnl, wx.ID_EXIT)

        # Bind widgets to methods
        self.pnl.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)
        self.pnl.Bind(wx.EVT_BUTTON, self.on_exit, exit_button)

        this_sizer = wx.BoxSizer(wx.HORIZONTAL)
        this_sizer.AddStretchSpacer()
        this_sizer.Add(cancel_button, 0)
        this_sizer.Add(exit_button, 0)

        return this_sizer

    def create_sizer_heading(self):
        """Create a sizer to hold some text at the top of our frame"""

        # Static text
        label_common_frame = wx.StaticText(self.pnl, label="We Are Here")

        # Create text controls, check boxes, buttons, etc.
        # in tab traversal order.

        # Bind widgets to methods

        this_sizer = wx.BoxSizer(wx.VERTICAL)
        this_sizer.Add(label_common_frame, 0)

        return this_sizer

    def create_sizer_main(self):
        """The main sizer holds everthing the user will interact with"""

        # Use a vertical sizer to stack our window
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(self.create_sizer_heading(),
            1, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())
        sizer_main.Add(self.create_sizer_bottom_buttons(),
            0, wx.EXPAND | wx.ALL,
            border=self.cmn.stns.get_widget_border_size())

        return sizer_main

    def on_about(self, _event):
        """Create a message dialog box"""
        dlg = wx.MessageDialog(self,
            "About text.",
            "About Box Title", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished

    def on_cancel(self, _event):
        """Cancel"""
        self.Destroy()  # Close the frame

    def on_exit(self, _event):
        """Exit"""
        self.Close()  # Close the frame


if __name__ == '__main__':
    common.init_logging()
    common_stuff = common.Common()
    stns = common_stuff.stns
    app = wx.App(False)
    frame = CommonFrame(None, common_stuff,
        "Base for xsdPatrol")
#    frame.SetPosition(stns.get_window_pos_time())
#    frame.SetSize(stns.get_window_size_time())
    app.MainLoop()
