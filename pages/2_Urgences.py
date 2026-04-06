import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.generator import generate_cr_stream
from core.pdf_export import generate_pdf

st.set_page_config(page_title="Urgences CR — ClinIA", page_icon="🚨", layout="wide")
st.title("🚨 Compte-Rendu Urgences")

cr_type = st.selectbox("Type de document", [
    "Lettre de passage aux urgences",
    "Compte-rendu médical urgences",
    "Lettre de sortie des urgences"
])

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    patient = st.text_input("Nom / Prénom du patient")
    age = st.text_input("Âge / Sexe", placeholder="ex: 45 ans, femme")
    medecin = st.text_input("Dr. (votre nom)")
    motif = st.text_area("Motif de venue / circonstances", height=80,
                         placeholder="ex: Douleur abdominale aiguë depuis 6h, fièvre à 38.8°C...")
    atcd = st.text_area("Antécédents", height=80,
                        placeholder="ex: Appendicectomie 2010, pas d'allergie connue...")
    traitement = st.text_area("Traitement habituel", height=60,
                              placeholder="ex: Aucun / Contraception orale...")

with col2:
    constantes = st.text_area("Constantes à l'arrivée", height=80,
                               placeholder="ex: TA 110/70, FC 102/min, T° 38.9°C, SpO2 98%, FR 18/min, Glasgow 15")
    examen = st.text_area("Examen clinique", height=100,
                          placeholder="ex: Abdomen souple, douleur en FID, défense localisée, pas de masse...")
    bilan = st.text_area("Bilan complémentaire", height=80,
                         placeholder="ex: NFS: GB 14.2G/L, CRP 85, Echo abdo: épanchement FID, Scanner: appendicite")
    scores_urgences = st.text_area("Scores (qSOFA, Glasgow...)", height=50,
                                   placeholder="ex: qSOFA 1, Glasgow 15")
    orientation = st.text_area("Orientation / décision", height=60,
                                placeholder="ex: Hospitalisation en chirurgie viscérale pour appendicectomie...")

st.markdown("---")
if st.button("🤖 Générer le compte-rendu", type="primary", use_container_width=True):
    fields = {
        "Patient": f"{patient}, {age}" if patient else age,
        "Médecin": medecin,
        "Motif de venue": motif,
        "Antécédents": atcd,
        "Traitement habituel": traitement,
        "Constantes à l'arrivée": constantes,
        "Examen clinique": examen,
        "Bilan complémentaire": bilan,
        "Scores": scores_urgences,
        "Orientation et décision": orientation
    }

    st.markdown("### Compte-rendu généré")
    cr_placeholder = st.empty()
    cr_text = ""

    with st.spinner("Rédaction en cours..."):
        for chunk in generate_cr_stream("Médecine d'Urgence", cr_type, fields):
            cr_text += chunk
            cr_placeholder.markdown(
                f'<div style="background:#1e293b;border-radius:12px;padding:20px;'
                f'border-left:4px solid #ef4444;white-space:pre-wrap;font-family:monospace;'
                f'font-size:0.9rem;line-height:1.6">{cr_text}</div>',
                unsafe_allow_html=True
            )

    st.session_state["last_cr"] = cr_text
    st.session_state["last_patient"] = patient
    st.session_state["last_medecin"] = medecin
    st.session_state["last_specialty"] = f"Urgences — {cr_type}"

if "last_cr" in st.session_state and st.session_state["last_cr"]:
    st.markdown("---")
    col_copy, col_pdf = st.columns(2)
    with col_copy:
        st.text_area("📋 Copier le texte", st.session_state["last_cr"], height=200)
    with col_pdf:
        pdf_bytes = generate_pdf(
            st.session_state["last_cr"],
            patient_name=st.session_state.get("last_patient", ""),
            doctor_name=st.session_state.get("last_medecin", ""),
            specialty=st.session_state.get("last_specialty", "Urgences")
        )
        st.download_button(
            label="⬇️ Télécharger PDF",
            data=pdf_bytes,
            file_name=f"CR_Urgences_{st.session_state.get('last_patient','patient').replace(' ','_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.markdown("---")
st.caption("ClinIA © 2026 — Dr. Mamadou Lamine TALL, PhD · mamadoulaminetallgithub@gmail.com")
