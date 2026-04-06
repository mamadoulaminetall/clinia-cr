import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.generator import generate_cr_stream
from core.pdf_export import generate_pdf

st.set_page_config(page_title="Pneumo CR — ClinIA", page_icon="🫁", layout="wide")
st.title("🫁 Compte-Rendu Pneumologique")

cr_type = st.selectbox("Type de document", [
    "Consultation pneumologique",
    "Compte-rendu d'hospitalisation",
    "Lettre de sortie pneumologie",
    "Compte-rendu EFR"
])

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    patient = st.text_input("Nom / Prénom du patient")
    age = st.text_input("Âge / Sexe", placeholder="ex: 62 ans, homme")
    medecin = st.text_input("Dr. (votre nom)")
    motif = st.text_area("Motif de consultation / hospitalisation", height=80,
                         placeholder="ex: Dyspnée progressive stade III mMRC, toux chronique productive...")
    atcd = st.text_area("Antécédents", height=80,
                        placeholder="ex: Tabagisme 40PA sevré, BPCO stade GOLD III, HTA...")
    traitement = st.text_area("Traitement habituel", height=60,
                              placeholder="ex: Tiotropium 18µg/j, Formotérol/Budésonide, Salbutamol si besoin...")

with col2:
    examen = st.text_area("Examen clinique", height=80,
                          placeholder="ex: SpO2 91% AA, FR 22/min, distension thoracique, sibilants diffus, pas de cyanose...")
    efr = st.text_area("EFR / Spirométrie", height=80,
                       placeholder="ex: VEMS 48%, VEMS/CVF 58%, CPT 125%, DLCO 52%...")
    imagerie = st.text_area("Imagerie (Radio / Scanner)", height=60,
                             placeholder="ex: TDM: emphysème panlobulaire, pas de nodule, pas d'épanchement...")
    bio = st.text_area("Biologie / GDS", height=60,
                       placeholder="ex: GDS: pH 7.38, PaO2 58mmHg, PaCO2 46mmHg, SaO2 90%...")
    csi = st.text_area("Conclusion / CAT", height=80,
                       placeholder="ex: Majoration traitement inhalé, oxygénothérapie nocturne à discuter, réhabilitation respiratoire...")

st.markdown("---")
if st.button("🤖 Générer le compte-rendu", type="primary", use_container_width=True):
    fields = {
        "Patient": f"{patient}, {age}" if patient else age,
        "Médecin": medecin,
        "Motif": motif,
        "Antécédents": atcd,
        "Traitement habituel": traitement,
        "Examen clinique": examen,
        "EFR / Spirométrie": efr,
        "Imagerie": imagerie,
        "Biologie / GDS": bio,
        "Conclusion / CAT": csi
    }

    st.markdown("### Compte-rendu généré")
    cr_placeholder = st.empty()
    cr_text = ""

    with st.spinner("Rédaction en cours..."):
        for chunk in generate_cr_stream("Pneumologie", cr_type, fields):
            cr_text += chunk
            cr_placeholder.markdown(
                f'<div style="background:#1e293b;border-radius:12px;padding:20px;'
                f'border-left:4px solid #06b6d4;white-space:pre-wrap;font-family:monospace;'
                f'font-size:0.9rem;line-height:1.6">{cr_text}</div>',
                unsafe_allow_html=True
            )

    st.session_state["last_cr"] = cr_text
    st.session_state["last_patient"] = patient
    st.session_state["last_medecin"] = medecin
    st.session_state["last_specialty"] = f"Pneumologie — {cr_type}"

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
            specialty=st.session_state.get("last_specialty", "Pneumologie")
        )
        st.download_button(
            label="⬇️ Télécharger PDF",
            data=pdf_bytes,
            file_name=f"CR_Pneumo_{st.session_state.get('last_patient','patient').replace(' ','_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.markdown("---")
st.caption("ClinIA © 2026 — Dr. Mamadou Lamine TALL, PhD · mamadoulaminetallgithub@gmail.com")
