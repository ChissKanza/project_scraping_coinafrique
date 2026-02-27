"""
scraper.py — CoinAfrique Sénégal
Sélecteurs robustes + erreurs visibles dans Streamlit
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

CATEGORIES = {
    "Chiens":                "https://sn.coinafrique.com/categorie/chiens",
    "Moutons":               "https://sn.coinafrique.com/categorie/moutons",
    "Poules-Lapins-Pigeons": "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
    "Autres Animaux":        "https://sn.coinafrique.com/categorie/autres-animaux",
}


def _extraire_carte(card):
    """Extrait nom/prix/adresse/image avec plusieurs sélecteurs fallback."""

    # Nom
    nom = None
    for sel in ["p.ad__card-description", "h3", "h4",
                "p[class*='description']", "p[class*='title']",
                "div[class*='title']", "span[class*='name']"]:
        t = card.select_one(sel)
        if t:
            nom = t.get_text(strip=True)
            break
    nom = nom or "N/A"

    # Prix
    prix = None
    for sel in ["p.ad__card-price", "span.price", "p[class*='price']",
                "span[class*='price']", "div[class*='price']"]:
        t = card.select_one(sel)
        if t:
            prix = t.get_text(strip=True)
            break
    if not prix:
        m = re.search(r"\d[\d\s]*(?:CFA|FCFA|F CFA)", card.get_text(" "), re.I)
        prix = m.group(0).strip() if m else "N/A"

    # Adresse
    adresse = None
    for sel in ["p.ad__card-location span:last-child", "p.ad__card-location",
                "span[class*='location']", "p[class*='location']",
                "div[class*='location']"]:
        t = card.select_one(sel)
        if t:
            adresse = t.get_text(strip=True)
            break
    adresse = adresse or "N/A"

    # Image
    image = ""
    img = card.select_one("img")
    if img:
        image = (img.get("src") or img.get("data-src") or
                 img.get("data-lazy-src") or img.get("data-original") or "")
    if image and not any(e in image for e in [".jpg",".jpeg",".png",".webp",".gif"]):
        image = ""

    if nom == "N/A" and prix == "N/A" and adresse == "N/A":
        return None

    return {"nom": nom, "prix_brut": prix, "adresse": adresse, "image_lien": image}


def scrape_page(url, categorie):
    """
    Retourne (liste_annonces, erreur_str_ou_None).
    """
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except requests.exceptions.ConnectionError:
        return [], f"Connexion impossible. Vérifiez votre connexion internet."
    except requests.exceptions.Timeout:
        return [], f"Timeout — le site ne répond pas."
    except requests.exceptions.HTTPError as e:
        return [], f"Erreur HTTP {e.response.status_code}"
    except Exception as e:
        return [], f"Erreur : {e}"

    soup = BeautifulSoup(r.text, "html.parser")
    annonces = []

    # 4 stratégies de sélection
    cards = soup.select("div.col.s12.m4")
    if not cards:
        cards = soup.select("div[class*='ad__card']")
    if not cards:
        parents = set()
        for a in soup.select("a[href*='/annonce/']"):
            if a.parent and a.parent.name in ["div","li","article"]:
                parents.add(id(a.parent))
                cards.append(a.parent)
        # Dédupliquer
        seen = set(); cards_u = []
        for c in cards:
            if id(c) not in seen:
                seen.add(id(c)); cards_u.append(c)
        cards = cards_u
    if not cards:
        cards = soup.select("article")

    if not cards:
        titre = soup.title.string if soup.title else "?"
        nb_liens = len(soup.select("a[href*='/annonce/']"))
        return [], (
            f"Page chargée ('{titre}') mais aucune carte trouvée. "
            f"{nb_liens} liens d'annonces détectés. "
            "Le site a peut-être changé sa structure HTML."
        )

    for card in cards:
        data = _extraire_carte(card)
        if data:
            data["categorie"] = categorie
            annonces.append(data)

    return annonces, None


def scrape_categorie(nom_cat, base_url, nb_pages=3, cb=None):
    toutes, erreurs = [], []
    for page in range(1, nb_pages + 1):
        url = f"{base_url}?page={page}"
        if cb:
            cb(f"⏳ {nom_cat} — page {page}/{nb_pages}")
        annonces, err = scrape_page(url, nom_cat)
        if err:
            erreurs.append(f"[{nom_cat} p.{page}] {err}")
        toutes.extend(annonces)
        time.sleep(0.8)
    return (pd.DataFrame(toutes) if toutes else pd.DataFrame()), erreurs


def scrape_toutes_categories(nb_pages=3, categories_choisies=None, cb=None):
    cats = categories_choisies or list(CATEGORIES.keys())
    frames, toutes_erreurs = [], []
    for nom in cats:
        df, errs = scrape_categorie(nom, CATEGORIES[nom], nb_pages, cb)
        if not df.empty:
            frames.append(df)
        toutes_erreurs.extend(errs)
    df_final = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    return df_final, toutes_erreurs


# ─── Nettoyage ────────────────────────────────────────────────────────────────

def nettoyer_prix(val):
    if pd.isna(val): return None
    val = re.sub(r"[^\d]", "", str(val))
    return float(val) if val else None


def _deduire_categorie(url):
    url = str(url).lower()
    if "chien"  in url: return "Chiens"
    if "mouton" in url: return "Moutons"
    if "poules" in url: return "Poules-Lapins-Pigeons"
    if "autres" in url: return "Autres Animaux"
    return "Inconnue"


def nettoyer_dataframe(df, source="bs4"):
    df = df.copy()
    col_map = {}
    for c in df.columns:
        cl = c.lower().strip()
        if   cl == "nom":                             col_map[c] = "nom"
        elif cl == "prix" and "prix_brut" not in df.columns:
                                                      col_map[c] = "prix_brut"
        elif cl in ("adresse","adress","address"):    col_map[c] = "adresse"
        elif cl == "image":                           col_map[c] = "image_lien"
    df = df.rename(columns=col_map)

    # ── Supprimer les colonnes dupliquées (ex: adresse + adress → 2x adresse) ──
    df = df.loc[:, ~df.columns.duplicated(keep="first")]

    for col in ["nom","prix_brut","adresse","image_lien"]:
        if col not in df.columns: df[col] = ""

    if "categorie" not in df.columns:
        if "web_scraper_start_url" in df.columns:
            df["categorie"] = df["web_scraper_start_url"].apply(_deduire_categorie)
        else:
            df["categorie"] = "Inconnue"

    df["prix"] = df["prix_brut"].apply(nettoyer_prix)

    for col in ["nom","adresse"]:
        df[col] = (df[col].replace("N/A", pd.NA).fillna("Non précisé")
                          .astype(str).str.replace(r"\s+", " ", regex=True).str.strip())

    avant = len(df)
    df = df.drop_duplicates(subset=["nom","prix_brut","adresse"]).reset_index(drop=True)
    print(f"[NETTOYAGE] {avant-len(df)} doublons supprimés → {len(df)} annonces")

    df["source"] = source
    cols = ["nom","prix_brut","prix","adresse","image_lien","categorie","source"]
    return df[[c for c in cols if c in df.columns]]
