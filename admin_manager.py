import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# ----------- Load questions from questions.txt -----------
def parse_questions_file(path="questions.txt"):
    questions = {
        "OPEN": {},
        "LIKERT": {},
        "ORDERING": {}
    }
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("::")
                if len(parts) < 4:
                    continue
                q_type, q_id, q_text, q_desc = parts[0], parts[1], parts[2], parts[3]
                if q_type in questions:
                    questions[q_type][q_id] = {"text": q_text, "description": q_desc}
    except FileNotFoundError:
        st.error("❌ No se encontró el archivo 'questions.txt'.")
    return questions

# ----------- Load answers from answers.txt -----------
def parse_answers_file(path="answers.txt"):
    answers_by_type = {
        "OPEN": {},
        "LIKERT": {},
        "ORDERING": {}
    }
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("::")
                if len(parts) < 4:
                    continue
                q_type, q_id, name, response = parts[0], parts[1], parts[2], "::".join(parts[3:])
                if q_type not in answers_by_type:
                    continue
                if q_id not in answers_by_type[q_type]:
                    answers_by_type[q_type][q_id] = {}
                answers_by_type[q_type][q_id][name] = response
    except FileNotFoundError:
        st.error("❌ No se encontró el archivo 'answers.txt'.")
    return answers_by_type

# ----------- Render Open Questions -----------
def render_open_questions(questions, answers):
    st.markdown("### ✏️ Preguntas Abiertas")
    st.markdown("---")
    for q_id, responses in answers.get("OPEN", {}).items():
        q_data = questions["OPEN"].get(q_id, {"text": f"Pregunta Abierta {q_id}", "description": ""})
        with st.container():
            st.markdown(f"**🔹 {q_data['text']}**")
            if q_data["description"]:
                st.caption(q_data["description"])

            with st.expander("📋 Ver respuestas individuales"):
                for name, answer in responses.items():
                    if name.upper() in ["AI", "AI_FOLLOWUP"]:
                        continue
                    st.markdown(f"""
                    <div style="
                        border-left: 4px solid #4F9DFF;
                        background-color: #f9f9f9;
                        padding: 0.75rem 1rem;
                        margin-bottom: 0.5rem;
                        border-radius: 6px;
                    ">
                        <strong>{name}:</strong><br>{answer}
                    </div>
                    """, unsafe_allow_html=True)

            if "AI" in responses:
                with st.expander("🤖 Resumen generado por IA"):
                    st.info(responses["AI"])
            else:
                with st.expander("🤖 Resumen generado por IA"):
                    st.info("Resumen automático pendiente o generado manualmente.")

            if "AI_FOLLOWUP" in responses:
                with st.expander("🤖 Preguntas y observaciones de seguimiento IA"):
                    st.info(responses["AI_FOLLOWUP"])

            st.markdown("---")

# ----------- Render Likert Questions -----------
def render_likert_questions(questions, answers):
    st.markdown("### 📊 Preguntas de Escala Likert")
    st.markdown("---")

    for q_id, responses in answers.get("LIKERT", {}).items():
        q_data = questions["LIKERT"].get(q_id, {"text": f"Pregunta Likert {q_id}", "description": ""})
        with st.container():
            st.markdown(f"**🔹 {q_data['text']}**")
            if q_data["description"]:
                st.caption(q_data["description"])

            filtered_responses = {k: v for k, v in responses.items() if k.upper() not in ["AI", "AI_FOLLOWUP"]}

            counts = {i: 0 for i in range(1, 6)}
            for score_str in filtered_responses.values():
                try:
                    score = int(score_str)
                    if 1 <= score <= 5:
                        counts[score] += 1
                except:
                    continue

            fig = go.Figure(data=[go.Bar(
                x=[str(i) for i in range(1, 6)],
                y=[counts[i] for i in range(1, 6)],
                marker_color='royalblue'
            )])
            fig.update_layout(
                title="Distribución de respuestas",
                xaxis_title="Puntaje Likert",
                yaxis_title="Cantidad de respuestas",
                yaxis=dict(dtick=1),
                margin=dict(t=40, b=40)
            )
            st.plotly_chart(fig, use_container_width=True, key=f"likert_chart_{q_id}")

            mean = pd.to_numeric(list(filtered_responses.values()), errors='coerce').mean()
            std = pd.to_numeric(list(filtered_responses.values()), errors='coerce').std()
            st.markdown(f"📈 **Media:** {mean:.2f} &nbsp;&nbsp; | 📉 **Desviación estándar:** {std:.2f}", unsafe_allow_html=True)

            if "AI" in responses:
                with st.expander("🤖 Interpretación IA"):
                    st.info(responses["AI"])
            else:
                with st.expander("🤖 Interpretación IA"):
                    if mean >= 4:
                        st.success("Existe un alto grado de consenso positivo.")
                    elif std >= 1.0:
                        st.warning("Las respuestas muestran variabilidad, podría requerirse discusión adicional.")
                    else:
                        st.info("Se observa una tendencia favorable moderada.")

            if "AI_FOLLOWUP" in responses:
                with st.expander("🤖 Preguntas y observaciones de seguimiento IA"):
                    st.info(responses["AI_FOLLOWUP"])
            st.markdown("---")

