"""Bouwt de oefendatabases (SQLite) op: companydb, ziekenhuis en bibliotheek.

companydb komt uit data/companydb.sql (van de cursus).
ziekenhuis en bibliotheek volgen de datamodellen uit de cursus, met verzonnen
(maar vaste) voorbeelddata zodat je resultaten kunt controleren.
"""
import os
import random
import sqlite3
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def build_company(path):
    with open(os.path.join(DATA, "companydb.sql")) as f:
        sql = f.read()
    lines = [l for l in sql.splitlines()
             if "pg_catalog" not in l and not l.startswith("ALTER")]
    sql = "\n".join(lines).replace("serial PRIMARY", "INTEGER PRIMARY")
    db = sqlite3.connect(path)
    db.executescript(sql)
    db.commit()
    db.close()


ZH_SCHEMA = """
CREATE TABLE zh_afdeling (nummer CHAR(5) PRIMARY KEY, naam VARCHAR(50) NOT NULL,
  kantoor_locatie VARCHAR(25) NOT NULL, tel_nr CHAR(10), lst_bijwerkdat DATE);
CREATE TABLE personeel (nummer CHAR(5) PRIMARY KEY, bsn CHAR(9) NOT NULL,
  achternaam VARCHAR(50) NOT NULL, voornaam VARCHAR(50) NOT NULL, tussenvoegsel VARCHAR(50),
  afd_toegewezen CHAR(5) REFERENCES zh_afdeling(nummer), kantoor_locatie VARCHAR(10),
  datum_in_dienst DATE, ziekenhuis_titel VARCHAR(50) NOT NULL, tel_werk CHAR(10),
  tel_doorkies VARCHAR(4), reg_nr VARCHAR(20), salaris INTEGER, tarief NUMERIC(5,2), bijwerkdat DATE);
CREATE TABLE medisch_specialisme (cd CHAR(4) PRIMARY KEY, titel VARCHAR(50) NOT NULL,
  hoe_behaald VARCHAR(100), lst_bijwerkdat DATE);
CREATE TABLE personeel_medspec (pers_nr CHAR(5) REFERENCES personeel(nummer),
  medspec_cd CHAR(4) REFERENCES medisch_specialisme(cd), datum_behaald DATE, lst_bijwerkdat DATE,
  PRIMARY KEY (pers_nr, medspec_cd));
CREATE TABLE patient (nummer CHAR(6) PRIMARY KEY, bsn CHAR(9) NOT NULL, achternaam VARCHAR(50) NOT NULL,
  voornaam VARCHAR(50) NOT NULL, tussenvoegsel VARCHAR(50), adres VARCHAR(50), plaats VARCHAR(50),
  provincie CHAR(2), postcode VARCHAR(7), geboortedatum DATE, tel_nr CHAR(10), lst_bijwerkdat DATE);
CREATE TABLE medicijn (cd CHAR(7) PRIMARY KEY, wetensch_naam VARCHAR(50) NOT NULL,
  handelsnaam VARCHAR(50) NOT NULL, normale_dos VARCHAR(300) NOT NULL, opmerking VARCHAR(500),
  voorraad_hoev INTEGER, eenheid VARCHAR(20), lst_bijwerkdat DATE);
CREATE TABLE recept (nummer INTEGER PRIMARY KEY, recept_datum DATE,
  medicijn_cd CHAR(7) NOT NULL REFERENCES medicijn(cd), patient_nr CHAR(6) NOT NULL REFERENCES patient(nummer),
  pers_nr CHAR(5) NOT NULL REFERENCES personeel(nummer), voorgeschr_dos VARCHAR(50) NOT NULL,
  dos_voorschr VARCHAR(500), lst_bijwerkdat DATE);
CREATE TABLE verrichting_cat (cat_nr CHAR(3) PRIMARY KEY, cat_omschrijving VARCHAR(50) NOT NULL,
  lst_bijwerkdat DATE);
CREATE TABLE verrichting (nummer CHAR(5) PRIMARY KEY, omschrijving VARCHAR(50) NOT NULL,
  rek_totaal NUMERIC(9,2), opmerking VARCHAR(2000), cat_nr CHAR(3) REFERENCES verrichting_cat(cat_nr),
  lst_bijwerkdat DATE);
CREATE TABLE behandeling (nummer INTEGER NOT NULL, behandel_datum DATE NOT NULL,
  patient_nr CHAR(6) NOT NULL REFERENCES patient(nummer), pers_nr CHAR(5) NOT NULL REFERENCES personeel(nummer),
  verrichting_nr CHAR(5) NOT NULL REFERENCES verrichting(nummer), huidige_rek_totaal NUMERIC(9,2),
  opmerking VARCHAR(2000), lst_bijwerkdat DATE, PRIMARY KEY (nummer, behandel_datum));
CREATE TABLE kamer (nummer CHAR(6) PRIMARY KEY, omschrijving VARCHAR(25), lst_bijwerkdat DATE);
CREATE TABLE bed_type (nummer CHAR(2) PRIMARY KEY, omschrijving VARCHAR(50), lst_bijwerkdat DATE);
CREATE TABLE bed (nummer INTEGER PRIMARY KEY, kamer_nummer CHAR(6) REFERENCES kamer(nummer),
  bed_type_nummer CHAR(2) NOT NULL REFERENCES bed_type(nummer), lst_bijwerkdat DATE);
CREATE TABLE patient_bed (patient_nr CHAR(6) REFERENCES patient(nummer), bed_nr INTEGER REFERENCES bed(nummer),
  intake_datum DATE NOT NULL, uitschrijf_datum DATE, lst_bijwerkdat DATE,
  PRIMARY KEY (patient_nr, bed_nr, intake_datum));
CREATE TABLE brmo (nummer CHAR(3) PRIMARY KEY, naam TEXT);
CREATE TABLE patient_melding_brmo (brmo_melding CHAR(5) PRIMARY KEY, patient_nr CHAR(6) REFERENCES patient(nummer),
  brmo_nr CHAR(3) REFERENCES brmo(nummer), melding_datum DATE, afd_behandeld TEXT, maatregel TEXT);
CREATE TABLE patient_notitie (patient_nr CHAR(6) REFERENCES patient(nummer), notitie_datum DATE NOT NULL,
  commentaar VARCHAR(4000), lst_bijwerkdat DATE, PRIMARY KEY (patient_nr, notitie_datum));
"""

