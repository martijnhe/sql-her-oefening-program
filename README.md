# SQL Trainer (DATFI)

Oefen SQL in je terminal: **offline, geen AI, geen afleiding.** Alleen Python 3 nodig (geen extra pakketten).

```bash
python3 trainer.py
```

- 10 lessen, 107 opgaven uit de DATFI-oefenbestanden: SELECT, GROUP BY/HAVING, subqueries (companydb),
  JOIN/GROUP BY/HAVING/subqueries (ziekenhuis), CodeGrade-opgaven, CREATE/INSERT/UPDATE/DELETE + keys, en de oefentoets (bibliotheek).
- Je antwoord wordt automatisch nagekeken door je resultaat te vergelijken met dat van de uitwerking.
- `:hint` voor een tip, de uitwerking pas na 3 pogingen. `:schema` toont de tabellen. `:timer 25` voor een focus-timer.
- Voortgang wordt bewaard in `progress.json`.

De databases draaien op SQLite (PostgreSQL-functies als `AGE`/`TO_CHAR` zijn vervangen door SQLite-varianten).
companydb is de echte cursusdata; ziekenhuis en bibliotheek volgen de datamodellen met verzonnen voorbeelddata.
