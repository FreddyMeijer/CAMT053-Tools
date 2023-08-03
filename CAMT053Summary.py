import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import datetime

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
    vandaag=(datetime.date.today()).strftime("%d-%m-%Y")

    if count == 0:
        bericht = f"\n\n{element_name} komt helemaal niet voor. Er is waarschijnlijk iets mis gegaan met downloaden. Download het bestand opnieuw\n\n"
    elif count == 1:
        bericht = f"\n\n{element_name} komt 1 keer voor. Het betreft het bestand van 1 dag. Het bestand kan je inlezen in PAL21\n\n"
    elif count > 1:
        bericht = f"\n\n{element_name} komt meerdere keren voor ({count} keer). Donwload het bestand opnieuw vanuit de bank.\n\n"
    else:
        bericht = f"\n\nOnverwachte fout. Meldt de fout bij Functioneel beheer. Stuur het CAMT053 bestand mee.\n\n"

    bestandsnaam = os.path.basename(xml_file)
    headerblok=f"**************************************************************************************************************************************************************\nRAPPORT CAMT053 BESTAND\nBestand: {bestandsnaam}\nDatum: {vandaag}\n**************************************************************************************************************************************************************"
    footerblok="**************************************************************************************************************************************************************\nEINDE RAPPORTAGE\n**************************************************************************************************************************************************************"
    with open(output_file, 'w') as f:
        f.write(headerblok)
        f.write(bericht)
        f.write(footerblok)
