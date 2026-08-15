import streamlit as st
import google.generativeai as genai

# 1. UI 설정
st.set_page_config(page_title="AI 프로페셔널 여행 콘텐츠 에디터", page_icon="✈️", layout="centered")
st.title("✈️ 프로페셔널 여행 콘텐츠 에디터")
st.markdown("여행의 기억을 가감 없이 입력해 주시면, 신뢰감 있는 고품질 블로그 글과 인스타 캡션, 해시태그를 완성해 드립니다.")

# 2. 시스템에 영구 저장된 Gemini 키 자동 불러오기
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    gemini_api_key = None

# 3. 상단 탭 생성 (여행 전체 / 호텔 / 관광지 / 맛집 / 이동수단)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "✈️ 여행 전체", 
    "🏨 호텔 리뷰", 
    "🗺️ 관광지 리뷰", 
    "🍽️ 맛집 리뷰", 
    "🚆 이동수단 리뷰"
])

# ==================== [탭 1] 여행 전체 에디터 ====================
with tab1:
    st.subheader("🧭 여행 세부 정보 입력하기")
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("여행지", placeholder="예: 스페인 바르셀로나", key="t_dest")
        travel_period = st.text_input("여행 시기", placeholder="예: 2026년 5월", key="t_period")
        duration = st.text_input("여행 기간", placeholder="예: 3박 4일", key="t_dur")
        companions = st.text_input("동행", placeholder="예: 친구 1명", key="t_comp")
    with col2:
        tone = st.text_input("글 분위기", placeholder="예: 담백하고 솔직한 일기체", key="t_tone")
        actual_costs = st.text_input("실제 비용 (선택)", placeholder="예: 숙소 1박당 15만 원 등", key="t_cost")

    places_visited = st.text_area("방문 장소", placeholder="예: 사그라다 파밀리아, 람블라스 거리", key="t_places")
    itinerary = st.text_area("여행 일정 또는 동선", placeholder="예: 첫날 도착해서 숙소 체크인 후...", key="t_itin")
    memorable_moments = st.text_area("가장 기억에 남는 장면", placeholder="예: 성당 내부로 햇빛이 들어올 때...", key="t_mem")
    positive_experiences = st.text_area("좋았던 점", placeholder="예: 예약하고 가서 웨이팅 없이 입장함", key="t_pos")
    regrets_or_mistakes = st.text_area("아쉬웠던 점 또는 실수", placeholder="예: 가방을 너무 긴장해서 맸음", key="t_reg")
    stay_food_transport = st.text_area("숙소, 음식, 교통 경험", placeholder="예: 지하철 카드가 편리했음", key="t_sft")
    tips = st.text_area("독자에게 전하고 싶은 팁", placeholder="예: 티켓은 최소 한 달 전 예약 필수", key="t_tips")
    additional_notes = st.text_area("추가 메모 또는 사진 설명", placeholder="예: 기타 특이사항", key="t_add")

    if st.button("🚀 여행 전체 블로그 초안 생성하기", use_container_width=True, key="btn_t1"):
        if not destination:
            st.warning("최소한 '여행지'는 입력해 주세요!")
        elif not gemini_api_key:
            st.error("Streamlit Secrets에 Gemini API 키가 설정되어 있지 않습니다.")
        else:
            data = {
                "destination": destination, "travel_period": travel_period or "정보 없음",
                "duration": duration or "정보 없음", "companions": companions or "정보 없음",
                "places_visited": places_visited or "정보 없음", "itinerary": itinerary or "정보 없음",
                "memorable_moments": memorable_moments or "정보 없음", "positive_experiences": positive_experiences or "정보 없음",
                "regrets_or_mistakes": regrets_or_mistakes or "정보 없음", "stay_food_transport": stay_food_transport or "정보 없음",
                "actual_costs": actual_costs or "정보 없음", "tips": tips or "정보 없음",
                "tone": tone or "담백하고 생생한 여행 기록 문체", "additional_notes": additional_notes or "정보 없음"
            }
            prompt = f"""
            [역할]
            당신은 사용자가 직접 다녀온 세계여행 경험을 신뢰감 있고 읽기 좋은 한국어 블로그 글로 편집하는 여행 콘텐츠 에디터다.
            사용자가 입력한 여행 메모, 사진 설명, 방문 장소, 일정, 감정, 실제 비용, 실수, 팁을 바탕으로 여행 후기를 작성한다.

            [절대 원칙]
            1. 사용자가 제공하지 않은 개인 경험, 방문 사실, 대화, 감정, 가격, 이동 시간, 맛 평가, 숙소 상태를 지어내지 않는다.
            2. 정보가 부족한 부분은 자연스럽게 생략하거나 “[추가 정보 필요]”로 표시한다.
            3. “내가 느낀 점”, “내 일정에서는”, “방문 당시에는” 등으로 주관적 경험임을 자연스럽게 드러낸다.
            4. 변동 가능성이 있는 정보(비자, 요금, 예약 규정 등)는 “[최신 정보 확인 필요]”라고 표시한다.
            5. 과장된 광고 문구, 근거 없는 최상급 표현은 사용하지 않는다.
            6. 모든 글은 한국어로 작성한다.
            7. 블로그 본문 내용이 풍부하도록 공백 포함 500자 이상으로 상세히 작성한다.
            8. 가식적이거나 지나치게 딱딱한 홍보 톤은 쓰지 않는다(어투는 "~요" 활용).

            [작성 방식]
            - 도입에서 여행의 핵심 경험 또는 가장 인상적인 장면을 먼저 제시한다.
            - 시간 순서 또는 지역 순서로 자연스럽게 전개하고 문단은 하나의 경험/장소에 집중한다.
            - 추천할 때는 추천 이유와 아쉬운 점 또는 유의사항을 함께 쓴다.

            [출력 형식]
            ## 🔍 AI 검색(Cue:) 및 포털 상위 노출 최적화 제목 추천
            # 본문 제목
            ## 한눈에 보는 여행
            - 여행지: {data['destination']}
            - 여행 시기: {data['travel_period']}
            - 여행 기간: {data['duration']}
            - 동행: {data['companions']}
            - 여행의 핵심 한 줄:
            ## 여행을 떠나게 된 이유
            ## 가장 기억에 남는 순간
            ## 여행 기록
            ## 직접 다녀와서 느낀 점
            ## 여행 준비와 실용 팁
            ## 이런 여행자에게 추천
            ## 마무리
            ---
            ## 🏷️ 검색 유입 해시태그 30개
            ---
            ## 📱 인스타그램 캡션

            [사용자 입력 정보]
            - 여행지: {data['destination']}, 시기: {data['travel_period']}, 기간: {data['duration']}, 동행: {data['companions']}
            - 방문 장소: {data['places_visited']}, 동선: {data['itinerary']}
            - 기억에 남는 순간: {data['memorable_moments']}, 좋았던 점: {data['positive_experiences']}
            - 아쉬운 점/실수: {data['regrets_or_mistakes']}, 숙소/음식/교통: {data['stay_food_transport']}
            - 비용: {data['actual_costs']}, 팁: {data['tips']}, 분위기: {data['tone']}, 추가 메모: {data['additional_notes']}
            """
            with st.spinner("에디터가 여행 전체 후기를 작성 중입니다... ✍️"):
                try:
                    genai.configure(api_key=gemini_api_key)
                    model = genai.GenerativeModel('gemini-3.7-flash')
                    res = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

