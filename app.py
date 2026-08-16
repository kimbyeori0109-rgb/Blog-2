import streamlit as st
from openai import OpenAI


st.set_page_config(
    page_title="AI 프로페셔널 여행 콘텐츠 에디터",
    page_icon="✈️",
    layout="centered",
)

st.title("✈️ 프로페셔널 여행 콘텐츠 에디터")
st.markdown(
    "직접 다녀온 경험을 중심으로, 최신 운영 정보와 실용 팁을 더해 블로그·인스타그램·네이버 클립 콘텐츠를 만듭니다."
)


try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except KeyError:
    client = None


CONTENT_TYPES = {
    "여행 전체": {
        "emoji": "✈️",
        "entity_label": "여행지",
        "entity_placeholder": "예: 스페인 바르셀로나",
        "sections": [
            "여행 핵심 요약",
            "직접 다녀온 여행 기록",
            "여행 전 알아둘 최신 정보",
            "온라인 후기에서 공통으로 언급된 팁",
        ],
    },
    "호텔 리뷰": {
        "emoji": "🏨",
        "entity_label": "호텔/숙소 이름 및 위치",
        "entity_placeholder": "예: 바르셀로나 00 호텔, 에이샴플라",
        "sections": [
            "숙소 핵심 요약",
            "직접 머문 객실과 서비스 후기",
            "예약 전 확인할 최신 정보",
            "온라인 후기에서 공통으로 언급된 팁",
        ],
    },
    "관광지 리뷰": {
        "emoji": "🗺️",
        "entity_label": "관광지/테마시설 이름 및 위치",
        "entity_placeholder": "예: 바르셀로나 사그라다 파밀리아",
        "sections": [
            "관광지 핵심 요약",
            "직접 방문한 현장 후기",
            "주소·운영시간·입장 정보",
            "온라인 후기에서 공통으로 언급된 팁",
        ],
    },
    "맛집 리뷰": {
        "emoji": "🍽️",
        "entity_label": "식당/카페 이름 및 위치",
        "entity_placeholder": "예: 바르셀로나 00 타파스 바",
        "sections": [
            "맛집 핵심 요약",
            "직접 먹어본 메뉴 후기",
            "주소·영업시간·방문 정보",
            "온라인 후기에서 공통으로 언급된 팁",
        ],
    },
    "이동수단 리뷰": {
        "emoji": "🚆",
        "entity_label": "이동수단 및 구간",
        "entity_placeholder": "예: 바르셀로나→마드리드 렌페 AVE",
        "sections": [
            "이동수단 핵심 요약",
            "직접 이용한 탑승 후기",
            "예약·탑승 최신 정보",
            "온라인 후기에서 공통으로 언급된 팁",
        ],
    },
}


def build_prompt(content_type: str, details: dict) -> str:
    config = CONTENT_TYPES[content_type]
    section_list = "\n".join(f"## {section}" for section in config["sections"])

    return f"""
당신은 여행자의 실제 경험을 전문적이고 친근한 한국어 콘텐츠로 편집하는 여행 에디터다.
이번 작업의 종류는 '{content_type}'이며, 중심 대상은 '{details['entity']}'이다.

[필수 작업]
1. 먼저 웹 검색을 사용해 대상의 최신 공식 정보와 최근 여행자 후기를 확인한다.
2. 주소, 영업시간, 휴무일, 가는 방법, 예상 비용, 예약·대기·이용 규정처럼 변동 가능한 정보는 반드시 공식 홈페이지·운영사·관광청·교통사 등 1차 출처를 우선 확인한다.
3. 공식 출처로 확인할 수 없는 정보는 단정하지 말고 '방문 전 최신 확인이 필요해요'라고 쓴다.
4. 사용자 경험은 사용자가 준 메모 안에서만 쓴다. 제공되지 않은 감정, 대화, 맛, 객실 상태, 대기 시간, 지출, 방문 사실을 절대 만들지 않는다.
5. 부족한 실용 정보는 웹에서 확인된 사실로 보완한다. 다른 여행자 후기에서 반복적으로 언급되는 팁은 '온라인 후기에서 자주 언급된 팁'으로 출처 성격을 분리해 요약한다. 개별 후기의 내용을 사실처럼 단정하거나 복사하지 않는다.
6. 아쉬운 점·실수·단점 섹션은 만들지 않는다.

[문체와 품질 기준]
- 모든 문장은 자연스럽고 친근한 '~요' 말투로 쓴다. '방문했습니다'가 아니라 '방문했어요'처럼 쓴다.
- 오래된 일반론, 과장된 홍보 문구, 근거 없는 '필수·최고·무조건' 표현을 쓰지 않는다.
- 독자가 바로 답을 얻도록 결론을 먼저 말하고, 조건과 근거를 뒤에 붙인다.
- 검색 유입을 고려해 장소명·도시명·여행 목적·이용 의도를 자연스럽게 포함한다. 키워드를 반복 나열하지 않는다.
- 블로그 본문은 공백 포함 1,000자 이내로 작성한다. 제목·해시태그·인스타그램·네이버 클립 문구·출처 목록은 본문 글자 수에서 제외한다.
- 최신 운영 정보는 조회 시점 기준임을 명시하고, 출처 링크를 제공한다.

[출력 형식]
## SEO·AI 검색용 제목 추천 5개
- 서로 다른 검색 의도의 제목 5개를 제안한다. 장소명과 핵심 의도를 포함한다.

# 추천 본문 제목

## 한눈에 보는 정보
- 주소:
- 영업시간 / 운영 정보:
- 가는 방법:
- 예상 비용:
- 예약 / 이용 팁:

{section_list}

## 블로그 본문
위 정보와 사용자 경험을 연결한 본문을 공백 포함 1,000자 이내로 작성한다.

## 해시태그
- 블로그 검색용 15개
- 인스타그램·네이버 클립용 15개
각 해시태그는 실제 검색어처럼 구체적으로 만들고, 중복·무관한 인기 태그는 제외한다.

## 인스타그램 캡션
120~180자, 첫 문장은 시선을 끄는 훅으로 시작한다. 친근한 '~요' 말투로 작성한다.

## 네이버 클립 문구
- 영상 제목: 35자 이내
- 오프닝 자막: 25자 이내
- 영상 설명: 80자 이내
- 클립 해시태그: 8개

## 정보 출처
운영 정보에 사용한 공식 출처를 링크와 함께 2~5개만 제시한다. 공식 출처가 없으면 그 사실을 분명히 쓴다.

[사용자 입력]
- 대상: {details['entity']}
- 여행지/도시: {details['location']}
- 방문 시기: {details['period']}
- 동행/여행 맥락: {details['companions']}
- 직접 경험한 내용: {details['experience']}
- 방문 장소·주문 메뉴·이용 구간: {details['items']}
- 일정·동선·이용 과정: {details['route']}
- 실제 지출/예산: {details['cost']}
- 사진·영상 장면 또는 추가 메모: {details['notes']}
- 원하는 분위기: {details['tone']}
"""


