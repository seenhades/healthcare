import streamlit as st

# 預設推薦邏輯及成分說明
recommendation_rules = {
    "關節保養": ["UC-II", "薑黃素", "葡萄糖胺", "MSM"],
    "睡眠品質": ["GABA", "色胺酸", "褪黑激素"],
    "美容抗老": ["膠原蛋白", "維生素C", "玻尿酸"],
    "免疫力提升": ["維生素C", "鋅", "益生菌"],
    "心血管保養": ["魚油", "納豆激酶", "紅麴"],
    "排便不順/腸胃保健": ["益生菌", "洋車前子殼", "乳酸菌", "酵素"],
    "視力保健": ["葉黃素", "玉米黃素", "蝦紅素", "維生素A"],
    "血糖控制": ["苦瓜胜肽", "鉻", "肉桂萃取", "白腎豆萃取"],
    "過敏體質": ["益生菌", "維生素C", "魚油", "螺旋藻"]
}

supplement_descriptions = {
    "UC-II": "幫助軟骨修復，減緩關節疼痛與僵硬。",
    "薑黃素": "強效抗發炎成分，改善關節不適。",
    "葡萄糖胺": "促進軟骨合成，維持關節健康。",
    "MSM": "減輕關節炎症狀，改善靈活度。",
    "GABA": "天然鎮靜劑，幫助放鬆與睡眠。",
    "色胺酸": "促進血清素生成，改善睡眠品質。",
    "褪黑激素": "調節生理時鐘，幫助入眠。",
    "膠原蛋白": "維持皮膚彈性，減緩老化。",
    "維生素C": "抗氧化，促進膠原蛋白合成，提升免疫力。",
    "玻尿酸": "保濕滋潤皮膚與關節軟骨。",
    "鋅": "增強免疫系統功能，促進傷口癒合。",
    "益生菌": "維持腸道菌叢平衡，促進消化健康。",
    "魚油": "富含Omega-3脂肪酸，降低發炎反應。",
    "納豆激酶": "促進血液循環，降低血栓風險。",
    "紅麴": "調節血脂，有助心血管健康。",
    "洋車前子殼": "促進腸道蠕動，改善便秘。",
    "乳酸菌": "幫助消化與免疫調節。",
    "酵素": "分解食物，提升吸收效率。",
    "葉黃素": "保護視網膜，預防黃斑部病變。",
    "玉米黃素": "抗氧化，保護眼睛健康。",
    "蝦紅素": "強效抗氧化，減緩視力退化。",
    "維生素A": "維持視力正常，支持免疫系統。",
    "苦瓜胜肽": "幫助調節血糖平衡。",
    "鉻": "促進胰島素作用，穩定血糖。",
    "肉桂萃取": "改善胰島素敏感性，調節血糖。",
    "白腎豆萃取": "抑制澱粉分解，幫助控糖。",
    "螺旋藻": "天然抗氧化，提升免疫力，減輕過敏反應。",
    # 新增個人化調整中用到的成分
    "鈣質": "強化骨骼結構，預防骨質疏鬆。",
    "維生素D": "促進鈣吸收，維持骨骼健康。",
    "黑升麻": "緩解女性更年期症狀，調節荷爾蒙。",
    "大豆異黃酮": "植物性雌激素，有助女性更年期健康。"
}

def adjust_recommendations(recommended, age, gender, pregnant, chronic):
    warnings = []

    # 老年人加強骨骼保養
    if age >= 65:
        recommended.add("鈣質")
        recommended.add("維生素D")

    # 女性更年期（45-60歲女性）建議骨骼與荷爾蒙調節
    if gender == "女" and 45 <= age <= 60:
        recommended.add("黑升麻")
        recommended.add("大豆異黃酮")

    # 孕婦避免特定成分
    if pregnant:
        if "褪黑激素" in recommended:
            recommended.remove("褪黑激素")
            warnings.append("⚠️ 褪黑激素孕婦不建議使用")
        # 可在此擴充其他孕婦禁忌

    # 慢性病避免紅麴
    if chronic and "紅麴" in recommended:
        recommended.remove("紅麴")
        warnings.append("⚠️ 紅麴不適合有肝臟或慢性病問題者")

    return recommended, warnings


st.title("🧬 個人化保健食品建議問卷")

# 基本資料輸入
age = st.number_input("請輸入您的年齡：", min_value=1, max_value=120, value=40)
gender = st.radio("請選擇您的性別：", ["男", "女"])

# 選擇健康目標
health_goals = st.multiselect(
    "您目前最關注的健康面向（可複選）：",
    list(recommendation_rules.keys())
)

# 特殊狀況
pregnant = st.checkbox("目前懷孕或哺乳中")
chronic = st.checkbox("有慢性疾病（如糖尿病、高血壓）")

# 顯示建議
if st.button("🔍 產生建議"):
    if not health_goals:
        st.warning("請先選擇至少一個健康面向")
    else:
        st.subheader("✅ 根據您的情況，建議補充以下成分：")
        recommended = set()
        for goal in health_goals:
            for item in recommendation_rules[goal]:
                recommended.add(item)

        # 依年齡、性別、特殊狀況調整推薦
        recommended, warnings = adjust_recommendations(recommended, age, gender, pregnant, chronic)

        # 顯示推薦成分與說明
        for supp in recommended:
            desc = supplement_descriptions.get(supp, "無說明資料")
            st.markdown(f"**{supp}** － {desc}")

        if warnings:
            st.markdown("---")
            st.warning("\n".join(warnings))