# ==================== [탭 2] 호텔 리뷰 에디터 ====================
with tab2:
    st.subheader("🏨 호텔/숙소 세부 정보 입력하기")
    h_name = st.text_input("호텔 이름 및 위치", placeholder="예: 바르셀로나 00 호텔", key="h_name")
    col3, col4 = st.columns(2)
    with col3:
        h_room = st.text_input("객실 타입", placeholder="예: 디럭스 더블룸", key="h_room")
        h_price = st.text_input("1박 실제 비용", placeholder="예: 약 18만 원", key="h_price")
    with col4:
        h_book = st.text_input("예약 플랫폼", placeholder="예: 아고다 예약", key="h_book")
        h_tone = st.text_input("글 분위기", placeholder="예: 담백하고 솔직한 후기 톤", key="h_tone")

    h_cond = st.text_area("룸 컨디션 및 청결도", placeholder="예: 침구가 포근하고 뷰가 좋았음", key="h_cond")
    h_serv = st.text_area("부대시설 및 서비스", placeholder="예: 조식이 맛있고 직원 응대가 친절함", key="h_serv")
    h_bad = st.text_area("아쉬웠던 점 / 단점", placeholder="예: 방음이 살짝 아쉬움", key="h_bad")
    h_tips = st.text_area("예약 및 이용 꿀팁", placeholder="예: 고층 방으로 요청하는 것 추천", key="h_tips")

    if st.button("🚀 호텔 리뷰 초안 생성하기", use_container_width=True, key="btn_t2"):
        if not h_name:
            st.warning("최소한 '호텔 이름 및 위치'는 입력해 주세요!")
        elif not gemini_api_key:
            st.error("Streamlit Secrets에 Gemini API 키가 설정되어 있지 않습니다.")
        else:
            h_data = {
                "name": h_name, "room": h_room or "정보 없음", "price": h_price or "정보 없음",
                "book": h_book or "정보 없음", "cond": h_cond or "정보 없음", "serv": h_serv or "정보 없음",
                "bad": h_bad or "정보 없음", "tips": h_tips or "정보 없음", "tone": h_tone or "담백하고 솔직한 숙소 후기 문체"
            }
            h_prompt = f"""
            [역할]
            당신은 사용자가 직접 숙박한 호텔/숙소 경험을 신뢰감 있고 읽기 좋은 한국어 블로그 글로 편집하는 여행 콘텐츠 에디터다.
            사용자가 입력한 숙소 정보, 룸 컨디션, 서비스, 단점, 팁을 바탕으로 리뷰를 작성한다.

            [절대 원칙]
            1. 사용자가 제공하지 않은 시설 상태, 서비스, 가격, 조식 맛 등을 지어내지 않는다.
            2. 정보가 부족한 부분은 생략하거나 “[추가 정보 필요]”로 표시한다.
            3. “내가 머물렀을 때는”, “체크인해보니” 등으로 주관적 경험임을 자연스럽게 드러낸다.
            4. 변동 가능성이 있는 요금이나 규정은 “[최신 정보 확인 필요]”라고 표시한다.
            5. 모든 글은 한국어로 작성한다.
            6. 블로그 본문 내용이 풍부하도록 공백 포함 500자 이상으로 상세히 작성한다.
            7. 가식적이거나 지나치게 딱딱한 홍보 톤은 쓰지 않는다(어투는 "~요" 활용).

            [작성 방식]
            - 도입에서 이 숙소를 선택한 이유와 전체적인 첫인상을 제시한다.
            - 객실, 서비스, 아쉬운 점을 객관적 사실 기반으로 풀어낸다.
            - 추천 이유와 주의사항을 함께 쓴다.

            [출력 형식]
            ## 🔍 AI 검색(Cue:) 및 호텔 후기 상위 노출 최적화 제목 추천
            # 본문 제목
            ## 📌 한눈에 보는 숙소 요약
            - 호텔 이름 및 위치: {h_data['name']}
            - 객실 타입: {h_data['room']}
            - 1박 비용: {h_data['price']}
            - 예약 플랫폼: {h_data['book']}
            ## 호텔을 선택한 이유
            ## 객실 컨디션 및 청결도
            ## 조식 및 부대시설 서비스
            ## 아쉬웠던 점 및 단점
            ## 예약 꿀팁 및 추천 여부
            ---
            ## 🏷️ 검색 유입 해시태그 30개
            ---
            ## 📱 인스타그램 호텔 캡션

            [사용자 입력 정보]
            - 호텔명: {h_data['name']}, 객실: {h_data['room']}, 비용: {h_data['price']}, 예약처: {h_data['book']}
            - 룸컨디션: {h_data['cond']}, 서비스: {h_data['serv']}, 단점: {h_data['bad']}, 팁: {h_data['tips']}, 분위기: {h_data['tone']}
            """
            with st.spinner("에디터가 호텔 리뷰를 작성 중입니다... 🏨"):
                try:
                    genai.configure(api_key=gemini_api_key)
                    model = genai.GenerativeModel('gemini-3.7-flash')
                    res = model.generate_content(h_prompt)
                    st.markdown("---")
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

