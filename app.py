import streamlit as st
import google.generativeai as genai

# 1. UI 설정
st.set_page_config(page_title="AI 프로페셔널 여행 블로그 에디터", page_icon="✈️", layout="centered")
st.title("✈️ 프로페셔널 여행 콘텐츠 에디터")
st.markdown("여행의 기억을 가감 없이 입력해 주시면, 절대 지어내지 않고 신뢰감 있는 고품질 여행 후기와 인스타 캡션, 해시태그까지 완성해 드립니다.")

# 2. 시스템에 영구 저장된 Gemini 키 자동 불러오기
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    gemini_api_key = None

# 3. 핵심 함수 (인스타 캡션, 해시태그, AI 최적화 제목 포함)
def generate_blog_draft(data, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.7-flash')
    
    prompt = f"""
    [역할]
    당신은 사용자가 직접 다녀온 세계여행 경험을 신뢰감 있고 읽기 좋은 한국어 블로그 글로 편집하는 여행 콘텐츠 에디터다.
    사용자가 입력한 여행 메모, 사진 설명, 방문 장소, 일정, 감정, 실제 비용, 실수, 팁을 바탕으로 여행 후기를 작성한다. 글의 목적은 단순한 장소 소개가 아니라, 사용자의 고유한 여행 경험을 독자가 생생하게 이해하고 실질적으로 참고할 수 있도록 만드는 것이다.

    [절대 원칙]
    1. 사용자가 제공하지 않은 개인 경험, 방문 사실, 대화, 감정, 가격, 이동 시간, 맛 평가, 숙소 상태를 지어내지 않는다.
    2. 정보가 부족한 부분은 자연스럽게 생략하거나 “[추가 정보 필요]”로 표시한다.
    3. “내가 느낀 점”, “내 일정에서는”, “방문 당시에는” 등으로 주관적 경험임을 자연스럽게 드러낸다.
    4. 비자, 입국 조건, 영업시간, 교통요금, 환율, 안전, 날씨, 예약 규정처럼 바뀔 수 있는 정보는 확정적으로 단정하지 않는다.
    5. 변동 가능성이 있는 정보는 “[최신 정보 확인 필요]”라고 표시한다.
    6. 과장된 광고 문구, 근거 없는 최상급 표현, 지나치게 일반적인 감상은 사용하지 않는다.
    7. 독자가 실제로 여행을 계획할 때 참고할 수 있도록 구체적인 이유, 선택 기준, 주의점을 포함한다.
    8. 작성자의 경험과 일반 여행 정보가 섞이지 않도록 명확히 구분한다.
    9. 모든 글은 한국어로 작성한다.
    10. 블로그 본문 내용이 풍부하도록 공백 포함 500자 이상으로 상세히 작성한다.
    11. 가식적이거나 지나치게 딱딱한 홍보 톤은 쓰지 않는다(어투는 "~요" 활용)

    [작성 방식]
    - 도입에서 여행의 핵심 경험 또는 가장 인상적인 장면을 먼저 제시한다.
    - 이후 시간 순서 또는 지역 순서로 자연스럽게 여행을 전개한다.
    - 각 문단은 하나의 경험, 장소 또는 메시지에 집중한다.
    - 단순히 “좋았다”, “예뻤다”라고 쓰지 말고, 왜 그렇게 느꼈는지 사용자가 제공한 사실을 바탕으로 설명한다.
    - 여행지, 식당, 숙소, 교통수단을 추천할 때는 추천 이유와 아쉬운 점 또는 유의사항을 함께 쓴다.
    - 비용, 동선, 일정, 교통수단 비교가 필요한 경우에만 Markdown 표를 사용한다.
    - 문체는 친근하지만 신뢰감 있는 1인칭 여행 후기 문체로 작성한다.
    - 사용자가 정한 분위기를 우선 반영한다. 분위기가 없으면 담백하고 생생한 여행 기록 문체를 사용한다.

    [출력 형식]
    ## 🔍 AI 검색(Cue:) 및 포털 상위 노출 최적화 제목 추천
    (검색 유입과 AI 인용에 유리하고 매력적인 블로그 제목 2~3가지를 추천해 주세요)

    # 본문 제목

    ## 한눈에 보는 여행
    - 여행지:
    - 여행 시기:
    - 여행 기간:
    - 동행:
    - 여행의 핵심 한 줄:

    ## 여행을 떠나게 된 이유
    (여행의 계기 또는 이번 여행에서 기대했던 점을 작성한다. 제공된 정보가 없으면 생략한다.)

    ## 가장 기억에 남는 순간
    (여행 전체를 대표하는 장면이나 감정을 먼저 작성한다.)

    ## 여행 기록
    (여행 일정 또는 지역별 경험을 자연스럽게 작성한다. 각 소제목에는 날짜, 지역, 장소 또는 핵심 경험을 포함한다.)

    ## 직접 다녀와서 느낀 점
    (좋았던 점, 예상과 달랐던 점, 아쉬웠던 점을 균형 있게 정리한다.)

    ## 여행 준비와 실용 팁
    (사용자가 실제로 경험한 예약, 이동, 비용, 짐, 식당, 숙소, 일정 관련 팁을 정리한다. 변동 가능성이 있는 정보는 “[최신 정보 확인 필요]”를 붙인다.)

    ## 이런 여행자에게 추천
    (이 여행 또는 특정 장소가 잘 맞는 여행자와 그렇지 않을 수 있는 여행자를 구체적으로 설명한다.)

    ## 마무리
    (여행을 통해 남은 감정이나 다음 여행자에게 전하고 싶은 한 문장으로 마무리한다.)

    ---
    ## 🏷️ 검색 유입 해시태그 30개
    (해당 여행지와 관련된 인기 해시태그 30개를 띄어쓰기로 나열해 주세요)

    ---
    ## 📱 인스타그램 캡션
    (인스타그램 피드에 바로 복사해 올릴 수 있는 감성적이고 간결한 본문 요약 + 이모지 캡션을 작성해 주세요)

    [사용자 입력 정보]
    - 여행지: {data['destination']}
    - 여행 시기: {data['travel_period']}
    - 여행 기간: {data['duration']}
    - 동행: {data['companions']}
    - 방문 장소: {data['places_visited']}
    - 여행 일정 또는 동선: {data['itinerary']}
    - 가장 기억에 남는 장면: {data['memorable_moments']}
    - 좋았던 점: {data['positive_experiences']}
    - 아쉬웠던 점 또는 실수: {data['regrets_or_mistakes']}
    - 숙소, 음식, 교통 경험: {data['stay_food_transport']}
    - 실제 비용: {data['actual_costs']}
    - 독자에게 전하고 싶은 팁: {data['tips']}
    - 글 분위기: {data['tone']}
    - 추가 메모 또는 사진 설명: {data['additional_notes']}

    [최종 지시]
    위 입력 정보를 빠짐없이 활용해 하나의 완성된 블로그 글과 해시태그, 인스타 캡션을 작성한다.
    제공되지 않은 사실은 추측하거나 만들어내지 않는다.
    글의 첫 문단에서 독자가 이 글을 읽어야 하는 이유와 여행의 핵심 경험을 분명하게 전달한다.
    """
    
    response = model.generate_content(prompt)
    return response.text

# 4. 메인 화면 (상세 입력 폼 구성)
st.subheader("🧭 여행 세부 정보 입력하기")
st.markdown("기억나는 만큼 편하게 적어주세요. 적지 않은 항목은 AI가 무리해서 지어내지 않고 자연스럽게 생략합니다.")

col1, col2 = st.columns(2)
with col1:
    destination = st.text_input("여행지", placeholder="예: 스페인 바르셀로나")
    travel_period = st.text_input("여행 시기", placeholder="예: 2026년 5월")
    duration = st.text_input("여행 기간", placeholder="예: 3박 4일")
    companions = st.text_input("동행", placeholder="예: 친구 1명")

with col2:
    tone = st.text_input("글 분위기", placeholder="예: 담백하고 솔직한 일기체")
    actual_costs = st.text_input("실제 비용 (선택)", placeholder="예: 숙소 1박당 15만 원 등")

places_visited = st.text_area("방문 장소", placeholder="예: 사그라다 파밀리아, 람블라스 거리, 00 타파스 바")
itinerary = st.text_area("여행 일정 또는 동선", placeholder="예: 첫날 도착해서 숙소 체크인 후 바로 타파스 바 이동...")
memorable_moments = st.text_area("가장 기억에 남는 장면", placeholder="예: 성당 내부로 햇빛이 들어올 때 소름 돋았던 순간")
positive_experiences = st.text_area("좋았던 점", placeholder="예: 예약하고 가서 웨이팅 없이 바로 입장함")
regrets_or_mistakes = st.text_area("아쉬웠던 점 또는 실수", placeholder="예: 소매치기 걱정하느라 가방을 너무 긴장해서 맸음")
stay_food_transport = st.text_area("숙소, 음식, 교통 경험", placeholder="예: 지하철 카드가 생각보다 편리했음")
tips = st.text_area("독자에게 전하고 싶은 팁", placeholder="예: 티켓은 최소 한 달 전에 공식 홈페이지에서 예약할 것")
additional_notes = st.text_area("추가 메모 또는 사진 설명", placeholder="예: 기타 특이사항이나 기억하고 싶은 디테일")

if st.button("🚀 블로그 글, 해시태그, 인스타 캡션 한 번에 생성하기", use_container_width=True):
    if not destination:
        st.warning("최소한 '여행지'는 입력해 주세요!")
    else:
        user_data = {
            "destination": destination,
            "travel_period": travel_period if travel_period else "정보 없음",
            "duration": duration if duration else "정보 없음",
            "companions": companions if companions else "정보 없음",
            "places_visited": places_visited if places_visited else "정보 없음",
            "itinerary": itinerary if itinerary else "정보 없음",
            "memorable_moments": memorable_moments if memorable_moments else "정보 없음",
            "positive_experiences": positive_experiences if positive_experiences else "정보 없음",
            "regrets_or_mistakes": regrets_or_mistakes if regrets_or_mistakes else "정보 없음",
            "stay_food_transport": stay_food_transport if stay_food_transport else "정보 없음",
            "actual_costs": actual_costs if actual_costs else "정보 없음",
            "tips": tips if tips else "정보 없음",
            "tone": tone if tone else "담백하고 생생한 여행 기록 문체",
            "additional_notes": additional_notes if additional_notes else "정보 없음"
        }
        
        with st.spinner("에디터가 입력하신 경험을 바탕으로 블로그 포스팅과 해시태그, 인스타 캡션을 작성 중입니다... ✍️"):
            try:
                draft = generate_blog_draft(user_data, gemini_api_key)
                st.markdown("---")
                st.markdown(draft)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
