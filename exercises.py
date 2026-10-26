"""Alle lessen en oefeningen, gebaseerd op de DATFI-oefenbestanden.

Per oefening:
  q      de vraag
  sol    een correcte uitwerking (wordt gebruikt om jouw antwoord te controleren)
  hint   een duwtje in de goede richting
  check  (optioneel) query die NA jouw statements wordt uitgevoerd; voor CREATE/INSERT/UPDATE/DELETE
  names  True = kolomnamen (aliassen) moeten ook kloppen
"""

LESSONS = [
    {
        "id": "select", "title": "1. SELECT basis (WHERE, ORDER BY, LIKE, IN, BETWEEN)", "db": "companydb",
        "uitleg": """\
SELECT kolommen FROM tabel WHERE voorwaarde ORDER BY kolom [ASC|DESC];

  DISTINCT            dubbele rijen weg:          SELECT DISTINCT birthdate FROM employee;
  AND / OR / NOT      voorwaarden combineren
  IN (...)            lijst van waarden:          WHERE lastname IN ('Best', 'King')
  BETWEEN a AND b     bereik (inclusief):         WHERE salary BETWEEN 40000 AND 70000
  LIKE                patroon, % = alles, _ = 1 teken:  WHERE address LIKE '%Houston%'
  IS NULL             leeg veld (NOOIT = NULL):   WHERE supervisor IS NULL
  ||                  tekst plakken:              SELECT firstname || ' ' || lastname
  AS                  kolom hernoemen:            SELECT COUNT(*) AS aantal

Datums schrijf je als tekst: '1980-01-01'.""",
    },
    {
        "id": "groupby_c", "title": "2. Kolomfuncties, GROUP BY en HAVING (companydb)", "db": "companydb",
        "uitleg": """\
Kolomfuncties maken van veel rijen één waarde:
  COUNT(*)  COUNT(kolom)  COUNT(DISTINCT kolom)  SUM()  AVG()  MIN()  MAX()

GROUP BY maakt groepjes; de kolomfunctie werkt dan per groep:
  SELECT department, COUNT(*) FROM employee GROUP BY department;

Regel: elke kolom in SELECT die GEEN kolomfunctie is, moet in GROUP BY staan.

WHERE filtert rijen VOOR het groeperen, HAVING filtert groepen NA het groeperen:
  SELECT department, AVG(salary) FROM employee
   GROUP BY department HAVING AVG(salary) > 35000;

Volgorde: SELECT .. FROM .. WHERE .. GROUP BY .. HAVING .. ORDER BY .. LIMIT""",
    },
    {
        "id": "sub_c", "title": "3. Subqueries (companydb)", "db": "companydb",
        "uitleg": """\
Een subquery is een query binnen een query, tussen haakjes.

  Eén waarde:   WHERE salary > (SELECT AVG(salary) FROM employee)
  Lijst:        WHERE id IN (SELECT employee FROM dependent)
                WHERE id NOT IN (SELECT employee FROM dependent)
  Bestaat:      WHERE EXISTS (SELECT 1 FROM dependent d WHERE d.employee = e.id)
  ALL / ANY:    salary > ALL(...) is hetzelfde als salary > (SELECT MAX(...))
                (SQLite kent ALL/ANY niet; gebruik hier MAX/MIN)

Gecorreleerd: de subquery gebruikt een kolom van de buitenste query:
  SELECT e.lastname FROM employee e
   WHERE e.salary > (SELECT s.salary FROM employee s WHERE s.id = e.supervisor);

Let op: een subquery na = of > mag maar 1 waarde teruggeven!""",
    },
    {
        "id": "join_zh", "title": "4. JOIN (ziekenhuis)", "db": "ziekenhuis",
        "uitleg": """\
JOIN koppelt tabellen via primary key = foreign key.

  SELECT patient.achternaam, medicijn.handelsnaam
    FROM patient
   INNER JOIN recept   ON patient.nummer = recept.patient_nr
   INNER JOIN medicijn ON recept.medicijn_cd = medicijn.cd;

  INNER JOIN   alleen rijen met een match in beide tabellen
  LEFT JOIN    ALLE rijen van de linker tabel; geen match -> NULL

Tip: kijk in het datamodel (typ :schema) welke kolommen naar elkaar verwijzen.
Gebruik tabel.kolom als een kolomnaam in meerdere tabellen voorkomt.""",
    },
    {
        "id": "groupby_zh", "title": "5. GROUP BY (ziekenhuis)", "db": "ziekenhuis",
        "uitleg": """\
Zelfde regels als les 2, nu op de ziekenhuisdatabase.

  SELECT patient_nr, COUNT(*) AS totaal FROM behandeling GROUP BY patient_nr;

Datums in SQLite (in PostgreSQL gebruik je AGE / datum - datum):
  julianday(a) - julianday(b)                     verschil in dagen
  (julianday('now') - julianday(geboortedatum)) / 365.25   leeftijd in jaren""",
    },
    {
        "id": "having_zh", "title": "6. GROUP BY + HAVING (ziekenhuis)", "db": "ziekenhuis",
        "uitleg": """\
HAVING filtert op het resultaat van een kolomfunctie:

  SELECT afd_toegewezen, COUNT(*) FROM personeel
   GROUP BY afd_toegewezen
  HAVING COUNT(*) > 2;

Je mag in HAVING ook een subquery gebruiken:
  HAVING COUNT(*) > (SELECT AVG(...) FROM (...) AS sub)""",
    },
    {
        "id": "sub_zh", "title": "7. Subqueries (ziekenhuis)", "db": "ziekenhuis",
        "uitleg": """\
  NOT IN       wat ontbreekt:  WHERE cd NOT IN (SELECT medicijn_cd FROM recept)
  = (... LIMIT 1)   de 'meeste': ORDER BY COUNT(*) DESC LIMIT 1 in de subquery
  Subquery in FROM (afgeleide tabel) heeft een naam nodig:
     SELECT AVG(n) FROM (SELECT COUNT(*) AS n FROM bed GROUP BY kamer_nummer) AS sub""",
    },
    {
        "id": "codegrade", "title": "8. CodeGrade-oefeningen (ziekenhuis)", "db": "ziekenhuis",
        "uitleg": """\
Zo worden de opdrachten in CodeGrade gesteld: precies de gevraagde kolommen,
in de gevraagde volgorde, met de gevraagde kolomnamen (aliassen), sortering en LIMIT.
Hier worden kolomnamen dus OOK gecontroleerd.""",
    },
    {
        "id": "ddl", "title": "9. CREATE / INSERT / UPDATE / DELETE + keys", "db": "leeg",
        "uitleg": """\
  CREATE TABLE teacher (
      id      INTEGER PRIMARY KEY,
      name    VARCHAR(50) NOT NULL,
      subject VARCHAR(50) DEFAULT 'onbekend',
      age     INTEGER CHECK (age > 17)
  );
  INSERT INTO teacher (id, name, subject) VALUES (1, 'Ann', 'Wiskunde');
  UPDATE teacher SET subject = 'Logica' WHERE name = 'Ann';
  DELETE FROM teacher WHERE id = 1;
  DROP TABLE teacher;
  CREATE INDEX idx_name ON teacher (name);   CREATE UNIQUE INDEX ...;  DROP INDEX idx_name;

Foreign key + referentiele acties:
  singer INTEGER REFERENCES singer(id) ON DELETE CASCADE ON UPDATE CASCADE
  ON DELETE CASCADE   kind-rijen worden mee verwijderd
  ON DELETE SET NULL  FK in kind-rij wordt NULL
  ON DELETE RESTRICT  verwijderen mag niet zolang er kind-rijen zijn

Je mag meerdere statements achter elkaar typen (elk eindigend op ;).
Typ ':run' als je klaar bent om te laten controleren.""",
    },
    {
        "id": "toets", "title": "10. Oefentoets (bibliotheek)", "db": "bibliotheek",
        "uitleg": """\
Dit is de CodeGrade Oefentoets op de Bibliotheek database.
Echte toets: 45 minuten, geen hulpmiddelen. Typ ':timer 45' om jezelf te klokken.""",
    },
]

