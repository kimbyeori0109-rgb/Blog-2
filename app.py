import streamlit as st
import google.generativeai as genai

# 1. UI 설정
st.set_page_config(page_title="AI 블로그 어시스턴트", page_icon="📝")
st.title("📝 나만의 AI 블로그 어시스턴트 (무료 버전)")

# 2. Gemini 키 입력 (사이드바)
with st.sidebar:
    st.header("🔑 API 키 설정")
    gemini_api_key = st.text_input("Gemini API Key", type="password")

# 3. 핵심 함수 (Google Gemini 최신 모델 사용)
def generate_blog_draft(keyword, api_key):
    genai.configure(api_key=api_key)
    # 구글의 최신 무료 모델로 이름 변경 (1.5 -> 3.5)
    model = genai.GenerativeModel('gemini-3.5-flash')
    
    prompt = f"""
    당신은 세계여행, 국내여행, 맛집 전문 인플루언서입니다.
    사용자가 입력한 주제에 대해 매거진 스타일의 정보성 글을 작성해 주세요.
    1. 비교 분석과 숫자 활용
    2. 핵심 Q&A 2가지 포함
    3. 인스타 캡션과 해시태그 15개 작성
    4. 친근하고 전문적인 어투 사용
    
    주제: {keyword}
    """
    
    response = model.generate_content(prompt)
    return response.text

# 4. 메인 화면
target_keyword = st.text_input("어떤 주제로 글을 쓰실 건가요?", placeholder="예: 오사카 3박4일 코스")

if st.button("🚀 블로그 초안 생성하기", use_container_width=True):
    if not gemini_api_key:
        st.error("Gemini API 키를 먼저 입력해 주세요.")
    elif not target_keyword:
        st.warning("주제를 입력해 주세요.")
    else:
        with st.spinner("AI가 글을 작성 중입니다... ✍️"):
            try:
                draft = generate_blog_draft(target_keyword, gemini_api_key)
                st.markdown("---")
                st.markdown(draft)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
