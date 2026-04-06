import anthropic
import streamlit as st


def get_client():
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return None
    return anthropic.Anthropic(api_key=api_key)


def generate_cr(specialty: str, cr_type: str, fields: dict) -> str:
    client = get_client()
    if not client:
        return "⚠️ Clé API non configurée. Contactez l'administrateur."

    fields_text = "\n".join([f"- {k} : {v}" for k, v in fields.items() if v])

    prompt = f"""Tu es un médecin spécialiste en {specialty} qui rédige un compte-rendu médical professionnel en français.

Type de document : {cr_type}
Spécialité : {specialty}

Données cliniques fournies :
{fields_text}

Rédige un compte-rendu médical complet, structuré et professionnel en français.
Respecte les conventions médicales françaises.
Utilise un style médical formel et précis.
Structure le document avec des sections claires (Motif, Antécédents, Examen clinique, Bilan, Conclusion/Conduite à tenir).
Ne mentionne que les éléments fournis, sans inventer de données.
Si une information manque, écris "non renseigné" plutôt que d'inventer.
Le compte-rendu doit être directement utilisable sans modification majeure."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def generate_cr_stream(specialty: str, cr_type: str, fields: dict):
    client = get_client()
    if not client:
        yield "⚠️ Clé API non configurée."
        return

    fields_text = "\n".join([f"- {k} : {v}" for k, v in fields.items() if v])

    prompt = f"""Tu es un médecin spécialiste en {specialty} qui rédige un compte-rendu médical professionnel en français.

Type de document : {cr_type}
Spécialité : {specialty}

Données cliniques fournies :
{fields_text}

Rédige un compte-rendu médical complet, structuré et professionnel en français.
Respecte les conventions médicales françaises.
Utilise un style médical formel et précis.
Structure avec des sections : Motif de consultation, Antécédents, Traitement habituel, Examen clinique, Bilan complémentaire, Conclusion et conduite à tenir.
Ne mentionne que les éléments fournis. Si une information manque, écris "non renseigné".
Le compte-rendu doit être directement utilisable."""

    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            yield text