SINGER_SETUP = """
CREATE TABLE singer (id INTEGER, firstname TEXT, lastname TEXT, age INTEGER, PRIMARY KEY (id));
INSERT INTO singer VALUES (1,'Miley','Cyrus',27),(2,'Carley Rae','Jepsen',35),(3,'Selena','Gomez',28),
 (4,'Ariane','Grande',27),(5,'Lady','Gaga',34);
CREATE TABLE song (id INTEGER, name TEXT, year INTEGER, singer INTEGER, PRIMARY KEY (id),
 FOREIGN KEY (singer) REFERENCES singer (id) ON DELETE CASCADE ON UPDATE CASCADE);
INSERT INTO song VALUES (1,'Bad Romance',2008,5),(2,'Bang Bang',2014,4),(3,'It Ain''t Me',2017,3),
 (4,'Call Me Maybe',2012,2),(5,'Wrecking Ball',2013,1);
"""

E = []


def ex(lesson, q, sol, hint="", names=False, check=None, setup=None):
    E.append(dict(lesson=lesson, q=q, sol=sol.strip(), hint=hint, names=names, check=check, setup=setup))


# ---------------- 1. SELECT basis (Week 2 DD2) ----------------
L = "select"
ex(L, "Haal de unieke geboortedata op van alle werknemers (employee).",
   "SELECT DISTINCT birthdate FROM employee;", "DISTINCT")
ex(L, "Haal de voor- en achternamen op van alle werknemers, gesorteerd op achternaam aflopend.",
   "SELECT firstname, lastname FROM employee ORDER BY lastname DESC;", "ORDER BY ... DESC")
ex(L, "Vind id, voornaam, achternaam, salaris en afdeling van werknemers met een salaris van meer dan 50000 die op afdeling 7 werken.",
   "SELECT id, firstname, lastname, salary, department FROM employee WHERE salary > 50000 AND department = 7;", "Twee voorwaarden: AND")
ex(L, "Vind alle informatie van werknemers die worden begeleid door leidinggevende (supervisor) nummer 30.",
   "SELECT * FROM employee WHERE supervisor = 30;", "SELECT * ... WHERE supervisor = ...")
ex(L, "Vind alle informatie van werknemers geboren vóór 1 januari 1980 die op afdeling 6 werken, gesorteerd op geboortedatum aflopend.",
   "SELECT * FROM employee WHERE birthdate < '1980-01-01' AND department = 6 ORDER BY birthdate DESC;", "birthdate < '1980-01-01'")
ex(L, "Haal de voor- en achternamen op van alle mannelijke werknemers.",
   "SELECT firstname, lastname FROM employee WHERE sex = 'M';", "Kolom sex bevat 'M' of 'F'")
ex(L, "Geef het aantal werknemers dat in Atlanta woont (één getal).",
   "SELECT COUNT(*) FROM employee WHERE address LIKE '%Atlanta%';", "COUNT(*) en LIKE '%Atlanta%' op address")
ex(L, "Haal de volledige namen (voornaam, achternaam) en salarissen op van werknemers die GEEN leidinggevende hebben.",
   "SELECT firstname, lastname, salary FROM employee WHERE supervisor IS NULL;", "IS NULL, niet = NULL")
ex(L, "Geef voor- en achternamen van werknemers geboren tussen 1 januari 1980 en 31 december 1990.",
   "SELECT firstname, lastname FROM employee WHERE birthdate BETWEEN '1980-01-01' AND '1990-12-31';", "BETWEEN ... AND ...")
ex(L, "Geef achternaam en salaris van medewerkers met achternaam 'Best', 'English' of 'King'. Gebruik IN.",
   "SELECT lastname, salary FROM employee WHERE lastname IN ('Best', 'English', 'King');", "IN ('a', 'b', 'c')")
ex(L, "Vind alle unieke steden (location) waar afdelingen zich bevinden.",
   "SELECT DISTINCT location FROM department_location;", "Tabel department_location")
ex(L, "Haal voor- en achternamen op van werknemers die op afdeling 5 of 6 werken.",
   "SELECT firstname, lastname FROM employee WHERE department IN (5, 6);", "OR of IN")
