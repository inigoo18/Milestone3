import streamlit as st
from datetime import datetime, timedelta
import calendar


# --- Load questions from file ---
def load_questions_from_txt(filepath="./questions.txt"):
    open_questions = []
    likert_questions = []
    ordering_question = None

    with open(filepath, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("::")
            if len(parts) < 4:
                continue

            qtype, qid, question, param = parts[0], parts[1], parts[2], parts[3]
            if qtype == "OPEN":
                open_questions.append((qid, question, param))
            elif qtype == "LIKERT":
                likert_questions.append((qid, question, param))
            elif qtype == "ORDERING":
                ordering_question = (qid, question, param.split(","))
    return open_questions, likert_questions, ordering_question

# --- Open-ended questions ---
def render_open_ended_questions(questions, start_number=1):
    answers = []
    with st.expander("✏️ Preguntas Abiertas"):
        for i, (qid, label, help_text) in enumerate(questions, start=start_number):
            st.markdown(f"**{i}.** {label}")
            ans = st.text_area("", help=help_text, height=100, key=f"open_{qid}")
            answers.append((qid, ans))
    return answers, start_number + len(questions)

# --- Likert scale questions ---
def render_likert_questions(questions, start_number=1):
    responses = []
    with st.expander("📊 Escala de Valoración"):
        for i, (qid, question, range_str) in enumerate(questions, start=start_number):
            scale_min, scale_max = map(int, range_str.split("-"))
            st.markdown(f"**{i}.** {question}")
            res = st.slider("", scale_min, scale_max, key=f"likert_{qid}")
            responses.append((qid, question, res))
    return responses, start_number + len(questions)

# --- Orderable questions via dropdowns ---
def render_orderable_questions(title, options, start_number=1):
    ranked = []
    remaining = options.copy()
    with st.expander("🔃 Ordena según tu preferencia"):
        st.markdown(f"**{start_number}.** {title}")
        for i in range(1, len(options) + 1):
            choice = st.selectbox(f"{i}º:", ["--"] + remaining, key=f"order_{i}")
            ranked.append(choice)
            if choice in remaining:
                remaining.remove(choice)
    return [item for item in ranked if item != "--"], start_number + 1

# --- Calendar rendering ---
def render_meeting_calendar(kol_meeting):
    st.markdown("### 📅 Calendario")
    year, month = kol_meeting.year, kol_meeting.month
    cal = calendar.Calendar(firstweekday=0)
    days = list(cal.itermonthdays(year, month))

    html_calendar = """
    <style>
      .calendar { display: grid; grid-template-columns: repeat(7,1fr); gap:5px; }
      .day-header { font-weight:bold; text-align:center; color:#444; }
      .day { text-align:center; padding:6px 0; border-radius:4px; background:#eee; }
      .meeting-day { background:#FFDDDD; color:red; font-weight:bold; border:1px solid red; }
      .empty-day { background:transparent; }
    </style>
    <div class="calendar">
      <div class="day-header">Sun</div><div class="day-header">Mon</div>
      <div class="day-header">Tue</div><div class="day-header">Wed</div>
      <div class="day-header">Thu</div><div class="day-header">Fri</div>
      <div class="day-header">Sat</div>
    """
    for day in days:
        if day == 0:
            html_calendar += '<div class="empty-day"></div>'
        elif day == kol_meeting.day:
            html_calendar += f'<div class="meeting-day">{day}</div>'
        else:
            html_calendar += f'<div class="day">{day}</div>'
    html_calendar += "</div>"

    st.markdown(f"#### {kol_meeting.strftime('%B %Y')}", unsafe_allow_html=True)
    st.markdown(html_calendar, unsafe_allow_html=True)

# --- Main interface ---
def render_user_view():
    st.markdown("## 🙋 Cuestionario Clínico")

    # Get next Monday
    kol_meeting = datetime.today()
    while kol_meeting.weekday() != 0:
        kol_meeting += timedelta(days=1)

    st.markdown(f"""
    <div style="
      margin:20px 0; padding:15px; background:linear-gradient(135deg,#4F9DFF,#0047AB);
      color:white; text-align:center; font-size:18px; border-radius:10px;">
      📢 Próxima sesión KOL: <strong>{kol_meeting.strftime('%A, %d de %B %Y')}</strong>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        open_qs, likert_qs, ordering_q = load_questions_from_txt()

        # Render questions with global numbering
        open_answers, next_number = render_open_ended_questions(open_qs, start_number=1)
        likert_responses, next_number = render_likert_questions(likert_qs, start_number=next_number)
        ordered, next_number = render_orderable_questions(ordering_q[1], ordering_q[2], start_number=next_number) if ordering_q else ([], next_number)

        if st.button("🚀 Enviar respuestas"):
            st.success("✅ ¡Gracias por compartir tus respuestas!")
            st.markdown("### 🧾 Resumen:")
            for qid, ans in open_answers:
                question_text = next(q[1] for q in open_qs if q[0] == qid)
                st.markdown(f"- **{question_text}**: {ans}")
            for qid, question, score in likert_responses:
                st.markdown(f"- **{question}**: {score}/5")
            if ordered:
                st.markdown(f"- **{ordering_q[1]}**: {', '.join(ordered)}")

    with col2:
        render_meeting_calendar(kol_meeting)

# --- Run the app ---
if __name__ == "__main__":
    render_user_view()
