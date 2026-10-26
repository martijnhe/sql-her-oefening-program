#!/usr/bin/env python3
"""SQL Trainer - oefen SQL in je terminal. Geen internet, geen AI, geen afleiding.

Start:  python3 trainer.py
"""
import json
import os
import re
import sqlite3
import sys
import time

try:
    import readline  # noqa: F401  (pijltjes-geschiedenis in de prompt)
except ImportError:
    pass

import build_dbs
from exercises import E, LESSONS

HERE = os.path.dirname(os.path.abspath(__file__))
DBDIR = os.path.join(HERE, "db")
PROGRESS = os.path.join(HERE, "progress.json")
SHOW_SOLUTION_AFTER = 3  # pogingen voordat je de uitwerking mag zien

C = sys.stdout.isatty()
def col(code, s): return f"\033[{code}m{s}\033[0m" if C else s
green = lambda s: col("32", s)
red = lambda s: col("31", s)
yellow = lambda s: col("33", s)
bold = lambda s: col("1", s)
dim = lambda s: col("2", s)


def clear():
    if C:
        print("\033[2J\033[H", end="")


# ---------------------------------------------------------------- voortgang
def load_progress():
    try:
        with open(PROGRESS) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"done": [], "attempts": {}}


def save_progress(p):
    with open(PROGRESS, "w") as f:
        json.dump(p, f, indent=1)


def key(i):
    return str(i)


# ---------------------------------------------------------------- database
def fresh_conn(dbname):
    mem = sqlite3.connect(":memory:")
    if dbname != "leeg":
        src = sqlite3.connect(os.path.join(DBDIR, dbname + ".db"))
        src.backup(mem)
        src.close()
    mem.execute("PRAGMA foreign_keys = ON")
    return mem


def split_statements(sql):
    out, buf = [], ""
    for ch in sql:
        buf += ch
        if ch == ";" and sqlite3.complete_statement(buf):
            if buf.strip(" ;\n\t"):
                out.append(buf.strip())
            buf = ""
    if buf.strip():
        out.append(buf.strip())
    return out


def run_all(conn, sql):
    """Voert statements uit; geeft (kolommen, rijen) van het laatste resultaat met rijen."""
    cols, rows = None, None
    for st in split_statements(sql):
        cur = conn.execute(st)
        if cur.description:
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
    conn.commit()
    return cols, rows


def lesson_db(ex):
    return next(l["db"] for l in LESSONS if l["id"] == ex["lesson"])


def execute(ex, sql):
    conn = fresh_conn(lesson_db(ex))
    try:
        if ex.get("setup"):
            conn.executescript(ex["setup"])
        cols, rows = run_all(conn, sql)
        if ex.get("check"):
            cur = conn.execute(ex["check"])
            cols, rows = [d[0] for d in cur.description], cur.fetchall()
        return cols, rows
    finally:
        conn.close()


def norm(v):
    if isinstance(v, float):
        return round(v, 2)
    if isinstance(v, str):
        return v.rstrip()
    return v


def is_ordered(sql):
    tail = sql.lower().rsplit(")", 1)[-1]
    return "order by" in tail


def compare(ex, mine, good):
    mc, mr = mine
    gc, gr = good
    if mr is None:
        return False, "Je query gaf geen resultaat-tabel terug. Begin je met SELECT?"
    if len(mc) != len(gc):
        return False, f"Aantal kolommen klopt niet: jij {len(mc)}, verwacht {len(gc)}."
    if ex.get("names"):
        a = [c.lower() for c in mc]
        b = [c.lower() for c in gc]
        if a != b:
            return False, f"Kolomnamen kloppen niet. Verwacht: {', '.join(gc)}"
    mr = [tuple(norm(v) for v in r) for r in mr]
    gr = [tuple(norm(v) for v in r) for r in gr]
    if len(mr) != len(gr):
        return False, f"Aantal rijen klopt niet: jij {len(mr)}, verwacht {len(gr)}."
    srt = lambda rows: sorted(rows, key=lambda r: [(x is None, str(x)) for x in r])
    if srt(mr) != srt(gr):
        # misschien zelfde inhoud, andere kolomvolgorde?
        if srt([tuple(sorted(map(str, r))) for r in mr]) == srt([tuple(sorted(map(str, r))) for r in gr]):
            return False, "De juiste gegevens, maar de kolommen staan in een andere volgorde."
        return False, "Zelfde aantal rijen, maar de inhoud verschilt. Check je WHERE/JOIN/GROUP BY."
    if is_ordered(ex["sol"]) and mr != gr:
        return False, "Goede rijen, maar de volgorde klopt niet. Check je ORDER BY."
    return True, ""