ex(L, "Haal de volledige naam (voornaam, achternaam) op van werknemers geboren tussen 1960 en 1970 (1 jan 1960 t/m 31 dec 1970).",
   "SELECT firstname, lastname FROM employee WHERE birthdate BETWEEN '1960-01-01' AND '1970-12-31';")
ex(L, "Vind alle informatie van werknemers met een salaris van minder dan 40000 of meer dan 80000.",
   "SELECT * FROM employee WHERE salary < 40000 OR salary > 80000;", "OR")
ex(L, "Haal voor- en achternamen op van werknemers die in een stad wonen die met 'M' begint. "
      "(address heeft de vorm 'straat stad staat'; de stad is het voorlaatste woord, maar zoek gewoon op ' M' in het adres)",
   "SELECT firstname, lastname FROM employee WHERE address LIKE '% M%';", "LIKE '% M%'")
ex(L, "Haal de volledige namen op van werknemers die NIET op afdeling 7 werken.",
   "SELECT firstname, lastname FROM employee WHERE department <> 7;", "<> of !=")
ex(L, "Vind volledige naam en salaris van werknemers met een salaris tussen 40000 en 70000.",
   "SELECT firstname, lastname, salary FROM employee WHERE salary BETWEEN 40000 AND 70000;")
ex(L, "Vind alle werknemers (alle kolommen) die niet in Chicago, Milwaukee of Dallas wonen. Gebruik LIKE.",
   "SELECT * FROM employee WHERE address NOT LIKE '%Chicago%' AND address NOT LIKE '%Milwaukee%' AND address NOT LIKE '%Dallas%';",
   "NOT LIKE ... AND NOT LIKE ...")
ex(L, "Haal voor- en achternamen op van werknemers die in de afdeling 'Software' werken en meer dan 75000 verdienen.",
   "SELECT firstname, lastname FROM employee WHERE department = (SELECT id FROM department WHERE name = 'Software') AND salary > 75000;",
   "Zoek eerst het id van 'Software' in department (of gebruik een JOIN)")
ex(L, "Haal volledige namen en salarissen op van werknemers die niet in een plaats wonen die eindigt op 'TX' of 'CA'.",
   "SELECT firstname, lastname, salary FROM employee WHERE address NOT LIKE '%TX' AND address NOT LIKE '%CA';", "LIKE '%TX'")
ex(L, "Toon voor iedere werknemer één kolom 'naam' met voornaam, spatie, achternaam (bijv. 'John Smith').",
   "SELECT firstname || ' ' || lastname AS naam FROM employee;", "|| plakt tekst aan elkaar; AS naam", names=True)

# ---------------- 2. GROUP BY/HAVING companydb (Week 3 DD3) ----------------
L = "groupby_c"
ex(L, "Geef het totaal aantal rijen van de tabel employee.", "SELECT COUNT(*) FROM employee;")
ex(L, 'Geef het aantal medewerkers dat een leidinggevende (supervisor) heeft, met kolomnaam "employees-having-manager".',
   'SELECT COUNT(supervisor) AS "employees-having-manager" FROM employee;',
   'COUNT(kolom) telt geen NULLs. Alias met streepjes tussen dubbele quotes', names=True)
ex(L, 'Geef het gemiddelde salaris van alle medewerkers, kolomnaam "average-salary".',
   'SELECT AVG(salary) AS "average-salary" FROM employee;', names=True)
ex(L, 'Geef het gemiddelde van alle VERSCHILLENDE salarissen, kolomnaam "average-distinct-salaries".',
   'SELECT AVG(DISTINCT salary) AS "average-distinct-salaries" FROM employee;', "AVG(DISTINCT ...)", names=True)
ex(L, 'Geef de som van de salarissen van afdeling 1, kolomnaam "salary-total-dep-1".',
   'SELECT SUM(salary) AS "salary-total-dep-1" FROM employee WHERE department = 1;', names=True)
ex(L, "Geef in één rij de alfabetisch eerste voornaam en de alfabetisch laatste achternaam.",
   "SELECT MIN(firstname), MAX(lastname) FROM employee;", "MIN en MAX werken ook op tekst")
ex(L, 'Geef per afdelingsnummer ("department") het aantal medewerkers ("employees").',
   'SELECT department AS "department", COUNT(*) AS "employees" FROM employee GROUP BY department;', names=True)
ex(L, 'Geef per afdeling ("department") het gemiddelde salaris ("average-salary") en dat gemiddelde maal 1,25 ("new-average-salary").',
   'SELECT department AS "department", AVG(salary) AS "average-salary", AVG(salary) * 1.25 AS "new-average-salary" FROM employee GROUP BY department;',
   names=True)
ex(L, 'Geef per medewerker ("employee") het totaal aantal uren op alle projecten ("total-hours"). Alles staat in works_on.',
   'SELECT employee AS "employee", SUM(hours) AS "total-hours" FROM works_on GROUP BY employee;', names=True)
ex(L, "Geef per afdeling (behalve nr 1) het gemiddelde salaris, alleen afdelingen met gemiddelde > 35000, gesorteerd op afdelingsnummer.",
   "SELECT department, AVG(salary) FROM employee WHERE department <> 1 GROUP BY department HAVING AVG(salary) > 35000 ORDER BY department;",
   "WHERE voor rijen, HAVING voor de groepen")
ex(L, 'Geef afdelingsnummer, afdelingsnaam en het aantal locaties ("locations"), gesorteerd op afdelingsnummer.',
   'SELECT department.id, department.name, COUNT(department_location.location) AS "locations" FROM department '
   'LEFT JOIN department_location ON department.id = department_location.department GROUP BY department.id, department.name ORDER BY department.id;',
   names=True)
ex(L, 'Geef afdelingsnaam ("department") en het aantal medewerkers ("employees"), gesorteerd op afdelingsnaam, zonder afdeling 8.',
   'SELECT department.name AS "department", COUNT(employee.id) AS "employees" FROM department '
   'JOIN employee ON department.id = employee.department WHERE department.id <> 8 GROUP BY department.name ORDER BY department.name;',
   names=True)
