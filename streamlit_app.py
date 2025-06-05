import streamlit as st
import openai
from parse_hh import get_html, extract_vacancy_data, extract_resume_data

# Настройки страницы
st.set_page_config(page_title="Сравнение резюме и вакансии", layout="centered")
st.title("🔍 Анализ соответствия кандидата вакансии")

# Ввод двух ссылок
job_url = st.text_input("🔗 Вставь ссылку на вакансию (hh.ru)")
resume_url = st.text_input("🔗 Вставь ссылку на резюме (hh.ru)")

# OpenAI API (вставь свой ключ)
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

# Кнопка запуска
if st.button("🚀 Оценить соответствие"):
    if not job_url or not resume_url:
        st.warning("❗ Вставь обе ссылки на hh.ru")
    else:
        try:
            with st.spinner("📥 Получаем данные с hh.ru..."):
                job_html = get_html(job_url).text
                resume_html = get_html(resume_url).text

                job_description = extract_vacancy_data(job_html)
                resume_text = extract_resume_data(resume_html)

            # Показываем обе части
            st.subheader("📄 Вакансия")
            st.markdown(job_description)

            st.subheader("👤 Резюме")
            st.markdown(resume_text)

            with st.spinner("🤖 GPT анализирует..."):
                system_prompt = """
                Ты HR-эксперт. Проанализируй, насколько кандидат подходит под вакансию.
                Дай:
                1. Краткий разбор (сильные/слабые стороны)
                2. Отдельно оцени качество описания опыта в резюме
                3. Итоговая оценка соответствия от 1 до 10
                """

                user_prompt = f"Вакансия:\n{job_description}\n\nРезюме:\n{resume_text}"

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=1000,
                    temperature=0
                )
                result = response.choices[0].message.content

            st.success("✅ Анализ готов")
            st.markdown(result)

        except Exception as e:
            st.error(f"❌ Произошла ошибка: {e}")