# ==================== [탭 3] 관광지 리뷰 에디터 ====================
with tab3:
    st.subheader("🗺️ 관광지/명소 세부 정보 입력하기")
    p_name = st.text_input("관광지 이름 및 위치", placeholder="예: 바르셀로나 사그라다 파밀리아", key="p_name")
    col5, col6 = st.columns(2)
    with col5:
        p_time = st.text_input("소요 시간", placeholder="예: 약 2시간 소요", key="p_time")
        p_cost = st.text_input("입장료 또는 비용", placeholder="예: 성인 26유로", key="p_cost")
    with col6:
        p_res = st.text_input("예약 여부", placeholder="예: 공식 홈페이지 사전 예매", key="p_res")
        p_tone = st.text_input("글 분위기", placeholder="예: 생생한 명소 방문기 톤", key="p_tone")

    p_exp = st.text_area("관람 경험 및 느낀 점", placeholder="예: 실제로 보니 웅장함에 압도당함", key="p_exp")
    p_photo = st.text_area("사진 스팟 및 분위기", placeholder="예: 성당 맞은편 공원 연못 앞에서 찍으면 예쁨", key="p_photo")
    p_bad = st.text_area("아쉬웠던 점 / 주의사항", placeholder="예: 사람이 너무 많아서 정신없음", key="p_bad")
    p_tips = st.text_area("방문 꿀팁", placeholder="예: 오디오 가이드 대여 필수", key="p_tips")

    if st.button("🚀 관광지 리뷰 초안 생성하기", use_container_width=True, key="btn_t3"):
        if not p_name:
            st.warning("최소한 '관광지 이름 및 위치'는 입력해 주세요!")
        elif not gemini_api_key:
            st.error("Streamlit Secrets에 Gemini API 키가 설정되어 있지 않습니다.")
        else:
            p_data = {
                "name": p_name, "time": p_time or "정보 없음", "cost": p_cost or "정보 없음",
                "res": p_res or "정보 없음", "exp": p_exp or "정보 없음", "photo": p_photo or "정보 없음",
                "bad": p_bad or "정보 없음", "tips": p_tips or "정보 없음", "tone": p_tone or "생생한 명소 방문기 문체"
            }
            p_prompt = f"""
            [역할]
            당신은 사용자가 직접 방문한 관광지/명소 경험을 신뢰감 있고 읽기 좋은 한국어 블로그 글로 편집하는 여행 콘텐츠 에디터다.
            사용자가 입력한 명소 정보, 관람 경험, 포토스팟, 주의사항, 팁을 바탕으로 리뷰를 작성한다.

            [절대 원칙]
            1. 사용자가 제공하지 않은 역사적 사실, 관람 환경, 가격, 소요 시간을 지어내지 않는다.
            2. 정보가 부족한 부분은 생략하거나 “[추가 정보 필요]”로 표시한다.
            3. “방문했을 때”, “직접 보니” 등으로 주관적 경험임을 자연스럽게 드러낸다.
            4. 변동 가능성이 있는 입장료나 예약 규정은 “[최신 정보 확인 필요]”라고 표시한다.
            5. 모든 글은 한국어로 작성한다.
            6. 블로그 본문 내용이 풍부하도록 공백 포함 500자 이상으로 상세히 작성한다.
            7. 가식적이거나 지나치게 딱딱한 홍보 톤은 쓰지 않는다(어투는 "~요" 활용).

            [작성 방식]
            - 도입에서 이 관광지를 찾게 된 이유와 첫인상을 제시한다.
            - 관람 과정에서 느낀 점, 포토 스팟, 아쉬운 점을 상세히 다룬다.
            - 방문 시 유의사항과 꿀팁을 포함한다.

            [출력 형식]
            ## 🔍 AI 검색(Cue:) 및 관광지 후기 상위 노출 최적화 제목 추천
            # 본문 제목
            ## 📌 한눈에 보는 관광지 요약
            - 관광지 이름 및 위치: {p_data['name']}
            - 소요 시간: {p_data['time']}
            - 입장료/비용: {p_data['cost']}
            - 예약 여부: {p_data['res']}
            ## 방문 계기 및 첫인상
            ## 현장 관람 후기 및 감동 포인트
            ## 추천 포토 스팟
            ## 아쉬웠던 점 및 주의사항
            ## 필수 관람 꿀팁
            ---
            ## 🏷️ 검색 유입 해시태그 30개
            ---
            ## 📱 인스타그램 관광지 캡션

            [사용자 입력 정보]
            - 관광지명: {p_data['name']}, 소요시간: {p_data['time']}, 비용: {p_data['cost']}, 예약: {p_data['res']}
            - 경험: {p_data['exp']}, 포토스팟: {p_data['photo']}, 단점: {p_data['bad']}, 팁: {p_data['tips']}, 분위기: {p_data['tone']}
            """
            with st.spinner("에디터가 관광지 리뷰를 작성 중입니다... 🗺️"):
                try:
                    genai.configure(api_key=gemini_api_key)
                    model = genai.GenerativeModel('gemini-3.7-flash')
                    res = model.generate_content(p_prompt)
                    st.markdown("---")
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