ex(L, "Geef voornaam, achternaam en totaal aantal gewerkte uren per medewerker (alleen medewerkers die uren hebben).",
   "SELECT firstname, lastname, SUM(hours) FROM employee JOIN works_on ON employee.id = works_on.employee GROUP BY employee.id, firstname, lastname;")
ex(L, "Geef per afdelingsnaam het hoogste en laagste salaris.",
   "SELECT department.name, MAX(salary), MIN(salary) FROM department JOIN employee ON department.id = employee.department GROUP BY department.name;")
ex(L, "Geef per project (naam) het aantal medewerkers dat eraan werkt.",
   "SELECT project.name, COUNT(works_on.employee) FROM project LEFT JOIN works_on ON project.id = works_on.project GROUP BY project.name;")
ex(L, "Geef de afdelingsnamen met meer dan 5 medewerkers, met het aantal.",
   "SELECT department.name, COUNT(*) FROM department JOIN employee ON department.id = employee.department GROUP BY department.name HAVING COUNT(*) > 5;")
ex(L, "Geef per afdelingsnaam het gemiddelde salaris, alleen voor afdelingen met gemiddeld meer dan 50000.",
   "SELECT department.name, AVG(salary) FROM department JOIN employee ON department.id = employee.department GROUP BY department.name HAVING AVG(salary) > 50000;")
ex(L, "Geef per project (naam) het totaal aantal uren, alleen projecten met meer dan 100 uur.",
   "SELECT project.name, SUM(hours) FROM project JOIN works_on ON project.id = works_on.project GROUP BY project.name HAVING SUM(hours) > 100;")
ex(L, "Geef medewerkers (id, achternaam) en het aantal projecten, alleen wie aan minstens 3 projecten werkt.",
   "SELECT employee.id, lastname, COUNT(*) FROM employee JOIN works_on ON employee.id = works_on.employee GROUP BY employee.id, lastname HAVING COUNT(*) >= 3;")
ex(L, "Deze query geeft een error: SELECT department.name, count(employee.id) FROM department LEFT JOIN employee ON department.id = employee.department "
      "WHERE COUNT(employee.id) > 1 GROUP BY department.name ORDER BY department.name;  Herschrijf hem zodat hij werkt.",
   "SELECT department.name, COUNT(employee.id) FROM department LEFT JOIN employee ON department.id = employee.department "
   "GROUP BY department.name HAVING COUNT(employee.id) > 1 ORDER BY department.name;", "Een kolomfunctie hoort in HAVING, niet in WHERE")

# ---------------- 3. Subqueries companydb (Week 3 DD2) ----------------
L = "sub_c"
ex(L, "Geef achternaam en salaris van alle medewerkers die meer verdienen dan het gemiddelde salaris. Gebruik een subquery.",
   "SELECT lastname, salary FROM employee WHERE salary > (SELECT AVG(salary) FROM employee);")
ex(L, "Geef id en achternaam van medewerkers met één of meer gezinsleden (dependent). Gebruik een subquery.",
   "SELECT id, lastname FROM employee WHERE id IN (SELECT employee FROM dependent);", "IN (SELECT employee FROM dependent)")
ex(L, "Geef id en achternaam van medewerkers ZONDER gezinsleden. Gebruik een subquery.",
   "SELECT id, lastname FROM employee WHERE id NOT IN (SELECT employee FROM dependent);")
ex(L, "Zelfde als hierboven (geen gezinsleden), maar nu met een JOIN in plaats van een subquery.",
   "SELECT employee.id, employee.lastname FROM employee LEFT JOIN dependent ON employee.id = dependent.employee WHERE dependent.employee IS NULL;",
   "LEFT JOIN ... WHERE dependent.employee IS NULL")
ex(L, "Geef achternaam en salaris van medewerkers die meer verdienen dan IEDEREEN van afdeling 6 (herschrijf '> ALL' met MAX).",
   "SELECT lastname, salary FROM employee WHERE salary > (SELECT MAX(salary) FROM employee WHERE department = 6);")
ex(L, "Geef achternaam en salaris van medewerkers die meer verdienen dan minstens één persoon van afdeling 6 ('> ANY' met een kolomfunctie).",
   "SELECT lastname, salary FROM employee WHERE salary > (SELECT MIN(salary) FROM employee WHERE department = 6);", "> ANY  ==  > MIN")
ex(L, "Geef achternaam en voornaam van medewerkers die werken aan project 10, 20 en/of 30, gesorteerd op achternaam.",
   "SELECT lastname, firstname FROM employee WHERE id IN (SELECT employee FROM works_on WHERE project IN (10, 20, 30)) ORDER BY lastname;")
ex(L, "Geef achternaam en voornaam van medewerkers die NIET aan project 10, 20 of 30 werken, gesorteerd op achternaam.",
   "SELECT lastname, firstname FROM employee WHERE id NOT IN (SELECT employee FROM works_on WHERE project IN (10, 20, 30)) ORDER BY lastname;")
ex(L, "Geef achternaam en voornaam van medewerkers die meer dan 40 uur aan project 'DatabaseSystem' werkten. Subquery in een subquery.",
   "SELECT lastname, firstname FROM employee WHERE id IN (SELECT employee FROM works_on WHERE hours > 40 AND project = "
   "(SELECT id FROM project WHERE name = 'DatabaseSystem'));")
ex(L, "Geef de namen van projecten waaraan geen enkele medewerker meer dan 20 uur heeft gewerkt.",
   "SELECT name FROM project WHERE id NOT IN (SELECT project FROM works_on WHERE hours > 20);")
ex(L, "Geef voornaam en achternaam van medewerkers die werken in een afdeling met minstens één locatie in 'Houston'.",
   "SELECT firstname, lastname FROM employee WHERE department IN (SELECT department FROM department_location WHERE location = 'Houston');")
ex(L, "Geef voornaam en achternaam van medewerkers die meer verdienen dan hun supervisor.",
   "SELECT e.firstname, e.lastname FROM employee e WHERE e.salary > (SELECT s.salary FROM employee s WHERE s.id = e.supervisor);",
   "Gecorreleerde subquery: geef employee twee aliassen (e en s)")
