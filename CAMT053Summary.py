import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import datetime
import pandas as pd

class Camt053SummaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CAMT053 Samenvatting")

        self.label = tk.Label(self.root, text="CAMT053 SAMENVATTING\n")
        self.label.pack()

        self.select_button = tk.Button(self.root, text="Selecteer CAMT053 Bestand", command=self.select_file)
        self.select_button.pack()

        self.text = tk.Text(self.root, height=50, width=150)
        self.text.pack()

    def count_xml_elements(self, xml_file, element_name):
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

    def parse_camt053_xml(self, xml_file):
            tree = ET.parse(xml_file)
            root = tree.getroot()

            transactions = []
            for entry in root.findall('.//{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}Stmt/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}TxsSummry'):
                txn_data = {
                    'Totaal aantal boekingen': entry.findtext('{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}TtlNtries/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}NbOfNtries'),
                    'Totale som van boekingen': entry.findtext('{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}TtlNtries/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}Sum'),
                    'Totaal aantal credit boekingen': entry.findtext('{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}TtlCdtNtries/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}NbOfNtries'),
                    'Totale som van credit boekingen': entry.findtext('{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}TtlCdtNtries/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}Sum'),
                    'Totaal aantal debet boekingen': entry.findtext('{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}TtlDbtNtries/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}NbOfNtries'),
                    'Totale som van debet boekingen': entry.findtext('{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}TtlDbtNtries/{urn:iso:std:iso:20022:tech:xsd:camt.053.001.02}Sum')
                }
                transactions.append(txn_data)

            df = pd.DataFrame(transactions, ['Totaal aantal boekingen','Totale som van boekingen','Totaal aantal credit boekingen','Totale som van credit boekingen','Totaal aantal debet boekingen','Totale som van debet boekingen'])
            df = (df.iloc[0])
            return df

    def select_file(self):
        xml_file = filedialog.askopenfilename(
            title="Selecteer het CAMT053 Bestand",
            filetypes=[("Bankbestanden", "*.xml"), ("Alle bestanden", "*.*")]
        )
        
        if xml_file:
            element_name = 'Stmt'
            count = self.count_xml_elements(xml_file, element_name)
            output_file = xml_file.replace('.xml', '.txt')
            vandaag = (datetime.date.today()).strftime("%d-%m-%Y")

            if count == 0:
                bericht = f"\n\n{element_name} komt helemaal niet voor. Er is waarschijnlijk iets mis gegaan met downloaden. Download het bestand opnieuw\n\n"
            elif count == 1:
                bericht = f"\n\n{element_name} komt 1 keer voor. Het betreft het bestand van 1 dag. Het bestand kan je inlezen in PAL21\n\n"
            elif count > 1:
                bericht = f"\n\n{element_name} komt meerdere keren voor ({count} keer). Donwload het bestand opnieuw vanuit de bank.\n\n"
            else:
                bericht = f"\n\nOnverwachte fout. Meldt de fout bij Functioneel beheer. Stuur het CAMT053 bestand mee.\n\n"

            df = self.parse_camt053_xml(xml_file)
            df_as_string = df.to_string()

            bestandsnaam = os.path.basename(xml_file)
            headerblok = f"RAPPORT CAMT053 BESTAND\n\nBestand: {bestandsnaam}\nDatum: {vandaag}"
            footerblok = "\n\nEINDE RAPPORTAGE"
            result_text = f"{headerblok}{bericht}{df_as_string}{footerblok}"

            with open(output_file, 'w') as f:
                f.write(result_text)

            self.text.delete(1.0, tk.END)  # Clear the text widget
            self.text.insert(tk.END, result_text)

if __name__ == '__main__':
    root = tk.Tk()
    app = Camt053SummaryApp(root)
    root.mainloop()