# ==================== [탭 4] 맛집 리뷰 에디터 ====================
with tab4:
    st.subheader("🍽️ 맛집 세부 정보 입력하기")
    r_name = st.text_input("식당 이름 및 위치", placeholder="예: 바르셀로나 00 타파스 바", key="r_name")
    col7, col8 = st.columns(2)
    with col7:
        r_menu = st.text_input("주문한 메뉴", placeholder="예: 하몬, 감바스", key="r_menu")
        r_price = st.text_input("실제 지출 비용", placeholder="예: 총 45유로", key="r_price")
    with col8:
        r_waiting = st.text_input("웨이팅 및 예약 상황", placeholder="예: 30분 대기", key="r_wait")
        r_tone = st.text_input("글 분위기", placeholder="예: 솔직하고 유쾌한 맛집 탐방 톤", key="r_tone")

    r_taste = st.text_area("맛에 대한 솔직한 평가", placeholder="예: 감바스가 짜지 않고 환상적이었음", key="r_taste")
    r_mood = st.text_area("식당 분위기 및 서비스", placeholder="예: 직원들이 유쾌하고 활기참", key="r_mood")
    r_cons = st.text_area("아쉬웠던 점 / 단점", placeholder="예: 테이블 간격이 너무 좁음", key="r_cons")
    r_tips = st.text_area("방문 꿀팁", placeholder="예: 오픈 시간 10분 전 방문 추천", key="r_tips")

    if st.button("🚀 맛집 리뷰 초안 생성하기", use_container_width=True, key="btn_t4"):
        if not r_name:
            st.warning("최소한 '식당 이름 및 위치'는 입력해 주세요!")
        elif not gemini_api_key:
            st.error("Streamlit Secrets에 Gemini API 키가 설정되어 있지 않습니다.")
        else:
            r_data = {
                "name": r_name, "menu": r_menu or "정보 없음", "price": r_price or "정보 없음",
                "waiting": r_waiting or "정보 없음", "taste": r_taste or "정보 없음", "mood": r_mood or "정보 없음",
                "cons": r_cons or "정보 없음", "tips": r_tips or "정보 없음", "tone": r_tone or "솔직하고 생생한 맛집 탐방 문체"
            }
            r_prompt = f"""
            [역할]
            당신은 사용자가 직접 방문한 식당/카페 경험을 신뢰감 있고 읽기 좋은 한국어 블로그 글로 편집하는 여행 콘텐츠 에디터다.
            사용자가 입력한 메뉴, 맛 평가, 가격, 웨이팅, 분위기, 팁을 바탕으로 리뷰를 작성한다.

            [절대 원칙]
            1. 사용자가 제공하지 않은 맛, 가격, 웨이팅 상황, 서비스 경험을 지어내지 않는다.
            2. 정보가 부족한 부분은 생략하거나 “[추가 정보 필요]”로 표시한다.
            3. “먹어보니”, “방문했을 때” 등으로 주관적 경험임을 자연스럽게 드러낸다.
            4. 변동 가능성이 있는 가격이나 영업시간은 “[최신 정보 확인 필요]”라고 표시한다.
            5. 모든 글은 한국어로 작성한다.
            6. 블로그 본문 내용이 풍부하도록 공백 포함 500자 이상으로 상세히 작성한다.
            7. 가식적이거나 지나치게 딱딱한 홍보 톤은 쓰지 않는다(어투는 "~요" 활용).

            [작성 방식]
            - 도입에서 이 맛집을 찾게 된 계기와 첫인상을 제시한다.
            - 주문한 메뉴별 맛 평가와 서비스, 아쉬운 점을 솔직하게 풀어낸다.
            - 재방문 의사와 꿀팁을 함께 쓴다.

            [출력 형식]
            ## 🔍 AI 검색(Cue:) 및 맛집 후기 상위 노출 최적화 제목 추천
            # 본문 제목
            ## 📌 한눈에 보는 맛집 요약
            - 식당 이름 및 위치: {r_data['name']}
            - 대표 주문 메뉴: {r_data['menu']}
            - 실제 지출 비용: {r_data['price']}
            - 웨이팅 / 예약 여부: {r_data['waiting']}
            ## 찾아간 이유와 첫인상
            ## 주문한 메뉴 솔직 맛 평가
            ## 분위기 및 서비스
            ## 아쉬웠던 점
            ## 재방문 의사 및 꿀팁
            ---
            ## 🏷️ 검색 유입 해시태그 30개
            ---
            ## 📱 인스타그램 맛집 캡션

            [사용자 입력 정보]
            - 식당명: {r_data['name']}, 메뉴: {r_data['menu']}, 비용: {r_data['price']}, 웨이팅: {r_data['waiting']}
            - 맛평가: {r_data['taste']}, 분위기: {r_data['mood']}, 단점: {r_data['cons']}, 팁: {r_data['tips']}, 분위기: {r_data['tone']}
            """
            with st.spinner("에디터가 맛집 리뷰를 작성 중입니다... 🍽️"):
                try:
                    genai.configure(api_key=gemini_api_key)
                    model = genai.GenerativeModel('gemini-3.7-flash')
                    res = model.generate_content(r_prompt)
                    st.markdown("---")
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

