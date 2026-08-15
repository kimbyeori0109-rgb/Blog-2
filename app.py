import streamlit as st
from openai import OpenAI

# 1. UI 설정
st.set_page_config(page_title="AI 블로그 어시스턴트", page_icon="📝")
st.title("📝 나만의 AI 블로그 어시스턴트")

# 2. OpenAI 키만 입력하도록 수정
with st.sidebar:
    st.header("🔑 API 키 설정")
    openai_api_key = st.text_input("OpenAI API Key", type="password")

# 3. 핵심 함수 (OpenAI만 사용)
def generate_blog_draft(keyword, api_key):
    client = OpenAI(api_key=api_key)
    system_prompt = """
    당신은 세계여행, 국내여행, 맛집 전문 인플루언서입니다.
    사용자가 입력한 주제에 대해 매거진 스타일의 정보성 글을 작성해 주세요.
    1. 비교 분석과 숫자 활용
    2. 핵심 Q&A 2가지 포함
    3. 인스타 캡션과 해시태그 15개 작성
    4. 친근하고 전문적인 어투 사용
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"주제: {keyword}\n\n위 주제로 포스팅 초안을 작성해 줘."}
        ]
    )
    return response.choices[0].message.content

# 4. 메인 화면
target_keyword = st.text_input("어떤 주제로 글을 쓰실 건가요?", placeholder="예: 오사카 3박4일 코스")

if st.button("🚀 블로그 초안 생성하기"):
    if not openai_api_key:
        st.error("OpenAI API 키를 먼저 입력해 주세요.")
    elif not target_keyword:
        st.warning("주제를 입력해 주세요.")
    else:
        with st.spinner("글을 작성 중입니다... ✍️"):
            draft = generate_blog_draft(target_keyword, openai_api_key)
            st.markdown("---")
            st.markdown(draft)
