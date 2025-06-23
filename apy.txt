import streamlit as st

# 預設推薦邏輯
recommendation_rules = {
    "關節保養": ["UC-II", "薑黃素", "葡萄糖胺", "MSM"],
    "睡眠品質": ["GABA", "色胺酸", "褪黑激素"],
    "美容抗老": ["膠原蛋白", "維生素C", "玻尿酸"],
    "免疫力提升": ["維生素C", "鋅", "益生菌"],
    "心血管保養": ["魚油", "納豆激酶", "紅麴"]
}

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

        # 排除條件提示
        warnings = []
        if pregnant and "褪黑激素" in recommended:
            recommended.remove("褪黑激素")
            warnings.append("⚠️ 褪黑激素孕婦不建議使用")
        if chronic and "紅麴" in recommended:
            recommended.remove("紅麴")
            warnings.append("⚠️ 紅麴不適合有肝臟或慢性病問題者")

        st.write("\n".join(f"- {r}" for r in recommended))

        if warnings:
            st.markdown("---")
            st.warning("\n".join(warnings))
