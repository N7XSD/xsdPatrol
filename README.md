# xsdPatrol
Next generation of software to support SCS Patrol. 

As of September 2025, Patrol volunteers use multiple applications
and spreadsheets for their work.  xsdPatrol modules will, in time, replace
existing applications.

### Goals
* FOSS with repository on Github.
* Run software on Windows, Linux, and macOS.
* Store data in MS Access or MariaDB.
* Customizable through SQL tables and config files.

### Priorities
1.  Automate paper processes.
1.  Replace spreadsheets with Python applications.
1.  Replace MS Access forms and reports with python applications.
1.  Replace Dispatch and Watch Commander Visual Basic logging
    applications with Python applications.
1.  Migrate data to MariaDB.

## Ticket Tracking Module
The paper process is a single page Ongoing Event Report
(OER, AKA pink sheet).  Events that will have to be tracked by
multiple shifts are recorded on the form.  The form has room
for updates and is discarded when the event is no longer active.

The Ticket application will present a window that is similar to
the paper form.  The ticket is opened by selecting an initial
event. Information needed for the ticket that is not available
in the event is added by the user (often the dispatcher).
Follow up events can be added to the ticket.

The application can print a report similar to the manual form.

Events must be edited in the Dispatch or Watch Commander applications.

### Changes required for DispatchDB
* Add a "Tickets" table.
* Add a "Responder" table to map an integer to a name.
* Add a "Consoles" table to map an integer to a name.

## Time Reporting Module
Timekeepers enter hours credited to members into an Excel workbook.
The workbook holds data for one year and has sheets for each month.
Hours for a week are entered as formulas so Excel can do the sums.
Sheets are written to PDF to provide reports for members.

Data is collected by reading printed dispatch logs.

### Minimal Requirements
Give the timekeepers something better than paging through the log book. 
* Read the previous week's dispatch logs. 
* Collect the names of each person who worked and provide a sum of hours. 
* Create a simple report that can be printed or emailed. A window that allows text to be copied is good enough. Look at wx.ListCtrl and wx.dataview.DataViewCtrl.
* Run from an icon on the desktop. 

### Additions
* Sanity check hours
    * Calculate expected hours for each shift
    * Print exceptions when they don't match
    * Print both entered and calculated hours
* Produce a simple CSV report
* Sanity check names
    * Read active members from MemberDB
    * Mark dispatch log names that are not active members
    * Produce separate report IT Officer and Personnel  can use to harmonize names
* GUI interface to allow Timekeepers to edit data
* Allow Timekeepers to enter data
    * This may require separate forms for meetings, etc. 
    * Create form to accept CSV files from the web and require Timekeeper acceptance
* Produce HTML "Hours Monthly" report
* Produce HTML "Hours Summary" report
* Produce report for awards officer
* Allow awards officer to edit awards level
* Limit data editing to appropriate people
* Keep time data in PatrolDB