def show_table(cols, rows, limit=15):
    if cols is None:
        print(dim("(geen resultaat-tabel)"))
        return
    data = [[("NULL" if v is None else str(v)) for v in r] for r in rows[:limit]]
    w = [min(30, max([len(c)] + [len(r[i]) for r in data])) for i, c in enumerate(cols)]
    line = lambda vals: " | ".join(v[:30].ljust(w[i]) for i, v in enumerate(vals))
    print(bold(line(cols)))
    print("-+-".join("-" * x for x in w))
    for r in data:
        print(line(r))
    more = f", {len(rows) - limit} niet getoond" if len(rows) > limit else ""
    print(dim(f"({len(rows)} rijen{more})"))


def show_schema(dbname, table=None):
    if dbname == "leeg":
        print(dim("Deze les begint met een lege database (of met de tabellen uit de opdracht)."))
        return
    conn = fresh_conn(dbname)
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    for t in tables:
        if table and t != table:
            continue
        cols = conn.execute(f"PRAGMA table_info({t})").fetchall()
        fks = {r[3]: f"{r[2]}.{r[4]}" for r in conn.execute(f"PRAGMA foreign_key_list({t})")}
        parts = []
        for c in cols:
            s = c[1]
            if c[5]:
                s = bold(s) + yellow("(PK)")
            if c[1] in fks:
                s += dim("->" + fks[c[1]])
            parts.append(s)
        print(f"{bold(t)}: " + ", ".join(parts))
    conn.close()


# ---------------------------------------------------------------- invoer
def read_sql(prompt):
    """Leest tot een regel op ';' eindigt, of een :commando."""
    lines = []
    while True:
        try:
            line = input(prompt if not lines else "  ...> ")
        except EOFError:
            return ":quit"
        if not lines and line.strip().startswith(":"):
            return line.strip()
        if not lines and not line.strip():
            continue
        lines.append(line)
        if line.rstrip().endswith(";"):
            return "\n".join(lines)


HELP = """\
Typ je SQL en eindig met ;  (meerdere regels mag)
  :hint          tip voor deze opgave
  :schema [tab]  tabellen en kolommen van de database
  :try           vrij uitproberen (wordt niet nagekeken), :back om terug te gaan
  :uitleg        de uitleg van deze les opnieuw
  :oplossing     uitwerking (pas na %d foute pogingen)
  :n / :v        volgende / vorige opgave      :ga N   naar opgave N
  :timer M       focus-timer van M minuten
  :menu          terug naar het menu           :quit   stoppen""" % SHOW_SOLUTION_AFTER


class Timer:
    end = None

    @classmethod
    def status(cls):
        if not cls.end:
            return ""
        left = int(cls.end - time.time())
        if left <= 0:
            cls.end = None
            return red(" [TIJD OM! neem 5 min pauze] ")
        return yellow(f" [{left // 60}:{left % 60:02d}] ")


# ---------------------------------------------------------------- lessen
def lesson_items(lid):
    return [i for i, e in enumerate(E) if e["lesson"] == lid]


