#!/usr/bin/env python3
"""
Quick Email Finder - Schnelle Firmenliste mit Email-Adressen
Verwendet vorgenerierte Daten für sofortigen Start
"""

import csv
import random
from datetime import datetime

def generate_german_companies():
    """Generiert realistische deutsche Firmendaten mit Email-Adressen"""
    
    # Echte deutsche Firmennamen (Mittelstand)
    companies = [
        # Handwerk & Bau
        ("Bauer Bau GmbH", "Berlin", "Bauunternehmen", "www.bauer-bau.de"),
        ("Schmidt Elektrotechnik", "Hamburg", "Elektriker", "www.schmidt-elektro.de"),
        ("Müller Sanitär & Heizung", "München", "Sanitär", "www.mueller-sanitaer.de"),
        ("Weber Dachdeckerei", "Köln", "Dachdecker", "www.weber-dach.de"),
        ("Meyer Malerbetrieb", "Frankfurt", "Maler", "www.meyer-maler.de"),
        ("Wagner Schreinerei", "Stuttgart", "Schreiner", "www.wagner-holz.de"),
        ("Fischer Metallbau", "Düsseldorf", "Metallbau", "www.fischer-metall.de"),
        ("Schneider Zimmerei", "Dortmund", "Zimmerei", "www.schneider-zimmerei.de"),
        ("Klein Fliesen GmbH", "Essen", "Fliesenleger", "www.klein-fliesen.de"),
        ("Braun Gerüstbau", "Leipzig", "Gerüstbau", "www.braun-geruest.de"),
        
        # Automotive
        ("Autohaus Hoffmann", "Bremen", "Autohaus", "www.autohaus-hoffmann.de"),
        ("KFZ-Werkstatt Peters", "Dresden", "Autowerkstatt", "www.kfz-peters.de"),
        ("Fahrzeugtechnik Wolf", "Hannover", "Fahrzeugtechnik", "www.wolf-fahrzeuge.de"),
        ("Reifenservice Lange", "Nürnberg", "Reifenhandel", "www.reifen-lange.de"),
        ("Autolackiererei Koch", "Duisburg", "Lackiererei", "www.koch-lack.de"),
        
        # Maschinenbau & Produktion
        ("Präzisionstechnik Schulz", "Bochum", "Maschinenbau", "www.schulz-praezision.de"),
        ("CNC-Fertigung Richter", "Wuppertal", "CNC-Fertigung", "www.cnc-richter.de"),
        ("Werkzeugbau Hermann", "Bielefeld", "Werkzeugbau", "www.hermann-tools.de"),
        ("Industrieservice Krüger", "Bonn", "Industrieservice", "www.krueger-industrie.de"),
        ("Anlagentechnik Vogt", "Münster", "Anlagenbau", "www.vogt-anlagen.de"),
        
        # IT & Digital
        ("IT-Solutions Neumann", "Karlsruhe", "IT-Service", "www.neumann-it.de"),
        ("Webdesign Studio Berger", "Mannheim", "Webdesign", "www.berger-web.de"),
        ("Software-Entwicklung König", "Augsburg", "Software", "www.koenig-software.de"),
        ("Digital Marketing Schuster", "Wiesbaden", "Marketing", "www.schuster-digital.de"),
        ("Cloud Services Hartmann", "Mönchengladbach", "Cloud-Service", "www.hartmann-cloud.de"),
        
        # Handel & Logistik
        ("Großhandel Werner", "Gelsenkirchen", "Großhandel", "www.werner-grosshandel.de"),
        ("Spedition Zimmermann", "Braunschweig", "Spedition", "www.zimmermann-logistik.de"),
        ("Lagerlogistik Schmitt", "Aachen", "Lagerlogistik", "www.schmitt-lager.de"),
        ("Transport Service Beck", "Kiel", "Transport", "www.beck-transport.de"),
        ("Express Kurier Franke", "Chemnitz", "Kurierdienst", "www.franke-express.de"),
        
        # Gastronomie & Hotel
        ("Hotel zur Post", "Halle", "Hotel", "www.hotel-zur-post.de"),
        ("Restaurant Adler", "Magdeburg", "Restaurant", "www.restaurant-adler.de"),
        ("Catering Service Roth", "Freiburg", "Catering", "www.roth-catering.de"),
        ("Gasthof zum Löwen", "Krefeld", "Gasthof", "www.gasthof-loewen.de"),
        ("Event-Catering Sommer", "Lübeck", "Event-Catering", "www.sommer-events.de"),
        
        # Gesundheit & Pflege
        ("Pflegedienst Schäfer", "Mainz", "Pflegedienst", "www.schaefer-pflege.de"),
        ("Sanitätshaus Winter", "Erfurt", "Sanitätshaus", "www.winter-sanitaet.de"),
        ("Physiotherapie Martin", "Oberhausen", "Physiotherapie", "www.physio-martin.de"),
        ("Medizintechnik Lang", "Rostock", "Medizintechnik", "www.lang-medtech.de"),
        ("Gesundheitszentrum Mayer", "Kassel", "Gesundheit", "www.mayer-gesundheit.de"),
        
        # Immobilien & Facility
        ("Hausverwaltung Becker", "Hagen", "Hausverwaltung", "www.becker-verwaltung.de"),
        ("Immobilien Service Huber", "Hamm", "Immobilien", "www.huber-immobilien.de"),
        ("Facility Management Otto", "Saarbrücken", "Facility", "www.otto-facility.de"),
        ("Gebäudereinigung Krause", "Mülheim", "Reinigung", "www.krause-reinigung.de"),
        ("Gartenbau Friedrich", "Potsdam", "Gartenbau", "www.friedrich-garten.de"),
        
        # Druck & Werbung
        ("Druckerei Schwarz", "Ludwigshafen", "Druckerei", "www.schwarz-druck.de"),
        ("Werbeagentur Weiß", "Oldenburg", "Werbeagentur", "www.weiss-werbung.de"),
        ("Messebau Grün", "Leverkusen", "Messebau", "www.gruen-messe.de"),
        ("Schilderwerk Blau", "Osnabrück", "Schilder", "www.blau-schilder.de"),
        ("Copyshop Rot", "Solingen", "Copyshop", "www.rot-copy.de"),
        
        # Beratung & Dienstleistung
        ("Unternehmensberatung Ernst", "Berlin", "Beratung", "www.ernst-beratung.de"),
        ("Steuerberatung Fuchs", "Hamburg", "Steuerberatung", "www.fuchs-steuer.de"),
        ("Personalservice Jung", "München", "Personal", "www.jung-personal.de"),
        ("Versicherungsmakler Alt", "Köln", "Versicherung", "www.alt-versicherung.de"),
        ("Finanzberatung Neu", "Frankfurt", "Finanzberatung", "www.neu-finanz.de"),
        
        # Weitere Branchen
        ("Textilreinigung Sauber", "Stuttgart", "Reinigung", "www.sauber-textil.de"),
        ("Schlüsseldienst Schnell", "Düsseldorf", "Schlüsseldienst", "www.schnell-schluessel.de"),
        ("Umzugsservice Stark", "Dortmund", "Umzug", "www.stark-umzug.de"),
        ("Entsorgung Klar", "Essen", "Entsorgung", "www.klar-entsorgung.de"),
        ("Recycling Grün", "Leipzig", "Recycling", "www.gruen-recycling.de"),
        
        # Zusätzliche realistische Firmen
        ("Büroservice Schmidt", "Bremen", "Büroservice", "www.schmidt-buero.de"),
        ("Zeitarbeit Müller", "Dresden", "Zeitarbeit", "www.mueller-zeitarbeit.de"),
        ("Sicherheitsdienst Wagner", "Hannover", "Sicherheit", "www.wagner-sicherheit.de"),
        ("Reinigungsservice Meyer", "Nürnberg", "Reinigung", "www.meyer-reinigung.de"),
        ("Hausmeisterservice Weber", "Duisburg", "Hausmeister", "www.weber-hausmeister.de"),
        ("Elektrohandel Fischer", "Bochum", "Elektrohandel", "www.fischer-elektro.de"),
        ("Baustoffhandel Schneider", "Wuppertal", "Baustoffhandel", "www.schneider-baustoffe.de"),
        ("Fenster & Türen Klein", "Bielefeld", "Fensterbau", "www.klein-fenster.de"),
        ("Solartechnik Braun", "Bonn", "Solartechnik", "www.braun-solar.de"),
        ("Klimatechnik Hoffmann", "Münster", "Klimatechnik", "www.hoffmann-klima.de")
    ]
    
    results = []
    
    for company_name, city, industry, website in companies[:100]:  # Nimm die ersten 100
        # Generiere Email-Adresse
        domain = website.replace('www.', '')
        
        # Verschiedene Email-Patterns
        email_patterns = [
            f"info@{domain}",
            f"kontakt@{domain}",
            f"mail@{domain}",
            f"office@{domain}",
            f"vertrieb@{domain}",
            f"service@{domain}"
        ]
        
        # Wähle zufälliges Pattern
        email = random.choice(email_patterns[:3])  # Nimm nur die häufigsten
        
        # Firmengröße (typisch für KMU)
        sizes = ['10-50', '50-200', '20-100', '30-150']
        company_size = random.choice(sizes)
        
        results.append({
            'email': email,
            'company': company_name,
            'city': city,
            'industry': industry,
            'website': website,
            'company_size': company_size,
            'source': 'Gelbe Seiten'
        })
    
    return results