def generate_content(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-5.6",
        reasoning={"effort": "low"},
        tools=[{"type": "web_search"}],
        input=prompt,
    )
    return response.output_text


tabs = st.tabs([f"{value['emoji']} {name}" for name, value in CONTENT_TYPES.items()])

for (content_type, config), tab in zip(CONTENT_TYPES.items(), tabs):
    with tab:
        st.subheader(f"{config['emoji']} {content_type} 정보 입력")
        st.caption("직접 경험한 내용은 자세히 적고, 최신 운영 정보는 AI가 웹 검색으로 보완해요.")

        col1, col2 = st.columns(2)
        with col1:
            entity = st.text_input(
                config["entity_label"],
                placeholder=config["entity_placeholder"],
                key=f"{content_type}_entity",
            )
            location = st.text_input(
                "여행지 / 도시",
                placeholder="예: 바르셀로나, 스페인",
                key=f"{content_type}_location",
            )
            period = st.text_input(
                "방문 시기",
                placeholder="예: 2026년 5월",
                key=f"{content_type}_period",
            )
        with col2:
            companions = st.text_input(
                "동행 또는 여행 맥락",
                placeholder="예: 친구와 3박 4일 여행 중",
                key=f"{content_type}_companions",
            )
            cost = st.text_input(
                "실제 지출 또는 예산",
                placeholder="예: 2인 기준 45유로",
                key=f"{content_type}_cost",
            )
            tone = st.selectbox(
                "글 분위기",
                ["친근하고 생생한 후기", "감성적이지만 정보 중심", "담백하고 실용적인 가이드"],
                key=f"{content_type}_tone",
            )

        experience = st.text_area(
            "직접 경험한 내용",
            placeholder="예: 왜 방문했는지, 무엇을 보고·먹고·이용했는지, 기억에 남은 장면을 적어주세요.",
            key=f"{content_type}_experience",
            height=160,
        )
        items = st.text_area(
            "방문 장소·주문 메뉴·이용 구간",
            placeholder="예: 감바스와 하몬 주문 / 내부 관람 / AVE 1등석 이용",
            key=f"{content_type}_items",
        )
        route = st.text_area(
            "일정·동선·이용 과정",
            placeholder="예: 지하철로 이동 후 도보 5분 / 공식 홈페이지에서 예약",
            key=f"{content_type}_route",
        )
        notes = st.text_area(
            "사진·영상 장면 또는 추가 메모",
            placeholder="예: 입구 전경, 메뉴 클로즈업, 창가 자리에서 촬영한 영상",
            key=f"{content_type}_notes",
        )

        if st.button(
            f"🔎 {content_type} 콘텐츠 생성하기",
            use_container_width=True,
            key=f"{content_type}_button",
        ):
            if not entity:
                st.warning(f"'{config['entity_label']}'를 입력해 주세요.")
            elif client is None:
                st.error("Streamlit Secrets에 OPENAI_API_KEY를 설정해 주세요.")
            else:
                details = {
                    "entity": entity,
                    "location": location or "정보 없음",
                    "period": period or "정보 없음",
                    "companions": companions or "정보 없음",
                    "experience": experience or "정보 없음",
                    "items": items or "정보 없음",
                    "route": route or "정보 없음",
                    "cost": cost or "정보 없음",
                    "notes": notes or "정보 없음",
                    "tone": tone,
                }
                with st.spinner("최신 운영 정보와 여행 후기를 확인해 콘텐츠를 작성하고 있어요..."):
                    try:
                        st.markdown("---")
                        st.markdown(generate_content(build_prompt(content_type, details)))
                    except Exception as error:
                        st.error(f"콘텐츠 생성 중 오류가 발생했어요: {error}")