VOORNAMEN = ["Jan", "Sanne", "Pieter", "Emma", "Lucas", "Julia", "Daan", "Sophie", "Bram", "Lotte",
             "Thijs", "Eva", "Ruben", "Anna", "Milan", "Fleur", "Sem", "Noor", "Tim", "Lisa"]
ACHTERNAMEN = ["de Jong", "Jansen", "de Vries", "van Dijk", "Bakker", "Visser", "Smit", "Meijer",
               "de Boer", "Mulder", "Bos", "Vos", "Peters", "Hendriks", "Dekker", "Brouwer",
               "Kok", "Verhoeven", "Willems", "Koster"]
PLAATSEN = [("Leiden", "ZH"), ("Den Haag", "ZH"), ("Utrecht", "UT"), ("Amersfoort", "UT"),
            ("Haarlem", "NH"), ("Amsterdam", "NH"), ("Eindhoven", "NB"), ("Breda", "NB")]


def d(rng, start, end):
    s, e = date.fromisoformat(start), date.fromisoformat(end)
    return (s + timedelta(days=rng.randint(0, (e - s).days))).isoformat()


def build_ziekenhuis(path):
    rng = random.Random(24)
    db = sqlite3.connect(path)
    db.executescript(ZH_SCHEMA)
    ins = lambda t, rows: db.executemany(
        f"INSERT INTO {t} VALUES ({','.join('?' * len(rows[0]))})", rows)

    afd = [("A01", "Cardiologie", "Gebouw A", "0715000001", None),
           ("A02", "Chirurgie", "Gebouw B", "0715000002", None),
           ("A03", "Kindergeneeskunde", "Gebouw C", "0715000003", None),
           ("A04", "Radiologie", "Gebouw A", "0715000004", None),
           ("A05", "Administratie", "Gebouw D", "0715000005", None)]
    ins("zh_afdeling", afd)

    titels = ["Arts", "Verpleegkundige", "Chirurg", "Specialist", "Administratief medewerker"]
    pers = []
    for i in range(1, 19):
        a = afd[(i - 1) % 4][0] if i <= 16 else "A05"
        if i == 18:
            a = None  # niet toegewezen
        pers.append((f"P{i:04d}", f"1{i:08d}", rng.choice(ACHTERNAMEN), rng.choice(VOORNAMEN), None,
                     a, f"K{i:03d}", d(rng, "2005-01-01", "2023-12-31"), rng.choice(titels),
                     f"07150{i:05d}", f"{i:04d}", f"BIG{i:05d}", rng.randrange(2800, 9500, 100),
                     round(rng.uniform(40, 150), 2), None))
    ins("personeel", pers)

    spec = [("CARD", "Cardiologie", "Opleiding 6 jaar"), ("CHIR", "Chirurgie", "Opleiding 6 jaar"),
            ("KIND", "Kindergeneeskunde", "Opleiding 5 jaar"), ("RADI", "Radiologie", "Opleiding 5 jaar"),
            ("ANES", "Anesthesiologie", "Opleiding 5 jaar"), ("NEUR", "Neurologie", "Opleiding 6 jaar")]
    ins("medisch_specialisme", [s + (None,) for s in spec])
    pm = set()
    for p in pers[:16]:
        for s in rng.sample(spec[:5], rng.choice([1, 1, 1, 2, 2, 3])):
            pm.add((p[0], s[0]))
    pm.add(("P0001", "CARD"))
    ins("personeel_medspec", [(p, s, d(rng, "2000-01-01", "2020-01-01"), None) for p, s in sorted(pm)])

    pats = []
    for i in range(1, 41):
        pl, pr = rng.choice(PLAATSEN)
        pats.append((f"{i:06d}", f"2{i:08d}", rng.choice(ACHTERNAMEN), rng.choice(VOORNAMEN), None,
                     f"Straat {i}", pl, pr, f"{2300 + i}AB", d(rng, "1935-01-01", "2020-12-31"),
                     f"06{i:08d}", None))
    ins("patient", pats)

    med = [("MED0001", "Paracetamolum", "Panadol", "3x daags 500mg", None, 500, "tablet"),
           ("MED0002", "Ibuprofenum", "Advil", "3x daags 400mg", None, 300, "tablet"),
           ("MED0003", "Amoxicillinum", "Amoxil", "3x daags 500mg", None, 120, "capsule"),
           ("MED0004", "Omeprazolum", "Losec", "1x daags 20mg", None, 80, "capsule"),
           ("MED0005", "Metforminum", "Glucophage", "2x daags 500mg", None, 200, "tablet"),
           ("MED0006", "Salbutamolum", "Ventolin", "zo nodig 100mcg", None, 40, "inhalator"),
           ("MED0007", "Morfinum", "Oramorph", "zo nodig 10mg", None, 15, "ml"),
           ("MED0008", "Insulinum", "Novorapid", "volgens schema", None, 25, "ml"),
           ("MED0009", "Diazepamum", "Valium", "1x daags 5mg", None, 60, "tablet"),
           ("MED0010", "Simvastatinum", "Zocor", "1x daags 20mg", None, 150, "tablet")]
    ins("medicijn", [m + (None,) for m in med])
    weights = [10, 6, 5, 3, 3, 2, 1, 1, 0, 0]  # MED0009/MED0010 nooit voorgeschreven
    rec = []
    for i in range(1, 71):
        m = rng.choices(med, weights)[0]
        rec.append((i, d(rng, "2023-01-01", "2024-12-31"), m[0], rng.choice(pats[:34])[0],
                    rng.choice(pers[:16])[0], m[3], None, None))
    ins("recept", rec)

    ins("verrichting_cat", [("C01", "Onderzoek", None), ("C02", "Operatie", None),
                            ("C03", "Beeldvorming", None), ("C04", "Consult", None)])
    verr = [("V0001", "Bloedonderzoek", 85.00, "C01"), ("V0002", "ECG", 150.00, "C01"),
            ("V0003", "Blindedarmoperatie", 3200.00, "C02"), ("V0004", "Knieoperatie", 5400.00, "C02"),
            ("V0005", "Röntgenfoto", 120.00, "C03"), ("V0006", "MRI-scan", 950.00, "C03"),
            ("V0007", "CT-scan", 1100.00, "C03"), ("V0008", "Polikliniek consult", 110.00, "C04"),
            ("V0009", "Second opinion", 250.00, "C04")]
    ins("verrichting", [(v[0], v[1], v[2], None, v[3], None) for v in verr])

    beh = []
    for i in range(1, 91):
        v = rng.choice(verr)
        beh.append((i, d(rng, "2023-01-01", "2024-12-31"), rng.choice(pats[:32])[0],
                    rng.choice(pers[:16])[0], v[0], v[2], None, None))
    ins("behandeling", beh)

    kamers = [(f"K{i:03d}", f"Kamer {i} ({o})", None) for i, o in
              zip(range(101, 109), ["IC", "Zaal", "Zaal", "Eenpersoons", "Kinderen", "Zaal", "Eenpersoons", "IC"])]
    ins("kamer", kamers)
    ins("bed_type", [("ST", "Standaard", None), ("IC", "Intensive care", None), ("KI", "Kinderbed", None)])
    beds_per = [2, 4, 4, 1, 3, 4, 1, 2]
    bed, n = [], 1
    for k, c in zip(kamers, beds_per):
        for _ in range(c):
            bt = "IC" if "IC" in k[1] else ("KI" if "Kinderen" in k[1] else "ST")
            bed.append((n, k[0], bt, None))
            n += 1
    ins("bed", bed)
    pb = []
    for i, p in enumerate(pats[:20]):
        pb.append((p[0], bed[i % len(bed)][0] if i < 15 else bed[(i * 3) % len(bed)][0],
                   d(rng, "2023-01-01", "2024-06-30"), None, None))
    ins("patient_bed", pb)
    db.execute("UPDATE patient_bed SET uitschrijf_datum = date(intake_datum, '+7 days') WHERE rowid % 2 = 0")

    ins("brmo", [("B01", "MRSA"), ("B02", "ESBL"), ("B03", "VRE")])
    ins("patient_melding_brmo", [("M0001", "000003", "B01", "2024-02-01", "Chirurgie", "Isolatie"),
                                 ("M0002", "000011", "B02", "2024-05-12", "Cardiologie", "Contactisolatie")])
    ins("patient_notitie", [("000001", "2024-01-10", "Allergisch voor penicilline", None),
                            ("000002", "2024-03-02", "Valrisico", None)])
    db.commit()
    db.close()