ex(L, "Geef voornaam, achternaam en salaris van medewerkers met minstens één gezinslid en een salaris lager dan 40000.",
   "SELECT firstname, lastname, salary FROM employee WHERE salary < 40000 AND id IN (SELECT employee FROM dependent);")
ex(L, "Geef voornaam en achternaam van medewerkers die meer verdienen dan het gemiddelde salaris van afdeling 'Research'.",
   "SELECT firstname, lastname FROM employee WHERE salary > (SELECT AVG(salary) FROM employee WHERE department = "
   "(SELECT id FROM department WHERE name = 'Research'));")
ex(L, "Geef voornaam en achternaam van medewerkers die meer verdienen dan het hoogste salaris in afdeling 'Administration'.",
   "SELECT firstname, lastname FROM employee WHERE salary > (SELECT MAX(salary) FROM employee WHERE department = "
   "(SELECT id FROM department WHERE name = 'Administration'));")
ex(L, "Geef voornaam en achternaam van medewerkers die werken aan een project waarvan de naam eindigt op 'System'.",
   "SELECT firstname, lastname FROM employee WHERE id IN (SELECT employee FROM works_on WHERE project IN "
   "(SELECT id FROM project WHERE name LIKE '%System'));")
ex(L, "Geef de namen van projecten die in dezelfde stad liggen als een locatie van de afdeling die het project beheert.",
   "SELECT name FROM project p WHERE p.location IN (SELECT location FROM department_location dl WHERE dl.department = p.department);")

# ---------------- 4. JOIN ziekenhuis ----------------
L = "join_zh"
ex(L, "Toon alle patiënten (nummer, achternaam, voornaam) met nummer en kamer_nummer van hun bed. Ook patiënten zonder bed!",
   "SELECT patient.nummer, patient.achternaam, patient.voornaam, bed.nummer, bed.kamer_nummer FROM patient "
   "LEFT JOIN patient_bed ON patient.nummer = patient_bed.patient_nr LEFT JOIN bed ON patient_bed.bed_nr = bed.nummer;",
   "LEFT JOIN patient_bed, dan LEFT JOIN bed")
ex(L, "Toon patiënten (nummer, achternaam, voornaam) met wetensch_naam en handelsnaam van hun voorgeschreven medicijnen.",
   "SELECT patient.nummer, patient.achternaam, patient.voornaam, medicijn.wetensch_naam, medicijn.handelsnaam FROM patient "
   "INNER JOIN recept ON patient.nummer = recept.patient_nr INNER JOIN medicijn ON recept.medicijn_cd = medicijn.cd;",
   "patient -> recept -> medicijn")
ex(L, "Toon personeel (nummer, achternaam, voornaam) met de titel van hun medisch specialisme.",
   "SELECT personeel.nummer, personeel.achternaam, personeel.voornaam, medisch_specialisme.titel FROM personeel "
   "INNER JOIN personeel_medspec ON personeel.nummer = personeel_medspec.pers_nr "
   "INNER JOIN medisch_specialisme ON personeel_medspec.medspec_cd = medisch_specialisme.cd;")
ex(L, "Toon behandelingen (nummer, behandel_datum, patient_nr, pers_nr) met omschrijving en rek_totaal van de verrichting.",
   "SELECT behandeling.nummer, behandeling.behandel_datum, behandeling.patient_nr, behandeling.pers_nr, verrichting.omschrijving, "
   "verrichting.rek_totaal FROM behandeling INNER JOIN verrichting ON behandeling.verrichting_nr = verrichting.nummer;")
ex(L, "Toon per kamer (nummer, omschrijving) de patiënten die er liggen (patient nummer, achternaam, voornaam).",
   "SELECT kamer.nummer, kamer.omschrijving, patient.nummer, patient.achternaam, patient.voornaam FROM kamer "
   "INNER JOIN bed ON kamer.nummer = bed.kamer_nummer INNER JOIN patient_bed ON bed.nummer = patient_bed.bed_nr "
   "INNER JOIN patient ON patient_bed.patient_nr = patient.nummer;", "kamer -> bed -> patient_bed -> patient")
ex(L, "Toon al het personeel (nummer, achternaam, voornaam) met de naam van hun afdeling. Ook personeel zonder afdeling.",
   "SELECT personeel.nummer, personeel.achternaam, personeel.voornaam, zh_afdeling.naam FROM personeel "
   "LEFT JOIN zh_afdeling ON personeel.afd_toegewezen = zh_afdeling.nummer;")
ex(L, "Toon de specialisme-titel met behandelingen (nummer, behandel_datum, patient_nr, pers_nr), gesorteerd op titel en dan behandelnummer.",
   "SELECT medisch_specialisme.titel, behandeling.nummer, behandeling.behandel_datum, behandeling.patient_nr, behandeling.pers_nr "
   "FROM behandeling INNER JOIN personeel ON behandeling.pers_nr = personeel.nummer "
   "INNER JOIN personeel_medspec ON personeel.nummer = personeel_medspec.pers_nr "
   "INNER JOIN medisch_specialisme ON personeel_medspec.medspec_cd = medisch_specialisme.cd ORDER BY medisch_specialisme.titel, behandeling.nummer;")

# ---------------- 5. GROUP BY ziekenhuis ----------------
L = "groupby_zh"
ex(L, "Tel per kamer_nummer hoeveel patiënten er (ooit) in een bed lagen. Ook kamers met 0.",
   "SELECT bed.kamer_nummer, COUNT(patient_bed.patient_nr) AS aantal_patienten FROM bed "
   "LEFT JOIN patient_bed ON bed.nummer = patient_bed.bed_nr GROUP BY bed.kamer_nummer;", "COUNT(kolom) telt NULL niet mee")
ex(L, "Bereken per eenheid de gemiddelde voorraad (voorraad_hoev) in medicijn.",
   "SELECT eenheid, AVG(voorraad_hoev) AS gemiddelde_voorraad FROM medicijn GROUP BY eenheid;")
ex(L, "Tel per patient_nr het aantal behandelingen.",
   "SELECT patient_nr, COUNT(*) AS totaal_aantal_behandelingen FROM behandeling GROUP BY patient_nr;")
ex(L, "Bereken per afdeling (afd_toegewezen) het gemiddelde salaris van personeel.",
   "SELECT afd_toegewezen, AVG(salaris) AS gemiddeld_salaris FROM personeel GROUP BY afd_toegewezen;")
