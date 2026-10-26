"""Alle lessen en oefeningen (PostgreSQL), opgebouwd vanaf nul tot toetsniveau.

Per oefening:
  q       de vraag
  sol     correcte uitwerking (jouw resultaat wordt vergeleken met het resultaat hiervan)
  hint    duwtje in de goede richting
  check   (optioneel) query die NA jouw statements draait; voor CREATE/INSERT/UPDATE/DELETE
  setup   (optioneel) SQL die vooraf wordt uitgevoerd
  names   True = kolomnamen (aliassen) moeten ook kloppen
  db      (optioneel) andere database dan die van de les
  choices (optioneel) meerkeuzevraag: lijst opties; sol = juiste letter
"""

LESSONS = []
E = []


def lesson(id, title, db, uitleg):
    LESSONS.append(dict(id=id, title=title, db=db, uitleg=uitleg))


def ex(q, sol, hint="", names=False, check=None, setup=None, db=None, choices=None, uitleg=""):
    E.append(dict(lesson=LESSONS[-1]["id"], q=q, sol=sol.strip(), hint=hint, names=names,
                  check=check, setup=setup, db=db, choices=choices, uitleg=uitleg))


MATCH_SETUP = """
CREATE TABLE match_schedule (id SERIAL PRIMARY KEY, hometeam TEXT, awayteam TEXT,
  matchdate TIMESTAMP WITH TIME ZONE, lastupdate TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP);
INSERT INTO match_schedule (hometeam, awayteam, matchdate) VALUES ('Ajax', 'PSV', '2024-10-10 14:30'),
 ('Feyenoord', 'AZ', '2024-10-15 16:45'), ('Twente', 'Utrecht', '2024-10-20 18:00'),
 ('Vitesse', 'Sparta', '2024-11-05 20:00'), ('Heerenveen', 'Groningen', '2024-12-01 12:00');
"""

SINGER_SETUP = """
CREATE TABLE singer (id INTEGER, firstname TEXT, lastname TEXT, age INTEGER, PRIMARY KEY (id));
INSERT INTO singer VALUES (1,'Miley','Cyrus',27),(2,'Carley Rae','Jepsen',35),(3,'Selena','Gomez',28),
 (4,'Ariane','Grande',27),(5,'Lady','Gaga',34);
CREATE TABLE song (id INTEGER, name TEXT, year INTEGER, singer INTEGER, PRIMARY KEY (id),
 FOREIGN KEY (singer) REFERENCES singer (id));
INSERT INTO song VALUES (1,'Bad Romance',2008,5),(2,'Bang Bang',2014,4),(3,'It Ain''t Me',2017,3),
 (4,'Call Me Maybe',2012,2),(5,'Wrecking Ball',2013,1);
"""

TEACHER_SETUP = """CREATE TABLE teacher (id SERIAL PRIMARY KEY, name VARCHAR(50), subject VARCHAR(50));
INSERT INTO teacher (name, subject) VALUES ('Michiel Boere','Wiskunde'),('James Wall','Wiskunde'),('Anna Smit','Databases');"""

# =====================================================================================
lesson("start", "1. Je eerste query: SELECT ... FROM", "companydb", """\
Een DATABASE bestaat uit TABELLEN. Een tabel is net een spreadsheet:
  - kolommen  = de eigenschappen   (bijv. firstname, lastname, salary)
  - rijen     = de records         (elke rij is 1 werknemer)

We gebruiken de 'companydb' van de cursus. Belangrijkste tabel: employee (werknemers).

Gegevens opvragen doe je met SELECT:

    SELECT *         FROM employee;     -- * = alle kolommen
    SELECT lastname  FROM employee;     -- alleen de kolom lastname
    SELECT firstname, lastname FROM employee;   -- meerdere kolommen: komma ertussen

Regels:
  - Eindig elke query met een puntkomma ;
  - Hoofdletters maken niet uit (SELECT = select), maar SQL-woorden in HOOFDLETTERS leest makkelijker.
  - Typ :schema om alle tabellen en kolommen te zien (doe dat nu eens!).""")
ex("Toon ALLE kolommen en rijen van de tabel employee.", "SELECT * FROM employee;", "SELECT * FROM tabelnaam;")
ex("Toon alleen de kolom lastname van alle werknemers.", "SELECT lastname FROM employee;")
ex("Toon de voornaam (firstname) en achternaam (lastname) van alle werknemers.", "SELECT firstname, lastname FROM employee;",
   "Kolommen scheiden met een komma")
ex("Toon alle kolommen van de tabel department (afdelingen).", "SELECT * FROM department;")
ex("Toon van elk project (tabel project) de naam en de locatie.", "SELECT name, location FROM project;",
   "Kijk met :schema project welke kolommen er zijn")
ex("Toon van alle werknemers: achternaam, salaris en afdeling (department), in die volgorde.",
   "SELECT lastname, salary, department FROM employee;", "De volgorde in SELECT = de volgorde van de kolommen")

# =====================================================================================
lesson("reken", "2. Rekenen, tekst en kolomnamen (AS)", "companydb", """\
SELECT kan ook rekenen, zelfs zonder tabel:

    SELECT 10 - 3;                 -- 7
    SELECT 1, 2, 3;                -- drie kolommen
    SELECT PI() * POWER(5, 2);     -- oppervlakte cirkel met straal 5
    SELECT ROUND(3.14159, 2);      -- 3.14

Met kolommen uit een tabel:
    SELECT lastname, salary * 12 FROM employee;

Tekst staat tussen ENKELE quotes 'zo'. Plakken met ||:
    SELECT firstname || ' ' || lastname FROM employee;
Handige tekstfuncties: UPPER(), LOWER(), LENGTH()

Kolom een naam geven met AS (alias):
    SELECT salary * 12 AS jaarsalaris FROM employee;
    SELECT 1 AS "Mijn Kolom";    -- dubbele quotes bij spaties/hoofdletters/streepjes

In PostgreSQL: 'tekst' = waarde, "naam" = kolomnaam. Niet door elkaar halen!""")
ex("Selecteer de getallen 1, 2, 3, 4 en 5 als vijf kolommen (zonder tabel).", "SELECT 1, 2, 3, 4, 5;", "SELECT 1, 2, ...;")
ex("Bereken het verschil tussen 250 en 75.", "SELECT 250 - 75;")
ex("Bereken de oppervlakte van een cirkel met straal 5. Gebruik PI() en POWER().", "SELECT PI() * POWER(5, 2);")
ex("Maak de zin 'SQL is leuk' door 'SQL', ' is ' en 'leuk' aan elkaar te plakken met ||.", "SELECT 'SQL' || ' is ' || 'leuk';")
ex("Toon van elke werknemer één kolom 'naam' met voornaam, spatie, achternaam (bijv. 'John Smith').",
   "SELECT firstname || ' ' || lastname AS naam FROM employee;", "firstname || ' ' || lastname AS naam", names=True)
ex("Toon achternaam en het jaarsalaris (salary * 12) met kolomnaam jaarsalaris.",
   "SELECT lastname, salary * 12 AS jaarsalaris FROM employee;", names=True)
ex("Toon de achternamen in HOOFDLETTERS met kolomnaam achternaam.", "SELECT UPPER(lastname) AS achternaam FROM employee;",
   "UPPER(...)", names=True)
ex('Toon achternaam en salaris met 10% verhoging, kolomnaam "nieuw salaris".',
   'SELECT lastname, salary * 1.10 AS "nieuw salaris" FROM employee;', 'Alias met spatie: dubbele quotes', names=True)

# =====================================================================================
lesson("where", "3. Filteren met WHERE", "companydb", """\
Met WHERE kies je welke RIJEN je wilt zien:

    SELECT * FROM employee WHERE department = 5;
    SELECT * FROM employee WHERE salary > 50000;
    SELECT * FROM employee WHERE sex = 'F';          -- tekst tussen enkele quotes
    SELECT * FROM employee WHERE birthdate < '1980-01-01';   -- datum ook als tekst

Vergelijken:  =   <> (niet gelijk, ook !=)   <   >   <=   >=
Combineren:   AND (beide waar)   OR (een van beide)   NOT
    WHERE salary > 50000 AND department = 7
    WHERE department = 5 OR department = 6
Gebruik haakjes bij AND en OR samen:  WHERE (a OR b) AND c

Volgorde in de query: SELECT ... FROM ... WHERE ...""")
ex("Toon alle informatie van werknemers die op afdeling 5 werken.", "SELECT * FROM employee WHERE department = 5;")
ex("Haal voor- en achternamen op van alle mannelijke werknemers (sex = 'M').",
   "SELECT firstname, lastname FROM employee WHERE sex = 'M';")
ex("Vind alle informatie van werknemers die begeleid worden door leidinggevende (supervisor) nummer 30.",
   "SELECT * FROM employee WHERE supervisor = 30;")
ex("Vind id, voornaam, achternaam, salaris en afdeling van werknemers met meer dan 50000 salaris die op afdeling 7 werken.",
   "SELECT id, firstname, lastname, salary, department FROM employee WHERE salary > 50000 AND department = 7;", "AND")
ex("Haal de volledige namen (voornaam, achternaam) op van werknemers die NIET op afdeling 7 werken.",
   "SELECT firstname, lastname FROM employee WHERE department <> 7;", "<>")
ex("Vind alle informatie van werknemers met een salaris van minder dan 40000 of meer dan 80000.",
   "SELECT * FROM employee WHERE salary < 40000 OR salary > 80000;", "OR")
