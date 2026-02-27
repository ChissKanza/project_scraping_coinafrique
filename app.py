"""
app.py — CoinAfrique Animaux Sénégal
Design : Premium Dark — Elegant & Moderne
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scraper
import database

# ─── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CoinAfrique Animaux",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)
database.initialiser_base()

# ─── CSS Global ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: #0a0e1a;
    color: #e8eaf0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f1526 !important;
    border-right: 1px solid #1e2a45;
}
[data-testid="stSidebar"] * { color: #c5cde0 !important; }
[data-testid="stSidebar"] .stRadio label {
    background: #161d33;
    border: 1px solid #1e2a45;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 4px 0;
    display: block;
    cursor: pointer;
    transition: all .2s;
    font-size: 0.88rem;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: #1e2a45;
    border-color: #f4a023;
}
[data-testid="stSidebar"] .stRadio [aria-checked="true"] + label,
[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
    background: linear-gradient(135deg,#f4a023,#e8871a) !important;
    color: #0a0e1a !important;
    border-color: #f4a023 !important;
    font-weight: 600;
}

/* ── Cards KPI ── */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin: 20px 0; }
.kpi { background: #111827; border: 1px solid #1e2a45;
       border-radius: 14px; padding: 22px 18px; text-align: center;
       position: relative; overflow: hidden; }
.kpi::before { content:''; position:absolute; inset:0;
   background: linear-gradient(135deg, rgba(244,160,35,.07), transparent); }
.kpi-val { font-family:'Syne',sans-serif; font-size:2rem;
           font-weight:800; color:#f4a023; letter-spacing:-1px; }
.kpi-lbl { font-size:.78rem; color:#8892a4; margin-top:4px;
           text-transform:uppercase; letter-spacing:.08em; }
.kpi-icon { font-size:1.5rem; margin-bottom:6px; }

/* ── Section titles ── */
.sec-title {
    font-family:'Syne',sans-serif; font-size:1.35rem;
    font-weight:700; color:#f4a023;
    border-left: 4px solid #f4a023;
    padding-left: 12px; margin: 28px 0 14px;
}

/* ── Page hero ── */
.page-hero {
    background: linear-gradient(135deg,#111827 0%, #0d1630 100%);
    border: 1px solid #1e2a45;
    border-radius: 18px;
    padding: 32px 36px;
    margin-bottom: 24px;
    position: relative; overflow: hidden;
}
.page-hero::after {
    content: attr(data-emoji);
    position: absolute; right: 36px; top: 50%;
    transform: translateY(-50%);
    font-size: 5rem; opacity: .15;
}
.hero-title {
    font-family:'Syne',sans-serif;
    font-size: 1.8rem; font-weight: 800;
    color: #ffffff; margin-bottom: 6px;
}
.hero-sub { color: #8892a4; font-size: .93rem; line-height:1.6; }

/* ── Badge catégorie ── */
.badge {
    display:inline-block; padding:3px 10px;
    border-radius:20px; font-size:.75rem; font-weight:600;
    background:#1e2a45; color:#f4a023; margin:2px;
    border:1px solid #f4a023;
}

/* ── Boutons ── */
.stButton > button {
    background: linear-gradient(135deg,#f4a023,#e8871a);
    color: #0a0e1a; font-weight:700; border:none;
    border-radius:10px; padding:10px 20px;
    font-family:'Syne',sans-serif; font-size:.9rem;
    transition: all .2s; letter-spacing:.03em;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(244,160,35,.35);
}
.stDownloadButton > button {
    background: #111827 !important;
    color: #f4a023 !important;
    border: 1px solid #f4a023 !important;
    border-radius: 10px;
}

/* ── Tables ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
.dataframe { background: #111827 !important; }

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea, .stSelectbox div,
.stSlider, .stMultiSelect div {
    background: #111827 !important;
    border: 1px solid #1e2a45 !important;
    color: #e8eaf0 !important;
    border-radius: 10px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #f4a023 !important;
    box-shadow: 0 0 0 2px rgba(244,160,35,.2) !important;
}

/* ── Info / success / warning ── */
.stInfo { background: rgba(244,160,35,.1) !important; border-color: #f4a023 !important; }
.stSuccess { background: rgba(52,211,153,.1) !important; border-color: #34d399 !important; }

/* ── Progress ── */
.stProgress > div > div { background: #f4a023 !important; border-radius:4px; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] {
    background: #111827; color: #8892a4;
    border-radius: 8px 8px 0 0; border:1px solid #1e2a45;
    padding: 8px 20px; margin-right:4px;
    font-family:'Syne',sans-serif; font-size:.85rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#f4a023,#e8871a) !important;
    color: #0a0e1a !important; border-color: #f4a023 !important;
    font-weight:700;
}

/* ── Métriques sidebar ── */
[data-testid="stMetric"] {
    background: #161d33; border-radius:10px;
    padding: 10px 14px; border: 1px solid #1e2a45;
    margin-bottom: 8px;
}
[data-testid="stMetricValue"] { color: #f4a023 !important; font-family:'Syne',sans-serif; }
[data-testid="stMetricLabel"] { color: #8892a4 !important; font-size:.75rem; }

/* ── Expander ── */
details { background:#111827; border:1px solid #1e2a45; border-radius:10px; }
summary { color:#f4a023 !important; font-weight:600; padding:12px; cursor:pointer; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:#0a0e1a; }
::-webkit-scrollbar-thumb { background:#1e2a45; border-radius:3px; }
::-webkit-scrollbar-thumb:hover { background:#f4a023; }
</style>
""", unsafe_allow_html=True)

