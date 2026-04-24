import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ─────────────────────────────────────────────
# OOP CLASSES  (Projet Jour 1 solution)
# ─────────────────────────────────────────────

class PuitsPetrolier:
    """Représente un puits de pétrole."""

    def __init__(self, nom: str, profondeur: float, type_reservoir: str):
        self.nom = nom
        self.profondeur = profondeur
        self.type_reservoir = type_reservoir
        self.production_quotidienne: list[float] = []
        self.nombre_jours = 0

    def ajouter_production(self, production: float):
        self.production_quotidienne.append(production)
        self.nombre_jours += 1

    def production_moyenne(self) -> float:
        if self.production_quotidienne:
            return sum(self.production_quotidienne) / len(self.production_quotidienne)
        return 0.0

    def production_cumulee(self) -> float:
        return sum(self.production_quotidienne)

    def to_dict(self) -> dict:
        return {
            "Nom": self.nom,
            "Profondeur (m)": self.profondeur,
            "Type réservoir": self.type_reservoir,
            "Prod. moyenne (bbl/j)": round(self.production_moyenne(), 1),
            "Prod. cumulée (bbl)": round(self.production_cumulee(), 1),
            "Jours de production": self.nombre_jours,
        }


class ChampPetrolier:
    """Représente un champ pétrolier contenant plusieurs puits."""

    def __init__(self, nom: str):
        self.nom = nom
        self.puits: list[PuitsPetrolier] = []
        self.reserves_initiales: float = 0.0

    def definir_reserves(self, reserves: float):
        self.reserves_initiales = reserves

    def ajouter_puits(self, puits: PuitsPetrolier):
        self.puits.append(puits)

    def production_totale(self) -> float:
        return sum(p.production_moyenne() for p in self.puits)

    def production_moyenne_champ(self) -> float:
        if not self.puits:
            return 0.0
        return self.production_totale() / len(self.puits)

    def production_cumulee_champ(self) -> float:
        return sum(p.production_cumulee() for p in self.puits)

    def taux_recuperation(self, prod_cumulee: float) -> float:
        if self.reserves_initiales == 0:
            return 0.0
        return (prod_cumulee / self.reserves_initiales) * 100

    def trouver_puits(self, nom: str):
        for p in self.puits:
            if p.nom == nom:
                return p
        return None

    def statistiques_avancees(self) -> dict | None:
        if not self.puits:
            return None
        prods = [p.production_moyenne() for p in self.puits]
        moy = sum(prods) / len(prods)
        ecart = (sum((x - moy) ** 2 for x in prods) / len(prods)) ** 0.5
        return {"min": min(prods), "max": max(prods), "moyenne": moy, "ecart_type": ecart}

    def puits_le_plus_productif(self):
        if not self.puits:
            return None
        return max(self.puits, key=lambda p: p.production_moyenne())

    def estimer_duree_vie(self) -> float:
        """Jours restants selon la prod. moyenne actuelle et les réserves restantes."""
        prod_cumulee = self.production_cumulee_champ()
        reserves_restantes = self.reserves_initiales - prod_cumulee
        prod_moy = self.production_totale()
        if prod_moy == 0:
            return 0.0
        return reserves_restantes / prod_moy


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Gestion de Champ Pétrolier – Hassi Messaoud",
    page_icon="🛢️",
    layout="wide",
)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.markdown("""
<div style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);
            padding:2rem 2.5rem;border-radius:12px;margin-bottom:1.5rem">
  <h1 style="color:#e8b84b;margin:0;font-size:2rem">🛢️ Gestion de Champ Pétrolier</h1>
  <p style="color:#aac4de;margin:0.4rem 0 0">
      Formation Python – Projet Jour 1 &nbsp;|&nbsp; Dr. Kadi &nbsp;|&nbsp; Hassi Messaoud, Algérie
  </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE – persistent data
# ─────────────────────────────────────────────

if "champ" not in st.session_state:
    # Build default scenario from the project spec
    champ = ChampPetrolier("Hassi Messaoud")
    champ.definir_reserves(1_000_000_000)

    p1 = PuitsPetrolier("MD-01", 3200, "Grès")
    p1.ajouter_production(500)
    p1.ajouter_production(520)

    p2 = PuitsPetrolier("MD-02", 3150, "Grès")
    p2.ajouter_production(480)
    p2.ajouter_production(490)

    champ.ajouter_puits(p1)
    champ.ajouter_puits(p2)
    st.session_state.champ = champ

champ: ChampPetrolier = st.session_state.champ

# ─────────────────────────────────────────────
# SIDEBAR – champ config + add puits
# ─────────────────────────────────────────────

with st.sidebar:
    st.header("⚙️ Configuration du champ")
    new_nom_champ = st.text_input("Nom du champ", value=champ.nom)
    new_reserves = st.number_input(
        "Réserves initiales (bbl)",
        value=int(champ.reserves_initiales),
        step=1_000_000,
        format="%d",
    )
    if st.button("✅ Mettre à jour le champ"):
        champ.nom = new_nom_champ
        champ.definir_reserves(new_reserves)
        st.success("Champ mis à jour !")

    st.divider()
    st.header("➕ Ajouter un puits")
    with st.form("form_puits"):
        nom_p = st.text_input("Nom du puits", placeholder="ex: MD-03")
        prof_p = st.number_input("Profondeur (m)", min_value=100.0, value=3100.0)
        type_p = st.selectbox("Type de réservoir", ["Grès", "Calcaire", "Dolomite", "Autre"])
        prods_raw = st.text_input(
            "Productions journalières (bbl/j, séparées par des virgules)",
            placeholder="450, 470, 490",
        )
        submitted = st.form_submit_button("Ajouter le puits")
        if submitted:
            if not nom_p:
                st.error("Le nom du puits est obligatoire.")
            else:
                try:
                    prods = [float(x.strip()) for x in prods_raw.split(",") if x.strip()]
                    puits_new = PuitsPetrolier(nom_p, prof_p, type_p)
                    for pr in prods:
                        puits_new.ajouter_production(pr)
                    champ.ajouter_puits(puits_new)
                    st.success(f"Puits **{nom_p}** ajouté !")
                    st.rerun()
                except ValueError:
                    st.error("Valeurs de production invalides.")

    st.divider()
    if st.button("🔄 Réinitialiser (données projet)", use_container_width=True):
        del st.session_state["champ"]
        st.rerun()

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────

prod_totale = champ.production_totale()
prod_cumulee = champ.production_cumulee_champ()
taux = champ.taux_recuperation(prod_cumulee)
duree_vie = champ.estimer_duree_vie()
stats = champ.statistiques_avancees()
top_puits = champ.puits_le_plus_productif()

c1, c2, c3, c4 = st.columns(4)
c1.metric("🛢️ Production totale", f"{prod_totale:,.0f} bbl/j")
c2.metric("📦 Production cumulée", f"{prod_cumulee:,.0f} bbl")
c3.metric("⚗️ Taux de récupération", f"{taux:.4f}%")
c4.metric("⏳ Durée de vie estimée", f"{duree_vie:,.0f} jours")

st.divider()

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Rapport du champ",
    "📊 Visualisations",
    "🔬 Statistiques avancées",
    "🖥️ Console (sortie texte)",
])

# ── TAB 1 : Rapport ──────────────────────────
with tab1:
    st.subheader(f"Rapport – Champ {champ.nom.upper()}")
    col_info, col_top = st.columns([2, 1])
    with col_info:
        st.markdown(f"""
| Paramètre | Valeur |
|---|---|
| Nombre de puits | {len(champ.puits)} |
| Production totale | {prod_totale:,.0f} bbl/j |
| Production moyenne/puits | {champ.production_moyenne_champ():,.0f} bbl/j |
| Réserves initiales | {champ.reserves_initiales:,.0f} bbl |
| Production cumulée | {prod_cumulee:,.0f} bbl |
| Taux de récupération | {taux:.4f}% |
| Durée de vie estimée | {duree_vie:,.0f} jours |
| Date du rapport | {datetime.now().strftime('%d/%m/%Y %H:%M')} |
""")
    with col_top:
        if top_puits:
            st.markdown("**🏆 Puits le plus productif**")
            st.info(f"**{top_puits.nom}**\n\n{top_puits.production_moyenne():.0f} bbl/j (moy.)")

    st.markdown("---")
    st.subheader("Détail par puits")
    if champ.puits:
        df = pd.DataFrame([p.to_dict() for p in champ.puits])
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Add production to existing well
        with st.expander("➕ Ajouter une production à un puits existant"):
            sel = st.selectbox("Sélectionner un puits", [p.nom for p in champ.puits])
            new_prod = st.number_input("Production (bbl/j)", min_value=0.0, value=500.0)
            if st.button("Enregistrer"):
                p = champ.trouver_puits(sel)
                if p:
                    p.ajouter_production(new_prod)
                    st.success(f"{new_prod} bbl/j ajouté pour {sel}")
                    st.rerun()
    else:
        st.info("Aucun puits dans le champ. Ajoutez-en depuis la barre latérale.")

# ── TAB 2 : Visualisations ───────────────────
with tab2:
    if not champ.puits:
        st.info("Ajoutez des puits pour voir les graphiques.")
    else:
        col_a, col_b = st.columns(2)

        # Bar chart – production moyenne par puits
        with col_a:
            noms = [p.nom for p in champ.puits]
            prods_moy = [p.production_moyenne() for p in champ.puits]
            fig_bar = go.Figure(go.Bar(
                x=noms, y=prods_moy,
                marker_color="#e8b84b",
                text=[f"{v:.0f}" for v in prods_moy],
                textposition="outside",
            ))
            fig_bar.update_layout(
                title="Production moyenne par puits (bbl/j)",
                xaxis_title="Puits", yaxis_title="bbl/j",
                plot_bgcolor="#0f3460", paper_bgcolor="#16213e",
                font_color="white",
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Pie – part de chaque puits dans prod totale
        with col_b:
            fig_pie = go.Figure(go.Pie(
                labels=noms, values=prods_moy,
                hole=0.4,
                marker_colors=px.colors.qualitative.Bold,
            ))
            fig_pie.update_layout(
                title="Répartition de la production (%)",
                plot_bgcolor="#0f3460", paper_bgcolor="#16213e",
                font_color="white",
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # Line chart – historique de production par puits
        st.subheader("📈 Historique de production journalière")
        fig_line = go.Figure()
        colors = px.colors.qualitative.Bold
        for i, p in enumerate(champ.puits):
            if p.production_quotidienne:
                fig_line.add_trace(go.Scatter(
                    x=list(range(1, p.nombre_jours + 1)),
                    y=p.production_quotidienne,
                    mode="lines+markers",
                    name=p.nom,
                    line=dict(color=colors[i % len(colors)], width=2),
                ))
        fig_line.update_layout(
            xaxis_title="Jour", yaxis_title="Production (bbl/j)",
            plot_bgcolor="#0f3460", paper_bgcolor="#16213e",
            font_color="white", legend_bgcolor="#1a1a2e",
        )
        st.plotly_chart(fig_line, use_container_width=True)

# ── TAB 3 : Statistiques avancées ────────────
with tab3:
    if not champ.puits:
        st.info("Ajoutez des puits pour voir les statistiques.")
    else:
        stats = champ.statistiques_avancees()
        if stats:
            s1, s2, s3, s4 = st.columns(4)
            s1.metric("📉 Production min", f"{stats['min']:,.0f} bbl/j")
            s2.metric("📈 Production max", f"{stats['max']:,.0f} bbl/j")
            s3.metric("📊 Moyenne", f"{stats['moyenne']:,.1f} bbl/j")
            s4.metric("📐 Écart-type", f"{stats['ecart_type']:,.1f} bbl/j")

        st.divider()
        st.subheader("Profondeur vs Production moyenne")
        df_scatter = pd.DataFrame({
            "Puits": [p.nom for p in champ.puits],
            "Profondeur (m)": [p.profondeur for p in champ.puits],
            "Prod. moyenne (bbl/j)": [p.production_moyenne() for p in champ.puits],
            "Type": [p.type_reservoir for p in champ.puits],
        })
        fig_sc = px.scatter(
            df_scatter, x="Profondeur (m)", y="Prod. moyenne (bbl/j)",
            text="Puits", color="Type", size="Prod. moyenne (bbl/j)",
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig_sc.update_layout(
            plot_bgcolor="#0f3460", paper_bgcolor="#16213e", font_color="white"
        )
        st.plotly_chart(fig_sc, use_container_width=True)

# ── TAB 4 : Console ──────────────────────────
with tab4:
    st.subheader("🖥️ Sortie console – Projet Jour 1")
    lines = []
    lines.append("=" * 60)
    lines.append("SYSTEME DE GESTION DE CHAMP PETROLIER")
    lines.append("=" * 60)
    lines.append(f"\n>>> Initialisation du champ petrolier...")
    lines.append(f"Reserves du champ {champ.nom} definies a {champ.reserves_initiales:,.0f} bbl")
    for p in champ.puits:
        lines.append(f"\n>>> Puits {p.nom} | Prof: {p.profondeur} m | Type: {p.type_reservoir}")
        for i, prod in enumerate(p.production_quotidienne, 1):
            lines.append(f"  Production ajoutee pour {p.nom} : {prod} bbl/j (Jour {i})")
    lines.append(f"\n>>> Ajout des puits au champ...")
    for p in champ.puits:
        lines.append(f"Puits {p.nom} ajoute au champ {champ.nom}")
    lines.append("\n" + "=" * 50)
    lines.append(f"RAPPORT DU CHAMP {champ.nom.upper()}")
    lines.append("=" * 50)
    lines.append(f"Nombre de puits: {len(champ.puits)}")
    lines.append(f"Production totale: {prod_totale:.0f} bbl/j")
    lines.append(f"Production moyenne par puits: {champ.production_moyenne_champ():.0f} bbl/j")
    lines.append(f"Reserves initiales: {champ.reserves_initiales:,.0f} bbl")
    lines.append("-" * 50)
    lines.append("Detail par puits:")
    for i, p in enumerate(champ.puits, 1):
        lines.append(f"  {i}. {p.nom} | Prof: {p.profondeur} m | Type: {p.type_reservoir} | Prod moy: {p.production_moyenne():.0f} bbl/j")
    lines.append("=" * 50)
    lines.append(f"\n>>> Calcul du taux de recuperation...")
    for p in champ.puits:
        lines.append(f"Production cumulee {p.nom}: {p.production_cumulee():.0f} bbl")
    lines.append(f"Production totale cumulee: {prod_cumulee:.0f} bbl")
    lines.append(f"Taux de recuperation: {taux:.4f}%")
    lines.append(f"\nDuree de vie estimee: {duree_vie:,.0f} jours")
    lines.append("\n" + "=" * 60)
    lines.append("FIN DU PROGRAMME")
    lines.append("=" * 60)

    st.code("\n".join(lines), language="text")