ex("Haal voor- en achternamen op van werknemers die op afdeling 5 of 6 werken.",
   "SELECT firstname, lastname FROM employee WHERE department = 5 OR department = 6;")
ex("Toon voornaam en achternaam van vrouwen (sex = 'F') die op afdeling 6 of 7 werken. Let op de haakjes!",
   "SELECT firstname, lastname FROM employee WHERE sex = 'F' AND (department = 6 OR department = 7);",
   "sex = 'F' AND (... OR ...)")

# =====================================================================================
lesson("like", "4. LIKE, ILIKE, IN, BETWEEN en IS NULL", "companydb", """\
    IN (...)            komt voor in een lijst:     WHERE lastname IN ('Best', 'King')
    BETWEEN a AND b     tussen (grenzen doen mee):  WHERE salary BETWEEN 40000 AND 70000
    LIKE                tekstpatroon:  % = willekeurige tekst, _ = precies 1 teken
                        WHERE address LIKE '%Houston%'    -- bevat Houston
                        WHERE lastname LIKE 'B%'          -- begint met B
                        WHERE address LIKE '%TX'          -- eindigt op TX
    ILIKE               als LIKE maar hoofdletter-ONgevoelig (alleen PostgreSQL!)
    NOT IN / NOT LIKE / NOT BETWEEN   het omgekeerde

    IS NULL / IS NOT NULL   leeg veld.  NOOIT  = NULL  schrijven, dat werkt niet!
                        WHERE supervisor IS NULL""")
ex("Geef achternaam en salaris van medewerkers met achternaam 'Best', 'English' of 'King'. Gebruik IN.",
   "SELECT lastname, salary FROM employee WHERE lastname IN ('Best', 'English', 'King');")
ex("Haal voor- en achternamen op van werknemers geboren tussen 1 januari 1980 en 31 december 1990. Gebruik BETWEEN.",
   "SELECT firstname, lastname FROM employee WHERE birthdate BETWEEN '1980-01-01' AND '1990-12-31';")
ex("Vind volledige naam en salaris van werknemers met een salaris tussen 40000 en 70000.",
   "SELECT firstname, lastname, salary FROM employee WHERE salary BETWEEN 40000 AND 70000;")
ex("Haal volledige namen en salarissen op van werknemers die GEEN leidinggevende (supervisor) hebben.",
   "SELECT firstname, lastname, salary FROM employee WHERE supervisor IS NULL;", "IS NULL")
ex("Toon voornaam en achternaam van werknemers waarvan de achternaam met 'B' begint.",
   "SELECT firstname, lastname FROM employee WHERE lastname LIKE 'B%';", "LIKE 'B%'")
ex("Toon voornaam, achternaam en adres van werknemers die in Houston wonen (address bevat 'Houston').",
   "SELECT firstname, lastname, address FROM employee WHERE address LIKE '%Houston%';")
ex("Toon voornaam en achternaam van werknemers waarvan de achternaam begint met 'ja' (kleine letters in je patroon!). Gebruik ILIKE.",
   "SELECT firstname, lastname FROM employee WHERE lastname ILIKE 'ja%';", "ILIKE 'ja%' vindt ook 'James' en 'Jarvis'")
ex("Vind alle werknemers (alle kolommen) die niet in Chicago, Milwaukee of Dallas wonen. Gebruik LIKE.",
   "SELECT * FROM employee WHERE address NOT LIKE '%Chicago%' AND address NOT LIKE '%Milwaukee%' AND address NOT LIKE '%Dallas%';",
   "NOT LIKE ... AND NOT LIKE ...")
ex("Haal volledige namen en salarissen op van werknemers die niet in een plaats wonen die eindigt op 'TX' of 'CA'.",
   "SELECT firstname, lastname, salary FROM employee WHERE address NOT LIKE '%TX' AND address NOT LIKE '%CA';")

# =====================================================================================
lesson("order", "5. Sorteren en beperken: ORDER BY, LIMIT, DISTINCT", "companydb", """\
    ORDER BY kolom          oplopend (A-Z, klein-groot) — ASC is de standaard
    ORDER BY kolom DESC     aflopend
    ORDER BY a, b           eerst op a, bij gelijke a op b
    LIMIT 5                 alleen de eerste 5 rijen
    SELECT DISTINCT kolom   dubbele waarden maar 1 keer

Volgorde van de onderdelen (uit je hoofd leren!):
    SELECT ... FROM ... WHERE ... ORDER BY ... LIMIT ...;""")
ex("Haal voor- en achternamen op van alle werknemers, gesorteerd op achternaam aflopend.",
   "SELECT firstname, lastname FROM employee ORDER BY lastname DESC;")
ex("Haal de unieke geboortedata op van alle werknemers.", "SELECT DISTINCT birthdate FROM employee;", "DISTINCT")
ex("Vind alle unieke steden (location) waar afdelingen zich bevinden (tabel department_location).",
   "SELECT DISTINCT location FROM department_location;")
ex("Toon achternaam en salaris van de 5 best verdienende werknemers (hoogste eerst).",
   "SELECT lastname, salary FROM employee ORDER BY salary DESC LIMIT 5;", "ORDER BY ... DESC LIMIT 5")
ex("Vind alle informatie van werknemers geboren vóór 1 januari 1980 die op afdeling 6 werken, gesorteerd op geboortedatum aflopend.",
   "SELECT * FROM employee WHERE birthdate < '1980-01-01' AND department = 6 ORDER BY birthdate DESC;")
ex("Toon afdeling, achternaam en voornaam van alle werknemers, gesorteerd op afdeling en daarbinnen op achternaam.",
   "SELECT department, lastname, firstname FROM employee ORDER BY department, lastname;")

# =====================================================================================
lesson("datum", "6. Datums en tijd in PostgreSQL", "leeg", """\
Datumtypes:  DATE (2024-10-10)   TIME (14:30)   TIMESTAMP (2024-10-10 14:30)
             TIMESTAMP WITH TIME ZONE (timestamptz, met tijdzone)

    CURRENT_DATE / NOW()             vandaag / nu
    kolom::date   kolom::time        omzetten (casten) naar een ander type  (ook: CAST(x AS date))
    datum + INTERVAL '30 days'       rekenen met tijd
    datum1 - datum2                  verschil (bij DATE: aantal dagen)
    AGE(geboortedatum)               leeftijd als interval (bijv. '45 years 3 mons')
    EXTRACT(YEAR FROM datum)         stuk eruit halen: YEAR, MONTH, DAY, HOUR, DOW, EPOCH
    DATE_PART('year', datum)         zelfde als EXTRACT
    MAKE_DATE(2024, 12, 25)          datum maken
    TO_CHAR(datum, 'formaat')        datum als tekst opmaken:
        'YYYY-MM-DD'   'DD-MM-YYYY'   'HH24:MI'   'HH12:MIam'
        'Day' (Monday   - opgevuld met spaties)   'FMDay' (Monday - zonder spaties)
        'Month' / 'FMMonth'   'DD'

In deze les bestaat de tabel match_schedule (wedstrijdschema) - typ :schema.""")
ex("Geef een lijst van alle wedstrijden: hometeam, awayteam en matchdate.",
   "SELECT hometeam, awayteam, matchdate FROM match_schedule;", setup=MATCH_SETUP)
ex("Toon hometeam, awayteam en alleen de DATUM (zonder tijd) van de wedstrijd.",
   "SELECT hometeam, awayteam, matchdate::date FROM match_schedule;", "::date", setup=MATCH_SETUP)
ex("Toon hometeam, awayteam en alleen het TIJDSTIP (zonder datum) van de wedstrijd.",
   "SELECT hometeam, awayteam, matchdate::time FROM match_schedule;", "::time", setup=MATCH_SETUP)
ex("Toon hometeam en de wedstrijddatum in het formaat 'Thursday, 10 October 2024, 02:30pm'. Gebruik TO_CHAR.",
   "SELECT hometeam, TO_CHAR(matchdate, 'FMDay, DD FMMonth YYYY, HH12:MIam') FROM match_schedule;",
   "TO_CHAR(matchdate, 'FMDay, DD FMMonth YYYY, HH12:MIam')", setup=MATCH_SETUP)
ex("Toon hometeam, matchdate en een extra kolom met de datum 30 dagen na de wedstrijd.",
   "SELECT hometeam, matchdate, matchdate + INTERVAL '30 days' FROM match_schedule;", "+ INTERVAL '30 days'", setup=MATCH_SETUP)
ex("Toon voor elke wedstrijd hometeam en op welke dag van de week (bijv. 'Thursday', zonder extra spaties) hij is.",
   "SELECT hometeam, TO_CHAR(matchdate, 'FMDay') FROM match_schedule;", "TO_CHAR(..., 'FMDay')", setup=MATCH_SETUP)
ex("Toon hometeam en een kolom met Kerstmis (25 december) van hetzelfde jaar als de wedstrijd, als datum.",
   "SELECT hometeam, MAKE_DATE(EXTRACT(YEAR FROM matchdate)::int, 12, 25) FROM match_schedule;",
   "MAKE_DATE(EXTRACT(YEAR FROM matchdate)::int, 12, 25)", setup=MATCH_SETUP)
