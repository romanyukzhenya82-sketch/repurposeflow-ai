import streamlit as st
from groq import Groq
import json
from datetime import date

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
st.caption("Экономь 4–6 часов в неделю на контенте для малого бизнеса")

# Инициализация счётчика
if 'usage_count' not in st.session_state:
    st.session_state.usage_count = 0
if 'last_date' not in st.session_state:
    st.session_state.last_date = str(date.today())

# Сброс счётчика при новом дне
if st.session_state.last_date != str(date.today()):
    st.session_state.usage_count = 0
    st.session_state.last_date = str(date.today())

api_key = st.text_input("🔑 Вставь свой Groq API Key (получи бесплатно на groq.com)", type="password")

if not api_key:
    st.info("Без ключа приложение не работает. Получи бесплатно → https://console.groq.com")
    st.stop()

client = Groq(api_key=api_key)

content = st.text_area("Вставь исходный текст (статья, транскрипт, заметка, идея...)", height=280)

platforms = ["X (Twitter thread)", "LinkedIn post", "Instagram carousel caption", "TikTok script", 
             "YouTube Shorts script", "Newsletter email", "Pinterest pin description", 
             "Facebook post", "Reddit thread", "Threads post", "SEO title + meta description", 
             "Image prompt для Flux / Midjourney"]

selected_platforms = st.multiselect("Выбери платформы для репурпоза", platforms, default=platforms[:6])

if st.button("🚀 Репурпозить контент", type="primary", use_container_width=True):
    if st.session_state.usage_count >= 5:
        st.error("🎯 Сегодня ты уже использовал 5 бесплатных репурпозов.")
        st.markdown("### 💰 Перейди на Unlimited за $19/мес")
        st.markdown("[Купить подписку сейчас →](https://buy.stripe.com/test_xxx)", unsafe_allow_html=True)
        st.caption("После оплаты — безлимит + сохранение всей истории")
    else:
        with st.spinner("Генерирую контент с помощью Groq Llama-3.3-70B..."):
            prompt = f"""Ты — топовый контент-стратег 2026 года. 
            Возьми этот исходный текст и создай готовый контент под каждую платформу из списка: {selected_platforms}.
            
            Исходный текст: {content}
            
            Для каждой платформы верни **только JSON** в формате:
            {{
              "platform_name": {{
                "hook": "сильный первый абзац",
                "text": "полный текст поста с эмодзи",
                "hashtags": ["tag1", "tag2", "tag3"],
                "cta": "призыв к действию"
              }}
            }}
            Ответ строго JSON, без каких-либо дополнительных слов.
            """

            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=6500
                )
                
                raw = chat_completion.choices[0].message.content.strip()
                result = json.loads(raw)
                
                st.session_state.usage_count += 1
                
                st.success(f"✅ Готово! Сегодня использовано: {st.session_state.usage_count}/5 бесплатных")
                
                for platform, data in result.items():
                    with st.expander(f"📌 {platform}", expanded=False):
                        st.markdown(f"**Хук:** {data.get('hook', '')}")
                        st.markdown(data.get('text', ''))
                        if data.get('hashtags'):
                            st.caption("**Хэштеги:** " + " ".join(data.get('hashtags', [])))
                        if data.get('cta'):
                            st.caption(f"**CTA:** {data.get('cta')}")
                        if st.button("📋 Скопировать весь блок", key=platform):
                            st.toast("Скопировано в буфер!")
                            
            except Exception as e:
                st.error(f"Ошибка обработки: {str(e)}. Попробуй сократить текст или сменить модель.")

st.divider()
st.metric("Бесплатных репурпозов сегодня", f"{st.session_state.usage_count}/5")

st.markdown("**После 5 использований — безлимит за $19 в месяц**")
st.markdown("[💰 Купить Unlimited подписку →](https://buy.stripe.com/test_xxx)", unsafe_allow_html=True)

st.caption("RepurposeFlow AI v0.2 • Работает на Groq • Запущен 24 марта 2026")
