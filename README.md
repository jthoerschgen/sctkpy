# The Scholarship Chairman's Toolkit 📚 

The Scholarship Chairman's Toolkit (_SCTK_) is a collection of Python scripts for automating regular duties of a fraternity's (or any student organization's) scholarship chairman. Specifically, this tool is designed to generate reports and paperwork from grade and member roster data provided from the [Missouri S&T Greek Life Management Tool](https://involvement.mst.edu/fraternityandsororitylife/greek-resources/memberresources/).

## Features

- Generate Grade Report Spreadsheets with individual term GPA's and corresponding study hours that accommodates for members going on CO-OP or otherwise dropping below full-time status
- TODO Study check sheets
- Files checklist
- TODO Generate Reports of member GPA overtime

## Usage Guide

To begin using SCTK download the __Membership Roster Report__ and __Individual Grade Report__ (select _Include class details in download file_ as well) from the [S&T Greek Life Management Tool](https://involvement.mst.edu/fraternityandsororitylife/greek-resources/memberresources/). The Membership Roster will save as _greeklife_roster_report.csv_, and each grade report will save as _ind_grade_report.csv_.

- Save _greeklife_roster_report.csv_ to the root directory of this repository.
- Save each _ind_grade_report.csv_ into the _./gradereports/_ directory.

### Report Structure

- The __Membership Roster Report__ data starts on row 4 and has the following columns:
  - Last Name
  - First Name
  - Chapter Name*
  - in/out House
    - Value will either be "IN" or "OUT"
  - Email
  - Term*
    - Value will be either SPXXXX or FSXXXX (e.g. SP2024)

- The __Individual Grade Report__ data starts on row 3 and has the following columns:
  - Name
  - Term*
    - Value will be either SPXXXX or FSXXXX (e.g. SP2024)
  - Chapter*
  - New Member
  - Enroll Hrs
  - Priv GPA
  - Priv Cum GPA
  - Term GPA
  - Term Cum GPA
  - Class
  - Catalog No
  - Hrs
  - Grade
  - Grade Type

`*all values in column are expected to be the same`

### Adding New Members and Removing Old Ones

If your chapter has new members who are not otherwise on the Membership Roster Report you will need to add their information to the bottom of the CSV file and save it. Ensure that the first and last names are those the campus has on file (no nicknames). The report file is used to determine what members reports are generated for. Additionally, if you need to remove a member simply delete their row from the roster report CSV.