ex("Bereken voor elke wedstrijd (hometeam) hoeveel dagen er zaten tussen 1 januari van dat jaar en de wedstrijddatum.",
   "SELECT hometeam, matchdate::date - MAKE_DATE(EXTRACT(YEAR FROM matchdate)::int, 1, 1) FROM match_schedule;",
   "datum - datum geeft dagen. Of: DATE_TRUNC('year', matchdate)", setup=MATCH_SETUP)
ex("(companydb) Toon voornaam, achternaam en het geboortejaar van elke werknemer. Gebruik EXTRACT.",
   "SELECT firstname, lastname, EXTRACT(YEAR FROM birthdate) FROM employee;", db="companydb")
ex("(companydb) Toon voornaam, achternaam en de leeftijd in hele jaren. Gebruik AGE en EXTRACT (of DATE_PART).",
   "SELECT firstname, lastname, EXTRACT(YEAR FROM AGE(birthdate)) FROM employee;",
   "EXTRACT(YEAR FROM AGE(birthdate))", db="companydb")

# =====================================================================================
lesson("aggr", "7. Kolomfuncties: COUNT, SUM, AVG, MIN, MAX", "companydb", """\
Een kolomfunctie (aggregatiefunctie) maakt van veel rijen ÉÉN waarde:

    SELECT COUNT(*)          FROM employee;   -- aantal rijen
    SELECT COUNT(supervisor) FROM employee;   -- aantal rijen waar supervisor NIET NULL is
    SELECT COUNT(DISTINCT department) FROM employee;  -- aantal verschillende waarden
    SELECT SUM(salary), AVG(salary), MIN(salary), MAX(salary) FROM employee;

Met WHERE eerst filteren:
    SELECT AVG(salary) FROM employee WHERE department = 5;

MIN en MAX werken ook op tekst (alfabetisch) en datums.
ROUND(AVG(salary), 2) rondt af op 2 decimalen.""")
ex("Geef het totaal aantal rijen van de tabel employee.", "SELECT COUNT(*) FROM employee;")
ex("Geef het gemiddelde, hoogste, laagste en totale salaris van alle werknemers (4 kolommen, in die volgorde).",
   "SELECT AVG(salary), MAX(salary), MIN(salary), SUM(salary) FROM employee;")
ex("Hoeveel werknemers werken op afdeling 8? (tel de salarissen: COUNT(salary))",
   "SELECT COUNT(salary) FROM employee WHERE department = 8;")
ex("Geef het aantal werknemers dat in Atlanta woont (één getal).",
   "SELECT COUNT(*) FROM employee WHERE address LIKE '%Atlanta%';")
ex('Geef het aantal medewerkers dat een leidinggevende (supervisor) heeft, kolomnaam "employees-having-manager".',
   'SELECT COUNT(supervisor) AS "employees-having-manager" FROM employee;', "COUNT(kolom) telt geen NULLs", names=True)
ex('Geef het gemiddelde salaris, kolomnaam "average-salary".', 'SELECT AVG(salary) AS "average-salary" FROM employee;', names=True)
ex('Geef het gemiddelde van alle VERSCHILLENDE salarissen, kolomnaam "average-distinct-salaries".',
   'SELECT AVG(DISTINCT salary) AS "average-distinct-salaries" FROM employee;', "AVG(DISTINCT ...)", names=True)
ex('Geef de som van de salarissen van afdeling 1, kolomnaam "salary-total-dep-1".',
   'SELECT SUM(salary) AS "salary-total-dep-1" FROM employee WHERE department = 1;', names=True)
ex("Geef in één rij de alfabetisch eerste voornaam en de alfabetisch laatste achternaam.",
   "SELECT MIN(firstname), MAX(lastname) FROM employee;")

# =====================================================================================
lesson("group", "8. GROUP BY en HAVING", "companydb", """\
GROUP BY maakt groepjes van rijen met dezelfde waarde. De kolomfunctie rekent dan PER groep:

    SELECT department, COUNT(*) FROM employee GROUP BY department;
    -> per afdeling het aantal werknemers

GOUDEN REGEL: elke kolom in SELECT die geen kolomfunctie is, MOET in GROUP BY staan.
    SELECT department, lastname FROM employee GROUP BY department;   -- FOUT in PostgreSQL!

WHERE  filtert RIJEN vóór het groeperen      (geen kolomfuncties in WHERE!)
HAVING filtert GROEPEN ná het groeperen      (wel kolomfuncties)
    SELECT department, AVG(salary) FROM employee
     WHERE department <> 1
     GROUP BY department
    HAVING AVG(salary) > 35000
     ORDER BY department;

Volgorde: SELECT .. FROM .. WHERE .. GROUP BY .. HAVING .. ORDER BY .. LIMIT""")
ex('Geef per afdelingsnummer ("department") het aantal medewerkers ("employees").',
   'SELECT department AS "department", COUNT(*) AS "employees" FROM employee GROUP BY department;', names=True)
ex('Geef per afdeling ("department") het gemiddelde salaris ("average-salary") en dat gemiddelde maal 1,25 ("new-average-salary").',
   'SELECT department AS "department", AVG(salary) AS "average-salary", AVG(salary) * 1.25 AS "new-average-salary" FROM employee GROUP BY department;',
   names=True)
ex('Geef per medewerker ("employee") het totaal aantal uren op alle projecten ("total-hours"). Alles staat in works_on.',
   'SELECT employee AS "employee", SUM(hours) AS "total-hours" FROM works_on GROUP BY employee;', names=True)
ex('Geef per medewerker met ssn groter dan \'333333333\' het id ("employee") en het gemiddeld aantal uren per project '
   '("average number of hours over all projects"), gesorteerd op id. (works_on + employee)',
   'SELECT employee AS "employee", AVG(hours) AS "average number of hours over all projects" FROM works_on '
   'WHERE employee IN (SELECT id FROM employee WHERE ssn > \'333333333\') GROUP BY employee ORDER BY employee;', names=True)
ex("Geef per afdeling (behalve nr 1) het gemiddelde salaris, alleen afdelingen met gemiddelde > 35000, gesorteerd op afdelingsnummer.",
   "SELECT department, AVG(salary) FROM employee WHERE department <> 1 GROUP BY department HAVING AVG(salary) > 35000 ORDER BY department;",
   "WHERE voor rijen, HAVING voor de groepen")
ex("Geef per afdeling (nummer) het aantal VERSCHILLENDE salarisbedragen.",
   "SELECT department, COUNT(DISTINCT salary) FROM employee GROUP BY department;")
ex("Geef per afdeling (nummer) het hoogste salaris, alleen als dat hoogste salaris meer dan 80000 is.",
   "SELECT department, MAX(salary) FROM employee GROUP BY department HAVING MAX(salary) > 80000;")
ex("Geef per afdeling (nummer) het aantal medewerkers, gesorteerd op aantal aflopend (bij gelijk aantal op afdelingsnummer).",
   "SELECT department, COUNT(*) FROM employee GROUP BY department ORDER BY COUNT(*) DESC, department;")
ex("Geef per afdeling (nummer) het aantal medewerkers dat meer dan 50000 verdient.",
   "SELECT department, COUNT(*) FROM employee WHERE salary > 50000 GROUP BY department;", "Filter eerst met WHERE")
ex("Geef medewerkers (works_on.employee) met hun totaal aantal uren, alleen wie aan meer dan 1 project werkt.",
   "SELECT employee, SUM(hours) FROM works_on GROUP BY employee HAVING COUNT(*) > 1;")

# =====================================================================================
lesson("join", "9. JOIN: tabellen koppelen", "companydb", """\
Gegevens staan verspreid over tabellen. Ze zijn verbonden via KEYS:
  employee.department  verwijst naar  department.id     (foreign key -> primary key)

JOIN koppelt rijen waarvan die kolommen gelijk zijn:

    SELECT employee.lastname, department.name
      FROM employee
     INNER JOIN department ON employee.department = department.id;

  INNER JOIN   alleen rijen die in BEIDE tabellen een match hebben  (JOIN = INNER JOIN)
  LEFT JOIN    ALLE rijen van de linker tabel; geen match -> NULL in de rechter kolommen

Aliassen maken het korter:
    SELECT e.lastname, d.name FROM employee e JOIN department d ON e.department = d.id;

Een tabel met zichzelf koppelen (self join), bijv. werknemer + zijn supervisor:
    SELECT e.lastname, s.lastname FROM employee e JOIN employee s ON e.supervisor = s.id;

Meer tabellen: gewoon nog een JOIN ... ON ... erachter.""")
ex("Toon achternaam van elke werknemer met de naam van zijn afdeling.",
   "SELECT employee.lastname, department.name FROM employee INNER JOIN department ON employee.department = department.id;",
   "JOIN department ON employee.department = department.id")
ex("Toon voor elke afdeling de naam en alle locaties (department + department_location), gesorteerd op afdelingsnummer en locatie.",
   "SELECT department.id, department.name, department_location.location FROM department "
   "JOIN department_location ON department.id = department_location.department ORDER BY department.id, department_location.location;")
ex("Toon achternaam van werknemers die in de afdeling 'Software' werken en meer dan 75000 verdienen, met hun salaris.",
   "SELECT e.lastname, e.salary FROM employee e JOIN department d ON e.department = d.id WHERE d.name = 'Software' AND e.salary > 75000;")
ex("Toon de achternaam van elke werknemer met de achternaam van zijn supervisor (alleen werknemers met supervisor).",
   "SELECT e.lastname, s.lastname FROM employee e JOIN employee s ON e.supervisor = s.id;", "Self join: employee e JOIN employee s")