ex(L, "Bereken per categorie (cat_nr) de totale kosten (rek_totaal) van verrichtingen.",
   "SELECT cat_nr, SUM(rek_totaal) AS totale_kosten FROM verrichting GROUP BY cat_nr;")
ex(L, "Tel per personeelslid (pers_nr) hoeveel VERSCHILLENDE patiënten het behandeld heeft.",
   "SELECT pers_nr, COUNT(DISTINCT patient_nr) AS aantal_patienten FROM behandeling GROUP BY pers_nr;", "COUNT(DISTINCT ...)")
ex(L, "Bereken per provincie de gemiddelde leeftijd in jaren van patiënten. (SQLite: (julianday('now') - julianday(geboortedatum)) / 365.25)",
   "SELECT provincie, AVG((julianday('now') - julianday(geboortedatum)) / 365.25) AS gemiddelde_leeftijd FROM patient GROUP BY provincie;")
ex(L, "Tel het aantal medicijnen per normale dosering (normale_dos).",
   "SELECT normale_dos, COUNT(*) AS aantal_medicijnen FROM medicijn GROUP BY normale_dos;")
ex(L, "Tel per personeelslid (pers_nr) het aantal behaalde specialismen.",
   "SELECT pers_nr, COUNT(medspec_cd) AS aantal_specialismen FROM personeel_medspec GROUP BY pers_nr;")

# ---------------- 6. HAVING ziekenhuis ----------------
L = "having_zh"
ex(L, "Vind afdelingen (afd_toegewezen) waar meer dan 2 personeelsleden werken, met het aantal.",
   "SELECT afd_toegewezen, COUNT(*) AS aantal_personeelsleden FROM personeel GROUP BY afd_toegewezen HAVING COUNT(*) > 2;")
ex(L, "Selecteer medicijnen (cd, voorraad_hoev) waarvan de voorraad lager is dan de gemiddelde voorraad.",
   "SELECT cd, voorraad_hoev FROM medicijn WHERE voorraad_hoev < (SELECT AVG(voorraad_hoev) FROM medicijn);",
   "Subquery met AVG (WHERE of HAVING mag allebei)")
ex(L, "Vind patiënten (patient_nr) met meer dan 3 behandelingen, met het aantal.",
   "SELECT patient_nr, COUNT(*) AS aantal_behandelingen FROM behandeling GROUP BY patient_nr HAVING COUNT(*) > 3;")
ex(L, "Zoek verrichtingen (nummer) waarvan de totale kosten (rek_totaal) meer dan 1000 zijn, met het totaal.",
   "SELECT nummer, SUM(rek_totaal) AS totale_kosten FROM verrichting GROUP BY nummer HAVING SUM(rek_totaal) > 1000;")
ex(L, "Identificeer specialismen (medspec_cd) met minder dan 4 gekwalificeerde personeelsleden, met het aantal.",
   "SELECT medspec_cd, COUNT(pers_nr) AS aantal_personeelsleden FROM personeel_medspec GROUP BY medspec_cd HAVING COUNT(pers_nr) < 4;")
ex(L, "Selecteer kamers (kamer_nummer) met meer dan 2 bedden, met het aantal.",
   "SELECT kamer_nummer, COUNT(*) AS aantal_bedden FROM bed GROUP BY kamer_nummer HAVING COUNT(*) > 2;")
ex(L, "Vind personeelsleden (pers_nr) met meer dan 1 specialisme, met het aantal.",
   "SELECT pers_nr, COUNT(medspec_cd) AS aantal_specialismen FROM personeel_medspec GROUP BY pers_nr HAVING COUNT(medspec_cd) > 1;")
ex(L, "Zoek medicijnen (medicijn_cd) die aan meer dan 10 VERSCHILLENDE patiënten zijn voorgeschreven, met het aantal.",
   "SELECT medicijn_cd, COUNT(DISTINCT patient_nr) AS aantal_patienten FROM recept GROUP BY medicijn_cd HAVING COUNT(DISTINCT patient_nr) > 10;")

# ---------------- 7. Subqueries ziekenhuis ----------------
L = "sub_zh"
ex(L, "Vind patiënten (nummer, achternaam, voornaam) die nog GEEN behandeling hebben gehad.",
   "SELECT nummer, achternaam, voornaam FROM patient WHERE nummer NOT IN (SELECT patient_nr FROM behandeling);")
ex(L, "Lijst medicijnen (cd, wetensch_naam, handelsnaam) die nog nooit zijn voorgeschreven.",
   "SELECT cd, wetensch_naam, handelsnaam FROM medicijn WHERE cd NOT IN (SELECT medicijn_cd FROM recept);")
ex(L, "Bepaal het meest voorgeschreven medicijn (cd, wetensch_naam, handelsnaam).",
   "SELECT cd, wetensch_naam, handelsnaam FROM medicijn WHERE cd = (SELECT medicijn_cd FROM recept GROUP BY medicijn_cd ORDER BY COUNT(*) DESC LIMIT 1);",
   "Subquery: GROUP BY medicijn_cd ORDER BY COUNT(*) DESC LIMIT 1")
ex(L, "Bereken per afdelingsnaam (zh_afdeling.naam) het gemiddelde salaris van het personeel.",
   "SELECT zh_afdeling.naam, AVG(personeel.salaris) FROM personeel LEFT JOIN zh_afdeling ON personeel.afd_toegewezen = zh_afdeling.nummer GROUP BY zh_afdeling.naam;")
ex(L, "Vind patiënten (nummer, achternaam, voornaam, geboortedatum) die ouder zijn dan de gemiddelde leeftijd. (Tip: ouder = eerder geboren)",
   "SELECT nummer, achternaam, voornaam, geboortedatum FROM patient WHERE julianday(geboortedatum) < (SELECT AVG(julianday(geboortedatum)) FROM patient);")
