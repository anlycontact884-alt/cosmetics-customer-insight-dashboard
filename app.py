import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="Customer Insight Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# STYLE — mô phỏng bố cục dashboard mẫu
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background: #EEF1F4;
}

.block-container {
    max-width: 1500px;
    padding: 18px 22px 30px 22px;
}

/* Header */
.dashboard-header {
    background: #17375E;
    color: white;
    border-radius: 3px;
    padding: 19px 24px 16px 24px;
    margin-bottom: 10px;
    box-shadow: 0 3px 8px rgba(0,0,0,.12);
}

.dashboard-title {
    font-size: 30px;
    line-height: 1.1;
    font-weight: 800;
    letter-spacing: -.3px;
}

.dashboard-subtitle {
    margin-top: 7px;
    font-size: 13px;
    color: #DCE8F5;
    font-weight: 500;
}

/* KPI */
.kpi-wrap {
    padding: 0;
}

.kpi {
    height: 116px;
    border-radius: 2px;
    padding: 13px 15px;
    color: white;
    box-shadow: 0 3px 8px rgba(0,0,0,.13);
}

.kpi-label {
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    margin-top: 13px;
    line-height: 1;
}

.kpi-note {
    margin-top: 8px;
    font-size: 10.5px;
    opacity: .93;
}