ex("Toon voornaam, achternaam en totaal aantal gewerkte uren per medewerker (alleen medewerkers met uren).",
   "SELECT firstname, lastname, SUM(hours) FROM employee JOIN works_on ON employee.id = works_on.employee GROUP BY employee.id, firstname, lastname;")
ex('Geef afdelingsnaam ("department") en het aantal medewerkers ("employees"), gesorteerd op afdelingsnaam, zonder afdeling 8.',
   'SELECT department.name AS "department", COUNT(employee.id) AS "employees" FROM department '
   'JOIN employee ON department.id = employee.department WHERE department.id <> 8 GROUP BY department.name ORDER BY department.name;', names=True)
ex('Geef afdelingsnummer, afdelingsnaam en het aantal locaties ("locations"), gesorteerd op afdelingsnummer.',
   'SELECT department.id, department.name, COUNT(department_location.location) AS "locations" FROM department '
   'LEFT JOIN department_location ON department.id = department_location.department GROUP BY department.id, department.name ORDER BY department.id;',
   names=True)
ex("Geef per project (naam) het aantal medewerkers en het totaal aantal uren. Ook projecten zonder medewerkers.",
   "SELECT project.name, COUNT(works_on.employee), SUM(works_on.hours) FROM project LEFT JOIN works_on ON project.id = works_on.project GROUP BY project.name;",
   "LEFT JOIN")
ex("Geef per afdelingsnaam het hoogste en laagste salaris.",
   "SELECT department.name, MAX(salary), MIN(salary) FROM department JOIN employee ON department.id = employee.department GROUP BY department.name;")
ex("Deze query geeft een error: SELECT department.name, count(employee.id) FROM department LEFT JOIN employee ON department.id = employee.department "
   "WHERE COUNT(employee.id) > 1 GROUP BY department.name ORDER BY department.name;  Herschrijf hem zodat hij werkt.",
   "SELECT department.name, COUNT(employee.id) FROM department LEFT JOIN employee ON department.id = employee.department "
   "GROUP BY department.name HAVING COUNT(employee.id) > 1 ORDER BY department.name;", "Kolomfunctie hoort in HAVING")

# =====================================================================================
lesson("sub", "10. Subqueries", "companydb", """\
Een subquery is een query binnen een query, tussen haakjes. De binnenste wordt eerst uitgevoerd.

  Eén waarde:  WHERE salary > (SELECT AVG(salary) FROM employee)
  Lijst:       WHERE id IN     (SELECT employee FROM dependent)
               WHERE id NOT IN (SELECT employee FROM dependent)
  ALL / ANY:   salary > ALL (SELECT salary FROM employee WHERE department = 6)   -- groter dan allemaal (= > MAX)
               salary > ANY (SELECT ...)                                         -- groter dan minstens één (= > MIN)
  EXISTS:      WHERE EXISTS (SELECT 1 FROM dependent d WHERE d.employee = e.id)

Gecorreleerde subquery: gebruikt een kolom van de buitenste query:
  SELECT e.lastname FROM employee e
   WHERE e.salary > (SELECT s.salary FROM employee s WHERE s.id = e.supervisor);

LET OP: na = < > mag de subquery maar 1 waarde (1 rij, 1 kolom) teruggeven.
        Na IN mag de subquery maar 1 kolom hebben.""")
ex("Geef achternaam en salaris van medewerkers die meer verdienen dan het gemiddelde salaris. Gebruik een subquery.",
   "SELECT lastname, salary FROM employee WHERE salary > (SELECT AVG(salary) FROM employee);")
ex("Geef id en achternaam van medewerkers met één of meer gezinsleden (tabel dependent). Gebruik een subquery.",
   "SELECT id, lastname FROM employee WHERE id IN (SELECT employee FROM dependent);")
ex("Geef id en achternaam van medewerkers ZONDER gezinsleden. Gebruik een subquery.",
   "SELECT id, lastname FROM employee WHERE id NOT IN (SELECT employee FROM dependent);")
ex("Zelfde (geen gezinsleden), maar nu met een LEFT JOIN in plaats van een subquery.",
   "SELECT employee.id, employee.lastname FROM employee LEFT JOIN dependent ON employee.id = dependent.employee WHERE dependent.employee IS NULL;",
   "LEFT JOIN ... WHERE dependent.employee IS NULL")
ex("Geef achternaam en salaris van medewerkers die meer verdienen dan IEDEREEN van afdeling 6. Gebruik ALL.",
   "SELECT lastname, salary FROM employee WHERE salary > ALL (SELECT salary FROM employee WHERE department = 6);")
ex("Zelfde als hierboven, maar herschrijf met de kolomfunctie MAX in plaats van ALL.",
   "SELECT lastname, salary FROM employee WHERE salary > (SELECT MAX(salary) FROM employee WHERE department = 6);")
ex("Geef achternaam en salaris van medewerkers die minder verdienen dan minstens één persoon van afdeling 6, met een kolomfunctie (i.p.v. < ANY).",
   "SELECT lastname, salary FROM employee WHERE salary < (SELECT MAX(salary) FROM employee WHERE department = 6);", "< ANY  ==  < MAX")
ex("Geef achternaam en voornaam van medewerkers die aan project 10, 20 en/of 30 werken, gesorteerd op achternaam.",
   "SELECT lastname, firstname FROM employee WHERE id IN (SELECT employee FROM works_on WHERE project IN (10, 20, 30)) ORDER BY lastname;")
ex("Geef achternaam en voornaam van medewerkers die NIET aan project 10, 20 of 30 werken, gesorteerd op achternaam.",
   "SELECT lastname, firstname FROM employee WHERE id NOT IN (SELECT employee FROM works_on WHERE project IN (10, 20, 30)) ORDER BY lastname;")
ex("Geef achternaam en voornaam van medewerkers die meer dan 40 uur aan project 'DatabaseSystem' werkten. Subquery in een subquery.",
   "SELECT lastname, firstname FROM employee WHERE id IN (SELECT employee FROM works_on WHERE hours > 40 AND project = "
   "(SELECT id FROM project WHERE name = 'DatabaseSystem'));")
ex("Geef de namen van projecten waaraan geen enkele medewerker meer dan 20 uur heeft gewerkt.",
   "SELECT name FROM project WHERE id NOT IN (SELECT project FROM works_on WHERE hours > 20);")
ex("Geef voornaam en achternaam van medewerkers in een afdeling met minstens één locatie in 'Houston'.",
   "SELECT firstname, lastname FROM employee WHERE department IN (SELECT department FROM department_location WHERE location = 'Houston');")
ex("Geef voornaam en achternaam van medewerkers die meer verdienen dan hun supervisor.",
   "SELECT e.firstname, e.lastname FROM employee e WHERE e.salary > (SELECT s.salary FROM employee s WHERE s.id = e.supervisor);",
   "Gecorreleerde subquery met aliassen e en s")
ex("Geef voornaam en achternaam van medewerkers die meer verdienen dan het gemiddelde salaris van afdeling 'Research'.",
   "SELECT firstname, lastname FROM employee WHERE salary > (SELECT AVG(salary) FROM employee WHERE department = "
   "(SELECT id FROM department WHERE name = 'Research'));")
ex("Geef voornaam en achternaam van medewerkers die werken aan een project waarvan de naam eindigt op 'System'.",
   "SELECT firstname, lastname FROM employee WHERE id IN (SELECT employee FROM works_on WHERE project IN "
   "(SELECT id FROM project WHERE name LIKE '%System'));")
ex("Geef de namen van projecten die in dezelfde stad liggen als een locatie van de afdeling die het project beheert.",
   "SELECT name FROM project p WHERE p.location IN (SELECT location FROM department_location dl WHERE dl.department = p.department);")

# =====================================================================================
lesson("zh_join", "11. Ziekenhuis: JOIN", "ziekenhuis", """\
Nu de database van het Bredeweg ziekenhuis (zoals in CodeGrade). Typ eerst :schema !
Belangrijke koppelingen:
  recept.patient_nr -> patient.nummer        recept.medicijn_cd -> medicijn.cd
  behandeling.pers_nr -> personeel.nummer    behandeling.verrichting_nr -> verrichting.nummer
  patient_bed.patient_nr -> patient.nummer   patient_bed.bed_nr -> bed.nummer -> kamer
  personeel_medspec koppelt personeel aan medisch_specialisme""")
ex("Toon alle patiënten (nummer, achternaam, voornaam) met nummer en kamer_nummer van hun bed. Ook patiënten zonder bed!",
   "SELECT patient.nummer, patient.achternaam, patient.voornaam, bed.nummer, bed.kamer_nummer FROM patient "
   "LEFT JOIN patient_bed ON patient.nummer = patient_bed.patient_nr LEFT JOIN bed ON patient_bed.bed_nr = bed.nummer;")
ex("Toon patiënten (nummer, achternaam, voornaam) met wetensch_naam en handelsnaam van hun voorgeschreven medicijnen.",
   "SELECT patient.nummer, patient.achternaam, patient.voornaam, medicijn.wetensch_naam, medicijn.handelsnaam FROM patient "
   "INNER JOIN recept ON patient.nummer = recept.patient_nr INNER JOIN medicijn ON recept.medicijn_cd = medicijn.cd;")
ex("Toon personeel (nummer, achternaam, voornaam) met de titel van hun medisch specialisme.",
   "SELECT personeel.nummer, personeel.achternaam, personeel.voornaam, medisch_specialisme.titel FROM personeel "
   "INNER JOIN personeel_medspec ON personeel.nummer = personeel_medspec.pers_nr "
   "INNER JOIN medisch_specialisme ON personeel_medspec.medspec_cd = medisch_specialisme.cd;")