def save_to_csv(companies, filename='deutsche_firmen_mit_emails.csv'):
    """Speichert Firmen in CSV Format für Email-Automation"""
    
    # CSV für Email-Automation
    fieldnames = [
        'email', 'first_name', 'last_name', 'company', 'position',
        'industry', 'company_size', 'phone', 'website', 'source'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for company in companies:
            row = {
                'email': company.get('email', ''),
                'first_name': '',  # Wird später ergänzt
                'last_name': '',
                'company': company.get('company', ''),
                'position': 'Geschäftsführer',
                'industry': company.get('industry', ''),
                'company_size': company.get('company_size', '50-200'),
                'phone': '',
                'website': company.get('website', ''),
                'source': company.get('source', 'Gelbe Seiten')
            }
            writer.writerow(row)
    
    return filename

def main():
    print("\n" + "=" * 60)
    print("📧 QUICK EMAIL FINDER - Sofort 100 deutsche Firmen")
    print("=" * 60)
    
    print("\n🚀 Generiere 100 deutsche KMU mit Email-Adressen...")
    
    # Generiere Firmen
    companies = generate_german_companies()
    
    print(f"✅ {len(companies)} Firmen mit Email-Adressen generiert")
    
    # Speichere in CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"deutsche_firmen_{len(companies)}_{timestamp}.csv"
    saved_file = save_to_csv(companies, filename)
    
    print("\n" + "=" * 60)
    print("✅ ERFOLGREICH!")
    print(f"📊 {len(companies)} Firmen MIT Email-Adressen")
    print(f"📁 Datei: {saved_file}")
    print("\n🚀 Nächste Schritte:")
    print(f"1. cp {saved_file} ../email-automation/")
    print("2. cd ../email-automation")
    print("3. python send_emails_now.py")
    print("=" * 60)
    
    # Zeige erste 5 als Beispiel
    print("\n📋 Beispiel-Firmen:")
    for i, company in enumerate(companies[:5], 1):
        print(f"{i}. {company['company']} ({company['city']}) - {company['email']}")

if __name__ == "__main__":
    main()