# ==================== [탭 5] 이동수단 리뷰 에디터 ====================
with tab5:
    st.subheader("🚆 이동수단 세부 정보 입력하기")
    v_name = st.text_input("이동수단 종류 및 구간", placeholder="예: 바르셀로나에서 마드리드 렌페(AVE) 고속열차", key="v_name")
    col9, col10 = st.columns(2)
    with col9:
        v_time = st.text_input("소요 시간", placeholder="예: 약 2시간 30분 소요", key="v_time")
        v_price = st.text_input("이용 요금", placeholder="예: 편도 60유로", key="v_price")
    with col10:
        v_book = st.text_input("예약 방법", placeholder="예: 공식 앱에서 사전 예매", key="v_book")
        v_tone = st.text_input("글 분위기", placeholder="예: 객관적이고 실용적인 이동 정보 톤", key="v_tone")

    v_cond = st.text_area("좌석 컨디션 및 편의시설", placeholder="예: 좌석이 넓고 와이파이 이용 가능함", key="v_cond")
    v_exp = st.text_area("이동 중 겪은 경험 및 상황", placeholder="예: 연착 없이 정시에 출발하고 도착함", key="v_exp")
    v_bad = st.text_area("아쉬웠던 점 / 불편한 점", placeholder="예: 수하물 보관 공간이 조금 부족함", key="v_bad")
    v_tips = st.text_area("이용 꿀팁", placeholder="예: 기차역 보안 검색대가 있으므로 여유 있게 도착할 것", key="v_tips")

    if st.button("🚀 이동수단 리뷰 초안 생성하기", use_container_width=True, key="btn_t5"):
        if not v_name:
            st.warning("최소한 '이동수단 종류 및 구간'은 입력해 주세요!")
        elif not gemini_api_key:
            st.error("Streamlit Secrets에 Gemini API 키가 설정되어 있지 않습니다.")
        else:
            v_data = {
                "name": v_name, "time": v_time or "정보 없음", "price": v_price or "정보 없음",
                "book": v_book or "정보 없음", "cond": v_cond or "정보 없음", "exp": v_exp or "정보 없음",
                "bad": v_bad or "정보 없음", "tips": v_tips or "정보 없음", "tone": v_tone or "실용적인 이동 정보 문체"
            }
            v_prompt = f"""
            [역할]
            당신은 사용자가 직접 이용한 이동수단(기차, 버스, 항공, 렌트카 등)의 경험을 신뢰감 있고 읽기 좋은 한국어 블로그 글로 편집하는 여행 콘텐츠 에디터다.
            사용자가 입력한 이동 구간, 요금, 예약 방법, 좌석 컨디션, 장단점, 팁을 바탕으로 리뷰를 작성한다.

            [절대 원칙]
            1. 사용자가 제공하지 않은 시간표, 요금, 좌석 상태, 연착 여부 등을 지어내지 않는다.
            2. 정보가 부족한 부분은 생략하거나 “[추가 정보 필요]”로 표시한다.
            3. “이용해 보니”, “탑승했을 때” 등으로 주관적 경험임을 자연스럽게 드러낸다.
            4. 변동 가능성이 있는 요금이나 시간표는 “[최신 정보 확인 필요]”라고 표시한다.
            5. 모든 글은 한국어로 작성한다.
            6. 블로그 본문 내용이 풍부하도록 공백 포함 500자 이상으로 상세히 작성한다.
            7. 가식적이거나 지나치게 딱딱한 홍보 톤은 쓰지 않는다(어투는 "~요" 활용).

            [작성 방식]
            - 도입에서 이 이동수단을 선택한 이유와 구간 정보를 제시한다.
            - 예약 방법, 좌석 컨디션, 탑승 과정에서 느낀 점을 실용적으로 다룬다.
            - 주의사항과 이용 꿀팁을 함께 쓴다.

            [출력 형식]
            ## 🔍 AI 검색(Cue:) 및 이동수단 후기 상위 노출 최적화 제목 추천
            # 본문 제목
            ## 📌 한눈에 보는 이동수단 요약
            - 이동 구간 및 수단: {v_data['name']}
            - 소요 시간: {v_data['time']}
            - 이용 요금: {v_data['price']}
            - 예약 방법: {v_data['book']}
            ## 이 이동수단을 선택한 이유
            ## 예약 방법 및 탑승 과정 후기
            ## 좌석 컨디션 및 편의시설
            ## 아쉬웠던 점 및 불편한 점
            ## 실용적인 탑승 꿀팁
            ---
            ## 🏷️ 검색 유입 해시태그 30개
            ---
            ## 📱 인스타그램 이동수단 캡션

            [사용자 입력 정보]
            - 수단/구간: {v_data['name']}, 소요시간: {v_data['time']}, 요금: {v_data['price']}, 예약: {v_data['book']}
            - 좌석컨디션: {v_data['cond']}, 탑승경험: {v_data['exp']}, 단점: {v_data['bad']}, 팁: {v_data['tips']}, 분위기: {v_data['tone']}
            """
            with st.spinner("에디터가 이동수단 리뷰를 작성 중입니다... 🚆"):
                try:
                    genai.configure(api_key=gemini_api_key)
                    model = genai.GenerativeModel('gemini-3.7-flash')
                    res = model.generate_content(v_prompt)
                    st.markdown("---")
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