ex("Toon behandelingen (nummer, behandel_datum, patient_nr, pers_nr) met omschrijving en rek_totaal van de verrichting.",
   "SELECT behandeling.nummer, behandeling.behandel_datum, behandeling.patient_nr, behandeling.pers_nr, verrichting.omschrijving, "
   "verrichting.rek_totaal FROM behandeling INNER JOIN verrichting ON behandeling.verrichting_nr = verrichting.nummer;")
ex("Toon per kamer (nummer, omschrijving) de patiënten die er liggen (patient nummer, achternaam, voornaam).",
   "SELECT kamer.nummer, kamer.omschrijving, patient.nummer, patient.achternaam, patient.voornaam FROM kamer "
   "INNER JOIN bed ON kamer.nummer = bed.kamer_nummer INNER JOIN patient_bed ON bed.nummer = patient_bed.bed_nr "
   "INNER JOIN patient ON patient_bed.patient_nr = patient.nummer;", "kamer -> bed -> patient_bed -> patient")
ex("Toon al het personeel (nummer, achternaam, voornaam) met de naam van hun afdeling. Ook personeel zonder afdeling.",
   "SELECT personeel.nummer, personeel.achternaam, personeel.voornaam, zh_afdeling.naam FROM personeel "
   "LEFT JOIN zh_afdeling ON personeel.afd_toegewezen = zh_afdeling.nummer;")
ex("Toon de specialisme-titel met behandelingen (nummer, behandel_datum, patient_nr, pers_nr), gesorteerd op titel en dan behandelnummer.",
   "SELECT medisch_specialisme.titel, behandeling.nummer, behandeling.behandel_datum, behandeling.patient_nr, behandeling.pers_nr "
   "FROM behandeling INNER JOIN personeel ON behandeling.pers_nr = personeel.nummer "
   "INNER JOIN personeel_medspec ON personeel.nummer = personeel_medspec.pers_nr "
   "INNER JOIN medisch_specialisme ON personeel_medspec.medspec_cd = medisch_specialisme.cd ORDER BY medisch_specialisme.titel, behandeling.nummer;")

# =====================================================================================
lesson("zh_group", "12. Ziekenhuis: GROUP BY en HAVING", "ziekenhuis", """\
Zelfde regels als les 7 en 8, nu op de ziekenhuisdatabase.
Leeftijd in PostgreSQL:  AGE(geboortedatum)  of  EXTRACT(YEAR FROM AGE(geboortedatum))
Dagen tussen datums:     datum1 - datum2""")
ex("Tel per kamer_nummer hoeveel patiënten er (ooit) in een bed lagen. Ook kamers met 0.",
   "SELECT bed.kamer_nummer, COUNT(patient_bed.patient_nr) AS aantal_patienten FROM bed "
   "LEFT JOIN patient_bed ON bed.nummer = patient_bed.bed_nr GROUP BY bed.kamer_nummer;", "COUNT(kolom) telt NULL niet mee")
ex("Bereken per eenheid de gemiddelde voorraad (voorraad_hoev) in medicijn.",
   "SELECT eenheid, AVG(voorraad_hoev) AS gemiddelde_voorraad FROM medicijn GROUP BY eenheid;")
ex("Tel per patient_nr het aantal behandelingen.",
   "SELECT patient_nr, COUNT(*) AS totaal_aantal_behandelingen FROM behandeling GROUP BY patient_nr;")
ex("Bereken per afdeling (afd_toegewezen) het gemiddelde salaris van personeel.",
   "SELECT afd_toegewezen, AVG(salaris) AS gemiddeld_salaris FROM personeel GROUP BY afd_toegewezen;")
ex("Bereken per categorie (cat_nr) de totale kosten (rek_totaal) van verrichtingen.",
   "SELECT cat_nr, SUM(rek_totaal) AS totale_kosten FROM verrichting GROUP BY cat_nr;")
ex("Tel per personeelslid (pers_nr) hoeveel VERSCHILLENDE patiënten het behandeld heeft.",
   "SELECT pers_nr, COUNT(DISTINCT patient_nr) AS aantal_patienten FROM behandeling GROUP BY pers_nr;")
ex("Bereken per provincie de gemiddelde leeftijd van patiënten (gebruik AGE).",
   "SELECT provincie, AVG(AGE(CURRENT_DATE, geboortedatum)) AS gemiddelde_leeftijd FROM patient GROUP BY provincie;")
ex("Tel het aantal medicijnen per normale dosering (normale_dos).",
   "SELECT normale_dos, COUNT(*) AS aantal_medicijnen FROM medicijn GROUP BY normale_dos;")
ex("Vind afdelingen (afd_toegewezen) waar meer dan 2 personeelsleden werken, met het aantal.",
   "SELECT afd_toegewezen, COUNT(*) AS aantal_personeelsleden FROM personeel GROUP BY afd_toegewezen HAVING COUNT(*) > 2;")
ex("Vind patiënten (patient_nr) met meer dan 3 behandelingen, met het aantal.",
   "SELECT patient_nr, COUNT(*) AS aantal_behandelingen FROM behandeling GROUP BY patient_nr HAVING COUNT(*) > 3;")
ex("Zoek verrichtingen (nummer) waarvan de totale kosten (rek_totaal) meer dan 1000 zijn, met het totaal.",
   "SELECT nummer, SUM(rek_totaal) AS totale_kosten FROM verrichting GROUP BY nummer HAVING SUM(rek_totaal) > 1000;")
ex("Identificeer specialismen (medspec_cd) met minder dan 4 gekwalificeerde personeelsleden, met het aantal.",
   "SELECT medspec_cd, COUNT(pers_nr) AS aantal_personeelsleden FROM personeel_medspec GROUP BY medspec_cd HAVING COUNT(pers_nr) < 4;")
ex("Selecteer kamers (kamer_nummer) met meer dan 2 bedden, met het aantal.",
   "SELECT kamer_nummer, COUNT(*) AS aantal_bedden FROM bed GROUP BY kamer_nummer HAVING COUNT(*) > 2;")
ex("Vind personeelsleden (pers_nr) met meer dan 1 specialisme, met het aantal.",
   "SELECT pers_nr, COUNT(medspec_cd) AS aantal_specialismen FROM personeel_medspec GROUP BY pers_nr HAVING COUNT(medspec_cd) > 1;")
ex("Zoek medicijnen (medicijn_cd) die aan meer dan 10 VERSCHILLENDE patiënten zijn voorgeschreven, met het aantal.",
   "SELECT medicijn_cd, COUNT(DISTINCT patient_nr) AS aantal_patienten FROM recept GROUP BY medicijn_cd HAVING COUNT(DISTINCT patient_nr) > 10;")

# =====================================================================================
lesson("zh_sub", "13. Ziekenhuis: subqueries", "ziekenhuis", """\
  NOT IN           wat ontbreekt:  WHERE cd NOT IN (SELECT medicijn_cd FROM recept)
  de 'meeste'      subquery met ORDER BY COUNT(*) DESC LIMIT 1
  Subquery in FROM (afgeleide tabel) MOET een naam (alias) hebben in PostgreSQL:
     SELECT AVG(n) FROM (SELECT COUNT(*) AS n FROM bed GROUP BY kamer_nummer) AS sub""")
ex("Vind patiënten (nummer, achternaam, voornaam) die nog GEEN behandeling hebben gehad.",
   "SELECT nummer, achternaam, voornaam FROM patient WHERE nummer NOT IN (SELECT patient_nr FROM behandeling);")
ex("Lijst medicijnen (cd, wetensch_naam, handelsnaam) die nog nooit zijn voorgeschreven.",
   "SELECT cd, wetensch_naam, handelsnaam FROM medicijn WHERE cd NOT IN (SELECT medicijn_cd FROM recept);")
ex("Bepaal het meest voorgeschreven medicijn (cd, wetensch_naam, handelsnaam).",
   "SELECT cd, wetensch_naam, handelsnaam FROM medicijn WHERE cd = (SELECT medicijn_cd FROM recept GROUP BY medicijn_cd ORDER BY COUNT(*) DESC LIMIT 1);")
ex("Lijst personeel (nummer, achternaam, voornaam, salaris) met een salaris boven het gemiddelde.",
   "SELECT nummer, achternaam, voornaam, salaris FROM personeel WHERE salaris > (SELECT AVG(salaris) FROM personeel);")
ex("Vind patiënten (nummer, achternaam, voornaam, geboortedatum) die ouder zijn dan de gemiddelde leeftijd. Gebruik AGE.",
   "SELECT nummer, achternaam, voornaam, geboortedatum FROM patient WHERE AGE(geboortedatum) > (SELECT AVG(AGE(geboortedatum)) FROM patient);")
ex("Selecteer medicijnen (cd, voorraad_hoev) waarvan de voorraad lager is dan de gemiddelde voorraad.",
   "SELECT cd, voorraad_hoev FROM medicijn WHERE voorraad_hoev < (SELECT AVG(voorraad_hoev) FROM medicijn);")
