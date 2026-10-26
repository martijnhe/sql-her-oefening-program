"""PostgreSQL-backend: start (indien nodig) een Postgres-container en voert queries uit via psql.

Instellen met omgevingsvariabelen (standaard: eigen docker-container op poort 55432):
  PGHOST PGPORT PGUSER PGPASSWORD
Gebruik je de Postgres uit de school-docker-compose? Zet dan PGPORT=5432.
"""
import csv
import io
import os
import shutil
import sqlite3
import subprocess
import time

import build_dbs

HOST = os.environ.get("PGHOST", "localhost")
PORT = os.environ.get("PGPORT", "55432")
USER = os.environ.get("PGUSER", "postgres")
PASSWORD = os.environ.get("PGPASSWORD", "postgres")
CONTAINER = "sqltrainer-pg"
DATABASES = ["companydb", "ziekenhuis", "bibliotheek", "leeg"]
PREFIX = "sqltrainer_"


class PgError(Exception):
    pass


def _env():
    e = dict(os.environ)
    e["PGPASSWORD"] = PASSWORD
    return e


def _psql(db, script, timeout=30):
    if not shutil.which("psql"):
        raise PgError("psql is niet geïnstalleerd (sudo pacman -S postgresql-libs).")
    p = subprocess.run(["psql", "-h", HOST, "-p", PORT, "-U", USER, "-d", db, "-X", "-q", "--csv"],
                       input=script, capture_output=True, text=True, env=_env(), timeout=timeout)
    if p.returncode != 0:
        err = p.stderr.strip()
        raise PgError(err or f"psql stopte met code {p.returncode}")
    return p.stdout


def alive():
    try:
        _psql("postgres", "SELECT 1;", timeout=5)
        return True
    except (PgError, subprocess.TimeoutExpired):
        return False


def start_server():
    """Start de docker-container als Postgres niet bereikbaar is."""
    if alive():
        return
    if PORT != "55432" or not shutil.which("docker"):
        raise PgError(f"Kan Postgres op {HOST}:{PORT} niet bereiken.")
    print("PostgreSQL wordt gestart (docker)... de eerste keer kan dit even duren.")
    r = subprocess.run(["docker", "start", CONTAINER], capture_output=True, text=True)
    if r.returncode != 0:
        r = subprocess.run(["docker", "run", "-d", "--name", CONTAINER, "-e", f"POSTGRES_PASSWORD={PASSWORD}",
                            "-p", "55432:5432", "postgres:16"], capture_output=True, text=True)
        if r.returncode != 0:
            raise PgError("docker kon Postgres niet starten:\n" + r.stderr.strip())
    for _ in range(60):
        if alive():
            return
        time.sleep(1)
    raise PgError("Postgres startte niet op tijd.")


def _sqlite_to_pg(path):
    """Zet een SQLite-db uit build_dbs om naar een PostgreSQL-script."""
    src = sqlite3.connect(path)
    out = []
    tables = src.execute("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY rowid").fetchall()
    for _, ddl in tables:
        out.append(ddl + ";")
    for name, _ in tables:
        info = src.execute(f"PRAGMA table_info({name})").fetchall()
        bools = {c[1] for c in info if c[2].upper() == "BOOLEAN"}
        colnames = [c[1] for c in info]
        for row in src.execute(f"SELECT * FROM {name}"):
            vals = []
            for c, v in zip(colnames, row):
                if v is None:
                    vals.append("NULL")
                elif c in bools:
                    vals.append("TRUE" if v else "FALSE")
                elif isinstance(v, (int, float)):
                    vals.append(repr(v))
                else:
                    vals.append("'" + str(v).replace("'", "''") + "'")
            out.append(f"INSERT INTO {name} VALUES ({', '.join(vals)});")
    src.close()
    return "\n".join(out)


def load_data(force=False):
    existing = set(_psql("postgres", "SELECT datname FROM pg_database;").split())
    tmp = os.path.join(build_dbs.HERE, "db")
    for name in DATABASES:
        db = PREFIX + name
        if db in existing and not force:
            continue
        if db in existing:
            _psql("postgres", f"DROP DATABASE {db} WITH (FORCE);")
        _psql("postgres", f"CREATE DATABASE {db};")
        if name == "companydb":
            with open(os.path.join(build_dbs.DATA, "companydb.sql")) as f:
                script = f.read()
        elif name == "leeg":
            continue
        else:
            build_dbs.ensure(tmp)
            script = _sqlite_to_pg(os.path.join(tmp, name + ".db"))
        _psql(db, "\\set ON_ERROR_STOP 1\n" + script, timeout=120)


def setup():
    start_server()
    load_data()


def split_statements(sql):
    """Knipt SQL op in losse statements (puntkomma's binnen quotes tellen niet)."""
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


def run(dbname, setup_sql, user_sql, check_sql=None):
    """Voert alles uit in één transactie die daarna wordt teruggedraaid.
    Geeft (kolommen, rijen) van het laatste resultaat (of van check_sql)."""
    stmts = split_statements(user_sql)
    if not stmts:
        raise PgError("Geen SQL gevonden.")
    last = None if check_sql else stmts.pop()
    lines = ["\\set ON_ERROR_STOP 1", "BEGIN;", "\\o /dev/null"]
    if setup_sql:
        lines.append(setup_sql)
    lines += [s if s.endswith(";") else s + ";" for s in stmts]
    lines.append("\\o")
    final = check_sql or last
    lines.append(final if final.rstrip().endswith(";") else final + ";")
    lines.append("ROLLBACK;")
    out = _psql(PREFIX + dbname, "\n".join(lines) + "\n")
    if not out.strip():
        return None, None
    rows = list(csv.reader(io.StringIO(out)))
    return rows[0], [tuple(r) for r in rows[1:]]
