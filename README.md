# The Scholarship Chairman's Toolkit 📚

The Scholarship Chairman's Toolkit is a collection of Python scripts designed to automatically generate academic reports. These reports use grade/roster data provided from the Missouri University of Science and Technology, and evaluate the data using guidelines from the Standing Rules and Legislation of Eta Chapter of Beta Sigma Psi.

## Report Types

There are four types of reports which can be generated using this program. These reports types are the following.

### Study Hour Report

This report is outlines what academic probations/study hours each member has for a given term. The specific GPA ranges for each academic probation is printed in the report's key. The average GPA for the house and each pledge class is also provided in this report. This report is designed to be sent out to the entire chapter.

### Study Check Report

This report is a checklist used for enforcing study hours. You may need to make changes to the generated spreadsheet for member's on two study hours who wish to move their study hours to the second half.

### Files Due List Report

This report groups all of the members who are enrolled in the same class together as a master checklist for keeping track of what files have been submitted and checked off.

### Membership/Strikes Report

This report aggregates all of the campus grade report data for each member. There is a master sheet which counts all of the academic strikes/super strikes each member has. There are also subsequent sheets for each member, with a summary of all of their courses/grades and their GPA for each term. This report is not meant to be shared with the entire chapter.

## Acquiring Data

In order to access roster/grade data you must have access as an officer to the [S&T Greek Life Management Tool](https://involvement.mst.edu/fraternityandsororitylife/greek-resources/memberresources/). Here, you will have access to download the _Membership Roster Report_ and _Individual Grade Reports_. The chapter may have archives of these as well.

### Greeklife Roster Report

The roster report will be a file named: _greeklife_roster_report.csv_, and will contain a list of info of all the active/associate members.

The header for the roster will be on _row four_ of the csv file, and is expected to have the following columns:

- "Last Name"
- "First Name"
- "Chapter Name"*
- "in/out House", _(Values will either be "IN" or "OUT")_
- "Email"
- "Term"*, _(Values will be in the format: "SPXXXX" or "FSXXXX", e.g. "SP2024")_

_*all rows in this column are expected to share the same value_

### Individual Grade Reports

The grade data will be from _FS/SPXXXX_ind_grade_report.csv_ files. For the program to work as intended, please provide grade reports for as far back as the earliest term any member being evaluated has been a member.

The header for each grade report will be on _row three_ of the csv file, and is expected to have the following columns:

- "Name"
- "Term"*, _(Values will be in the format: "SPXXXX" or "FSXXXX", e.g. "SP2024")_
- "Chapter"*
- "New Member", _(Values will either be "Y" or "N")_
- "Enroll Hrs"
- "Priv GPA"
- "Priv Cum GPA"
- "Term GPA"
- "Term Cum GPA"
- "Class"
- "Catalog No"
- "Hrs"
- "Grade"
- "Grade Type"

_*all rows in this column are expected to share the same value_

Do not be concerned with deleting records from older reports over members who are no longer active in the house. The roster is used to determine which grade data from older grade reports should be used.

If the data in the roster/grade reports does not have a header in the correct starting row, or any column label is misspelled, or any data which is expected to be in the format described above is not, then the program will throw an error.

You are able to modify either the roster/grade reports and see the changes reflected in the reports you generate using this program.

## Configuration

For making changes to the GPA thresholds for evaluating different levels of academic probation, modify the values in `.\sctkpy\sctkpy\config.toml`

## Using the Command-Line Tool

The command-line tool provides an easy to use interface for generating academic reports using the campus provided grade data.

To use the command-line tool in a _powershell_ window, execute the following command:

```powershell
.\sctkpy-cli.exe  --report-type TYPE --roster .\path\to\_greeklife_roster_report.csv --report-dir .\path\to\ind_grade_reports --save-dir .\path\where\report\saved --term TERM
```

The following are explanations of each option/flag required by the command-line tool.

### Report Type Options

To specify what kind of report you wish to generate, use one of the following options following the `--report-type` flag.

- Study Hour Report: __"study-hours"__
- Study Check Report: __"study-checks"__
- Files Due Report: __"files-list"__
- Member/Strikes Report: __"member-report"__

### Roster Path Flag

The `--roster` flag requires a path to the _greeklife_roster_report.csv_ file you wish to use for generating your report.

### Report Directory Flag

The `--report-dir` flag requires a path to a folder/directory of the _FS/SPXXXX_ind_grade_report.csv_ files you are using to generate your report.

### Save Directory Flag

The `--save-dir` flag specifies which folder/directory you want to save the generated report into.

### Term Flag

The `--term` flag specifies which term you want to generate the report from. The term must be in the format: _"SPXXXX"_ or _"FSXXXX"_. A valid example for a term would be _"FS2021"_. If you use a previous term, the report will still only generate for the member specified in the Greeklife Roster Report.

## Disclaimer

The design for all of the reports generated by the project are with the policy as of 2024 in mind. Any changes to the policy may require modifications. To request any modifications to the reports contact `jthoerschgen@gmail.com`, or otherwise make the modifications to this open-source project yourself.