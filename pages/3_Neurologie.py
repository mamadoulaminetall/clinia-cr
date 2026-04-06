import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.generator import generate_cr_stream
from core.pdf_export import generate_pdf

st.set_page_config(page_title="Neuro CR — ClinIA", page_icon="🧠", layout="wide")
st.title("🧠 Compte-Rendu Neurologique")

cr_type = st.selectbox("Type de document", [
    "Consultation neurologique",
    "Compte-rendu AVC / AIT",
    "Compte-rendu épilepsie",
    "Lettre de sortie neurologie"
])

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    patient = st.text_input("Nom / Prénom du patient")
    age = st.text_input("Âge / Sexe", placeholder="ex: 58 ans, homme")
    medecin = st.text_input("Dr. (votre nom)")
    motif = st.text_area("Motif de consultation / hospitalisation", height=80,
                         placeholder="ex: Déficit moteur hémicorps droit brutal, aphasie de 2h...")
    atcd = st.text_area("Antécédents", height=80,
                        placeholder="ex: HTA, FA sous AOD, AIT en 2022...")
    traitement = st.text_area("Traitement habituel", height=60,
                              placeholder="ex: Apixaban 5mg x2, Amlodipine 5mg...")

with col2:
    debut = st.text_input("Heure de début des symptômes", placeholder="ex: 14h30, vu à 16h15")
    examen = st.text_area("Examen neurologique", height=100,
                          placeholder="ex: NIHSS 8, déficit moteur MS droit 3/5, aphasie de Broca modérée, pas de paralysie faciale...")
    imagerie = st.text_area("Imagerie cérébrale", height=80,
                             placeholder="ex: IRM: hypersignal DWI capsule interne gauche 15mm, Angio-IRM: occlusion M1 gauche")
    bio = st.text_area("Biologie / ECG", height=60,
                       placeholder="ex: INR 1.1, Troponine neg, ECG: FA, GB 9.2, CRP <5")
    traitement_aigu = st.text_area("Traitement réalisé / décision thérapeutique", height=80,
                                    placeholder="ex: Thrombolyse IV alteplase 0.9mg/kg réalisée à 16h45, thrombectomie discutée...")

st.markdown("---")
if st.button("🤖 Générer le compte-rendu", type="primary", use_container_width=True):
    fields = {
        "Patient": f"{patient}, {age}" if patient else age,
        "Médecin": medecin,
        "Motif": motif,
        "Antécédents": atcd,
        "Traitement habituel": traitement,
        "Heure début symptômes": debut,
        "Examen neurologique": examen,
        "Imagerie cérébrale": imagerie,
        "Biologie / ECG": bio,
        "Traitement / décision": traitement_aigu
    }

    st.markdown("### Compte-rendu généré")
    cr_placeholder = st.empty()
    cr_text = ""

    with st.spinner("Rédaction en cours..."):
        for chunk in generate_cr_stream("Neurologie", cr_type, fields):
            cr_text += chunk
            cr_placeholder.markdown(
                f'<div style="background:#1e293b;border-radius:12px;padding:20px;'
                f'border-left:4px solid #8b5cf6;white-space:pre-wrap;font-family:monospace;'
                f'font-size:0.9rem;line-height:1.6">{cr_text}</div>',
                unsafe_allow_html=True
            )

    st.session_state["last_cr"] = cr_text
    st.session_state["last_patient"] = patient
    st.session_state["last_medecin"] = medecin
    st.session_state["last_specialty"] = f"Neurologie — {cr_type}"

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
            specialty=st.session_state.get("last_specialty", "Neurologie")
        )
        st.download_button(
            label="⬇️ Télécharger PDF",
            data=pdf_bytes,
            file_name=f"CR_Neuro_{st.session_state.get('last_patient','patient').replace(' ','_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.markdown("---")
st.caption("ClinIA © 2026 — Dr. Mamadou Lamine TALL, PhD · mamadoulaminetallgithub@gmail.com")
