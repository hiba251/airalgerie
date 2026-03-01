~# Feriel Boukerma et Hiba Doumar Master 1 APE DS2E


# Air Algérie – Outil Automatisé de Web Scraping

## Description du projet

Ce projet consiste à développer un outil automatisé de web scraping en Python utilisant Selenium.

L’objectif est de collecter automatiquement les offres promotionnelles disponibles sur le site public d’Air Algérie (offre et discount) et d’extraire des informations structurées telles que :

- Aéroport de départ
- Aéroport d’arrivée
- Prix original
- Devise
- Prix converti en euros (EUR)

Les données sont ensuite nettoyées, structurées et exportées sous forme de fichiers CSV et JSON.

---

## Objectifs pédagogiques

Ce projet met en œuvre :

- Web scraping avec Selenium
- Manipulation et nettoyage de données avec Pandas
- Extraction d’informations via parsing
- Programmation orientée objet
- Automatisation complète sans intervention manuelle

---

## Technologies utilisées

- Python
- Selenium
- Pandas
- WebDriver Manager

---

## Installation

Installer les dépendances :

pip install -r requirements.txt

---

## Exécution

Lancer le programme avec :

python scr/pipeline_spyder.py

Le script :

1. Ouvre automatiquement le site
2. Extrait les offres promotionnelles
3. Nettoie et structure les données
4. Convertit les prix en euros
5. Génère les fichiers de sortie

---

## Fichiers générés

Dans le dossier outputs/ (avec horodatage automatique) :

- offers_YYYYMMDD_HHMMSS.csv : données structurées et triées par prix en EUR
- summary_YYYYMMDD_HHMMSS.json : résumé de l’exécution
- best_offer_YYYYMMDD_HHMMSS.json : meilleure offre détectée
- raw_texts_YYYYMMDD_HHMMSS.txt : textes bruts extraits

Le script identifie automatiquement la meilleure offre (prix minimum en EUR) et l’affiche dans la console.
---

## Structure du projet

airalgerieProject/
│
├── scr/
│   ├── scraper.py
│   ├── parser.py
│   └── pipeline_spyder.py
│
├── outputs/
├── requirements.txt
├── README.md
└── .gitignore

---

## Aspects éthiques et légaux

- Le scraping concerne uniquement des données publiques.
- Aucune donnée personnelle n’est collectée.
- Aucun système d’authentification n’est contourné.
- Un délai entre les requêtes est implémenté.
- Le projet est réalisé à des fins pédagogiques uniquement.

---

## Analyse des données

Les offres sont converties en euros à l’aide de taux fixes définis dans le script.
Les résultats sont ensuite triés par prix croissant afin d’identifier automatiquement l’offre la plus avantageuse.

La meilleure offre est affichée dans la console et enregistrée séparément au format JSON.
---

## Limites

- Si la structure du site change, le script doit être adapté.
- Les taux de conversion sont fixes.
- Seule la page des offres promotionnelles est analysée.

---

## Améliorations possibles

- Utilisation d’une API de taux de change en temps réel
- Ajout d’un système de logs
- Amélioration des sélecteurs Selenium
- Création d’une interface graphique