ex("Afdelingen (naam + aantal personeel) met meer personeel dan het gemiddelde aantal per afdeling (tel alle afdelingen mee).",
   "SELECT zh_afdeling.naam, COUNT(personeel.nummer) FROM zh_afdeling LEFT JOIN personeel ON zh_afdeling.nummer = personeel.afd_toegewezen "
   "GROUP BY zh_afdeling.naam HAVING COUNT(personeel.nummer) > (SELECT AVG(n) FROM (SELECT COUNT(personeel.nummer) AS n FROM zh_afdeling "
   "LEFT JOIN personeel ON zh_afdeling.nummer = personeel.afd_toegewezen GROUP BY zh_afdeling.nummer) AS sub);",
   "Subquery in FROM die per afdeling telt; daarvan AVG")
ex("Identificeer het/de specialisme(n) (titel + aantal) met het hoogste aantal gekwalificeerde personeelsleden.",
   "SELECT medisch_specialisme.titel, COUNT(personeel_medspec.pers_nr) FROM medisch_specialisme LEFT JOIN personeel_medspec "
   "ON medisch_specialisme.cd = personeel_medspec.medspec_cd GROUP BY medisch_specialisme.titel HAVING COUNT(personeel_medspec.pers_nr) = "
   "(SELECT MAX(n) FROM (SELECT COUNT(pers_nr) AS n FROM personeel_medspec GROUP BY medspec_cd) AS sub);")
ex("Vind kamers (nummer, omschrijving, aantal bedden) met meer bedden dan het gemiddelde per kamer.",
   "SELECT kamer.nummer, kamer.omschrijving, COUNT(bed.nummer) FROM kamer LEFT JOIN bed ON kamer.nummer = bed.kamer_nummer "
   "GROUP BY kamer.nummer, kamer.omschrijving HAVING COUNT(bed.nummer) > (SELECT AVG(n) FROM (SELECT COUNT(bed.nummer) AS n FROM kamer "
   "LEFT JOIN bed ON kamer.nummer = bed.kamer_nummer GROUP BY kamer.nummer) AS sub);")

# =====================================================================================
lesson("codegrade", "14. CodeGrade-oefeningen (ziekenhuis)", "ziekenhuis", """\
Zo worden de opdrachten in CodeGrade gesteld: precies de gevraagde kolommen,
in de gevraagde volgorde, met de gevraagde kolomnamen, sortering en LIMIT.
Hier worden kolomnamen dus OOK gecontroleerd.""")
ex("Maak een lijst van patiënten en hun voorgeschreven medicijnen (JOIN patient, recept, medicijn). Sorteer op achternaam, dan "
   "patiëntnummer, dan handelsnaam. Toon de eerste 50. Kolommen: nummer, achternaam, voornaam, wetensch_naam, handelsnaam.",
   "SELECT patient.nummer, patient.achternaam, patient.voornaam, medicijn.wetensch_naam, medicijn.handelsnaam FROM patient "
   "INNER JOIN recept ON patient.nummer = recept.patient_nr INNER JOIN medicijn ON recept.medicijn_cd = medicijn.cd "
   "ORDER BY patient.achternaam, patient.nummer, medicijn.handelsnaam LIMIT 50;", names=True)
ex("Tel het aantal behandelingen per patiënt. Kolommen: patient_nr en totaal_aantal_behandelingen.",
   "SELECT patient_nr, COUNT(*) AS totaal_aantal_behandelingen FROM behandeling GROUP BY patient_nr;", names=True)
ex("Bepaal welk medicijn het meest is voorgeschreven (gebruik een subquery). Kolommen: cd, wetensch_naam, handelsnaam.",
   "SELECT cd, wetensch_naam, handelsnaam FROM medicijn WHERE cd = (SELECT medicijn_cd FROM recept GROUP BY medicijn_cd ORDER BY COUNT(*) DESC LIMIT 1);",
   names=True)

# =====================================================================================
lesson("create", "15. Tabellen maken: CREATE TABLE en veldtypen", "leeg", """\
    CREATE TABLE teacher (
        id       SERIAL PRIMARY KEY,          -- SERIAL = automatisch oplopend nummer (PostgreSQL)
        name     VARCHAR(50) NOT NULL,        -- verplicht veld
        subject  VARCHAR(50) DEFAULT 'onbekend',
        email    VARCHAR(100) UNIQUE,         -- geen dubbele waarden
        salary   NUMERIC(8,2) CHECK (salary > 0),
        active   BOOLEAN DEFAULT TRUE,
        hired    DATE
    );
    DROP TABLE teacher;                       -- tabel weggooien
    ALTER TABLE teacher ADD COLUMN phone VARCHAR(15);
    ALTER TABLE teacher DROP COLUMN phone;

Veldtypen (PostgreSQL):
  INTEGER / SMALLINT / BIGINT    gehele getallen (4 / 2 / 8 bytes)
  SERIAL                         INTEGER die automatisch ophoogt (via een sequence)
  NUMERIC(p,s) = DECIMAL         exact getal, p cijfers waarvan s achter de komma -> geld!
  REAL / FLOAT / DOUBLE PRECISION   benadering, snel; NIET voor geld
  CHAR(n)                        vaste lengte, wordt aangevuld met spaties
  VARCHAR(n)                     variabele lengte, max n
  TEXT                           onbeperkte lengte
  BOOLEAN                        TRUE / FALSE
  DATE, TIME, TIMESTAMP, TIMESTAMP WITH TIME ZONE, INTERVAL
  UUID                           wereldwijd unieke id

In deze les begin je met een LEGE database. Alles wordt na het nakijken teruggedraaid.""")
ex("Maak een tabel teacher met id (SERIAL PRIMARY KEY), name (VARCHAR(50), verplicht) en subject (VARCHAR(50)). "
   "Toon daarna met SELECT * FROM teacher; dat hij (leeg) bestaat.",
   "CREATE TABLE teacher (id SERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL, subject VARCHAR(50)); SELECT * FROM teacher;",
   check="SELECT column_name, data_type, is_nullable, column_default LIKE 'nextval%' AS auto FROM information_schema.columns "
         "WHERE table_name = 'teacher' ORDER BY ordinal_position;")
ex("Maak tabel product met: id SERIAL PRIMARY KEY, name TEXT NOT NULL, price NUMERIC(8,2) met CHECK price > 0, "
   "in_stock BOOLEAN DEFAULT TRUE.",
   "CREATE TABLE product (id SERIAL PRIMARY KEY, name TEXT NOT NULL, price NUMERIC(8,2) CHECK (price > 0), in_stock BOOLEAN DEFAULT TRUE);",
   check="SELECT column_name, data_type, numeric_precision, numeric_scale, is_nullable, column_default FROM information_schema.columns "
         "WHERE table_name = 'product' AND column_name <> 'id' ORDER BY ordinal_position;",
   hint="CHECK (price > 0)   DEFAULT TRUE")
ex("Maak tabel member met id SERIAL PRIMARY KEY, email VARCHAR(100) UNIQUE en joindate DATE met als standaardwaarde de huidige datum.",
   "CREATE TABLE member (id SERIAL PRIMARY KEY, email VARCHAR(100) UNIQUE, joindate DATE DEFAULT CURRENT_DATE);",
   check="SELECT column_name, data_type, column_default FROM information_schema.columns WHERE table_name = 'member' AND column_name <> 'id' "
         "UNION ALL SELECT 'unique', contype::text, NULL FROM pg_constraint WHERE conrelid = 'member'::regclass AND contype = 'u';",
   hint="DEFAULT CURRENT_DATE")
ex("De tabel teacher bestaat al. Voeg een kolom phone VARCHAR(15) toe met ALTER TABLE.",
   "ALTER TABLE teacher ADD COLUMN phone VARCHAR(15);", setup=TEACHER_SETUP,
   check="SELECT column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_name = 'teacher' ORDER BY ordinal_position;")

# =====================================================================================
lesson("dml", "16. INSERT, UPDATE en DELETE", "leeg", """\
    INSERT INTO teacher (name, subject) VALUES ('Ann', 'Wiskunde');          -- id via SERIAL
    INSERT INTO teacher (name, subject) VALUES ('Bob', 'SQL'), ('Cas', 'Java');  -- meerdere rijen
    INSERT INTO teacher VALUES (10, 'Dirk', 'Logica');   -- zonder kolomnamen: ALLE kolommen in de juiste volgorde
       (riskant: verandert de tabel, dan klopt je INSERT niet meer!)

    UPDATE teacher SET subject = 'Logica' WHERE name = 'Ann';
    UPDATE employee SET salary = salary * 1.05 WHERE department = 5;

    DELETE FROM teacher WHERE id = 3;

    !! Vergeet je WHERE bij UPDATE of DELETE, dan verander/verwijder je ALLE rijen !!

In deze les staat de tabel teacher(id, name, subject) al klaar met 3 docenten.""")
ex("Voeg docent 'Peter Smit' met vak 'Databases' toe aan teacher (id gaat automatisch). Toon daarna alle docenten.",
   "INSERT INTO teacher (name, subject) VALUES ('Peter Smit', 'Databases');", setup=TEACHER_SETUP,
   check="SELECT name, subject FROM teacher ORDER BY id;")
ex("Voeg in één statement twee docenten toe: ('Lisa Bos', 'Python') en ('Kees Vos', 'Wiskunde').",
   "INSERT INTO teacher (name, subject) VALUES ('Lisa Bos', 'Python'), ('Kees Vos', 'Wiskunde');", setup=TEACHER_SETUP,
   check="SELECT name, subject FROM teacher ORDER BY id;")
