# 📝 ClinIA CR — Générateur de Comptes-Rendus Médicaux IA

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://clinia-cr.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> Remplissez les données cliniques → L'IA génère le CR en français → Export PDF en un clic.

---

## Spécialités disponibles

| Spécialité | Types de CR |
|---|---|
| ❤️ Cardiologie | Consultation, Hospit, Sortie, Echo |
| 🚨 Urgences | Lettre de passage, CR médical, Sortie |
| 🧠 Neurologie | Consultation, AVC, Épilepsie, Sortie |
| 🫁 Pneumologie | Consultation, Hospit, Sortie, EFR |

---

## Configuration API

Créer `.streamlit/secrets.toml` :
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

Sur Streamlit Cloud : Settings → Secrets → coller la clé.

---

## Quick Start

```bash
git clone https://github.com/mamadoulaminetall/clinia-cr.git
cd clinia-cr
pip install -r requirements.txt
# Ajouter .streamlit/secrets.toml avec votre clé Anthropic
streamlit run app.py
```

---

## Stack

- **Frontend :** Streamlit 1.32+, dark theme
- **IA :** Claude Haiku (Anthropic API) — streaming
- **PDF :** ReportLab — export direct

---

## Author

**Dr. Mamadou Lamine TALL, PhD**  
mamadoulaminetallgithub@gmail.com  
[github.com/mamadoulaminetall](https://github.com/mamadoulaminetall)

---

MIT License
