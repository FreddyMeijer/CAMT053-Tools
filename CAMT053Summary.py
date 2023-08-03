import csv
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog


def count_xml_elements(xml_file, element_name):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        ns = {'default': 'urn:iso:std:iso:20022:tech:xsd:camt.053.001.02'}

        element_count = root.findall(
            f'.//default:{element_name}', namespaces=ns)
        return len(element_count)
    except Exception as e:
        print(f"Error: {e}")
        return 0

def selectFile():
    File = filedialog.askopenfilename(
        title="Selecteer het CAMT053 Bestand",
        filetypes=[("Bankbestanden", "*.xml"), ("Alle bestanden", "*.*")]
    )
    if File:
        return File

if __name__ == '__main__':
    xml_file = selectFile()
    element_name = 'Stmt'

    count = count_xml_elements(xml_file, element_name)
    output_file = xml_file.replace('.xml', '.txt')
    with open(output_file, 'w') as f:
        f.write(f"Het element '{element_name}' komt {count} keer voor in {xml_file}.\n")
