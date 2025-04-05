# 📊 **MOYO - Plateforme d'Aide à la Décision** ⚕️

MOYO est une application interactive développée avec **Streamlit** permettant d'estimer le temps de survie des patients atteints du cancer gastrique après traitement. L'objectif est d'offrir un outil d'aide à la décision basé sur l'intelligence artificielle et l'analyse de survie.

---

## 🚀 **Fonctionnalités**
- **🏠 Accueil** : Présentation générale de la plateforme.
- **📊 Analyse exploratoire** : Visualisation des données et distribution des variables.
- **🤖 Prédiction de survie** : Utilisation de modèles statistiques et d'apprentissage automatique pour estimer le temps de survie.
- **📚 À Propos** : Explication des causes, symptômes et traitements du cancer gastrique.
- **📩 Contact** : Formulaire de contact pour toute question ou suggestion.

---

## 🛠️ **Technologies utilisées**
- **Python**
- **Streamlit** pour l'interface utilisateur
- **Pandas** pour la gestion des données
- **Scikit-learn & Joblib** pour le chargement des modèles de machine learning
- **TensorFlow/Keras** pour les modèles de deep learning
- **Lifelines** pour l'analyse de survie (modèle de Cox)
- **Plotly** pour la visualisation des données

---

## 📁 **Structure du projet**
```
MOYO/
│-- assets/               # Images et logos
│-- data/                 # Fichiers de données (ex: data.xlsx)
│-- models/               # Modèles entraînés (joblib, keras)
│-- app.py                # Code principal de l'application
│-- requirements.txt      # Dépendances du projet
│-- README.md             # Documentation
```

---

## 🔧 **Installation et exécution**
### 1️⃣ Cloner le projet
```bash
git clone https://github.com/votre-repo/moyo.git
cd moyo
```

### 2️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3️⃣ Lancer l'application
```bash
streamlit run app.py
```

---

## 🎯 **Modèles de prédiction**
MOYO utilise plusieurs algorithmes pour estimer la survie des patients :
- **Cox Proportionnal Hazards (Cox PH)**
- **Random Survival Forest (RSF)**
- **DeepSurv (réseau de neurones)**
- **Gradient Boosted Survival Trees (GBST)**

Les modèles sont pré-entraînés et stockés dans le dossier `models/`.

---

## 📬 **Contact**
📍 **Université Alioune Diop de Bambey, Sénégal**  
📧 **Email** : ahmed.sefdine@uadb.edu.sn  
🌐 **LinkedIn** : [linkedin.com/in/sefdineahmed](https://linkedin.com/in/sefdineahmed)  

---

Ce projet a été réalisé dans le cadre du mémoire de Master 2 en **Statistique et Informatique Décisionnelle**.

---