.kpi-navy { background:#17375E; }
.kpi-green { background:#579B6A; }
.kpi-red { background:#D9534F; }
.kpi-yellow { background:#E3B844; }
.kpi-darkred { background:#C94E4B; }
.kpi-darkgreen { background:#68A875; }

/* Panel */
.panel {
    background: #FFFFFF;
    border: 1px solid #D6DCE2;
    border-radius: 2px;
    box-shadow: 0 3px 9px rgba(0,0,0,.08);
    padding: 7px 8px 4px 8px;
    height: 100%;
}

.panel-title {
    font-size: 15px;
    font-weight: 800;
    color: #263238;
    padding: 2px 4px 4px 4px;
    border-bottom: 1px solid #E6E9ED;
    margin-bottom: 2px;
}

/* Insights */
.insight {
    background: #FFFFFF;
    border: 1px solid #D6DCE2;
    border-radius: 2px;
    padding: 13px 15px;
    min-height: 108px;
    box-shadow: 0 2px 6px rgba(0,0,0,.06);
}

.insight-title {
    color: #17375E;
    font-weight: 800;
    font-size: 13px;
    margin-bottom: 7px;
}

.insight-text {
    color: #4B5563;
    font-size: 11.5px;
    line-height: 1.55;
}

/* Table */
div[data-testid="stDataFrame"] {
    border: 1px solid #D6DCE2;
}

/* Hide Streamlit chrome */
#MainMenu {visibility:hidden;}
header {visibility:hidden;}
footer {visibility:hidden;}

/* Remove excessive gaps */
div[data-testid="column"] {
    padding-left: 4px;
    padding-right: 4px;
}

.stPlotlyChart {
    margin-top: -2px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA
# ============================================================
FILE = "PowerBI_Cosmetics_Customer_Insight_10Topics.xlsx"

@st.cache_data
def load_data():
    topic = pd.read_excel(FILE, sheet_name="Topic_Sentiment")
    sentiment = pd.read_excel(FILE, sheet_name="Sentiment_Data")
    top10 = pd.read_excel(FILE, sheet_name="Top10_Topics")
    brand = pd.read_excel(FILE, sheet_name="Brand_Analysis")
    return topic, sentiment, top10, brand

try:
    topic_df, sentiment_df, top10_df, brand_df = load_data()
except FileNotFoundError:
    st.error(f"Không tìm thấy {FILE}. Hãy đặt file Excel cùng thư mục với app.py.")
    st.stop()

# Keep exactly 10 topics
top10_df = top10_df.sort_values("Rank").head(10).copy()

# Normalize topic names for the chart
if "Chủ đề" not in top10_df.columns:
    if "Topic Name" in top10_df.columns:
        top10_df["Chủ đề"] = top10_df["Topic Name"]
    elif "topic_name" in top10_df.columns:
        top10_df["Chủ đề"] = top10_df["topic_name"]

# Calculate rates
top10_df["Negative Rate"] = top10_df["Negative"] / top10_df["Total"]
top10_df["Neutral Rate"] = top10_df["Neutral"] / top10_df["Total"]
top10_df["Positive Rate"] = top10_df["Positive"] / top10_df["Total"]

# Sentiment totals
total_reviews = int(sentiment_df["Count"].sum())
negative_count = int(sentiment_df.loc[sentiment_df["Sentiment"]=="Negative", "Count"].sum())
neutral_count = int(sentiment_df.loc[sentiment_df["Sentiment"]=="Neutral", "Count"].sum())
positive_count = int(sentiment_df.loc[sentiment_df["Sentiment"]=="Positive", "Count"].sum())

negative_rate = negative_count / total_reviews
neutral_rate = neutral_count / total_reviews
positive_rate = positive_count / total_reviews

# Dashboard thresholds
pain_threshold = 0.30
strength_threshold = 0.80
pain_topics = top10_df[top10_df["Negative Rate"] >= pain_threshold]
strength_topics = top10_df[top10_df["Positive Rate"] >= strength_threshold]

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">BẢNG ĐIỀU HÀNH THẤU HIỂU KHÁCH HÀNG</div>
    <div class="dashboard-subtitle">
        PHÂN TÍCH 18.754 ĐÁNH GIÁ NGÀNH MỸ PHẨM
        &nbsp;•&nbsp; CẢM XÚC
        &nbsp;•&nbsp; CHỦ ĐỀ
        &nbsp;•&nbsp; CUSTOMER INSIGHTS
        &nbsp;•&nbsp; HỖ TRỢ QUYẾT ĐỊNH
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# KPI ROW
# ============================================================
kpis = [
    ("TỔNG ĐÁNH GIÁ", f"{total_reviews:,}".replace(",", "."), "quy mô dữ liệu", "kpi-navy"),
    ("TÍCH CỰC", f"{positive_rate:.1%}", "khách hàng phản hồi tích cực", "kpi-green"),
    ("TIÊU CỰC", f"{negative_rate:.1%}", "nhóm cần theo dõi", "kpi-red"),
    ("TRUNG TÍNH", f"{neutral_rate:.1%}", "chưa hình thành xu hướng", "kpi-yellow"),
    ("ĐIỂM ĐAU", f"{len(pain_topics)}", f"topic có Negative ≥ {pain_threshold:.0%}", "kpi-darkred"),
    ("ĐIỂM MẠNH", f"{len(strength_topics)}", f"topic có Positive ≥ {strength_threshold:.0%}", "kpi-darkgreen")
]

cols = st.columns(6, gap="small")
for col, (label, value, note, css) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi {css}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ============================================================
# PLOT HELPERS
# ============================================================
def clean_layout(fig, height=330):
    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=10, r=18, t=48, b=28),
        font=dict(family="Inter", color="#374151", size=11),
        title_font=dict(size=15, color="#263238"),
        hoverlabel=dict(bgcolor="white", font_size=11),
        legend=dict(font=dict(size=10))
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#D9DEE5",
        zeroline=False,
        linecolor="#C8CED5"
    )
    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#C8CED5"
    )
    return fig

def panel_title(title):
    return f'<div class="panel-title">{title}</div>'

# ============================================================
# ROW 1
# ============================================================
r1a, r1b, r1c = st.columns([1.05, 1.45, 1.05], gap="small")

# Donut
with r1a:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(panel_title("Cơ cấu cảm xúc khách hàng"), unsafe_allow_html=True)

    donut = px.pie(
        sentiment_df,
        names="Sentiment",
        values="Count",
        hole=.60,
        color="Sentiment",
        color_discrete_map={
            "Negative":"#D9534F",
            "Neutral":"#E5B84B",
            "Positive":"#70AD47"
        }
    )
    donut.update_traces(
        textinfo="percent",
        textfont_size=11,
        marker=dict(line=dict(color="white", width=2)),
        hovertemplate="%{label}: %{value:,} (%{percent})<extra></extra>"
    )
    donut.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-.08,
            x=.5,
            xanchor="center",
            font=dict(size=10)
        ),
        margin=dict(l=4,r=4,t=4,b=20),
        height=300,
        paper_bgcolor="white",
        plot_bgcolor="white",
        annotations=[dict(
            text=f"<b>{total_reviews:,}</b><br><span style='font-size:9px'>REVIEWS</span>",
            x=.5, y=.5, showarrow=False,
            font=dict(size=18, color="#17375E")
        )]
    )
    st.plotly_chart(donut, use_container_width=True, config={"displayModeBar":False})
    st.markdown('</div>', unsafe_allow_html=True)

# Top 10
with r1b:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(panel_title("10 chủ đề có nhiều phản hồi nhất"), unsafe_allow_html=True)

    df = top10_df.sort_values("Total", ascending=True)
    fig = px.bar(
        df,
        x="Total",
        y="Chủ đề",
        orientation="h",
        text="Total",
        color_discrete_sequence=["#315B8C"]
    )
    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}: %{x:,} review<extra></extra>"
    )
    fig.update_layout(
        xaxis_title="Số review",
        yaxis_title="",
        margin=dict(l=8,r=42,t=4,b=28),
        height=300
    )
    fig.update_xaxes(showgrid=True, gridcolor="#D9DEE5")
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    st.markdown('</div>', unsafe_allow_html=True)