ex("Update het vak van Michiel Boere naar 'Logica'.",
   "UPDATE teacher SET subject = 'Logica' WHERE name = 'Michiel Boere';", setup=TEACHER_SETUP,
   check="SELECT id, name, subject FROM teacher ORDER BY id;")
ex("Verwijder docent Anna Smit uit de tabel.",
   "DELETE FROM teacher WHERE name = 'Anna Smit';", setup=TEACHER_SETUP, check="SELECT id, name, subject FROM teacher ORDER BY id;")
ex("Toon alleen de namen van docenten die Wiskunde geven, gesorteerd op naam.",
   "SELECT name FROM teacher WHERE subject = 'Wiskunde' ORDER BY name;", setup=TEACHER_SETUP)
ex("Maak tabel classroom (id SERIAL PRIMARY KEY, roomnumber INTEGER, teachername VARCHAR(50)) en voeg James Wall toe met "
   "lokaalnummer 300 ZONDER kolomnamen te noemen (id = 1).",
   "CREATE TABLE classroom (id SERIAL PRIMARY KEY, roomnumber INTEGER, teachername VARCHAR(50)); INSERT INTO classroom VALUES (1, 300, 'James Wall');",
   check="SELECT id, roomnumber, teachername FROM classroom;", hint="INSERT INTO classroom VALUES (1, 300, 'James Wall');")
ex("(companydb) Geef alle werknemers van afdeling 5 een salarisverhoging van 5%. Controle toont hun nieuwe salaris.",
   "UPDATE employee SET salary = salary * 1.05 WHERE department = 5;", db="companydb",
   check="SELECT id, salary FROM employee ORDER BY id;")

# =====================================================================================
lesson("keys", "17. Keys: PRIMARY KEY, FOREIGN KEY, ON DELETE / ON UPDATE, indexen", "leeg", """\
PRIMARY KEY   identificeert elke rij uniek; nooit NULL; maar 1 per tabel (kan uit meerdere kolommen bestaan)
UNIQUE        geen dubbele waarden, maar NULL mag; meerdere per tabel
FOREIGN KEY   kolom verwijst naar de primary key van een andere tabel (referentiële integriteit):

    CREATE TABLE song (
        id     INTEGER PRIMARY KEY,
        name   TEXT,
        singer INTEGER REFERENCES singer(id) ON DELETE CASCADE ON UPDATE CASCADE
    );
    -- of apart:  FOREIGN KEY (singer) REFERENCES singer(id)
    -- of achteraf:
    ALTER TABLE song ADD CONSTRAINT fk_song_singer FOREIGN KEY (singer) REFERENCES singer(id) ON DELETE SET NULL;
    ALTER TABLE song DROP CONSTRAINT fk_song_singer;

Referentiële acties (wat gebeurt er met de kind-rijen als de ouder wordt verwijderd/gewijzigd):
  NO ACTION / RESTRICT   niet toegestaan zolang er kind-rijen zijn -> foutmelding (standaard)
  CASCADE                kind-rijen worden mee verwijderd / mee gewijzigd
  SET NULL               FK in de kind-rij wordt NULL
  SET DEFAULT            FK wordt de standaardwaarde

Indexen (sneller zoeken):
    CREATE INDEX idx_player_lastname ON player (lastname);
    CREATE UNIQUE INDEX idx_singer_name ON singer (firstname, lastname);
    DROP INDEX idx_player_lastname;

DROP TABLE singer;          faalt als song ernaar verwijst
DROP TABLE singer CASCADE;  verwijdert ook de foreign key constraint in song (song zelf blijft!)

Tabellen singer en song (uit de video) staan in deze les klaar - zonder ON DELETE actie.""")
ex("Maak tabel album: id (PRIMARY KEY), title, singer (FOREIGN KEY naar singer.id), release_year. Voeg album (1, 'Bangerz', 1, 2013) toe.",
   "CREATE TABLE album (id INTEGER PRIMARY KEY, title TEXT, singer INTEGER REFERENCES singer(id), release_year INTEGER);"
   "INSERT INTO album VALUES (1, 'Bangerz', 1, 2013);", setup=SINGER_SETUP,
   check="SELECT a.title, s.lastname, (SELECT COUNT(*) FROM pg_constraint WHERE conrelid = 'album'::regclass AND contype IN ('p','f')) "
         "FROM album a JOIN singer s ON a.singer = s.id;")
ex("Probeer een song toe te voegen met een niet-bestaande singer: INSERT INTO song VALUES (6, 'Test', 2020, 99); "
   "Wat gebeurt er? Typ daarna als antwoord deze query:  SELECT 'foreign key';  (Lees eerst de foutmelding!)",
   "SELECT 'foreign key';", setup=SINGER_SETUP, hint="Je krijgt: violates foreign key constraint")
ex("Pas de foreign key van song aan naar ON DELETE CASCADE: verwijder de oude constraint (naam: song_singer_fkey) en voeg een nieuwe toe. "
   "Verwijder daarna Lady Gaga (id 5).",
   "ALTER TABLE song DROP CONSTRAINT song_singer_fkey; ALTER TABLE song ADD CONSTRAINT song_singer_fkey FOREIGN KEY (singer) "
   "REFERENCES singer(id) ON DELETE CASCADE; DELETE FROM singer WHERE id = 5;", setup=SINGER_SETUP,
   check="SELECT id, name FROM song ORDER BY id;", hint="ALTER TABLE song DROP CONSTRAINT ...; ALTER TABLE song ADD CONSTRAINT ... ON DELETE CASCADE;")
ex("Pas de foreign key van song (song_singer_fkey) aan naar ON DELETE SET NULL en verwijder daarna Lady Gaga (id 5).",
   "ALTER TABLE song DROP CONSTRAINT song_singer_fkey; ALTER TABLE song ADD CONSTRAINT song_singer_fkey FOREIGN KEY (singer) "
   "REFERENCES singer(id) ON DELETE SET NULL; DELETE FROM singer WHERE id = 5;", setup=SINGER_SETUP,
   check="SELECT id, name, singer FROM song ORDER BY id;")
ex("Pas song_singer_fkey aan naar ON UPDATE CASCADE en verander het id van Selena Gomez van 3 naar 33.",
   "ALTER TABLE song DROP CONSTRAINT song_singer_fkey; ALTER TABLE song ADD CONSTRAINT song_singer_fkey FOREIGN KEY (singer) "
   "REFERENCES singer(id) ON UPDATE CASCADE; UPDATE singer SET id = 33 WHERE id = 3;", setup=SINGER_SETUP,
   check="SELECT id, name, singer FROM song ORDER BY id;")
ex("Maak een UNIQUE index idx_singer_name op firstname en lastname van singer.",
   "CREATE UNIQUE INDEX idx_singer_name ON singer (firstname, lastname);", setup=SINGER_SETUP,
   check="SELECT indexname, indexdef LIKE 'CREATE UNIQUE%' FROM pg_indexes WHERE tablename = 'singer' AND indexname = 'idx_singer_name';")
ex("Maak tabel player (id INTEGER PRIMARY KEY, firstname, lastname, age), voeg Frenkie de Jong 26, Matthijs de Ligt 25 en "
   "Memphis Depay 30 toe (id 1-3), en maak een index idx_player_lastname op lastname.",
   "CREATE TABLE player (id INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, age INTEGER);"
   "INSERT INTO player VALUES (1,'Frenkie','de Jong',26),(2,'Matthijs','de Ligt',25),(3,'Memphis','Depay',30);"
   "CREATE INDEX idx_player_lastname ON player (lastname);",
   check="SELECT p.firstname, p.lastname, p.age, (SELECT COUNT(*) FROM pg_indexes WHERE indexname = 'idx_player_lastname') FROM player p ORDER BY id;")
ex("Maak tabellen club (id PK, name, city) en matchup (id PK, hometeam, awayteam, year) waarbij hometeam en awayteam "
   "verwijzen naar club(id) met ON DELETE CASCADE. Voeg Ajax/Amsterdam (1), PSV/Eindhoven (2), Feyenoord/Rotterdam (3) toe "
   "en wedstrijd (1, 1, 2, 2023). Verwijder daarna PSV.",
   "CREATE TABLE club (id INTEGER PRIMARY KEY, name TEXT, city TEXT);"
   "CREATE TABLE matchup (id INTEGER PRIMARY KEY, hometeam INTEGER REFERENCES club(id) ON DELETE CASCADE, "
   "awayteam INTEGER REFERENCES club(id) ON DELETE CASCADE, year INTEGER);"
   "INSERT INTO club VALUES (1,'Ajax','Amsterdam'),(2,'PSV','Eindhoven'),(3,'Feyenoord','Rotterdam');"
   "INSERT INTO matchup VALUES (1,1,2,2023); DELETE FROM club WHERE name = 'PSV';",
   check="SELECT (SELECT COUNT(*) FROM club), (SELECT COUNT(*) FROM matchup);", hint="Na het verwijderen van PSV moet de wedstrijd ook weg zijn")

# =====================================================================================
lesson("theorie", "18. Theorie: veldtypen en keys (meerkeuze)", "leeg", """\
Meerkeuzevragen over de theorie uit week 1 (veldtypen, keys).
Antwoord met de letter (a, b, c of d) en Enter.""")
ex("Wat gebeurt er als je 'abc' opslaat in een CHAR(10) kolom in PostgreSQL?",
   "b", choices=["Foutmelding: te kort", "Het wordt aangevuld met spaties tot 10 tekens", "Het wordt opgeslagen als 'abc' zonder verder iets",
                 "Het wordt afgekapt"], uitleg="CHAR(n) heeft een vaste lengte en wordt aangevuld met spaties.")
