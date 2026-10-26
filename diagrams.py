"""Plaatjes (ASCII) van de databases. PK = primary key, -> = foreign key (verwijst naar)."""

COMPANYDB = r"""
  COMPANYDB  -  een bedrijf met werknemers, afdelingen en projecten

  ┌──────────────────────┐          ┌──────────────────────┐
  │ employee  (werknemer)│          │ department (afdeling)│
  ├──────────────────────┤          ├──────────────────────┤
  │ id          PK       │◄────┐    │ id          PK       │◄──────────┐
  │ firstname            │     │    │ name                 │           │
  │ middlename           │     ├────┤ manager  -> employee │           │
  │ lastname             │     │    │ managerstart         │           │
  │ ssn                  │     │    └──────────────────────┘           │
  │ birthdate            │     │               ▲                       │
  │ address              │     │               │                       │
  │ sex          'M'/'F' │     │    ┌──────────┴───────────┐           │
  │ salary               │     │    │ department_location  │           │
  │ supervisor -> employee─────┤    ├──────────────────────┤           │
  │ department -> department───┼──► │ department->department           │
  └──────────────────────┘     │    │ location   (stad)    │           │
                               │    └──────────────────────┘           │
  ┌──────────────────────┐     │    ┌──────────────────────┐           │
  │ dependent (gezinslid)│     │    │ project              │           │
  ├──────────────────────┤     │    ├──────────────────────┤           │
  │ employee -> employee ├─────┤    │ id          PK       │◄──┐       │
  │ name                 │     │    │ name                 │   │       │
  │ sex                  │     │    │ location             │   │       │
  │ birthdate            │     │    │ department -> department─┼───────┘
  │ relationship         │     │    └──────────────────────┘   │
  └──────────────────────┘     │    ┌──────────────────────┐   │
                               │    │ works_on (werkt aan) │   │
                               │    ├──────────────────────┤   │
                               └────┤ employee -> employee │   │
                                    │ project  -> project  ├───┘
                                    │ hours    (uren)      │
                                    └──────────────────────┘
"""

ZIEKENHUIS = r"""
  ZIEKENHUIS (Bredeweg)

  medicijn                    recept                         patient
  ┌──────────────────┐       ┌───────────────────────┐      ┌──────────────────┐
  │ cd           PK  │◄──────┤ medicijn_cd -> medicijn│      │ nummer       PK  │
  │ wetensch_naam    │       │ nummer          PK    │      │ bsn              │
  │ handelsnaam      │       │ recept_datum          │      │ achternaam       │
  │ normale_dos      │       │ patient_nr -> patient ├─────►│ voornaam         │
  │ voorraad_hoev    │       │ pers_nr -> personeel  ├──┐   │ tussenvoegsel    │
  │ eenheid          │       │ voorgeschr_dos        │  │   │ adres, plaats    │
  └──────────────────┘       └───────────────────────┘  │   │ provincie        │
                                                        │   │ postcode         │
  personeel_medspec          personeel                  │   │ geboortedatum    │
  ┌──────────────────┐       ┌───────────────────────┐  │   └──────────────────┘
  │ pers_nr -> pers. ├──────►│ nummer          PK    │◄─┘         ▲   ▲
  │ medspec_cd ──┐   │       │ bsn                   │◄──┐        │   │
  │ datum_behaald│   │       │ achternaam, voornaam  │   │        │   │
  └──────────────┼───┘       │ afd_toegewezen ──┐    │   │        │   │
                 ▼           │ ziekenhuis_titel │    │   │        │   │
  medisch_specialisme        │ salaris, tarief  │    │   │        │   │
  ┌──────────────────┐       │ datum_in_dienst  │    │   │        │   │
  │ cd           PK  │       └──────────────────┼────┘   │        │   │
  │ titel            │                          ▼        │        │   │
  │ hoe_behaald      │       zh_afdeling (afdeling)      │        │   │
  └──────────────────┘       ┌───────────────────────┐   │        │   │
                             │ nummer PK, naam,      │   │        │   │
                             │ kantoor_locatie       │   │        │   │
                             └───────────────────────┘   │        │   │
  verrichting_cat            behandeling                 │        │   │
  ┌──────────────────┐       ┌───────────────────────┐   │        │   │
  │ cat_nr       PK  │◄─┐    │ nummer, behandel_datum│   │        │   │
  │ cat_omschrijving │  │    │ patient_nr -> patient ├───┼────────┘   │
  └──────────────────┘  │    │ pers_nr -> personeel  ├───┘            │
  verrichting           │    │ verrichting_nr ──┐    │                │
  ┌──────────────────┐  │    │ huidige_rek_totaal│   │                │
  │ nummer       PK  │◄─┼────┼──────────────────┘    │                │
  │ omschrijving     │  │    └───────────────────────┘                │
  │ rek_totaal       │  │                                             │
  │ cat_nr ──────────┼──┘    kamer          bed                patient_bed
  └──────────────────┘       ┌──────────┐   ┌────────────────┐ ┌──────────────────┐
                             │nummer PK │◄──┤kamer_nummer    │ │patient_nr ───────┼─┘
                             │omschrijv.│   │nummer PK       │◄┤bed_nr            │
                             └──────────┘   │bed_type_nummer │ │intake_datum      │
                                            └────────────────┘ │uitschrijf_datum  │
                                                               └──────────────────┘
"""

BIBLIOTHEEK = r"""
  BIBLIOTHEEK

  author             category            publisher           department
  ┌─────────────┐    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
  │ id       PK │◄┐  │ id       PK │◄┐   │ id       PK │◄┐   │ id       PK │◄┐
  │ firstname   │ │  │ name        │ │   │ name        │ │   │ name        │ │
  │ lastname    │ │  │ description │ │   │ city        │ │   └─────────────┘ │
  │ birthyear   │ │  └─────────────┘ │   └─────────────┘ │   employee        │
  └─────────────┘ │  book            │                   │   ┌─────────────┐ │
                  │  ┌─────────────────────┐             │   │ id       PK │ │
                  └──┤ author    -> author │             │   │ firstname   │ │
                     │ category -> category├─┘           │   │ lastname    │ │
                     │ publisher->publisher├─────────────┘   │ sex 'M'/'V' │ │
                     │ id        PK        │◄──┐             │ ssn         │ │
                     │ title, isbn         │   │             │ department ─┼─┘
                     │ publicationyear     │   │             │ manager->employee
                     └─────────────────────┘   │             │ salary      │
                                               │             └─────────────┘
  member              loan (uitlening)         │      review
  ┌─────────────┐     ┌─────────────────────┐  │      ┌─────────────────────┐
  │ id       PK │◄────┤ member -> member    │  ├──────┤ book   -> book      │
  │ firstname   │     │ book   -> book      ├──┘      │ member -> member    │
  │ lastname    │◄─┐  │ id       PK         │◄─┐      │ rating, comment     │
  │ email       │  │  │ loandate, duedate   │  │      │ reviewdate          │
  │ joindate    │  │  │ returndate          │  │      └──────────┬──────────┘
  └─────────────┘  │  └─────────────────────┘  │                 │
                   └───────────────────────────┼─────────────────┘
                      fine (boete)             │
                      ┌─────────────────────┐  │
                      │ loan -> loan        ├──┘
                      │ amount, paid        │
                      └─────────────────────┘
"""

DIAGRAMS = {"companydb": COMPANYDB, "ziekenhuis": ZIEKENHUIS, "bibliotheek": BIBLIOTHEEK}
