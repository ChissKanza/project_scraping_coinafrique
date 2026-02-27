"""
database.py — SQLite : 3 tables
"""
import sqlite3
import pandas as pd

DB_PATH = "coinafrique.db"


def _conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def initialiser_base():
    con = _conn()
    con.executescript("""
        CREATE TABLE IF NOT EXISTS annonces_nettoyees (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            nom        TEXT, prix_brut TEXT, prix REAL,
            adresse    TEXT, image_lien TEXT,
            categorie  TEXT, source TEXT,
            date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS annonces_brutes (
            id                    INTEGER PRIMARY KEY AUTOINCREMENT,
            web_scraper_order     TEXT,
            web_scraper_start_url TEXT,
            nom TEXT, prix TEXT, adresse TEXT,
            image_lien TEXT, fichier_source TEXT,
            date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS evaluations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_eval    TEXT, prenom_eval TEXT, niveau TEXT,
            note_app    INTEGER, commentaire TEXT, recommande TEXT,
            date_eval   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    con.commit(); con.close()


def sauvegarder_annonces_nettoyees(df: pd.DataFrame) -> int:
    con = _conn()
    cols = ["nom","prix_brut","prix","adresse","image_lien","categorie","source"]
    df[[c for c in cols if c in df.columns]].to_sql(
        "annonces_nettoyees", con, if_exists="append", index=False)
    con.commit(); n = len(df); con.close()
    return n


def sauvegarder_annonces_brutes(df: pd.DataFrame, fichier: str = "") -> int:
    con = _conn()
    d = df.copy()
    d = d.rename(columns={"image": "image_lien", "prix_brut": "prix"})
    d["fichier_source"] = fichier
    cols = ["web_scraper_order","web_scraper_start_url","nom","prix",
            "adresse","image_lien","fichier_source"]
    d[[c for c in cols if c in d.columns]].to_sql(
        "annonces_brutes", con, if_exists="append", index=False)
    con.commit(); n = len(d); con.close()
    return n


def sauvegarder_evaluation(data: dict) -> bool:
    try:
        con = _conn()
        con.execute("""
            INSERT INTO evaluations
            (nom_eval,prenom_eval,niveau,note_app,commentaire,recommande)
            VALUES (?,?,?,?,?,?)
        """, (data.get("nom",""), data.get("prenom",""), data.get("niveau",""),
              data.get("note",5), data.get("commentaire",""), data.get("recommande","")))
        con.commit(); con.close()
        return True
    except Exception as e:
        print(f"[DB ERR] {e}"); return False


def lire_annonces_nettoyees() -> pd.DataFrame:
    try:
        con = _conn()
        df = pd.read_sql("SELECT * FROM annonces_nettoyees ORDER BY date_ajout DESC", con)
        con.close(); return df
    except Exception:
        return pd.DataFrame()


def lire_evaluations() -> pd.DataFrame:
    try:
        con = _conn()
        df = pd.read_sql("SELECT * FROM evaluations ORDER BY date_eval DESC", con)
        con.close(); return df
    except Exception:
        return pd.DataFrame()


def compter() -> dict:
    con = _conn(); cur = con.cursor(); r = {}
    for t in ["annonces_nettoyees","annonces_brutes","evaluations"]:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            r[t] = cur.fetchone()[0]
        except Exception:
            r[t] = 0
    con.close(); return r


def vider_table(table: str):
    con = _conn()
    con.execute(f"DELETE FROM {table}")
    con.commit(); con.close()