# Pain points
with r1c:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(panel_title("Điểm đau cần ưu tiên xem xét"), unsafe_allow_html=True)

    df = top10_df.sort_values("Negative Rate", ascending=True)
    fig = px.bar(
        df,
        x="Negative Rate",
        y="Chủ đề",
        orientation="h",
        text="Negative Rate",
        color_discrete_sequence=["#D9534F"]
    )
    fig.update_traces(
        texttemplate="%{text:.1%}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}: %{x:.1%} tiêu cực<extra></extra>"
    )
    fig.update_layout(
        xaxis_title="Tỷ lệ tiêu cực",
        yaxis_title="",
        xaxis_tickformat=".0%",
        margin=dict(l=8,r=42,t=4,b=28),
        height=300
    )
    fig.update_xaxes(showgrid=True, gridcolor="#D9DEE5")
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# ROW 2
# ============================================================
r2a, r2b, r2c = st.columns([1.05, 1.45, 1.05], gap="small")

# Strength
with r2a:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(panel_title("Điểm mạnh nổi bật"), unsafe_allow_html=True)

    df = top10_df.sort_values("Positive Rate", ascending=True)
    fig = px.bar(
        df,
        x="Positive Rate",
        y="Chủ đề",
        orientation="h",
        text="Positive Rate",
        color_discrete_sequence=["#5B9E6F"]
    )
    fig.update_traces(
        texttemplate="%{text:.1%}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}: %{x:.1%} tích cực<extra></extra>"
    )
    fig.update_layout(
        xaxis_title="Tỷ lệ tích cực",
        yaxis_title="",
        xaxis_tickformat=".0%",
        margin=dict(l=8,r=42,t=4,b=28),
        height=320
    )
    fig.update_xaxes(showgrid=True, gridcolor="#D9DEE5")
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    st.markdown('</div>', unsafe_allow_html=True)

# Sentiment by topic
with r2b:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(panel_title("Cơ cấu cảm xúc trong từng chủ đề"), unsafe_allow_html=True)

    long_df = top10_df[[
        "Chủ đề","Negative Rate","Neutral Rate","Positive Rate"
    ]].melt(
        id_vars="Chủ đề",
        var_name="Sentiment",
        value_name="Rate"
    )

    long_df["Sentiment"] = long_df["Sentiment"].map({
        "Negative Rate":"Tiêu cực",
        "Neutral Rate":"Trung tính",
        "Positive Rate":"Tích cực"
    })

    fig = px.bar(
        long_df,
        x="Rate",
        y="Chủ đề",
        color="Sentiment",
        orientation="h",
        color_discrete_map={
            "Tiêu cực":"#D9534F",
            "Trung tính":"#E5B84B",
            "Tích cực":"#70AD47"
        }
    )
    fig.update_layout(
        barmode="stack",
        xaxis_title="Tỷ lệ",
        yaxis_title="",
        xaxis_tickformat=".0%",
        xaxis_range=[0,1],
        legend=dict(
            orientation="h",
            y=-.13,
            x=.5,
            xanchor="center",
            font=dict(size=10)
        ),
        margin=dict(l=8,r=10,t=4,b=36),
        height=320
    )
    fig.update_xaxes(showgrid=True, gridcolor="#D9DEE5")
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    st.markdown('</div>', unsafe_allow_html=True)

