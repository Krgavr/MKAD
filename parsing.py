import json
import csv
import os
import html

# vytvořit seznam souborů
file_list = os.listdir("json_data")

# Zkontrolujte, zda soubor existuje a zda má být zapsána hlavička
file_exists = os.path.isfile('data.csv')

# otevřít soubor CSV v režimu přidávání
with open('data.csv', 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['město', 'nazev', 'datum']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

    # Hlavičku zapište pouze v případě, že je soubor vytvářen poprvé.
    if not file_exists:
        writer.writeheader()

    for file_name in file_list:
        file_path = os.path.join("json_data", file_name)
        
        try:
            # čtení dat z JSON
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error when reading a file {file_name}: {e}")
            continue

        # vyplňte CSV
        mesto_raw = " ".join([word.capitalize() for word in file_name.split('.')[0].split()])
        if 'Praha' in mesto_raw:
            mesto = 'Praha'
        else:
            mesto = mesto_raw
        
        for info in data.get('informace', []):
            # Výpis jména a data s kontrolou klíče
            nazev = info.get('název', {}).get('cs', 'N/A')
            nazev = html.unescape(nazev)  # odstranění entit HTML
            vyveseni = info.get('vyvěšení', {})
            datum = vyveseni.get('datum', vyveseni.get('datum_a_čas', 'N/A'))
            
            # Pokud formát data obsahuje čas, oddělte pouze datum
            if 'T' in datum:
                datum = datum.split('T')[0]
                
            # zapsat data
            writer.writerow({'město': mesto, "nazev": nazev, "datum": datum})