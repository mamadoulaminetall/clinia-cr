import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.generator import generate_cr_stream
from core.pdf_export import generate_pdf

st.set_page_config(page_title="Cardio CR — ClinIA", page_icon="❤️", layout="wide")
st.title("❤️ Compte-Rendu Cardiologique")

cr_type = st.selectbox("Type de document", [
    "Consultation cardiologique",
    "Compte-rendu d'hospitalisation",
    "Lettre de sortie",
    "Compte-rendu d'échocardiographie"
])

st.markdown("---")
st.markdown("### Informations patient et données cliniques")

col1, col2 = st.columns(2)
with col1:
    patient = st.text_input("Nom / Prénom du patient")
    age = st.text_input("Âge / Sexe", placeholder="ex: 67 ans, homme")
    medecin = st.text_input("Dr. (votre nom)", placeholder="ex: Dr. Martin")
    motif = st.text_area("Motif de consultation / hospitalisation", height=80,
                         placeholder="ex: Douleur thoracique atypique, palpitations...")
    atcd = st.text_area("Antécédents", height=80,
                        placeholder="ex: HTA, diabète type 2, tabagisme sevré...")
    traitement = st.text_area("Traitement habituel", height=80,
                              placeholder="ex: Ramipril 5mg, Bisoprolol 5mg, Metformine 1g...")

with col2:
    examen = st.text_area("Examen clinique", height=100,
                          placeholder="ex: TA 135/85, FC 78/min régulière, pas de souffle, pas d'œdème...")
    ecg = st.text_area("ECG", height=60,
                       placeholder="ex: RS 75/min, axe normal, pas de trouble de repolarisation...")
    echo = st.text_area("Échocardiographie (si disponible)", height=60,
                        placeholder="ex: FEVG 55%, pas de valvulopathie significative, VG non dilaté...")
    bio = st.text_area("Biologie", height=60,
                       placeholder="ex: Troponine 0.02, BNP 85, INR 2.3, NFS normale...")
    scores = st.text_area("Scores calculés (optionnel)", height=60,
                          placeholder="ex: CHA2DS2-VASc = 3 → anticoagulation indiquée")
    conclusion_libre = st.text_area("Éléments à inclure en conclusion / CAT", height=80,
                                    placeholder="ex: Majoration bisoprolol, contrôle TA à 1 mois, ETT à 6 mois...")

st.markdown("---")

if st.button("🤖 Générer le compte-rendu", type="primary", use_container_width=True):
    fields = {
        "Patient": f"{patient}, {age}" if patient else age,
        "Médecin": medecin,
        "Motif": motif,
        "Antécédents": atcd,
        "Traitement habituel": traitement,
        "Examen clinique": examen,
        "ECG": ecg,
        "Échocardiographie": echo,
        "Biologie": bio,
        "Scores cliniques": scores,
        "Conclusion / CAT souhaitée": conclusion_libre
    }

    st.markdown("### Compte-rendu généré")
    cr_placeholder = st.empty()
    cr_text = ""

    with st.spinner("Rédaction en cours..."):
        for chunk in generate_cr_stream("Cardiologie", cr_type, fields):
            cr_text += chunk
            cr_placeholder.markdown(
                f'<div style="background:#1e293b;border-radius:12px;padding:20px;'
                f'border-left:4px solid #3b82f6;white-space:pre-wrap;font-family:monospace;'
                f'font-size:0.9rem;line-height:1.6">{cr_text}</div>',
                unsafe_allow_html=True
            )

    st.session_state["last_cr"] = cr_text
    st.session_state["last_patient"] = patient
    st.session_state["last_medecin"] = medecin
    st.session_state["last_specialty"] = f"Cardiologie — {cr_type}"

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
            specialty=st.session_state.get("last_specialty", "Cardiologie")
        )
        st.download_button(
            label="⬇️ Télécharger PDF",
            data=pdf_bytes,
            file_name=f"CR_Cardio_{st.session_state.get('last_patient','patient').replace(' ','_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.markdown("---")
st.caption("ClinIA © 2026 — Dr. Mamadou Lamine TALL, PhD · mamadoulaminetallgithub@gmail.com")
