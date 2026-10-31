import streamlit as st
import pandas as pd
import math

st.set_page_config(
    page_title="2026年11月 Honda 銷售條件試算",
    page_icon="🚗",
    layout="centered"
)

st.markdown("""
<style>
.stApp { background-color: #f7f7f7; }
.honda-header {
    background: linear-gradient(135deg, #cc0000 0%, #990000 100%);
    color: white;
    padding: 20px 28px 16px 28px;
    border-radius: 14px;
    margin-bottom: 20px;
}
.honda-header h1 { color: white; font-size: 22px; font-weight: 700; margin: 0 0 4px 0; }
.honda-header p  { color: rgba(255,255,255,0.8); font-size: 12px; margin: 0; }
.metric-row { display: flex; gap: 10px; margin: 14px 0; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 130px;
    background: white;
    border-radius: 12px;
    padding: 12px 14px;
    border: 1px solid #ebebeb;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    text-align: center;
}
.metric-card .m-label { font-size: 10px; color: #999; margin-bottom: 5px; }
.metric-card .m-value { font-size: 20px; font-weight: 700; color: #cc0000; }
.metric-card .m-sub   { font-size: 10px; color: #aaa; margin-top: 3px; }
.metric-card.best { border-color: #cc0000; background: #fff8f8; }
.metric-card.htw  { border-color: #2196f3; background: #f0f7ff; }
.metric-card.htw .m-value { color: #1565c0; }
.section-label {
    font-size: 13px; font-weight: 700; color: #333;
    margin: 14px 0 8px 0; padding-left: 10px;
    border-left: 3px solid #cc0000;
}
.htw-box {
    background: #e3f2fd;
    border: 1px solid #90caf9;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 12px;
    color: #1565c0;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ── 頂部標題 ─────────────────────────────────────────────
st.markdown("""
<div class="honda-header">
  <h1>🚗 2026年11月 Honda 銷售條件試算</h1>
  <p>內促 ＋ SP銷售支援金 ＋ HTW銷售顧問獎勵（累點制）＋ 備註1車險獎勵　｜　領牌期間 2026/11/01–11/30</p>
</div>
""", unsafe_allow_html=True)

# ── 篩選器 ───────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    tier = st.radio(
        "① 各車型銷售台數（內促門檻）",
        ["1～3 台", "4 台以上"],
        horizontal=True,
        index=1
    )
    note1_option = st.radio(
        "③ 上月首年車體續保率（備註1，取9月成績）",
        ["60% 以上 → +7,000", "低於 60% → +3,000", "無母數（一年以下）→ +5,000", "無母數（一年以上）→ +3,000"]
    )

with col2:
    htw_hev = st.number_input(
        "② HTW e:HEV 台數（不含 PRELUDE，每台 2 點）",
        min_value=0, value=4, step=1
    )
    htw_petrol = st.number_input(
        "　 HTW 汽油/進口 台數（每台 1 點）",
        min_value=0, value=0, step=1
    )

# ── HTW 累點計算 ──────────────────────────────────────────
total_points   = htw_hev * 2 + htw_petrol
total_htw_cars = htw_hev + htw_petrol  # 非PRELUDE台數

if total_points >= 11:
    htw_rate, htw_tier_label = 6500, "累11點以上 → 每點 $6,500"
elif total_points >= 8:
    htw_rate, htw_tier_label = 4500, "累8~10點 → 每點 $4,500"
elif total_points >= 5:
    htw_rate, htw_tier_label = 2500, "累5~7點 → 每點 $2,500"
else:
    htw_rate, htw_tier_label = 0, "未達5點（不發放）"

total_htw   = total_points * htw_rate
htw_per_car = round(total_htw / total_htw_cars) if total_htw_cars > 0 else 0

if total_points > 0:
    st.markdown(f'<div class="htw-box">📊 HTW 累計 <strong>{total_points} 點</strong>（e:HEV {htw_hev}台×2 ＋ 其他 {htw_petrol}台×1）　→　{htw_tier_label}　→　月總 HTW <strong>${total_htw:,}</strong>　→　均攤每台 <strong>${htw_per_car:,}</strong>（共{total_htw_cars}台）</div>', unsafe_allow_html=True)

# ── 備註1 ────────────────────────────────────────────────
note1_map = {
    "60% 以上 → +7,000":        7000,
    "低於 60% → +3,000":        3000,
    "無母數（一年以下）→ +5,000": 5000,
    "無母數（一年以上）→ +3,000": 3000,
}
note1 = note1_map[note1_option]

# ── 備註2 & 備註3 ─────────────────────────────────────────
tg1, tg2 = st.columns(2)
with tg1:
    note2_on = st.toggle(
        "④ 備註2：現訂交庫存車（每台 +2,000）",
        value=True,
        help="11月底清空11月前庫存，CR-V庫存車再+3,000"
    )
with tg2:
    note2_crv_extra = st.toggle(
        "　 備註2 CR-V 清空庫存（CR-V 再 +3,000）",
        value=True,
        help="清空11月前CR-V庫存，每台CR-V額外+3,000"
    ) if note2_on else False

note3_option = st.select_slider(
    "⑤ 備註3：本月現訂交台數（CR-V e:HEV P 加給）",
    options=["未達5台（無加給）", "5台（+2,000/台）", "6台（+5,000/台）", "7台以上（+8,000/台）"],
    value="7台以上（+8,000/台）"
)
note3_crv_p_map = {
    "未達5台（無加給）": 0,
    "5台（+2,000/台）": 2000,
    "6台（+5,000/台）": 5000,
    "7台以上（+8,000/台）": 8000,
}
note3_crv_p = note3_crv_p_map[note3_option]

is_high  = (tier == "4 台以上")
n2_base  = 2000 if note2_on else 0

# ── 車型資料 ─────────────────────────────────────────────
# is_crv=True   → 備注2 CR-V加給適用
# is_prelude=True → HTW不計（PRELUDE不計）
# note5=True    → CIVIC備注5預接獎勵+5,000
# crv_p=True    → 備注3 CR-V e:HEV P加給適用
car_data = [
    {"section":"PRELUDE","model":"e:HEV 26'年",    "nL":10000,"nH":10000,"sp":0,    "sp_note":"無",              "is_prelude":True, "is_crv":False,"crv_p":False,"note5":False},
    {"section":"CIVIC",  "model":"e:HEV 26'年",    "nL":0,    "nH":0,   "sp":0,    "sp_note":"無（上市發佈）",   "is_prelude":False,"is_crv":False,"crv_p":False,"note5":True},
    {"section":"ZR-V",   "model":"e:HEV 26'年",    "nL":10000,"nH":15000,"sp":6000,"sp_note":"B案",             "is_prelude":False,"is_crv":False,"crv_p":False,"note5":False},
    {"section":"HR-V",   "model":"S",              "nL":19000,"nH":21000,"sp":15000,"sp_note":"F案",            "is_prelude":False,"is_crv":False,"crv_p":False,"note5":False},
    {"section":"HR-V",   "model":"e:HEV S",        "nL":23000,"nH":25000,"sp":17000,"sp_note":"F案",            "is_prelude":False,"is_crv":False,"crv_p":False,"note5":False},
    {"section":"HR-V",   "model":"e:HEV P",        "nL":25000,"nH":27000,"sp":27000,"sp_note":"F案",            "is_prelude":False,"is_crv":False,"crv_p":False,"note5":False},
    {"section":"FIT",    "model":"Home",            "nL":37000,"nH":37000,"sp":10000,"sp_note":"D案",            "is_prelude":False,"is_crv":False,"crv_p":False,"note5":False},
    {"section":"FIT",    "model":"e:HEV",           "nL":41000,"nH":41000,"sp":20000,"sp_note":"D案",            "is_prelude":False,"is_crv":False,"crv_p":False,"note5":False},
    {"section":"CR-V",   "model":"e:HEV S",        "nL":22000,"nH":24000,"sp":27000,"sp_note":"D案",            "is_prelude":False,"is_crv":True, "crv_p":False,"note5":False},
    {"section":"CR-V",   "model":"e:HEV P",        "nL":22000,"nH":24000,"sp":19000,"sp_note":"C案",            "is_prelude":False,"is_crv":True, "crv_p":True, "note5":False},
    {"section":"CR-V",   "model":"VTi-S / S",      "nL":15000,"nH":15000,"sp":5000, "sp_note":"A案",            "is_prelude":False,"is_crv":True, "crv_p":False,"note5":False},
]

# ── 計算 ─────────────────────────────────────────────────
totals, rows = [], []
for car in car_data:
    neicu     = car["nH"] if is_high else car["nL"]
    sp        = car["sp"]
    htw_val   = 0 if car["is_prelude"] else htw_per_car
    n1        = note1
    n2        = n2_base + (3000 if (note2_on and note2_crv_extra and car["is_crv"]) else 0)
    n3        = note3_crv_p if car["crv_p"] else 0
    n5        = 5000 if car["note5"] else 0

    # CIVIC 內促TBD
    if car["note5"]:
        neicu_label = "待公佈"
        total = sp + htw_val + n1 + n2 + n5
    else:
        neicu_label = f"${neicu:,}"
        total = neicu + sp + htw_val + n1 + n2 + n3

    totals.append(total)

    sp_display  = f"${sp:,}（{car['sp_note']}）" if sp > 0 else f"$0（{car['sp_note']}）"
    htw_display = "—（PRELUDE不計）" if car["is_prelude"] else f"${htw_val:,}"
    n2_display  = f"+${n2:,}" if n2 > 0 else "—"
    n3_display  = f"+${n3:,}" if n3 > 0 else ""
    n5_display  = "+$5,000（備5）" if n5 > 0 else ""

    rows.append({
        "車系":            car["section"],
        "車型":            car["model"],
        "內促":            neicu_label,
        "SP最高現金":      sp_display,
        "HTW均攤":         htw_display,
        "備註1":           f"+${n1:,}",
        "備註2":           n2_display,
        "每台合計（最高）": ("待公佈+" if car["note5"] else "") + f"${total:,}",
        "_total":          total,
    })

max_total = max(totals)
max_car   = car_data[totals.index(max_total)]

# ── 指標卡片 ─────────────────────────────────────────────
st.markdown(f"""
<div class="metric-row">
  <div class="metric-card htw">
    <div class="m-label">HTW 月總額</div>
    <div class="m-value">${total_htw:,}</div>
    <div class="m-sub">{total_points}點 × ${htw_rate:,}</div>
  </div>
  <div class="metric-card htw">
    <div class="m-label">HTW 均攤/台</div>
    <div class="m-value">${htw_per_car:,}</div>
    <div class="m-sub">÷ {total_htw_cars}台</div>
  </div>
  <div class="metric-card">
    <div class="m-label">備註1 每台加給</div>
    <div class="m-value">+${note1:,}</div>
    <div class="m-sub">{'60%以上' if note1==7000 else '低於60%' if '低於' in note1_option else '無母數一年以下' if '一年以下' in note1_option else '無母數一年以上'}</div>
  </div>
  <div class="metric-card best">
    <div class="m-label">🏆 本月最高獎金車型</div>
    <div class="m-value">${max_total:,}</div>
    <div class="m-sub">{max_car['section']} {max_car['model']}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 明細表格 ─────────────────────────────────────────────
st.markdown('<div class="section-label">各車型每台獎金明細</div>', unsafe_allow_html=True)

df = pd.DataFrame(rows).drop(columns=["_total"])

def style_table(df_in):
    def row_style(row):
        total_str = row["每台合計（最高）"].replace("待公佈+","").replace("$","").replace(",","")
        try:
            if int(total_str) == max_total:
                return ["background-color:#fff0f0; font-weight:bold; color:#cc0000"] * len(row)
        except:
            pass
        return [""] * len(row)
    return df_in.style.apply(row_style, axis=1)

st.dataframe(
    style_table(df),
    use_container_width=True,
    hide_index=True,
    height=430
)

# ── 計算式展開 ────────────────────────────────────────────
with st.expander("📋 查看各車型詳細計算式"):
    for car, total in zip(car_data, totals):
        neicu   = car["nH"] if is_high else car["nL"]
        htw_val = 0 if car["is_prelude"] else htw_per_car
        n2      = n2_base + (3000 if (note2_on and note2_crv_extra and car["is_crv"]) else 0)
        n3      = note3_crv_p if car["crv_p"] else 0
        n5      = 5000 if car["note5"] else 0
        color   = "#cc0000" if total == max_total else "#333"
        bold    = "700" if total == max_total else "400"

        if car["note5"]:
            formula = f"內促 待公佈 ＋ SP ${car['sp']:,} ＋ HTW均攤 ${htw_val:,} ＋ 備1 ${note1:,} ＋ 備2 ${n2:,} ＋ 備5 $5,000 ＝ 待公佈+${total:,}"
        else:
            parts = [f"內促 ${neicu:,}", f"SP ${car['sp']:,}", f"HTW ${htw_val:,}", f"備1 ${note1:,}"]
            if n2: parts.append(f"備2 ${n2:,}")
            if n3: parts.append(f"備3 ${n3:,}")
            formula = " ＋ ".join(parts) + f" ＝ ${total:,}"

        st.markdown(
            f"<span style='color:{color};font-weight:{bold}'>"
            f"**{car['section']} {car['model']}**　{formula}"
            f"</span>",
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("※ HTW 為累點制：e:HEV=2點/台、汽油/進口=1點/台（PRELUDE不計）。累5-7點→$2,500/點；累8-10點→$4,500/點；累11點以上→$6,500/點。")
st.caption("※ SP 取各方案最高現金選項。CIVIC/PRELUDE SP本月無現金（延保為加價購）。CR-V VTi-S/S A案需加選延長保固。")
st.caption("※ 備註1 取2026年9月成績。ZR-V 另有乙式保險+$3,000獎勵（未含於本表）。")
st.caption("※ 備註2：現訂交庫存車每台+2,000；11月底清空11月前庫存 → CR-V 再+3,000。")
st.caption("※ 備註3：現訂交5台+→CR-V e:HEV P每台+2,000；6台+→+5,000；7台+→+8,000（取最高適用）。")
st.caption("※ 備註5：CIVIC 上市前準備預接獎勵每台+5,000（需12/31前領牌），內促待上市公佈。")
st.caption("※ 本試算表僅供參考，實際獎金依 Honda Taiwan 官方公告為準。")
