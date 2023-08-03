import csv
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

def parse_camt053_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    transactions = []
    for entry in root.findall('.//{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}Stmt/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}Ntry'):
        txn_data = {
            'Referentienummer': entry.find('{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}NtryRef').text,
            'Bedrag': entry.find('{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}Amt').text,
            'CreditDebet': entry.find('{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}CdtDbtInd').text,
            'Valutadatum': entry.find('{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}ValDt/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}Dt').text,
            'Debiteur': entry.findtext('{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}NtryDtls/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}TxDtls/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}RltdPties/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}Dbtr/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}Nm'),
            'IBAN': entry.findtext('{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}NtryDtls/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}TxDtls/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}RltdPties/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}DbtrAcct/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}Id/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}IBAN'),
            'Betaalkenmerk':entry.findtext('{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}NtryDtls/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}TxDtls/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}RmtInf/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}Ustrd')
            # Add more fields as needed
        }
        transactions.append(txn_data)

    return transactions

def write_to_csv(transactions, csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Referentienummer','Bedrag','CreditDebet','Valutadatum','Debiteur','IBAN','Betaalkenmerk'])
        writer.writeheader()
        writer.writerows(transactions)

def selectFile():
    File=filedialog.askopenfilename(
        title="Selecteer het CAMT053 Bestand",
        filetypes=[("Bankbestanden","*.xml"),("Alle bestanden","*.*")]
    )
    if File:
        return File

if __name__ == '__main__':
    xml_file = selectFile()
    csv_file = xml_file.replace('.xml', '.csv')
    
    transactions = parse_camt053_xml(xml_file)
    write_to_csv(transactions, csv_file)