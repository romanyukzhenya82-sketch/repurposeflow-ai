import streamlit as st
from groq import Groq
import json
from datetime import date

st.set_page_config(page_title="RepurposeFlow AI", page_icon="🔄", layout="wide")

# Стиль
st.markdown("""
<style>
    .main {background-color: #0e1117; color: #fff;}
    .stButton>button {width: 100%; height: 3.2em; font-size: 1.1em; font-weight: bold;}
    .success {background-color: #1e2937; padding: 20px; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

st.title("🔄 RepurposeFlow AI")
st.subheader("Один текст → 12 платформ за 30 секунд")
st.caption("Экономь 4–6 часов в неделю • Для солопренёров и малого бизнеса")

# Счётчик бесплатных использований
if 'usage_count' not in st.session_state:
    st.session_state.usage_count = 0
if 'last_date' not in st.session_state:
    st.session_state.last_date = str(date.today())

if st.session_state.last_date != str(date.today()):
    st.session_state.usage_count = 0
    st.session_state.last_date = str(date.today())

api_key = st.text_input("🔑 Вставь свой Groq API Key (бесплатно на groq.com)", type="password")

if not api_key:
    st.info("Без ключа не работает. Получи бесплатно → https://console.groq.com")
    st.stop()

client = Groq(api_key=api_key)

content = st.text_area("Вставь исходный текст (статья, транскрипт, заметка...)", height=300)

platforms = ["X (Twitter thread)", "LinkedIn post", "Instagram carousel caption", "TikTok script", 
             "YouTube Shorts script", "Newsletter email", "Pinterest pin description", 
             "Facebook post", "Reddit thread", "Threads post", "SEO title + meta", 
             "Prompt для Flux/Midjourney"]

selected = st.multiselect("Выбери платформы", platforms, default=platforms[:6])

if st.button("🚀 Репурпозить контент", type="primary", use_container_width=True):
    if st.session_state.usage_count >= 5:
        st.error("🎯 Лимит бесплатных использований исчерпан (5 в день)")
        st.markdown("### 💰 Перейди на Unlimited всего за $19/мес")
        st.markdown(f'[**Купить подписку сейчас → Безлимит + история**]({ "https://buy.stripe.com/bJeeVdbdi9T1fHheZ9aVa00" })', unsafe_allow_html=True)
    else:
        with st.spinner("Генерирую мощный контент через Groq Llama-3.3-70B..."):
            prompt = f"""Ты — лучший контент-стратег 2026. 
            Исходный текст: {content}
            Создай оптимизированный контент для платформ: {selected}.
            Верни ТОЛЬКО JSON:
            {{"platform": {{"hook": "...", "text": "...", "hashtags": [".."], "cta": "..."}}}}
            """

            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.75,
                    max_tokens=6500
                )
                result = json.loads(response.choices[0].message.content.strip())
                
                st.session_state.usage_count += 1
                st.success(f"✅ Готово! Сегодня: {st.session_state.usage_count}/5 бесплатных")

                for plat, data in result.items():
                    with st.expander(f"📌 {plat}", expanded=True):
                        st.markdown(f"**Хук:** {data.get('hook','')}")
                        st.markdown(data.get('text',''))
                        st.caption(f"Хэштеги: {' '.join(data.get('hashtags',[]))}")
                        st.caption(f"CTA: {data.get('cta','')}")
                        if st.button("📋 Скопировать", key=plat):
                            st.toast("Скопировано!")

            except Exception as e:
                st.error(f"Ошибка: {e}")

st.metric("Бесплатных сегодня", f"{st.session_state.usage_count}/5")

st.divider()
st.markdown("**После лимита — Unlimited за $19/мес**")
st.markdown(f'[💰 Купить подписку прямо сейчас →](https://buy.stripe.com/bJeeVdbdi9T1fHheZ9aVa00)', unsafe_allow_html=True)
st.caption("RepurposeFlow AI v0.3 • Groq-powered • Запущен 24 марта 2026")