ex(L, "Afdelingen (naam + aantal personeel) met meer personeel dan het gemiddelde aantal per afdeling (tel alle afdelingen mee, ook met 0).",
   "SELECT zh_afdeling.naam, COUNT(personeel.nummer) AS aantal FROM zh_afdeling LEFT JOIN personeel ON zh_afdeling.nummer = personeel.afd_toegewezen "
   "GROUP BY zh_afdeling.naam HAVING COUNT(personeel.nummer) > (SELECT AVG(n) FROM (SELECT COUNT(personeel.nummer) AS n FROM zh_afdeling "
   "LEFT JOIN personeel ON zh_afdeling.nummer = personeel.afd_toegewezen GROUP BY zh_afdeling.nummer) AS sub);",
   "Subquery in FROM die per afdeling telt, daarvan AVG")
ex(L, "Lijst personeel (nummer, achternaam, voornaam, salaris) met een salaris boven het gemiddelde.",
   "SELECT nummer, achternaam, voornaam, salaris FROM personeel WHERE salaris > (SELECT AVG(salaris) FROM personeel);")
ex(L, "Identificeer het/de specialisme(n) (titel + aantal) met het hoogste aantal gekwalificeerde personeelsleden.",
   "SELECT medisch_specialisme.titel, COUNT(personeel_medspec.pers_nr) FROM medisch_specialisme LEFT JOIN personeel_medspec "
   "ON medisch_specialisme.cd = personeel_medspec.medspec_cd GROUP BY medisch_specialisme.titel HAVING COUNT(personeel_medspec.pers_nr) = "
   "(SELECT MAX(n) FROM (SELECT COUNT(pers_nr) AS n FROM personeel_medspec GROUP BY medspec_cd) AS sub);")
ex(L, "Vind kamers (nummer, omschrijving, aantal bedden) met meer bedden dan het gemiddelde per kamer.",
   "SELECT kamer.nummer, kamer.omschrijving, COUNT(bed.nummer) FROM kamer LEFT JOIN bed ON kamer.nummer = bed.kamer_nummer "
   "GROUP BY kamer.nummer, kamer.omschrijving HAVING COUNT(bed.nummer) > (SELECT AVG(n) FROM (SELECT COUNT(bed.nummer) AS n FROM kamer "
   "LEFT JOIN bed ON kamer.nummer = bed.kamer_nummer GROUP BY kamer.nummer) AS sub);")

# ---------------- 8. CodeGrade ----------------
L = "codegrade"
ex(L, "Maak een lijst van patiënten en hun voorgeschreven medicijnen. JOIN patient, recept, medicijn. Sorteer op achternaam en dan "
      "patiëntnummer en handelsnaam. Toon de eerste 50. Kolommen: nummer, achternaam, voornaam, wetensch_naam, handelsnaam.",
   "SELECT patient.nummer, patient.achternaam, patient.voornaam, medicijn.wetensch_naam, medicijn.handelsnaam FROM patient "
   "INNER JOIN recept ON patient.nummer = recept.patient_nr INNER JOIN medicijn ON recept.medicijn_cd = medicijn.cd "
   "ORDER BY patient.achternaam, patient.nummer, medicijn.handelsnaam LIMIT 50;", "ORDER BY a, b, c LIMIT 50", names=True)
ex(L, "Tel het aantal behandelingen per patiënt. Kolommen: patient_nr en totaal_aantal_behandelingen.",
   "SELECT patient_nr, COUNT(*) AS totaal_aantal_behandelingen FROM behandeling GROUP BY patient_nr;", names=True)
ex(L, "Bepaal welk medicijn het meest is voorgeschreven (gebruik een subquery). Kolommen: cd, wetensch_naam, handelsnaam.",
   "SELECT cd, wetensch_naam, handelsnaam FROM medicijn WHERE cd = (SELECT medicijn_cd FROM recept GROUP BY medicijn_cd ORDER BY COUNT(*) DESC LIMIT 1);",
   names=True)

# ---------------- 9. DDL / DML ----------------
L = "ddl"
ex(L, "Maak een tabel teacher met kolommen id (primary key), name en subject. Voeg 3 docenten toe: (1,'Michiel Boere','Wiskunde'), "
      "(2,'James Wall','Wiskunde'), (3,'Anna Smit','Databases').",
   "CREATE TABLE teacher (id INTEGER PRIMARY KEY, name VARCHAR(50), subject VARCHAR(50));"
   "INSERT INTO teacher VALUES (1,'Michiel Boere','Wiskunde'),(2,'James Wall','Wiskunde'),(3,'Anna Smit','Databases');",
   "CREATE TABLE ... ; INSERT INTO ... VALUES (...), (...);", check="SELECT id, name, subject FROM teacher;")
ex(L, "Tabel teacher bestaat al. Update het vak van Michiel Boere naar 'Logica' en verwijder daarna Anna Smit.",
   "UPDATE teacher SET subject = 'Logica' WHERE name = 'Michiel Boere'; DELETE FROM teacher WHERE name = 'Anna Smit';",
   "UPDATE ... SET ... WHERE ...; DELETE FROM ... WHERE ...;", check="SELECT * FROM teacher;",
   setup="CREATE TABLE teacher (id INTEGER PRIMARY KEY, name VARCHAR(50), subject VARCHAR(50));"
         "INSERT INTO teacher VALUES (1,'Michiel Boere','Wiskunde'),(2,'James Wall','Wiskunde'),(3,'Anna Smit','Databases');")
ex(L, "Tabel teacher bestaat al. Toon alleen de namen van docenten die Wiskunde geven, gesorteerd op naam.",
   "SELECT name FROM teacher WHERE subject = 'Wiskunde' ORDER BY name;",
   setup="CREATE TABLE teacher (id INTEGER PRIMARY KEY, name VARCHAR(50), subject VARCHAR(50));"
         "INSERT INTO teacher VALUES (1,'Michiel Boere','Wiskunde'),(2,'James Wall','Wiskunde'),(3,'Anna Smit','Databases');")
ex(L, "(singer/song bestaan, met ON DELETE CASCADE) Maak tabel album: id (PK), title, singer (FK naar singer.id), release_year. "
      "Voeg album (1, 'Bangerz', 1, 2013) toe.",
   "CREATE TABLE album (id INTEGER PRIMARY KEY, title TEXT, singer INTEGER REFERENCES singer(id), release_year INTEGER);"
   "INSERT INTO album VALUES (1, 'Bangerz', 1, 2013);", check="SELECT id, title, singer, release_year FROM album;", setup=SINGER_SETUP)
