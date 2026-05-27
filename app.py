import streamlit as st

st.set_page_config(
    page_title="2026年5月 Honda 銷售條件試算",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 2026年5月 Honda 銷售條件試算")
st.caption("內促 ＋ SP銷售支援金 ＋ HTW銷售顧問獎勵 ＋ 備註1車險獎勵　｜　領牌期間 2026/05/01–05/31")

st.divider()

# ── 篩選器 ──────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    tier = st.radio(
        "① 各車型銷售台數（內促門檻）",
        options=["1～2 台", "3 台以上"],
        horizontal=True
    )
    hrv_option = st.radio(
        "③ 本月有無販售 HR-V（HTW）",
        options=["有 HR-V", "無 HR-V"],
        horizontal=True
    )

with col2:
    total_sales = st.radio(
        "② 本月全車系總銷售台數（HTW）",
        options=["1台", "2台", "3台", "4台以上"],
        horizontal=True,
        index=3
    )
    note1_option = st.radio(
        "④ 上月首年車體續保率（備註1）",
        options=["60% 以上 → +7,000", "低於 60% → +3,000", "無續保（一年以下）→ +5,000"],
        horizontal=False
    )

st.divider()

# ── 計算邏輯 ──────────────────────────────────────────────
dm_table = {
    "有 HR-V":  {"1台": 5000, "2台": 6000, "3台": 7000, "4台以上": 8000},
    "無 HR-V":  {"1台": 3000, "2台": 4000, "3台": 5000, "4台以上": 6000},
}
dm = dm_table[hrv_option][total_sales]

note1_map = {
    "60% 以上 → +7,000": 7000,
    "低於 60% → +3,000": 3000,
    "無續保（一年以下）→ +5,000": 5000,
}
note1 = note1_map[note1_option]

is_high_tier = (tier == "3 台以上")

car_data = [
    {"section": "CIVIC", "model": "e:HEV 26'式樣", "nL": 31000, "nH": 39000, "sp": 0,     "sp_note": "延長保固（無現金）"},
    {"section": "HR-V",  "model": "S",              "nL": 12000, "nH": 15000, "sp": 25000, "sp_note": ""},
    {"section": "HR-V",  "model": "e:HEV S",        "nL": 14000, "nH": 17000, "sp": 30000, "sp_note": ""},
    {"section": "HR-V",  "model": "e:HEV P",        "nL": 16000, "nH": 19000, "sp": 30000, "sp_note": ""},
    {"section": "FIT",   "model": "Home",            "nL": 38000, "nH": 38000, "sp": 20000, "sp_note": ""},
    {"section": "FIT",   "model": "e:HEV",           "nL": 42000, "nH": 42000, "sp": 30000, "sp_note": ""},
]

# ── 摘要指標 ──────────────────────────────────────────────
totals = []
for car in car_data:
    neicu = car["nH"] if is_high_tier else car["nL"]
    total = neicu + car["sp"] + dm + note1
    totals.append(total)

max_total = max(totals)
max_car = car_data[totals.index(max_total)]

m1, m2, m3 = st.columns(3)
m1.metric("DM 每台單獎", f"${dm:,}")
m2.metric("備註1 每台加給", f"+${note1:,}")
m3.metric("本月最高獎金車型", f"${max_total:,}", f"{max_car['section']} {max_car['model']}")

st.divider()

# ── 明細表格 ──────────────────────────────────────────────
st.subheader("各車型每台獎金明細")

import pandas as pd

rows = []
prev_section = None
for car in car_data:
    neicu = car["nH"] if is_high_tier else car["nL"]
    sp = car["sp"]
    total = neicu + sp + dm + note1

    sp_display = f"${sp:,}" if sp > 0 else f"$0（{car['sp_note']}）"

    rows.append({
        "車系": car["section"],
        "車型": car["model"],
        "內促": f"${neicu:,}",
        "SP最高現金": sp_display,
        "HTW": f"${dm:,}",
        "備註1": f"+${note1:,}",
        "每台合計（最高）": f"${total:,}",
    })

df = pd.DataFrame(rows)

# 用顏色標示最高獎金列
def highlight_max(row):
    total_val = int(row["每台合計（最高）"].replace("$", "").replace(",", ""))
    if total_val == max_total:
        return ["background-color: #e1f5ee"] * len(row)
    return [""] * len(row)

styled = df.style.apply(highlight_max, axis=1)
st.dataframe(styled, use_container_width=True, hide_index=True)

# ── 備計算式展開區 ──────────────────────────────────────────
with st.expander("查看各車型詳細計算式"):
    for car in car_data:
        neicu = car["nH"] if is_high_tier else car["nL"]
        sp = car["sp"]
        total = neicu + sp + dm + note1
        st.markdown(
            f"**{car['section']} {car['model']}**　"
            f"內促 ${neicu:,} ＋ SP ${sp:,} ＋ DM ${dm:,} ＋ 備註1 ${note1:,} ＝ **${total:,}**"
        )

st.divider()
st.caption("※ SP取各方案最高現金選項（E/D案）。CIVIC SP僅延長保固（無現金支援金）。")
st.caption("※ 備註1為新車投保乙式＋代步金險之獎勵，每台適用。")
st.caption("※ 本試算表僅供參考，實際獎金依 Honda Taiwan 官方公告為準。")
