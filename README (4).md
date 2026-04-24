# 🛢️ Gestion de Champ Pétrolier – Hassi Messaoud

> **Formation Python pour l'Ingénierie Pétrolière – Projet Jour 1**  
> Dr. Kadi · Application Streamlit complète

---

## 📌 Description

Application web interactive construite avec **Python + Streamlit**, implémentant le système de gestion de champ pétrolier du Projet Jour 1.  
Elle modélise deux classes OOP (`PuitsPetrolier` & `ChampPetrolier`) et les expose dans une interface graphique moderne avec visualisations Plotly.

---

## 🗂️ Structure du projet

```
champ-petrolier/
│
├── app.py              # Application Streamlit principale
├── README.md           # Ce fichier
└── requirements.txt    # Dépendances Python
```

---

## ⚙️ Installation & Lancement

### 1. Cloner / télécharger le projet

```bash
git clone https://github.com/votre-user/champ-petrolier.git
cd champ-petrolier
```

### 2. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur à `http://localhost:8501`.

---

## 📦 requirements.txt

```
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
```

---

## 🏗️ Architecture OOP (Solution du Projet)

### Classe `PuitsPetrolier`

| Attribut | Type | Description |
|---|---|---|
| `nom` | `str` | Identifiant du puits (ex: MD-01) |
| `profondeur` | `float` | Profondeur en mètres |
| `type_reservoir` | `str` | Grès / Calcaire / Dolomite |
| `production_quotidienne` | `list[float]` | Historique bbl/j |
| `nombre_jours` | `int` | Jours de production |

| Méthode | Retour | Description |
|---|---|---|
| `ajouter_production(val)` | `None` | Ajoute une entrée de production |
| `production_moyenne()` | `float` | Moyenne des productions |
| `production_cumulee()` | `float` | Somme totale (bbl) |

### Classe `ChampPetrolier`

| Attribut | Type | Description |
|---|---|---|
| `nom` | `str` | Nom du champ |
| `puits` | `list[PuitsPetrolier]` | Liste des puits |
| `reserves_initiales` | `float` | Réserves en barils |

| Méthode | Description |
|---|---|
| `ajouter_puits(p)` | Ajoute un puits au champ |
| `production_totale()` | Somme des productions moyennes |
| `production_moyenne_champ()` | Moyenne par puits |
| `production_cumulee_champ()` | Production cumulée totale |
| `taux_recuperation(cumul)` | Taux de récup. en % |
| `estimer_duree_vie()` | Durée de vie restante (jours) |
| `statistiques_avancees()` | Min, max, moy, écart-type |
| `trouver_puits(nom)` | Recherche par nom |
| `puits_le_plus_productif()` | Retourne le meilleur puits |

---

## 🖥️ Fonctionnalités de l'application

| Onglet | Contenu |
|---|---|
| 📋 Rapport du champ | KPIs, tableau puits, ajout de production |
| 📊 Visualisations | Bar chart, Pie chart, courbe historique |
| 🔬 Statistiques avancées | Min/Max/Écart-type, scatter profondeur vs prod |
| 🖥️ Console | Sortie texte identique au terminal Python |

**Barre latérale :**
- Modifier le nom du champ et les réserves initiales
- Ajouter un nouveau puits dynamiquement
- Réinitialiser aux données du projet (MD-01, MD-02)

---

## 📊 Données de test (Projet Jour 1)

| Puits | Profondeur | Réservoir | Jour 1 | Jour 2 |
|---|---|---|---|---|
| MD-01 | 3 200 m | Grès | 500 bbl/j | 520 bbl/j |
| MD-02 | 3 150 m | Grès | 480 bbl/j | 490 bbl/j |

**Champ :** Hassi Messaoud · **Réserves :** 1 000 000 000 bbl

---

## 🌍 Déploiement sur Streamlit Cloud

1. Pousser le projet sur GitHub
2. Aller sur [share.streamlit.io](https://share.streamlit.io)
3. Connecter votre dépôt → sélectionner `app.py`
4. Cliquer **Deploy** — l'app est en ligne en quelques minutes !

---

## 👤 Auteur

**Souhil SERHOUDJI** – Next-Generation Oil Field Solutions  
Formation Python pour l'Ingénierie Pétrolière · 2026
