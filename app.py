import streamlit as st
import google.generativeai as genai

# 1. UI 설정
st.set_page_config(page_title="AI 블로그 어시스턴트", page_icon="📝")
st.title("📝 나만의 감성 & 정보 블로그 어시스턴트")

# 2. Gemini 키 입력 (사이드바)
with st.sidebar:
    st.header("🔑 API 키 설정")
    gemini_api_key = st.text_input("Gemini API Key", type="password")

# 3. 핵심 함수 (새로운 프롬프트 적용)
def generate_blog_draft(keyword, api_key):
    genai.configure(api_key=api_key)
    # 무료로 가장 안정적인 최신 모델
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    당신은 블로그에 솔직하고 생생한 여행/맛집 후기를 기록하는 현실적인 블로거입니다.
    사용자가 입력한 주제({keyword})를 바탕으로 아래의 5가지 조건을 철저히 지켜 블로그 초안을 작성해 주세요.

    [작성 규칙]
    1. 📌 장소 정보 요약 (서두 박스)
       - 글 시작 부분에 해당 장소의 기본 정보(위치/주소, 영업시간, 브레이크타임, 예약 필요 여부, 추천 메뉴 및 가격대 등)를 한눈에 보기 쉽게 깔끔한 리스트나 표 형태로 정리해 주세요.
    
    2. ✍️ 문체 및 어투 (현실적인 일기체)
       - 가식적이거나 지나치게 딱딱한 홍보 톤은 절대 쓰지 마세요.
       - 실제로 그 자리에 있었던 것처럼 생생하고 솔직한 일기체(~했음, ~인 줄 알았는데 아니었음, ~해서 어이없었음, ~각이다 등 자연스러운 어투)를 적극 활용하세요.
    
    3. 💡 정보 + 솔직한 감정과 느낌
       - 단순 정보 나열에 그치지 않고, 방문하면서 겪은 상황, 당시 느낀 감정(맛에 대한 솔직한 평, 웨이팅 팁, 당황했던 순간, 뜻밖의 만족감 등)을 디테일하게 녹여내세요.
    
    4. 🔍 검색 및 AI 인용 최적화 제목 + 해시태그 30개
       - 네이버 AI 검색(Cue:) 및 포털 상위 노출에 최적화된 매력적인 블로그 제목 2~3개를 먼저 추천해 주세요.
       - 글 맨 끝에는 검색 유입에 최적화된 인기 해시태그 30개를 띄어쓰기로 나열해 주세요.
    
    5. 📱 인스타그램 캡션
       - 블로그 본문 아래에 인스타그램 피드에 바로 복사해 올릴 수 있는 감성적이고 간결한 인스타 캡션(본문 요약 + 이모지 활용)을 따로 작성해 주세요.

    주제: {keyword}
    """
    
    response = model.generate_content(prompt)
    return response.text

# 4. 메인 화면
target_keyword = st.text_input("어떤 장소나 주제로 글을 쓰실 건가요?", placeholder="예: 바르셀로나 사그라다 파밀리아 타파스 맛집")

if st.button("🚀 블로그 초안 생성하기", use_container_width=True):
    if not gemini_api_key:
        st.error("Gemini API 키를 먼저 입력해 주세요.")
    elif not target_keyword:
        st.warning("주제를 입력해 주세요.")
    else:
        with st.spinner("AI가 생생한 후기와 정보를 작성 중입니다... ✍️"):
            try:
                draft = generate_blog_draft(target_keyword, gemini_api_key)
                st.markdown("---")
                st.markdown(draft)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
