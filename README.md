# CoinAfrique Animaux Sénégal

Ce dépôt contient une petite application **Streamlit** qui recense les annonces d'animaux publiées sur
CoinAfrique Sénégal. Elle s'appuie sur un scraper dédié et une base de données SQLite pour stocker
les résultats.

---

## 📦 Structure du projet

```
app.py              # Interface Streamlit (dark theme personnalisé)
scraper.py          # Logique de récupération et de nettoyage des annonces
database.py         # Wrapper SQLite (3 tables : annonces brutes, nettoyées et évaluations)

data/               # Copies CSV générées à la main / sorties de scraping
web scraper/        # mêmes CSV (peut être supprimé)
utils/              # notebooks d'expérimentation
```

La base SQLite générée est `coinafrique.db` à la racine.

## 🔧 Prérequis

- Python 3.8+ (le projet a été développé avec 3.13 sous Windows)
- La majorité des bibliothèques se gèrent via `pip`.

Installer les dépendances :

```bash
pip install -r requirements.txt   # si vous ajoutez ce fichier
# ou simplement :
pip install streamlit pandas plotly beautifulsoup4 requests
```

> `sqlite3` fait partie de la bibliothèque standard de Python.

## 🚀 Lancer l'application

1. Positionnez-vous dans le dossier du projet :
   `cd c:\Users\chris\OneDrive\Desktop\coinafrique_animaux`
2. Démarrez Streamlit :
   ```bash
   streamlit run app.py
   ```
3. L'interface s'ouvre dans le navigateur (http://localhost:8501 par défaut).

L'interface permet de visualiser des KPIs, des tableaux de données et de lancer un nouveau scraping.

## 🛠 Modules principaux

### `scraper.py`
- Contient des fonctions pour parcourir les catégories (`Chiens`, `Moutons`, ...)
- Garde en mémoire des sélecteurs « fallback » robustes.
- Nettoie les données (prix, doublons, etc.) et retourne des `DataFrame`.
- Offre également un utilitaire pour traiter un export de l'extension Web Scraper.

### `database.py`
- Initialise la base SQLite (3 tables).
- Fonctions de sauvegarde (`annonces_brutes`, `annonces_nettoyees`, `evaluations`).
- Quelques helpers de lecture/compte et de purge.

### `app.py`
- Interface Streamlit entièrement stylisée en « dark premium ».
- Utilise `scraper` et `database` pour récupérer et afficher les annonces.
- Prévoyez d'ajouter des évaluations (table `evaluations`).

## 🧪 Données existantes

Les sous-dossiers `data/` et `web scraper/` contiennent des exports `.csv` précédemment
utilisés pour tester. Ils ne sont pas nécessaires au fonctionnement de l'application mais
peuvent servir de base pour ré-importer des annonces.

## 📝 Suggestions

- Ajouter un `requirements.txt` ou `pyproject.toml` pour la gestion des dépendances.
- Mettre en place un fichier `.gitignore` pour exclure `__pycache__` et `coinafrique.db`.
- Documenter les workflows de scraping ou transformer `scraper` en package installable.

---

© 2026 — Utilisation libre, pas de licence explicite fournie.
