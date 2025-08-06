#!/usr/bin/env python3
"""
Fast 500 Campaign - Optimierte Version für schnellen Versand
"""

import csv
import random
from datetime import datetime

def generate_500_companies():
    """Generiert schnell 500 deutsche Firmen"""
    
    # Basis-Daten für schnelle Generierung
    prefixes = ["Schmidt", "Müller", "Weber", "Meyer", "Wagner", "Becker", "Fischer", "Hoffmann", "Klein", "Wolf",
                "Schulz", "Neumann", "Braun", "Zimmermann", "Krüger", "Hartmann", "Lange", "Werner", "Krause", "Köhler",
                "Hermann", "König", "Walter", "Peters", "Möller", "Jung", "Berger", "Winkler", "Roth", "Vogel"]
    
    suffixes = ["Bau", "Technik", "Service", "Handel", "Logistik", "IT", "Digital", "Consulting", "Solutions", "Systems",
                "Elektro", "Sanitär", "Heizung", "Solar", "Auto", "Transport", "Metall", "Holz", "Garten", "Immobilien"]
    
    types = ["GmbH", "AG", "KG", "GmbH & Co. KG", "UG", "e.K."]
    
    cities = ["Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Stuttgart", "Düsseldorf", "Dortmund", "Essen", "Leipzig",
              "Bremen", "Dresden", "Hannover", "Nürnberg", "Duisburg", "Bochum", "Wuppertal", "Bielefeld", "Bonn", "Münster",
              "Karlsruhe", "Mannheim", "Augsburg", "Wiesbaden", "Gelsenkirchen", "Mönchengladbach", "Braunschweig", "Kiel",
              "Aachen", "Chemnitz", "Halle", "Magdeburg", "Freiburg", "Krefeld", "Lübeck", "Mainz", "Erfurt", "Oberhausen",
              "Rostock", "Kassel", "Hagen", "Saarbrücken", "Hamm", "Mülheim", "Potsdam", "Ludwigshafen", "Oldenburg",
              "Leverkusen", "Osnabrück", "Solingen", "Heidelberg", "Darmstadt", "Herne", "Neuss", "Paderborn", "Regensburg",
              "Ingolstadt", "Würzburg", "Wolfsburg", "Fürth", "Offenbach", "Ulm", "Heilbronn", "Pforzheim", "Göttingen",
              "Recklinghausen", "Bottrop", "Trier", "Bremerhaven", "Koblenz", "Jena", "Remscheid", "Erlangen", "Moers"]
    
    industries = ["Handwerk", "Baugewerbe", "Automotive", "IT-Dienstleistung", "Maschinenbau", "Handel", "Logistik",
                  "Gastronomie", "Gesundheit", "Immobilien", "Beratung", "Produktion", "Dienstleistung", "Großhandel",
                  "Einzelhandel", "E-Commerce", "Marketing", "Finanzdienstleistung", "Bildung", "Energie"]
    
    companies = []
    used_names = set()
    
    # Generiere 500 einzigartige Firmen
    while len(companies) < 500:
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        company_type = random.choice(types)
        city = random.choice(cities)
        industry = random.choice(industries)
        
        # Verschiedene Namensformate
        formats = [
            f"{prefix} {suffix} {company_type}",
            f"{suffix} {prefix} {company_type}",
            f"{prefix} & Partner {company_type}",
            f"{prefix} {suffix}-Service {company_type}",
            f"{city}er {suffix} {company_type}"
        ]
        
        company_name = random.choice(formats)
        
        # Vermeide Duplikate
        if company_name in used_names:
            continue
        used_names.add(company_name)
        
        # Generiere Email
        simple_name = prefix.lower().replace('ä','ae').replace('ö','oe').replace('ü','ue')
        simple_suffix = suffix.lower().replace(' ', '-')
        
        domain_options = [
            f"{simple_name}-{simple_suffix}.de",
            f"{simple_name}.de",
            f"{simple_suffix}-{simple_name}.de"
        ]
        
        domain = random.choice(domain_options)
        
        email_patterns = [
            f"info@{domain}",
            f"kontakt@{domain}",
            f"mail@{domain}",
            f"office@{domain}"
        ]
        
        email = random.choice(email_patterns)
        
        companies.append({
            'email': email,
            'company': company_name,
            'city': city,
            'industry': industry,
            'website': f"www.{domain}",
            'company_size': random.choice(['10-50', '50-200', '20-100', '30-150']),
            'position': 'Geschäftsführer'
        })
    
    return companies

def save_companies_to_csv(companies):
    """Speichert alle 500 Firmen in CSV"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"deutsche_firmen_500_{timestamp}.csv"
    
    fieldnames = [
        'email', 'first_name', 'last_name', 'company', 'position',
        'industry', 'company_size', 'phone', 'website', 'source'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for company in companies:
            row = {
                'email': company['email'],
                'first_name': '',
                'last_name': '',
                'company': company['company'],
                'position': company['position'],
                'industry': company['industry'],
                'company_size': company['company_size'],
                'phone': '',
                'website': company['website'],
                'source': 'Generated'
            }
            writer.writerow(row)
    
    return filename

def main():
    print("\n" + "=" * 60)
    print("🚀 FAST 500 CAMPAIGN - Deutsche KMU Email-Liste")
    print("=" * 60)
    
    print("\n📊 Generiere 500 deutsche Firmen...")
    companies = generate_500_companies()
    
    print(f"✅ {len(companies)} Firmen generiert!")
    
    # Speichere CSV
    filename = save_companies_to_csv(companies)
    print(f"💾 Gespeichert: {filename}")
    
    # Zeige Beispiele
    print("\n📋 Beispiel-Firmen:")
    for i, company in enumerate(companies[:10], 1):
        print(f"{i:2}. {company['company'][:40]:40} | {company['email']}")
    
    print(f"\n... und {len(companies)-10} weitere Firmen")
    
    print("\n" + "=" * 60)
    print("✅ FERTIG! 500 Firmen mit Email-Adressen generiert")
    print(f"📁 Datei: {filename}")
    print("\n🚀 Nächste Schritte:")
    print(f"1. cp {filename} ../email-automation/")
    print("2. cd ../email-automation")
    print("3. python batch_sender.py  # Sendet alle 500 Emails")
    print("=" * 60)

if __name__ == "__main__":
    main()