ex(L, "(singer/song bestaan, met ON DELETE CASCADE) Verwijder Lady Gaga uit singer. Wat gebeurt er met haar songs? Controleer met SELECT * FROM song.",
   "DELETE FROM singer WHERE firstname = 'Lady' AND lastname = 'Gaga';", check="SELECT * FROM song;", setup=SINGER_SETUP,
   hint="Door ON DELETE CASCADE verdwijnt 'Bad Romance' ook")
ex(L, "(singer/song bestaan, met ON UPDATE CASCADE) Verander het id van Selena Gomez van 3 naar 33.",
   "UPDATE singer SET id = 33 WHERE id = 3;", check="SELECT * FROM song ORDER BY id;", setup=SINGER_SETUP,
   hint="Kijk daarna naar song: de FK verandert mee")
ex(L, "(singer bestaat) Maak een UNIQUE index idx_singer_name op firstname en lastname van singer.",
   "CREATE UNIQUE INDEX idx_singer_name ON singer (firstname, lastname);",
   check="SELECT name, \"unique\" FROM pragma_index_list('singer') WHERE name = 'idx_singer_name';", setup=SINGER_SETUP)
ex(L, "Maak tabellen club (id PK, name, city) en matchup (id PK, hometeam, awayteam, year) waarbij hometeam en awayteam "
      "verwijzen naar club(id) met ON DELETE CASCADE. Voeg Ajax/Amsterdam (1), PSV/Eindhoven (2), Feyenoord/Rotterdam (3) toe "
      "en de wedstrijd (1, 1, 2, 2023). Verwijder daarna club PSV.",
   "CREATE TABLE club (id INTEGER PRIMARY KEY, name TEXT, city TEXT);"
   "CREATE TABLE matchup (id INTEGER PRIMARY KEY, hometeam INTEGER REFERENCES club(id) ON DELETE CASCADE, "
   "awayteam INTEGER REFERENCES club(id) ON DELETE CASCADE, year INTEGER);"
   "INSERT INTO club VALUES (1,'Ajax','Amsterdam'),(2,'PSV','Eindhoven'),(3,'Feyenoord','Rotterdam');"
   "INSERT INTO matchup VALUES (1,1,2,2023); DELETE FROM club WHERE name = 'PSV';",
   check="SELECT (SELECT COUNT(*) FROM club), (SELECT COUNT(*) FROM matchup);",
   hint="Na het verwijderen van PSV moet de wedstrijd ook weg zijn")

# ---------------- 10. Oefentoets bibliotheek ----------------
L = "toets"
ex(L, "Toon alle medewerkers die man zijn en in afdeling 4 werken. Toon firstname, lastname en salary. Sorteer op salaris aflopend.",
   "SELECT firstname, lastname, salary FROM employee WHERE sex = 'M' AND department = 4 ORDER BY salary DESC;")
ex(L, "Toon de medewerkers die geen manager hebben. Toon firstname, lastname en ssn. Sorteer op ssn.",
   "SELECT firstname, lastname, ssn FROM employee WHERE manager IS NULL ORDER BY ssn;")
ex(L, "Geef het aantal werknemers per afdeling. Toon de afdelingsnaam en het aantal (count). Sorteer op aantal aflopend, dan op naam.",
   "SELECT department.name, COUNT(employee.id) AS count FROM department JOIN employee ON department.id = employee.department "
   "GROUP BY department.name ORDER BY count DESC, department.name;")
ex(L, "Toon alle boeken die (ooit) uitgeleend zijn: title, isbn, publicationyear en categorienaam (name). Sorteer op name aflopend, dan title. Gebruik een subquery.",
   "SELECT book.title, book.isbn, book.publicationyear, category.name FROM book JOIN category ON book.category = category.id "
   "WHERE book.id IN (SELECT book FROM loan) ORDER BY category.name DESC, book.title;")
ex(L, "Maak de tabellen company (id, name, street, city, state) en contact (id, firstname, initial, lastname, phone, email, company), "
      "waarbij contact.company een FK naar company is (kies zelf de referentiële actie). Voeg de 2 bedrijven en 2 contactpersonen uit de toets toe:\n"
      "  company: (1,'Blue Origin Enterprises, L.P.','21218 76th Ave S','Kent','WA'), (2,'Space Exploration Technologies Corp.','1 Rocket Road','Starbase','TX')\n"
      "  contact: (1,'Elon','R','Musk','310.363.6220','info@spacex.com',2), (2,'Jeff','P','Bezos','253.437.9300','info@blueorigin.com',1)\n"
      "Verander daarna met één statement het e-mailadres van Elon Musk in elon@spacex.com.",
   "CREATE TABLE company (id INTEGER PRIMARY KEY, name VARCHAR(100) NOT NULL, street VARCHAR(100), city VARCHAR(50), state CHAR(2));"
   "CREATE TABLE contact (id INTEGER PRIMARY KEY, firstname VARCHAR(50) NOT NULL, initial CHAR(1), lastname VARCHAR(50) NOT NULL, "
   "phone VARCHAR(20), email VARCHAR(100) UNIQUE, company INTEGER REFERENCES company(id) ON DELETE CASCADE);"
   "INSERT INTO company VALUES (1,'Blue Origin Enterprises, L.P.','21218 76th Ave S','Kent','WA'),"
   "(2,'Space Exploration Technologies Corp.','1 Rocket Road','Starbase','TX');"
   "INSERT INTO contact VALUES (1,'Elon','R','Musk','310.363.6220','info@spacex.com',2),(2,'Jeff','P','Bezos','253.437.9300','info@blueorigin.com',1);"
   "UPDATE contact SET email = 'elon@spacex.com' WHERE firstname = 'Elon' AND lastname = 'Musk';",
   check="SELECT c.id, c.firstname, c.lastname, c.email, co.name FROM contact c JOIN company co ON c.company = co.id;",
   hint="Denk ook na (op papier) wat DROP TABLE company doet met contact, afhankelijk van je ON DELETE keuze")