BIB_SCHEMA = """
CREATE TABLE author (id INTEGER PRIMARY KEY, firstname VARCHAR(50), lastname VARCHAR(50), birthyear INTEGER);
CREATE TABLE category (id INTEGER PRIMARY KEY, name VARCHAR(50), description TEXT);
CREATE TABLE publisher (id INTEGER PRIMARY KEY, name VARCHAR(100), city VARCHAR(50));
CREATE TABLE book (id INTEGER PRIMARY KEY, title VARCHAR(200), isbn VARCHAR(13) UNIQUE, publicationyear INTEGER,
  author INTEGER REFERENCES author(id), publisher INTEGER REFERENCES publisher(id),
  category INTEGER REFERENCES category(id));
CREATE TABLE department (id INTEGER PRIMARY KEY, name VARCHAR(50));
CREATE TABLE employee (id INTEGER PRIMARY KEY, firstname VARCHAR(50), lastname VARCHAR(50), sex CHAR(1),
  ssn VARCHAR(20) UNIQUE, department INTEGER REFERENCES department(id), manager INTEGER, salary NUMERIC(10,2));
CREATE TABLE member (id INTEGER PRIMARY KEY, firstname VARCHAR(50), lastname VARCHAR(50),
  email VARCHAR(100) UNIQUE, joindate DATE);
CREATE TABLE loan (id INTEGER PRIMARY KEY, book INTEGER REFERENCES book(id), member INTEGER REFERENCES member(id),
  loandate DATE, duedate DATE, returndate DATE);
CREATE TABLE review (id INTEGER PRIMARY KEY, book INTEGER REFERENCES book(id), member INTEGER REFERENCES member(id),
  rating INTEGER, comment TEXT, reviewdate DATE);
CREATE TABLE fine (id INTEGER PRIMARY KEY, loan INTEGER REFERENCES loan(id), amount NUMERIC(5,2), paid BOOLEAN);
"""