PLOT_THEME = dict(
    paper_bgcolor="#0a0e1a",
    plot_bgcolor="#111827",
    font_color="#c5cde0",
    font_family="DM Sans",
    colorway=["#f4a023","#34d399","#60a5fa","#f87171","#a78bfa","#fb923c"],
)

def apply_theme(fig):
    fig.update_layout(
        paper_bgcolor=PLOT_THEME["paper_bgcolor"],
        plot_bgcolor=PLOT_THEME["plot_bgcolor"],
        font=dict(color=PLOT_THEME["font_color"], family=PLOT_THEME["font_family"]),
        margin=dict(t=30, b=20, l=10, r=10),
        xaxis=dict(gridcolor="#1e2a45", zeroline=False),
        yaxis=dict(gridcolor="#1e2a45", zeroline=False),
    )
    return fig


# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 0 10px'>
        <div style='font-family:Syne;font-size:1.5rem;font-weight:800;color:#f4a023'>🐾 CoinAfrique</div>
        <div style='color:#8892a4;font-size:.8rem;margin-top:4px'>Animaux · Sénégal</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    page = st.radio("", [
        "🕷️ Scraping BeautifulSoup",
        "📂 Import CSV WebScraper",
        "📊 Dashboard Analytique",
        "📝 Évaluation",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("<div style='color:#8892a4;font-size:.75rem;text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px'>Base de données</div>", unsafe_allow_html=True)
    c = database.compter()
    st.metric("Annonces nettoyées", c["annonces_nettoyees"])
    st.metric("Annonces brutes",    c["annonces_brutes"])
    st.metric("Évaluations",        c["evaluations"])

    if st.button("🗑️ Vider annonces_nettoyees", use_container_width=True):
        database.vider_table("annonces_nettoyees")
        st.success("Table vidée !"); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — SCRAPING BS4
# ══════════════════════════════════════════════════════════════════════════════
if page == "🕷️ Scraping BeautifulSoup":

    st.markdown("""
    <div class="page-hero" data-emoji="🕷️">
        <div class="hero-title">Scraping automatique — BeautifulSoup</div>
        <div class="hero-sub">
            Récupère les annonces en temps réel depuis CoinAfrique Sénégal.<br>
            Nettoyage automatique · Déduplication · Export SQLite & CSV
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Test de connexion rapide ──
    with st.expander("🔌 Tester la connexion au site avant de scraper"):
        if st.button("▶  Vérifier l'accès à CoinAfrique", key="test_co"):
            import requests as _req
            try:
                resp = _req.get(
                    "https://sn.coinafrique.com/categorie/moutons?page=1",
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=10
                )
                if resp.status_code == 200:
                    from bs4 import BeautifulSoup as _BS
                    soup = _BS(resp.text, "html.parser")
                    cards = soup.select("div.col.s12.m4") or soup.select("div[class*='ad__card']")
                    liens = soup.select("a[href*='/annonce/']")
                    st.success(
                        f"✅ Site accessible (HTTP {resp.status_code}) — "
                        f"{len(cards)} cartes | {len(liens)} liens d'annonces détectés"
                    )
                    if not cards and not liens:
                        st.warning(
                            "⚠️ Le site répond mais aucune annonce détectée. "
                            "La structure HTML a peut-être changé."
                        )
                        st.code(resp.text[:1500], language="html")
                else:
                    st.error(f"❌ HTTP {resp.status_code} — Le site répond mais avec une erreur.")
            except Exception as e:
                st.error(f"❌ Impossible de joindre le site : {e}")

    col1, col2 = st.columns([3, 1])
    with col1:
        categories_choisies = st.multiselect(
            "Catégories à scraper",
            list(scraper.CATEGORIES.keys()),
            default=list(scraper.CATEGORIES.keys()),
        )
    with col2:
        nb_pages = st.number_input("Pages / catégorie", 1, 15, 3)

    est = nb_pages * len(categories_choisies) * 20
    st.markdown(f"<div style='color:#8892a4;font-size:.85rem'>Estimation : ≈ <b style='color:#f4a023'>{est}</b> annonces</div>", unsafe_allow_html=True)
    st.markdown("")

    if st.button("🚀  Lancer le Scraping", use_container_width=True):
        if not categories_choisies:
            st.warning("Sélectionnez au moins une catégorie.")
        else:
            bar = st.progress(0)
            msg = st.empty()
            total = nb_pages * len(categories_choisies)
            step  = [0]

            def cb(m):
                step[0] += 1
                bar.progress(min(step[0]/total, 1.0))
                msg.markdown(f"<div style='color:#f4a023;font-size:.85rem'>{m}</div>", unsafe_allow_html=True)

            with st.spinner(""):
                df_raw, erreurs = scraper.scrape_toutes_categories(nb_pages, categories_choisies, cb)

            bar.progress(1.0)
            msg.empty()

            # Afficher les erreurs même partielles
            if erreurs:
                with st.expander(f"⚠️ {len(erreurs)} avertissement(s) détecté(s) — cliquer pour voir", expanded=True):
                    for e in erreurs:
                        st.markdown(f"<div style='color:#f87171;font-size:.85rem;padding:4px 0'>• {e}</div>",
                                    unsafe_allow_html=True)

            if df_raw is None or df_raw.empty:
                st.error(
                    "❌ **Aucune annonce récupérée.**\n\n"
                    "Causes possibles :\n"
                    "- Connexion internet coupée\n"
                    "- Le site CoinAfrique est inaccessible depuis votre réseau\n"
                    "- Le site a changé sa structure HTML\n\n"
                    "👉 Testez d'abord : ouvrez https://sn.coinafrique.com/categorie/moutons dans votre navigateur."
                )
            else:
                df_clean = scraper.nettoyer_dataframe(df_raw, "BeautifulSoup")
                st.session_state["df_bs4"] = df_clean
                st.success(f"✅  **{len(df_clean)} annonces** récupérées et nettoyées !")

    if "df_bs4" in st.session_state:
        df = st.session_state["df_bs4"]
        prix_v = df["prix"].dropna()

        st.markdown('<div class="sec-title">Résultats</div>', unsafe_allow_html=True)

        # KPIs
        st.markdown(f"""
        <div class="kpi-grid">
            <div class="kpi">
                <div class="kpi-icon">📋</div>
                <div class="kpi-val">{len(df):,}</div>
                <div class="kpi-lbl">Total annonces</div>
            </div>
            <div class="kpi">
                <div class="kpi-icon">💰</div>
                <div class="kpi-val">{f"{prix_v.mean():,.0f}" if len(prix_v) else "—"}</div>
                <div class="kpi-lbl">Prix moyen (FCFA)</div>
            </div>
            <div class="kpi">
                <div class="kpi-icon">📍</div>
                <div class="kpi-val">{df['adresse'].nunique()}</div>
                <div class="kpi-lbl">Villes uniques</div>
            </div>
            <div class="kpi">
                <div class="kpi-icon">🏷️</div>
                <div class="kpi-val">{df['categorie'].nunique()}</div>
                <div class="kpi-lbl">Catégories</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(df, use_container_width=True, height=320)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💾  Sauvegarder dans SQLite", use_container_width=True):
                n = database.sauvegarder_annonces_nettoyees(df)
                st.success(f"{n} annonces sauvegardées !"); st.rerun()
        with col_b:
            st.download_button(
                "⬇️  Télécharger CSV",
                df.to_csv(index=False).encode("utf-8"),
                "bs4_annonces.csv", "text/csv",
                use_container_width=True,
            )


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — IMPORT CSV WEBSCRAPER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📂 Import CSV WebScraper":

    st.markdown("""
    <div class="page-hero" data-emoji="📂">
        <div class="hero-title">Import & Nettoyage — CSV WebScraper</div>
        <div class="hero-sub">
            Importez vos fichiers exportés par l'extension WebScraper Chrome.<br>
            Détection automatique des colonnes · Nettoyage · Sauvegarde
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Colonnes attendues</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#111827;border:1px solid #1e2a45;border-radius:12px;padding:16px;font-size:.85rem;color:#8892a4'>
        <span class="badge">web_scraper_order</span>
        <span class="badge">web_scraper_start_url</span>
        <span class="badge">nom</span>
        <span class="badge">prix</span>
        <span class="badge">adresse</span>
        <span class="badge">image</span>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Déposez vos fichiers CSV",
        type=["csv"], accept_multiple_files=True,
    )

    if uploaded:
        frames, brutes_ok = [], 0
        for f in uploaded:
            try:
                df_brut = pd.read_csv(f, encoding="utf-8-sig")
                database.sauvegarder_annonces_brutes(df_brut, fichier=f.name)
                brutes_ok += len(df_brut)

                df_net = scraper.nettoyer_dataframe(df_brut, source=f"WebScraper/{f.name}")
                frames.append(df_net)

                st.markdown(f"""
                <div style='background:#111827;border:1px solid #34d399;border-radius:10px;
                            padding:12px 16px;margin:6px 0;display:flex;justify-content:space-between'>
                    <span style='color:#34d399'>✓ {f.name}</span>
                    <span style='color:#8892a4'>{len(df_net)} annonces nettoyées</span>
                </div>""", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erreur {f.name} : {e}")

        if frames:
            df_all = pd.concat(frames, ignore_index=True)
            df_all = df_all.drop_duplicates(subset=["nom","prix_brut","adresse"]).reset_index(drop=True)
            st.session_state["df_ws"] = df_all

            prix_v = df_all["prix"].dropna()
            st.markdown('<div class="sec-title">Résumé global</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="kpi-grid">
                <div class="kpi">
                    <div class="kpi-icon">📁</div>
                    <div class="kpi-val">{len(uploaded)}</div>
                    <div class="kpi-lbl">Fichiers importés</div>
                </div>
                <div class="kpi">
                    <div class="kpi-icon">📋</div>
                    <div class="kpi-val">{len(df_all):,}</div>
                    <div class="kpi-lbl">Annonces nettoyées</div>
                </div>
                <div class="kpi">
                    <div class="kpi-icon">💰</div>
                    <div class="kpi-val">{f"{prix_v.mean():,.0f}" if len(prix_v) else "—"}</div>
                    <div class="kpi-lbl">Prix moyen (FCFA)</div>
                </div>
                <div class="kpi">
                    <div class="kpi-icon">🏷️</div>
                    <div class="kpi-val">{df_all['categorie'].nunique()}</div>
                    <div class="kpi-lbl">Catégories</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            tab1, tab2 = st.tabs(["📋  Données nettoyées", "📊  Distribution des prix"])
            with tab1:
                st.dataframe(df_all, use_container_width=True, height=350)
            with tab2:
                if len(prix_v) > 0:
                    fig = px.histogram(df_all[df_all["prix"].notna()], x="prix",
                                       nbins=35, color="categorie",
                                       labels={"prix":"Prix (FCFA)","count":"Annonces"},
                                       color_discrete_sequence=PLOT_THEME["colorway"])
                    st.plotly_chart(apply_theme(fig), use_container_width=True)
                else:
                    st.info("Aucun prix numérique dans ces données.")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾  Sauvegarder nettoyées → SQLite", use_container_width=True):
                    n = database.sauvegarder_annonces_nettoyees(df_all)
                    st.success(f"{n} annonces sauvegardées !"); st.rerun()
            with col2:
                st.download_button(
                    "⬇️  Télécharger CSV nettoyé",
                    df_all.to_csv(index=False).encode("utf-8"),
                    "webscraper_nettoye.csv", "text/csv",
                    use_container_width=True,
                )


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Dashboard Analytique":

    st.markdown("""
    <div class="page-hero" data-emoji="📊">
        <div class="hero-title">Dashboard Analytique</div>
        <div class="hero-sub">
            Exploration interactive des annonces CoinAfrique Animaux Sénégal.<br>
            8 graphiques · Statistiques descriptives · Export CSV
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Charger les données (DB + session) ──
    frames = []
    df_db = database.lire_annonces_nettoyees()
    if not df_db.empty:               frames.append(df_db)
    if "df_bs4" in st.session_state:  frames.append(st.session_state["df_bs4"])
    if "df_ws"  in st.session_state:  frames.append(st.session_state["df_ws"])

    if not frames:
        st.markdown("""
        <div style='background:#111827;border:2px dashed #1e2a45;border-radius:16px;
                    text-align:center;padding:60px;margin-top:20px'>
            <div style='font-size:3rem'>📭</div>
            <div style='font-family:Syne;font-size:1.2rem;color:#8892a4;margin-top:12px'>
                Aucune donnée disponible
            </div>
            <div style='color:#4a5568;font-size:.85rem;margin-top:8px'>
                Allez sur <b style='color:#f4a023'>Page 1</b> (scraping) ou
                <b style='color:#f4a023'>Page 2</b> (import CSV) puis cliquez
                <b style='color:#f4a023'>Sauvegarder dans SQLite</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates(subset=["nom","prix_brut","adresse"]).reset_index(drop=True)

    # ── Filtres sidebar ──
    with st.sidebar:
        st.markdown("---")
        st.markdown("<div style='color:#8892a4;font-size:.75rem;text-transform:uppercase;"
                    "letter-spacing:.1em;margin-bottom:10px'>Filtres Dashboard</div>",
                    unsafe_allow_html=True)

        cats = ["Toutes"] + sorted(df["categorie"].dropna().unique().tolist())
        f_cat = st.selectbox("Catégorie", cats)
        if f_cat != "Toutes":
            df = df[df["categorie"] == f_cat]

        sources = ["Toutes"] + sorted(df["source"].dropna().unique().tolist()) if "source" in df.columns else ["Toutes"]
        f_src = st.selectbox("Source", sources)
        if f_src != "Toutes" and "source" in df.columns:
            df = df[df["source"] == f_src]

        prix_v_all = df["prix"].dropna()
        if len(prix_v_all) > 1:
            pmin, pmax = int(prix_v_all.min()), int(prix_v_all.max())
            if pmin < pmax:
                f_prix = st.slider("Fourchette prix (FCFA)", pmin, pmax, (pmin, pmax),
                                   format="%d")
                df = df[(df["prix"].isna()) |
                        ((df["prix"] >= f_prix[0]) & (df["prix"] <= f_prix[1]))]

    prix_v = df["prix"].dropna()

    # ══════════════════════
    #  KPIs — 6 indicateurs
    # ══════════════════════
    nb_avec_prix = len(prix_v)
    nb_sans_prix = len(df) - nb_avec_prix
    mediane      = prix_v.median() if nb_avec_prix else 0
    ecart_type   = prix_v.std()    if nb_avec_prix else 0

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:20px 0">
        <div class="kpi">
            <div class="kpi-icon">📋</div>
            <div class="kpi-val">{len(df):,}</div>
            <div class="kpi-lbl">Total annonces</div>
        </div>
        <div class="kpi">
            <div class="kpi-icon">💰</div>
            <div class="kpi-val">{f"{prix_v.mean():,.0f}" if nb_avec_prix else "—"}</div>
            <div class="kpi-lbl">Prix moyen (FCFA)</div>
        </div>
        <div class="kpi">
            <div class="kpi-icon">📊</div>
            <div class="kpi-val">{f"{mediane:,.0f}" if nb_avec_prix else "—"}</div>
            <div class="kpi-lbl">Prix médian (FCFA)</div>
        </div>
        <div class="kpi">
            <div class="kpi-icon">🔽</div>
            <div class="kpi-val">{f"{prix_v.min():,.0f}" if nb_avec_prix else "—"}</div>
            <div class="kpi-lbl">Prix minimum (FCFA)</div>
        </div>
        <div class="kpi">
            <div class="kpi-icon">🔼</div>
            <div class="kpi-val">{f"{prix_v.max():,.0f}" if nb_avec_prix else "—"}</div>
            <div class="kpi-lbl">Prix maximum (FCFA)</div>
        </div>
        <div class="kpi">
            <div class="kpi-icon">📍</div>
            <div class="kpi-val">{df["adresse"].nunique()}</div>
            <div class="kpi-lbl">Villes uniques</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════
    #  GRAPHIQUE 1 & 2 — Pie + Histo
    # ══════════════════════════════════
    st.markdown('<div class="sec-title">📈 Répartition & Distribution</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Annonces par catégorie**")
        cat_c = df["categorie"].value_counts().reset_index()
        cat_c.columns = ["Catégorie", "Annonces"]
        fig = px.pie(cat_c, values="Annonces", names="Catégorie",
                     hole=0.5, color_discrete_sequence=PLOT_THEME["colorway"])
        fig.update_traces(textinfo="percent+label", textfont_size=12,
                          marker=dict(line=dict(color="#0a0e1a", width=2)))
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col2:
        st.markdown("**Distribution des prix**")
        if nb_avec_prix > 0:
            df_px = df[df["prix"].notna() & (df["prix"] <= df["prix"].quantile(0.97))]
            fig = px.histogram(df_px, x="prix", nbins=40, color="categorie",
                               labels={"prix": "Prix (FCFA)", "count": "Nb annonces"},
                               color_discrete_sequence=PLOT_THEME["colorway"])
            fig.update_layout(bargap=0.05)
            st.plotly_chart(apply_theme(fig), use_container_width=True)
        else:
            st.info("Aucun prix numérique disponible.")

    # ══════════════════════════════════
    #  GRAPHIQUE 3 — Annonces avec/sans prix
    # ══════════════════════════════════
    st.markdown('<div class="sec-title">💡 Qualité des données prix</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Annonces avec vs sans prix numérique**")
        dispo = pd.DataFrame({
            "Statut":  ["Avec prix",    "Prix sur demande / manquant"],
            "Nombre":  [nb_avec_prix,   nb_sans_prix],
        })
        fig = px.pie(dispo, values="Nombre", names="Statut", hole=0.45,
                     color_discrete_sequence=["#f4a023", "#1e2a45"])
        fig.update_traces(textinfo="percent+label",
                          marker=dict(line=dict(color="#0a0e1a", width=2)))
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col4:
        st.markdown("**Nombre d'annonces par catégorie**")
        cat_bar = df["categorie"].value_counts().reset_index()
        cat_bar.columns = ["Catégorie", "Annonces"]
        fig = px.bar(cat_bar, x="Catégorie", y="Annonces", color="Catégorie",
                     color_discrete_sequence=PLOT_THEME["colorway"],
                     text="Annonces")
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, xaxis_tickangle=-20)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    # ══════════════════════════════════
    #  GRAPHIQUE 4 — Top 10 adresses
    # ══════════════════════════════════
    st.markdown('<div class="sec-title">📍 Localisation</div>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)

    with col5:
        st.markdown("**Top 10 des adresses les plus actives**")
        top_addr = df["adresse"].value_counts().head(10).reset_index()
        top_addr.columns = ["Adresse", "Annonces"]
        fig = px.bar(top_addr, x="Annonces", y="Adresse", orientation="h",
                     color="Annonces",
                     color_continuous_scale=["#1e2a45", "#f4a023"])
        fig.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col6:
        if nb_avec_prix > 0:
            st.markdown("**Prix médian par adresse (Top 8)**")
            med_addr = (df[df["prix"].notna()]
                        .groupby("adresse")["prix"]
                        .agg(["median", "count"])
                        .reset_index()
                        .sort_values("count", ascending=False)
                        .head(8))
            med_addr.columns = ["Adresse", "Prix médian", "Nb annonces"]
            fig = px.bar(med_addr, x="Prix médian", y="Adresse", orientation="h",
                         color="Prix médian",
                         color_continuous_scale=["#1e2a45", "#34d399"],
                         hover_data=["Nb annonces"])
            fig.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
            st.plotly_chart(apply_theme(fig), use_container_width=True)

    # ══════════════════════════════════
    #  GRAPHIQUE 5 — Boxplot + Violin
    # ══════════════════════════════════
    if nb_avec_prix > 3:
        st.markdown('<div class="sec-title">📦 Dispersion des prix</div>', unsafe_allow_html=True)
        col7, col8 = st.columns(2)
        df_bx = df[df["prix"].notna() & (df["prix"] <= df["prix"].quantile(0.95))]

        with col7:
            st.markdown("**Boîte à moustaches par catégorie**")
            fig = px.box(df_bx, x="categorie", y="prix", color="categorie",
                         labels={"prix": "Prix (FCFA)", "categorie": ""},
                         color_discrete_sequence=PLOT_THEME["colorway"],
                         points="outliers")
            fig.update_layout(showlegend=False, xaxis_tickangle=-15)
            st.plotly_chart(apply_theme(fig), use_container_width=True)

        with col8:
            st.markdown("**Violin plot — densité des prix**")
            fig = px.violin(df_bx, x="categorie", y="prix", color="categorie",
                            labels={"prix": "Prix (FCFA)", "categorie": ""},
                            color_discrete_sequence=PLOT_THEME["colorway"],
                            box=True)
            fig.update_layout(showlegend=False, xaxis_tickangle=-15)
            st.plotly_chart(apply_theme(fig), use_container_width=True)

    # ══════════════════════════════════
    #  TABLEAU STATISTIQUES DESCRIPTIVES
    # ══════════════════════════════════
    if nb_avec_prix > 0:
        st.markdown('<div class="sec-title">🔢 Statistiques descriptives</div>', unsafe_allow_html=True)
        stats = (df.groupby("categorie")["prix"]
                   .agg(["count","mean","median","min","max","std"])
                   .reset_index())
        stats.columns = ["Catégorie","Nb annonces avec prix","Moyenne","Médiane","Min","Max","Écart-type"]
        for col in ["Moyenne","Médiane","Min","Max","Écart-type"]:
            stats[col] = stats[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "—")
        st.dataframe(stats, use_container_width=True, hide_index=True)

    # ══════════════════════════════════
    #  TABLEAU DONNÉES + RECHERCHE
    # ══════════════════════════════════
    st.markdown('<div class="sec-title">📋 Données complètes</div>', unsafe_allow_html=True)
    search = st.text_input("🔍 Rechercher", placeholder="Ex: chiot, Dakar, mouton…")
    df_show = df[df["nom"].str.contains(search, case=False, na=False)] if search else df
    st.markdown(f"<div style='color:#8892a4;font-size:.82rem;margin-bottom:6px'>"
                f"{len(df_show):,} résultats</div>", unsafe_allow_html=True)
    st.dataframe(df_show, use_container_width=True, height=360)

    st.download_button(
        "⬇️  Exporter toutes les données (CSV)",
        df.to_csv(index=False).encode("utf-8"),
        "coinafrique_export.csv", "text/csv",
    )


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 4 — ÉVALUATION KOBOTOOLBOX
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📝 Évaluation":

    KOBO_LIEN = "https://ee.kobotoolbox.org/x/YpaAZ32s"

    st.markdown("""
    <div class="page-hero" data-emoji="📝">
        <div class="hero-title">Formulaire d'Évaluation — KoboToolbox</div>
        <div class="hero-sub">
            Formulaire académique hébergé sur KoboToolbox.<br>
            Cliquez le bouton ci-dessous pour accéder au formulaire.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Carte info ──
    st.markdown("""
    <div style='background:#111827;border:1px solid #1e2a45;border-radius:18px;
                padding:30px;text-align:center;margin:10px 0 6px'>
        <div style='font-size:3rem;margin-bottom:10px'>📝</div>
        <div style='font-family:Syne,sans-serif;font-size:1.2rem;font-weight:700;
                    color:#ffffff;margin-bottom:6px'>
            Évaluation de l'Application CoinAfrique
        </div>
        <div style='color:#8892a4;font-size:.88rem;line-height:1.6'>
            6 sections · ~3 minutes · Réponses enregistrées sur KoboToolbox
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Bouton natif Streamlit — seul moyen fiable d'ouvrir un lien externe ──
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.link_button(
            "📝  Ouvrir le Formulaire KoboToolbox",
            url=KOBO_LIEN,
            use_container_width=True,
            type="primary",
        )

    st.markdown("<div style='text-align:center;color:#4a5568;font-size:.78rem;"
                "margin-top:6px'>S'ouvre dans un nouvel onglet</div>",
                unsafe_allow_html=True)

    st.markdown("---")

    # ── 2 colonnes info ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style='background:#111827;border:1px solid #1e2a45;border-radius:12px;padding:18px'>
            <div style='color:#f4a023;font-family:Syne,sans-serif;font-weight:700;
                        font-size:.95rem;margin-bottom:12px'>📋 Sections du formulaire</div>
            <div style='color:#c5cde0;font-size:.85rem;line-height:2.1'>
                <span style='color:#f4a023'>①</span> Informations sur l'évaluateur<br>
                <span style='color:#f4a023'>②</span> Première impression &amp; interface<br>
                <span style='color:#f4a023'>③</span> Fonctionnalités &amp; performances<br>
                <span style='color:#f4a023'>④</span> Problèmes rencontrés<br>
                <span style='color:#f4a023'>⑤</span> Satisfaction globale<br>
                <span style='color:#f4a023'>⑥</span> Suggestions d'amélioration
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background:#111827;border:1px solid #1e2a45;border-radius:12px;padding:18px'>
            <div style='color:#f4a023;font-family:Syne,sans-serif;font-weight:700;
                        font-size:.95rem;margin-bottom:12px'>💡 Récupérer les réponses</div>
            <div style='color:#c5cde0;font-size:.85rem;line-height:2.1'>
                <span style='color:#34d399'>1.</span> kf.kobotoolbox.org<br>
                <span style='color:#34d399'>2.</span> Ouvrir votre projet<br>
                <span style='color:#34d399'>3.</span> Onglet <b style='color:#fff'>DATA</b><br>
                <span style='color:#34d399'>4.</span> Downloads → CSV ou Excel<br>
                <span style='color:#34d399'>5.</span> Analyser dans Python / Excel
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style='background:#0d1526;border:1px solid #1e2a45;border-radius:10px;
                padding:12px 18px;color:#8892a4;font-size:.8rem'>
        <b style='color:#f4a023'>Lien direct :</b>
        <span style='font-family:Courier;color:#c5cde0;margin-left:8px'>{KOBO_LIEN}</span>
    </div>
    """, unsafe_allow_html=True)