ex("Wat gebeurt er als je een string van 25 tekens in een VARCHAR(20) wilt opslaan?",
   "c", choices=["Hij wordt stil afgekapt tot 20", "Hij wordt opgeslagen, VARCHAR negeert de lengte", "Foutmelding: value too long",
                 "Hij wordt omgezet naar TEXT"], uitleg="PostgreSQL geeft 'value too long for type character varying(20)'.")
ex("Waarom gebruik je NUMERIC/DECIMAL in plaats van FLOAT voor geldbedragen?",
   "a", choices=["NUMERIC is exact; FLOAT is een benadering met afrondingsfouten", "FLOAT kan geen negatieve getallen",
                 "NUMERIC is sneller", "FLOAT kan geen decimalen opslaan"], uitleg="0.1 + 0.2 in FLOAT is niet precies 0.3.")
ex("Wat is het verschil tussen TEXT en VARCHAR(n) in PostgreSQL?",
   "d", choices=["TEXT is langzamer", "VARCHAR kan geen letters met accenten", "TEXT is maximaal 255 tekens",
                 "TEXT heeft geen maximale lengte; VARCHAR(n) heeft maximaal n tekens"],
   uitleg="Qua snelheid zijn ze gelijk; TEXT is handig voor opmerkingen/artikelen van onbekende lengte.")
ex("Wat doet SERIAL?", "b", choices=["Maakt een kolom uniek", "Maakt een INTEGER die automatisch ophoogt via een sequence",
                                      "Slaat een serienummer als tekst op", "Maakt automatisch een foreign key"])
ex("Wat is een voordeel van een UUID boven een auto-increment integer als ID?",
   "c", choices=["Neemt minder ruimte in", "Is makkelijker te onthouden", "Is wereldwijd uniek, ook over meerdere databases/servers heen",
                 "Is sneller bij sorteren"])
ex("Welk type is het kleinste geheel getal (2 bytes)?", "a", choices=["SMALLINT", "INTEGER", "BIGINT", "SERIAL"])
ex("Wat is het verschil tussen TIMESTAMP WITH TIME ZONE en TIMESTAMP WITHOUT TIME ZONE?",
   "b", choices=["Geen verschil", "WITH TIME ZONE slaat het tijdstip op in UTC en toont het in de tijdzone van de gebruiker",
                 "WITHOUT TIME ZONE slaat ook seconden op", "WITH TIME ZONE kan alleen datums opslaan"])
ex("Wat is het verschil tussen een PRIMARY KEY en een UNIQUE constraint?",
   "d", choices=["Er is geen verschil", "UNIQUE mag maar 1 keer per tabel", "PRIMARY KEY mag NULL bevatten",
                 "PRIMARY KEY mag geen NULL en maar 1 per tabel; UNIQUE mag NULL en meerdere per tabel"])
ex("song.singer is een FK naar singer.id met ON DELETE CASCADE. Je verwijdert een singer. Wat gebeurt er?",
   "a", choices=["Alle songs van die singer worden ook verwijderd", "De songs krijgen singer = NULL", "Je krijgt een foutmelding",
                 "Er gebeurt niets met de songs"])
ex("Zelfde FK maar met ON DELETE SET NULL. Wat gebeurt er met de songs?",
   "b", choices=["Ze worden verwijderd", "Hun singer-kolom wordt NULL", "Foutmelding", "Ze krijgen singer = 0"])
ex("Zelfde FK zonder ON DELETE actie (standaard NO ACTION). Je verwijdert een singer die songs heeft. Wat gebeurt er?",
   "c", choices=["De songs worden verwijderd", "De songs krijgen NULL", "Foutmelding: violates foreign key constraint",
                 "Alleen de singer verdwijnt, songs blijven verwijzen"])
ex("Waarom is INSERT INTO tabel VALUES (...) zonder kolomnamen riskant?",
   "a", choices=["Als de tabelstructuur verandert (kolom erbij, andere volgorde) klopt de INSERT niet meer of komen waarden in de verkeerde kolom",
                 "Het is langzamer", "Het werkt niet in PostgreSQL", "Dan wordt de primary key genegeerd"])
ex("Waarom kun je niet WHERE AVG(salary) > 35000 gebruiken?",
   "c", choices=["AVG bestaat niet in PostgreSQL", "WHERE werkt alleen met tekst",
                 "WHERE wordt vóór het groeperen uitgevoerd; kolomfuncties horen in HAVING", "Het moet WHERE AVG(salary) >= 35000 zijn"])
ex("Waarom komt bij SELECT e.id, e.lastname FROM employee e JOIN dependent d ON e.id = d.employee sommige namen meerdere keren voor?",
   "b", choices=["Er zit een fout in de data", "Een werknemer met meerdere gezinsleden levert per gezinslid een rij op",
                 "JOIN dupliceert altijd alle rijen", "Door het ontbreken van ORDER BY"], uitleg="Gebruik DISTINCT of een subquery met IN.")

# =====================================================================================
lesson("toets", "19. Oefentoets (bibliotheek)", "bibliotheek", """\
Dit is de CodeGrade Oefentoets op de Bibliotheek database (typ :schema).
Echte toets: 45 minuten, geen hulpmiddelen. Typ ':timer 45' om jezelf te klokken.""")
ex("Toon alle medewerkers die man zijn en in afdeling 4 werken. Toon firstname, lastname en salary. Sorteer op salaris aflopend.",
   "SELECT firstname, lastname, salary FROM employee WHERE sex = 'M' AND department = 4 ORDER BY salary DESC;")
ex("Toon de medewerkers die geen manager hebben. Toon firstname, lastname en ssn. Sorteer op ssn.",
   "SELECT firstname, lastname, ssn FROM employee WHERE manager IS NULL ORDER BY ssn;")
ex("Geef het aantal werknemers per afdeling. Toon de afdelingsnaam en het aantal (count). Sorteer op aantal aflopend, dan op naam.",
   "SELECT department.name, COUNT(employee.id) AS count FROM department JOIN employee ON department.id = employee.department "
   "GROUP BY department.name ORDER BY count DESC, department.name;")
ex("Toon alle boeken die (ooit) uitgeleend zijn: title, isbn, publicationyear en categorienaam (name). Sorteer op name aflopend, dan title. Gebruik een subquery.",
   "SELECT book.title, book.isbn, book.publicationyear, category.name FROM book JOIN category ON book.category = category.id "
   "WHERE book.id IN (SELECT book FROM loan) ORDER BY category.name DESC, book.title;")
ex("Maak de tabellen company (id, name, street, city, state) en contact (id, firstname, initial, lastname, phone, email, company), "
   "waarbij contact.company een FK naar company is met ON DELETE CASCADE. Voeg de bedrijven en contactpersonen uit de toets toe:\n"
   "  company: (1,'Blue Origin Enterprises, L.P.','21218 76th Ave S','Kent','WA'), (2,'Space Exploration Technologies Corp.','1 Rocket Road','Starbase','TX')\n"
   "  contact: (1,'Elon','R','Musk','310.363.6220','info@spacex.com',2), (2,'Jeff','P','Bezos','253.437.9300','info@blueorigin.com',1)\n"
   "Verander daarna met één statement het e-mailadres van Elon Musk in elon@spacex.com.",
   "CREATE TABLE company (id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, street VARCHAR(100), city VARCHAR(50), state CHAR(2));"
   "CREATE TABLE contact (id SERIAL PRIMARY KEY, firstname VARCHAR(50) NOT NULL, initial CHAR(1), lastname VARCHAR(50) NOT NULL, "
   "phone VARCHAR(20), email VARCHAR(100) UNIQUE, company INTEGER REFERENCES company(id) ON DELETE CASCADE);"
   "INSERT INTO company VALUES (1,'Blue Origin Enterprises, L.P.','21218 76th Ave S','Kent','WA'),"
   "(2,'Space Exploration Technologies Corp.','1 Rocket Road','Starbase','TX');"
   "INSERT INTO contact VALUES (1,'Elon','R','Musk','310.363.6220','info@spacex.com',2),(2,'Jeff','P','Bezos','253.437.9300','info@blueorigin.com',1);"
   "UPDATE contact SET email = 'elon@spacex.com' WHERE firstname = 'Elon' AND lastname = 'Musk';",
   check="SELECT c.id, c.firstname, c.lastname, c.email, co.name, (SELECT confdeltype FROM pg_constraint WHERE conrelid = 'contact'::regclass AND contype = 'f') "
         "FROM contact c JOIN company co ON c.company = co.id ORDER BY c.id;",
   hint="Let op de quote in 'Enterprises, L.P.' (geen probleem) en dat company eerst moet bestaan")
ex("Vervolg op de vorige: wat gebeurt er met DROP TABLE company; als contact er met een FOREIGN KEY naar verwijst?",
   "c", choices=["company en alle contacten worden verwijderd", "Alleen company wordt verwijderd, contacten krijgen NULL",
                 "Foutmelding: andere objecten (de FK van contact) zijn afhankelijk van company; gebruik DROP TABLE company CASCADE",
                 "Het werkt door ON DELETE CASCADE"],
   uitleg="ON DELETE CASCADE geldt voor DELETE van rijen, niet voor DROP TABLE. DROP TABLE company CASCADE verwijdert alleen de FK-constraint; contact blijft bestaan.")