def build_bibliotheek(path):
    rng = random.Random(7)
    db = sqlite3.connect(path)
    db.executescript(BIB_SCHEMA)
    ins = lambda t, rows: db.executemany(
        f"INSERT INTO {t} VALUES ({','.join('?' * len(rows[0]))})", rows)
    ins("author", [(1, "Isaac", "Asimov", 1920), (2, "Arthur C.", "Clarke", 1917), (3, "Carl", "Sagan", 1934),
                   (4, "Mary", "Roach", 1959), (5, "Andy", "Weir", 1972), (6, "Harry", "Mulisch", 1927)])
    ins("category", [(1, "Science Fiction", "Verhalen over de toekomst"), (2, "Ruimtevaart", "Non-fictie over ruimtevaart"),
                     (3, "Wetenschap", "Populaire wetenschap"), (4, "Roman", "Literaire romans")])
    ins("publisher", [(1, "Penguin", "London"), (2, "De Bezige Bij", "Amsterdam"), (3, "Random House", "New York")])
    books = [(1, "Foundation", "9780553293357", 1951, 1, 3, 1), (2, "I, Robot", "9780553382563", 1950, 1, 3, 1),
             (3, "2001: A Space Odyssey", "9780451457998", 1968, 2, 1, 1), (4, "Cosmos", "9780345539434", 1980, 3, 3, 3),
             (5, "Pale Blue Dot", "9780345376596", 1994, 3, 3, 2), (6, "Packing for Mars", "9780393339918", 2010, 4, 1, 2),
             (7, "The Martian", "9780553418026", 2011, 5, 3, 1), (8, "Project Hail Mary", "9780593135204", 2021, 5, 3, 1),
             (9, "De ontdekking van de hemel", "9789023427914", 1992, 6, 2, 4), (10, "Rendezvous with Rama", "9780553287899", 1973, 2, 1, 1),
             (11, "Stiff", "9780393324822", 2003, 4, 1, 3), (12, "Het stenen bruidsbed", "9789023466340", 1959, 6, 2, 4)]
    ins("book", books)
    ins("department", [(1, "Directie"), (2, "Uitlening"), (3, "Collectie"), (4, "ICT")])
    emps = [(1, "Karin", "Vermeer", "V", "111111111", 1, None, 72000),
            (2, "Mark", "de Groot", "M", "222222222", 2, 1, 41000), (3, "Ilse", "Brand", "V", "333333333", 2, 2, 36000),
            (4, "Tom", "Hofman", "M", "444444444", 4, 1, 55000), (5, "Ahmed", "El Idrissi", "M", "555555555", 4, 4, 48000),
            (6, "Sven", "Kuipers", "M", "666666666", 4, 4, 51000), (7, "Nina", "Postma", "V", "777777777", 3, 1, 43000),
            (8, "Joost", "Wolters", "M", "888888888", 3, 7, 39000), (9, "Rik", "Jacobs", "M", "999999999", 4, None, 60000),
            (10, "Femke", "Prins", "V", "101010101", 2, 2, 34000)]
    ins("employee", emps)
    members = [(i, rng.choice(VOORNAMEN), rng.choice(ACHTERNAMEN).split()[-1], f"lid{i}@mail.nl",
                d(rng, "2018-01-01", "2024-01-01")) for i in range(1, 16)]
    ins("member", members)
    loans = []
    for i in range(1, 21):
        b = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 10, 11])  # boek 9 en 12 nooit uitgeleend
        ld = d(rng, "2024-01-01", "2024-10-01")
        due = (date.fromisoformat(ld) + timedelta(days=21)).isoformat()
        rd = (date.fromisoformat(ld) + timedelta(days=rng.randint(5, 35))).isoformat() if i % 4 else None
        loans.append((i, b, rng.randint(1, 15), ld, due, rd))
    ins("loan", loans)
    ins("review", [(i, rng.randint(1, 12), rng.randint(1, 15), rng.randint(1, 5), "Mooi boek", d(rng, "2024-01-01", "2024-10-01"))
                   for i in range(1, 16)])
    fines = [(n, l[0], 2.50 if n % 2 else 5.00, n % 3 == 0) for n, l in enumerate(
        [l for l in loans if l[5] is None or l[5] > l[4]], 1)]
    if fines:
        ins("fine", fines)
    db.commit()
    db.close()


BUILDERS = {"companydb": build_company, "ziekenhuis": build_ziekenhuis, "bibliotheek": build_bibliotheek}


def ensure(dbdir):
    os.makedirs(dbdir, exist_ok=True)
    for name, fn in BUILDERS.items():
        p = os.path.join(dbdir, name + ".db")
        if not os.path.exists(p):
            fn(p)


if __name__ == "__main__":
    out = os.path.join(HERE, "db")
    for f in os.listdir(out) if os.path.isdir(out) else []:
        os.remove(os.path.join(out, f))
    ensure(out)
    print("Databases gebouwd in", out)
