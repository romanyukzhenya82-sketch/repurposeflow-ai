import streamlit as st
from groq import Groq
import json

st.set_page_config(page_title="RepurposeFlow AI", page_icon="🔄", layout="wide")
st.title("🔄 RepurposeFlow AI")
st.subheader("Один текст → 12 платформ за 30 секунд")

api_key = st.text_input("Вставь свой Groq API Key (бесплатно на groq.com)", type="password", help="Ключ хранится только в твоей сессии")

if not api_key:
    st.info("Без ключа не работает. Получи бесплатно на https://console.groq.com")
    st.stop()

client = Groq(api_key=api_key)

content = st.text_area("Вставь исходный текст (статья, транскрипт, идея...)", height=300)

platforms = st.multiselect(
    "Выбери платформы",
    ["X (Twitter thread)", "LinkedIn post", "Instagram carousel caption", "TikTok script", "YouTube Shorts script", 
     "Newsletter email", "Pinterest pin description", "Facebook post", "Reddit thread", "Threads post", 
     "SEO title + meta", "Image prompt for Midjourney/Flux"],
    default=["X (Twitter thread)", "LinkedIn post", "Instagram carousel caption"]
)

if st.button("🚀 Репурпозить", type="primary"):
    with st.spinner("Генерирую контент..."):
        prompt = f"""Ты лучший контент-стратег 2026 года. Возьми этот текст и создай оптимизированный контент под каждую платформу из списка: {platforms}.
        Текст: {content}
        Для каждой платформы верни:
        - Заголовок/хук
        - Основной текст (с эмодзи и призывами)
        - Хэштеги (3-5)
        - CTA
        Ответ строго в JSON: {{"platform1": {{"hook": "...", "text": "...", ...}}}}
        """
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",  # или mixtral-8x7b-32768
            temperature=0.7,
            max_tokens=4000
        )
        
        try:
            result = json.loads(chat_completion.choices[0].message.content)
            for platform, data in result.items():
                with st.expander(f"✅ {platform}"):
                    st.markdown(f"**Хук:** {data.get('hook', '')}")
                    st.markdown(data.get('text', ''))
                    st.caption(f"Хэштеги: {' '.join(data.get('hashtags', []))}")
                    st.caption(f"CTA: {data.get('cta', '')}")
        except:
            st.error("Ошибка парсинга JSON. Попробуй ещё раз или смени модель.")

st.caption("RepurposeFlow AI v0.1 • Монетизация через Stripe после 5 бесплатных использований")