# ----------- Render Ordering Questions -----------
def render_ordering_questions(questions, answers):
    st.markdown("### 🔃 Priorización de Síntomas")
    st.markdown("---")

    for q_id, responses in answers.get("ORDERING", {}).items():
        q_data = questions["ORDERING"].get(q_id, {"text": f"Pregunta de Priorización {q_id}", "description": ""})
        st.markdown(f"**🔹 {q_data['text']}**")
        if q_data["description"]:
            st.caption(q_data["description"])

        rankings = [resp.split(",") for name, resp in responses.items() if name.upper() not in ["AI", "AI_FOLLOWUP"]]

        all_items = set()
        for r in rankings:
            all_items.update([item.strip() for item in r])
        all_items = sorted(all_items)

        rank_counts = {item: {str(rank): 0 for rank in range(1, 6)} for item in all_items}

        for ranking in rankings:
            for pos, item in enumerate(ranking, start=1):
                item = item.strip()
                if item in rank_counts and str(pos) in rank_counts[item]:
                    rank_counts[item][str(pos)] += 1

        fig = go.Figure()
        colors = px.colors.sequential.Purples[2:7][::-1]

        for rank in range(1, 6):
            fig.add_trace(go.Bar(
                name=f"Posición {rank}",
                x=all_items,
                y=[rank_counts[item][str(rank)] for item in all_items],
                marker_color=colors[(rank - 1) % len(colors)]
            ))

        fig.update_layout(
            barmode='stack',
            title="Distribución de posiciones asignadas a síntomas",
            xaxis_title="Síntomas",
            yaxis_title="Cantidad de selecciones",
            legend_title="Prioridad asignada (1 siento más alto)",
            margin=dict(t=40, b=100),
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig, use_container_width=True)

        if "AI" in responses:
            with st.expander("🤖 Análisis IA"):
                st.info(responses["AI"])
        else:
            with st.expander("🤖 Análisis IA"):
                st.info(
                    "Los síntomas con menor puntuación promedio son considerados más importantes en general. "
                    "Esto proporciona una visión clara de las prioridades clínicas del grupo."
                )

        if "AI_FOLLOWUP" in responses:
            with st.expander("🤖 Preguntas y observaciones de seguimiento IA"):
                st.info(responses["AI_FOLLOWUP"])

# ----------- Admin View -----------
def render_admin_view():
    questions = parse_questions_file("questions.txt")
    answers = parse_answers_file("answers.txt")

    kol_meeting = datetime.today()
    while kol_meeting.weekday() != 0:
        kol_meeting += timedelta(days=1)

    st.markdown(f"""
    <div style="
        margin-top: 20px;
        padding: 1rem;
        background: linear-gradient(135deg, #4F9DFF, #0047AB);
        color: white;
        text-align: center;
        border-radius: 10px;
        font-size: 18px;">
        📢 Próxima sesión KOL: <strong>{kol_meeting.strftime('%A, %d de %B %Y')}</strong>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🗒️ Resultados del Cuestionario")

    render_open_questions(questions, answers)
    render_likert_questions(questions, answers)
    render_ordering_questions(questions, answers)
