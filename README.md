# SQL Trainer (DATFI) — PostgreSQL

Leer SQL vanaf nul tot toetsniveau, in je terminal. **Echte PostgreSQL** (zoals op de toets), geen AI, geen afleiding.

## Starten
Nodig: Python 3, `psql` en Docker (de eerste keer wordt automatisch een PostgreSQL 16-container `sqltrainer-pg` gemaakt).

```bash
python3 trainer.py
```

Gebruik je liever de Postgres uit de school-docker-compose? `PGPORT=5432 python3 trainer.py`

## Lessen (166 opgaven)
1–5 basis: SELECT, rekenen/AS, WHERE, LIKE/ILIKE/IN/BETWEEN/IS NULL, ORDER BY/LIMIT/DISTINCT ·
6 datums in PostgreSQL (TO_CHAR, AGE, EXTRACT, INTERVAL, ::date) · 7 kolomfuncties · 8 GROUP BY/HAVING ·
9 JOIN · 10 subqueries (ALL/ANY) · 11–13 ziekenhuis · 14 CodeGrade · 15 CREATE TABLE + veldtypen ·
16 INSERT/UPDATE/DELETE · 17 keys, ON DELETE/UPDATE, indexen · 18 theorie (meerkeuze) · 19 oefentoets (bibliotheek)

Elke poging draait in een transactie die wordt teruggedraaid, dus je kunt niets kapotmaken.
`:hint`, `:schema`, `:try`, `:timer 25`; de uitwerking pas na 3 pogingen. Voortgang staat in `progress.json`.

companydb is de echte cursusdata; ziekenhuis en bibliotheek volgen de datamodellen met verzonnen voorbeelddata.
