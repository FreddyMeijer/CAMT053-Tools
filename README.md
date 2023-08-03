# CAMT053 Tools
Welcome to the CAMT053 tools repo. I am Freddy Meijer and at the time business engineer at Leiden. In a Betty Blocks application we retrieve information from the bank in a CAMT053 XML file. In this repo you find serveral tools to work with those files.
## Installation
To install the CAMT053 Tools al you need to do is:

- Download and install an instance of Python
- Open your terminal navigate to the desired folder and use `git clone https://github.com/FreddyMeijer/CAMT053-Tools.git`
- Open the folder in which the git was cloned
- Run `pip install -r requirements.txt`
- Run the desired function by using e.g. `python CAMT053ExtractTotals.py`
## .gitignore
The gitignore file states that .csv and .xml files will not be uploaded through git. The information in the files is personal en thereby protected under GDPA regulations. So the files itself should never be uploaded on GitHub.

## CAMT053Summary
There are serveral bugs reported in Leiden in which a CAMT053 file had serveral entries of another day. This may not occur. So with this tool, the CAMT053 file is evaluated. The element *Stmt* must be unique. So, there should only be once in the file. The user selects a file and the code checks how many times *Stmt* is in the file. The report is saved on the same place as the CAMT053. The report shows something like:

`**************************************************************************************************************************************************************
RAPPORT CAMT053 BESTAND
Bestand: 01abf918-302b-11ee-a98a-220ec8f976df-2023-07-21_CAMT053_NL57INGB0004207048_EUR_479651.xml
Datum: 03-08-2023
**************************************************************************************************************************************************************

Stmt komt 1 keer voor. Het betreft het bestand van 1 dag. Het bestand kan je inlezen in PAL21

**************************************************************************************************************************************************************
EINDE RAPPORTAGE
**************************************************************************************************************************************************************`

When the report states there are more than 1 Stmt elements, please download the CAMT053 again from the bank. 

## CAMT053ToCSV
The Python code to tanslate the XML to CSV is devided in three functions:

- parse_camt053_xml
Through naming the path (like XPath) the code will search the textelements in serveral XML elements. The information is saved in transactions.

- write_to_csv
This is the function which writes a header and the transactions to a file.

- selectfile
This is the function which asks the user to select a CAMT053 file. The location on which the CAMT053 is retrieved, the CSV will be saved.