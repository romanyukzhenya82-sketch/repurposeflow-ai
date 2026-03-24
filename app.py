import streamlit as st
from groq import Groq
import json
from datetime import datetime, date

st.set_page_config(page_title="RepurposeFlow AI", page_icon="🔄", layout="wide")

# === СТИЛЬ ===
st.markdown("""
<style>
    .main {background-color: #0e1117;}
    .stButton>button {width: 100%; height: 3.2em; font-size: 1.1em;}
    .result-box {background-color: #1e2937; padding: 20px; border-radius: 12px; margin: 15px 0;}
</style>
""", unsafe_allow_html=True)

st.title("🔄 RepurposeFlow AI")
st.subheader("Один текст → 12 платформ за 30 секунд")
st.caption("Экономь 4–6 часов в неделю на контенте")

# Инициализация счётчика
if 'usage_count' not in st.session_state:
    st.session_state.usage_count = 0
if 'last_date' not in st.session_state:
    st.session_state.last_date = str(date.today())

# Сброс счётчика при новом дне
if st.session_state.last_date != str(date.today()):
    st.session_state.usage_count = 0
    st.session_state.last_date = str(date.today())

api_key = st.text_input("Вставь свой Groq API Key (бесплатно на groq.com)", type="password")

if not api_key:
    st.info("🔑 Без ключа приложение не работает. Получи бесплатно → https://console.groq.com")
    st.stop()

client = Groq(api_key=api_key)

content = st.text_area("Вставь исходный текст (статья, транскрипт подкаста, заметка, идея...)", height=250)

platforms = ["X (Twitter thread)", "LinkedIn post", "Instagram carousel", "TikTok script", 
             "YouTube Shorts script", "Newsletter email", "Pinterest description", 
             "Facebook post", "Reddit thread", "Threads post", "SEO title + meta", 
             "Prompt для Flux/Midjourney"]

selected = st.multiselect("Выбери платформы (можно все)", platforms, default=platforms[:5])

col1, col2 = st.columns([3,1])
with col1:
    if st.button("🚀 Репурпозить контент", type="primary", use_container_width=True):
        if st.session_state.usage_count >= 5:
            st.error("🎯 Ты использовал 5 бесплатных репурпозов сегодня. Купи unlimited:")
            st.markdown("[**Купить за $19/мес — Unlimited + история**](https://buy.stripe.com/test_xxx)", unsafe_allow_html=True)
        else:
            with st.spinner("Генерирую контент с помощью Groq..."):
                prompt = f"""Ты — лучший контент-маркетолог 2026 года. 
                Возьми текст ниже и создай оптимизированный контент под каждую платформу из списка: {selected}.
                Текст: {content}
                
                Для каждой платформы верни строго JSON с полями:
                hook, text, hashtags (список 3-6), cta
                
                Ответ только JSON, без объяснений.
                """

                try:
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                        temperature=0.75,
                        max_tokens=6000
                    )
                    result = json.loads(chat_completion.choices[0].message.content.strip())
                    
                    st.session_state.usage_count += 1
                    
                    st.success(f"✅ Готово! Использовано сегодня: {st.session_state.usage_count}/5")
                    
                    for platform, data in result.items():
                        with st.expander(f"📌 {platform}", expanded=True):
                            st.markdown(f"**Хук:** {data.get('hook', '')}")
                            st.markdown(data.get('text', ''))
                            if data.get('hashtags'):
                                st.caption("Хэштеги: " + " ".join(data.get('hashtags', [])))
                            if data.get('cta'):
                                st.caption(f"CTA: {data.get('cta')}")
                            st.button("📋 Скопировать", key=f"copy_{platform}")
                            
                except Exception as e:
                    st.error(f"Ошибка: {str(e)}")

with col2:
    st.metric("Сегодня использовано", f"{st.session_state.usage_count}/5")

st.divider()
st.markdown("**После 5 бесплатных использований — $19/мес за безлимит + сохранение истории.**")
st.markdown("[Купить подписку →](https://buy.stripe.com/test_xxx)  ← заменим на реальную ссылку после настройки Stripe")

st.caption("RepurposeFlow AI v0.2 • Работает на Groq • Запущен 24 марта 2026")
