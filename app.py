import streamlit as st

st.set_page_config(
    page_title="ClinIA — Générateur CR",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.hero { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 16px; padding: 32px; margin-bottom: 24px;
        border: 1px solid #334155; }
.hero h1 { font-size: 2rem; color: #f1f5f9; margin: 0 0 8px 0; }
.hero p  { color: #94a3b8; margin: 0; font-size: 1rem; }
.card { background: #1e293b; border-radius: 12px; padding: 20px;
        border-left: 4px solid #3b82f6; margin: 8px 0; cursor: pointer; }
.card:hover { border-left-color: #60a5fa; }
.card-title { font-size: 1.1rem; font-weight: 700; color: #f1f5f9; }
.card-sub   { font-size: 0.85rem; color: #94a3b8; margin-top: 4px; }
.badge { background: #1e40af; color: #bfdbfe; border-radius: 6px;
         padding: 2px 8px; font-size: 0.72rem; margin: 2px; display: inline-block; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>📝 ClinIA — Générateur de Comptes-Rendus</h1>
  <p>Remplissez les données cliniques · L'IA rédige le CR en français · Exportez en PDF</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""<div class="card">
        <div class="card-title">❤️ Cardiologie</div>
        <div class="card-sub">Consultation · Hospit · Sortie · Echo</div>
        <span class="badge">FA</span><span class="badge">SCA</span><span class="badge">IC</span>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="card">
        <div class="card-title">🚨 Urgences</div>
        <div class="card-sub">Lettre de passage · CR urgences</div>
        <span class="badge">Sepsis</span><span class="badge">Trauma</span>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown("""<div class="card">
        <div class="card-title">🧠 Neurologie</div>
        <div class="card-sub">Consultation · CR AVC · Epilepsie</div>
        <span class="badge">AVC</span><span class="badge">Migraine</span>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown("""<div class="card">
        <div class="card-title">🫁 Pneumologie</div>
        <div class="card-sub">Consultation · Hospit · Sortie</div>
        <span class="badge">BPCO</span><span class="badge">EP</span>
    </div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### Sélectionner une spécialité dans le menu à gauche")

st.markdown("""
| Spécialité | Types de CR disponibles |
|---|---|
| ❤️ Cardiologie | Consultation, Compte-rendu d'hospitalisation, Lettre de sortie, Echo |
| 🚨 Urgences | Lettre de passage aux urgences, CR médical urgences |
| 🧠 Neurologie | Consultation neurologique, CR AVC, Compte-rendu épilepsie |
| 🫁 Pneumologie | Consultation, Compte-rendu d'hospitalisation, EFR |
""")

st.markdown("---")
st.markdown("""
<div style="background:linear-gradient(135deg,#1e3a5f,#0f172a);border-radius:16px;padding:24px;
     border:1px solid #3b82f6;text-align:center;margin:16px 0;">
  <div style="font-size:1.3rem;font-weight:700;color:#f1f5f9;margin-bottom:8px;">
    🔓 Accès illimité — 9€/mois
  </div>
  <div style="color:#94a3b8;margin-bottom:16px;font-size:0.95rem;">
    Essai gratuit 7 jours · Résiliable à tout moment · Toutes spécialités incluses
  </div>
  <a href="https://buy.stripe.com/9B63cvb3G8kZ5cGfHwb3q01" target="_blank"
     style="background:#3b82f6;color:white;padding:12px 32px;border-radius:8px;
     text-decoration:none;font-weight:700;font-size:1rem;">
    S'abonner maintenant
  </a>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("ClinIA © 2026 — Dr. Mamadou Lamine TALL, PhD · mamadoulaminetallgithub@gmail.com")