# Brand negative
with r2c:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown(panel_title("Thương hiệu có tỷ lệ tiêu cực cao*"), unsafe_allow_html=True)

    brand_chart_df = (
        brand_df.groupby("brand", as_index=False)
        .agg(Total=("Total","sum"), Negative=("Negative","sum"))
    )
    brand_chart_df["Negative Rate"] = brand_chart_df["Negative"] / brand_chart_df["Total"]
    brand_chart_df = (
        brand_chart_df[brand_chart_df["Total"] >= 30]
        .sort_values("Negative Rate", ascending=False)
        .head(5)
        .sort_values("Negative Rate", ascending=True)
    )

    fig = px.bar(
        brand_chart_df,
        x="Negative Rate",
        y="brand",
        orientation="h",
        text="Negative Rate",
        color_discrete_sequence=["#C0504D"]
    )
    fig.update_traces(
        texttemplate="%{text:.1%}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{y}: %{x:.1%}<extra></extra>"
    )
    fig.update_layout(
        xaxis_title="Tỷ lệ tiêu cực",
        yaxis_title="",
        xaxis_tickformat=".0%",
        margin=dict(l=8,r=42,t=4,b=28),
        height=320
    )
    fig.update_xaxes(showgrid=True, gridcolor="#D9DEE5")
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# INSIGHT STRIP
# ============================================================
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown('<div class="panel-title" style="background:#FFFFFF;padding:10px 12px;border:1px solid #D6DCE2;">CUSTOMER INSIGHTS</div>', unsafe_allow_html=True)

top_pain = top10_df.sort_values("Negative Rate", ascending=False).iloc[0]
top_strength = top10_df.sort_values("Positive Rate", ascending=False).iloc[0]
top_volume = top10_df.sort_values("Total", ascending=False).iloc[0]

ic1, ic2, ic3 = st.columns(3, gap="small")

with ic1:
    st.markdown(f"""
    <div class="insight">
        <div class="insight-title">🔴 ĐIỂM ĐAU NỔI BẬT</div>
        <div class="insight-text">
            <b>{top_pain["Chủ đề"]}</b> có tỷ lệ tiêu cực
            <b>{top_pain["Negative Rate"]:.1%}</b>, tương ứng
            <b>{int(top_pain["Negative"]):,}</b> phản hồi tiêu cực.
        </div>
    </div>
    """, unsafe_allow_html=True)

with ic2:
    st.markdown(f"""
    <div class="insight">
        <div class="insight-title">🟢 ĐIỂM MẠNH NỔI BẬT</div>
        <div class="insight-text">
            <b>{top_strength["Chủ đề"]}</b> có tỷ lệ tích cực
            <b>{top_strength["Positive Rate"]:.1%}</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)

with ic3:
    st.markdown(f"""
    <div class="insight">
        <div class="insight-title">📊 CHỦ ĐỀ ĐƯỢC QUAN TÂM NHẤT</div>
        <div class="insight-text">
            <b>{top_volume["Chủ đề"]}</b> có
            <b>{int(top_volume["Total"]):,}</b> review,
            chiếm <b>{top_volume["Total"]/total_reviews:.1%}</b> tổng dữ liệu.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# DETAIL TABLE
# ============================================================
with st.expander("Xem chi tiết 10 chủ đề"):
    detail = top10_df[[
        "Rank","Chủ đề","Total","Negative","Neutral","Positive",
        "Negative Rate","Neutral Rate","Positive Rate"
    ]].copy()

    detail.columns = [
        "Rank","Chủ đề","Tổng review","Tiêu cực","Trung tính","Tích cực",
        "Tỷ lệ tiêu cực","Tỷ lệ trung tính","Tỷ lệ tích cực"
    ]

    for c in ["Tỷ lệ tiêu cực","Tỷ lệ trung tính","Tỷ lệ tích cực"]:
        detail[c] = detail[c].map(lambda x: f"{x:.1%}")

    st.dataframe(detail, use_container_width=True, hide_index=True)

st.markdown(
    "<div style='text-align:center;color:#7B8794;font-size:10px;margin-top:12px;'>"
    "Dashboard phân tích sentiment ngành mỹ phẩm • 10 chủ đề chính • Streamlit"
    "</div>",
    unsafe_allow_html=True
)