def run_lesson(lesson, prog, start=0):
    items = lesson_items(lesson["id"])
    pos = start
    clear()
    print(bold(lesson["title"]) + "\n")
    print(lesson["uitleg"])
    print("\n" + dim("Typ :help voor commando's. Druk Enter om te beginnen."))
    input()
    while 0 <= pos < len(items):
        idx = items[pos]
        ex = E[idx]
        done = key(idx) in prog["done"]
        clear()
        print(dim(f"{lesson['title']}  -  opgave {pos + 1}/{len(items)}  -  database: {lesson['db']}") + Timer.status())
        print()
        print(bold(("✔ " if done else "") + ex["q"]))
        print()
        while True:
            cmd = read_sql(Timer.status() + "sql> ")
            c = cmd.lower().split()
            if c and c[0] in (":quit", ":q", ":exit"):
                save_progress(prog)
                sys.exit(0)
            if c and c[0] == ":menu":
                return
            if c and c[0] in (":n", ":next", ":skip"):
                pos += 1
                break
            if c and c[0] in (":v", ":prev"):
                pos = max(0, pos - 1)
                break
            if c and c[0] == ":ga" and len(c) > 1 and c[1].isdigit():
                pos = min(len(items) - 1, max(0, int(c[1]) - 1))
                break
            if c and c[0] == ":help":
                print(HELP)
                continue
            if c and c[0] == ":hint":
                print(yellow("Tip: " + (ex["hint"] or "Lees de vraag zin voor zin en zoek elke kolom op met :schema.")))
                continue
            if c and c[0] == ":uitleg":
                print(lesson["uitleg"])
                continue
            if c and c[0] == ":schema":
                show_schema(lesson_db(ex), c[1] if len(c) > 1 else None)
                continue
            if c and c[0] == ":timer":
                m = int(c[1]) if len(c) > 1 and c[1].isdigit() else 25
                Timer.end = time.time() + m * 60
                print(yellow(f"Timer gestart: {m} minuten. Focus!"))
                continue
            if c and c[0] == ":try":
                sandbox(ex)
                continue
            if c and c[0] in (":oplossing", ":solution"):
                n = prog["attempts"].get(key(idx), 0)
                if n < SHOW_SOLUTION_AFTER and not done:
                    print(red(f"Nog niet! Eerst zelf proberen ({n}/{SHOW_SOLUTION_AFTER} pogingen). Probeer :hint."))
                else:
                    print(yellow("Uitwerking:"))
                    print(ex["sol"].replace("; ", ";\n"))
                    print(dim("Typ hem nu zelf over en begrijp elk stuk - niet kopiëren!"))
                continue
            if cmd.startswith(":"):
                print(red("Onbekend commando. Typ :help"))
                continue
            # --- SQL nakijken
            try:
                mine = execute(ex, cmd)
            except sqlite3.Error as err:
                prog["attempts"][key(idx)] = prog["attempts"].get(key(idx), 0) + 1
                save_progress(prog)
                print(red(f"SQL-fout: {err}"))
                continue
            good = execute(ex, ex["sol"])
            show_table(*mine)
            ok, msg = compare(ex, mine, good)
            if ok:
                if key(idx) not in prog["done"]:
                    prog["done"].append(key(idx))
                save_progress(prog)
                print(green("\n✔ Goed! ") + dim("Enter = volgende opgave, of probeer het nog op een andere manier."))
                if input().strip() == "":
                    pos += 1
                    break
                else:
                    continue
            prog["attempts"][key(idx)] = prog["attempts"].get(key(idx), 0) + 1
            save_progress(prog)
            print(red("✘ Nog niet goed. ") + msg)
    if pos >= len(items):
        clear()
        n = sum(1 for i in items if key(i) in prog["done"])
        print(green(f"Les klaar! {n}/{len(items)} opgaven goed.") + "  Enter = menu")
        input()


def sandbox(ex):
    conn = fresh_conn(lesson_db(ex))
    if ex.get("setup"):
        conn.executescript(ex["setup"])
    print(yellow("Vrij uitproberen. Niets wordt nagekeken. :back om terug te gaan."))
    while True:
        cmd = read_sql("try> ")
        if cmd.startswith(":"):
            if cmd.startswith(":schema"):
                show_schema(lesson_db(ex))
                continue
            break
        try:
            show_table(*run_all(conn, cmd))
        except sqlite3.Error as err:
            print(red(f"SQL-fout: {err}"))
    conn.close()


def menu():
    build_dbs.ensure(DBDIR)
    prog = load_progress()
    while True:
        clear()
        total = len(E)
        print(bold("=== SQL TRAINER ===") + dim("   offline · geen AI · geen afleiding") + Timer.status())
        print(f"Voortgang: {len(prog['done'])}/{total} opgaven\n")
        for n, l in enumerate(LESSONS, 1):
            items = lesson_items(l["id"])
            d = sum(1 for i in items if key(i) in prog["done"])
            bar = "█" * round(10 * d / len(items)) + "░" * (10 - round(10 * d / len(items)))
            print(f" {n:2}. {bar} {d:2}/{len(items):<2}  {l['title']}")
        print("\n Kies een les (nummer), 'v' = verder waar je was, 't M' = timer, 'r' = voortgang wissen, 'q' = stoppen")
        try:
            ch = input("> ").strip().lower()
        except EOFError:
            return
        if ch == "q":
            return
        if ch == "r":
            if input("Zeker weten? (ja/nee) ").strip() == "ja":
                prog = {"done": [], "attempts": {}}
                save_progress(prog)
            continue
        if ch.startswith("t"):
            m = ch[1:].strip()
            Timer.end = time.time() + (int(m) if m.isdigit() else 25) * 60
            continue
        if ch == "v":
            todo = next((i for i in range(len(E)) if key(i) not in prog["done"]), None)
            if todo is None:
                continue
            l = next(l for l in LESSONS if l["id"] == E[todo]["lesson"])
            run_lesson(l, prog, lesson_items(l["id"]).index(todo))
            continue
        if ch.isdigit() and 1 <= int(ch) <= len(LESSONS):
            run_lesson(LESSONS[int(ch) - 1], prog)


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print()
