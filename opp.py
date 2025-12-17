import streamlit as st
import pandas as pd
import datetime

# --- 1. 앱 기본 설정 ---
st.set_page_config(page_title="삶의 질 척도(WHOQOL-BREF)", layout="centered")

st.title("🌿 삶의 질 척도 (WHOQOL-BREF)")
st.write("지난 2주 동안의 경험을 바탕으로 각 질문에 답해주세요.")
st.markdown("---")

# --- 2. 문항 데이터 정의 ---
questions = [
    (1, "1. 당신의 삶의 질을 어떻게 평가하십니까?", False),
    (2, "2. 당신의 건강 상태에 대해 얼마나 만족하십니까?", False),
    (3, "3. 현재의 신체적 통증이 당신이 해야 할 일을 막는 경우가 있습니까?", True),
    (4, "4. 일상생활을 유지하기 위해 어느 정도 의학적 치료가 필요합니까?", True),
    (5, "5. 인생을 얼마나 즐기고 계십니까?", False),
    (6, "6. 당신의 삶이 어느 정도 의미 있다고 생각하십니까?", False),
    (7, "7. 얼마나 집중을 잘 할 수 있습니까?", False),
    (8, "8. 생활에 필요한 만큼의 돈을 가지고 있습니까?", False),
    (9, "9. 일상생활에 필요한 정보들을 얼마나 쉽게 얻을 수 있습니까?", False),
    (10, "10. 일상생활을 할 수 있는 에너지는 충분합니까?", False),
    (11, "11. 당신의 외모를 있는 그대로 받아들일 수 있습니까?", False),
    (12, "12. 여가 활동을 즐길 기회가 충분합니까?", False),
    (13, "13. 당신이 살고 있는 곳의 주거 환경은 얼마나 좋습니까?", False),
    (14, "14. 의료 서비스 혜택을 받기 쉬운 곳에 살고 있습니까?", False),
    (15, "15. 당신의 신체적인 이동 능력에 대해 만족하십니까?", False),
    (16, "16. 당신의 수면에 대해 만족하십니까?", False),
    (17, "17. 일상생활을 수행하는 능력에 대해 만족하십니까?", False),
    (18, "18. 업무(또는 학업) 능력에 대해 만족하십니까?", False),
    (19, "19. 당신 자신에 대해 얼마나 만족하십니까?", False),
    (20, "20. 대인관계에 대해 얼마나 만족하십니까?", False),
    (21, "21. 성생활에 대해 얼마나 만족하십니까?", False),
    (22, "22. 친구들의 지지에 대해 얼마나 만족하십니까?", False),
    (23, "23. 현재 살고 있는 집의 상태에 만족하십니까?", False),
    (24, "24. 의료 서비스 이용 가능성에 대해 얼마나 만족하십니까?", False),
    (25, "25. 교통수단 이용의 편리성에 대해 얼마나 만족하십니까?", False),
    (26, "26. 우울, 불안, 절망과 같은 부정적인 기분을 얼마나 자주 느낍니까?", True),
]

# --- 3. 설문 입력 폼 ---
with st.form("survey_form"):
    user_name = st.text_input("응답자 성함 (또는 ID)", placeholder="홍길동")
    
    responses = {}
    options = {1: "1점 (전혀 아님/매우 불만족)", 
               2: "2점", 
               3: "3점 (보통)", 
               4: "4점", 
               5: "5점 (매우 많이/매우 만족)"}
    
    # 문항 반복 출력
    for q_num, q_text, is_reverse in questions:
        # index=None 으로 설정하여 초기 선택값을 없앱니다.
        val = st.radio(
            label=q_text,
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: options[x],
            key=f"q_{q_num}",
            horizontal=True,
            index=None
        )
        
        # 값이 선택되지 않았을 때(None)를 대비한 처리
        if val is not None:
            if is_reverse:
                score = 6 - val
            else:
                score = val
        else:
            score = None 
            
        responses[f"Q{q_num}"] = score

    submitted = st.form_submit_button("결과 제출 및 분석")

# --- 4. 결과 계산 및 출력 ---
if submitted:
    # 예외 처리: 이름 누락 확인
    if not user_name:
        st.error("⚠️ 성함을 입력해주세요.")
    # 예외 처리: 답변 누락 확인
    elif None in responses.values():
        st.error("⚠️ 아직 답변하지 않은 문항이 있습니다. 모든 문항에 체크해주세요.")
    else:
        # 영역별 점수 계산
        phy_items = [responses["Q3"], responses["Q4"], responses["Q10"], responses["Q15"], responses["Q16"], responses["Q17"], responses["Q18"]]
        phy_score = (sum(phy_items) / len(phy_items) - 1) * 25
        
        psy_items = [responses["Q5"], responses["Q6"], responses["Q7"], responses["Q11"], responses["Q19"], responses["Q26"]]
        psy_score = (sum(psy_items) / len(psy_items) - 1) * 25
        
        soc_items = [responses["Q20"], responses["Q21"], responses["Q22"]]
        soc_score = (sum(soc_items) / len(soc_items) - 1) * 25
        
        env_items = [responses["Q8"], responses["Q9"], responses["Q12"], responses["Q13"], responses["Q14"], responses["Q23"], responses["Q24"], responses["Q25"]]
        env_score = (sum(env_items) / len(env_items) - 1) * 25
        
        # 결과 보여주기
        st.success(f"✅ {user_name}님의 분석 결과가 생성되었습니다.")
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💪 신체적 영역", f"{phy_score:.1f}점")
        col2.metric("🧠 심리적 영역", f"{psy_score:.1f}점")
        col3.metric("🤝 사회적 영역", f"{soc_score:.1f}점")
        col4.metric("🏡 환경적 영역", f"{env_score:.1f}점")
        
        # 데이터프레임 생성
        result_data = {
            "이름": [user_name],
            "날짜": [datetime.datetime.now().strftime("%Y-%m-%d")],
            "신체적영역": [round(phy_score, 1)],
            "심리적영역": [round(psy_score, 1)],
            "사회적영역": [round(soc_score, 1)],
            "환경적영역": [round(env_score, 1)]
        }
        result_data.update(responses)
        df = pd.DataFrame(result_data)
        
        st.download_button(
            label="📥 결과 엑셀(CSV) 다운로드",
            data=df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'),
            file_name=f"WHOQOL_{user_name}.csv",
            mime="text/csv"
        )