import streamlit as st
import requests
from openai import OpenAI

# ---------------- 1. 기본 UI 설정 (모바일 최적화) ---------------- #
st.set_page_config(page_title="AI 블로그 어시스턴트", page_icon="📝", layout="centered")

st.title("📝 나만의 AI 블로그 어시스턴트")
st.markdown("여행/맛집 키워드를 입력하면 상위 노출 데이터를 분석해 블로그 초안과 인스타 캡션을 만들어줍니다.")

# ---------------- 2. API 키 입력 (사이드바) ---------------- #
with st.sidebar:
    st.header("🔑 API 키 설정")
    st.markdown("최초 1회만 입력해 주세요.")
    naver_client_id = st.text_input("Naver Client ID", type="password")
    naver_client_secret = st.text_input("Naver Client Secret", type="password")
    openai_api_key = st.text_input("OpenAI API Key", type="password")

# ---------------- 3. 핵심 함수 (네이버 & OpenAI) ---------------- #
def get_naver_blog_data(keyword, client_id, client_secret):
    url = "https://openapi.naver.com/v1/search/blog.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {"query": keyword, "display": 5, "sort": "sim"}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        blog_contents = []
        for item in data['items']:
            title = item['title'].replace('<b>', '').replace('</b>', '')
            desc = item['description'].replace('<b>', '').replace('</b>', '')
            blog_contents.append(f"- 제목: {title}\n  내용: {desc}")
        return "\n".join(blog_contents)
    else:
        return None

def generate_blog_draft(keyword, search_data, api_key):
    client = OpenAI(api_key=api_key)
    
    # AI의 페르소나와 작성 규칙을 범용적으로 수정했습니다.
    system_prompt = """
    당신은 세계여행, 국내여행, 맛집을 전문으로 다루는 네이버 탑 인플루언서입니다.
    누구나 유용하게 읽고 참고할 수 있도록, 대상을 특정하지 않은 범용적이고 정보성 넘치는 매거진 스타일의 글을 작성해 주세요.
    네이버 AI 검색(Cue:)에 인용되기 쉽도록 다음 규칙을 따르세요:
    1. 비교 분석과 숫자(Top 3 등)를 적극 활용할 것
    2. 독자가 가장 궁금해할 핵심 Q&A 2가지 필수 포함할 것
    3. 글 하단에 인스타그램 업로드용 요약(3문단)과 인기 해시태그 15개 작성할 것
    4. 친근하지만 전문성 있는 어투를 사용할 것
    """
    
    user_prompt = f"주제: {keyword}\n\n[네이버 상위 노출 참고 데이터]\n{search_data}\n\n위 데이터를 바탕으로 완벽한 포스팅 초안을 작성해 줘."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# ---------------- 4. 메인 화면 (검색어 입력 및 실행) ---------------- #
st.subheader("🔎 검색어 입력")
target_keyword = st.text_input("어떤 주제로 글을 쓰실 건가요?", placeholder="예: 오사카 3박4일 여행 코스")

if st.button("🚀 블로그 초안 생성하기", use_container_width=True):
    if not (naver_client_id and naver_client_secret and openai_api_key):
        st.error("앗! 왼쪽 메뉴(사이드바)에서 API 키를 모두 입력해 주세요.")
    elif not target_keyword:
        st.warning("글을 작성할 키워드를 입력해 주세요.")
    else:
        with st.spinner("네이버 상위 블로그를 분석하고 있습니다... ⏳"):
            naver_data = get_naver_blog_data(target_keyword, naver_client_id, naver_client_secret)
            
        if naver_data:
            with st.spinner("AI가 인플루언서 스타일로 글을 작성 중입니다... ✍️"):
                final_draft = generate_blog_draft(target_keyword, naver_data, openai_api_key)
                
            st.success("🎉 초안 생성이 완료되었습니다!")
            st.markdown("---")
            st.markdown(final_draft) # 화면에 결과 출력
        else:
            st.error("네이버 데이터를 불러오는 데 실패했습니다. API 키를 다시 확인해 주세요.")
