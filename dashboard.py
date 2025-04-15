import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import base64

# --- Toggle Display for Apps ---
SHOW_WEBEX = False  # Change to True to show Webex app
SHOW_FIREFOX = False  # Change to True to show Firefox app

# --- Page Config ---
st.set_page_config(page_title="Features vs Reviews Dashboard", layout="wide")

# --- Session State Init ---
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "selected_app" not in st.session_state:
    st.session_state.selected_app = "zoom"
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

# --- Navigation helper ---
def set_page(page_name):
    st.session_state.page = page_name

# --- Styling ---
st.markdown("""
    <style>
        body, .main, .block-container {
            background-color: #e9ecef !important;
            font-family: 'Segoe UI', sans-serif;
        }
        header[data-testid="stHeader"] {
            background-color: #ced4da !important;
            color: black;
        }
        [data-testid="stSidebar"] {
            background-color: #ced4da !important;
            color: black !important;
            width: 200px !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .sidebar-title {
            font-family: 'Trebuchet MS', sans-serif;
            color: black;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .element-container button {
            font-size: 15px !important;
            padding: 6px 16px !important;
            border-radius: 10px !important;
            transition: 0.3s ease;
        }
        .element-container button:hover {
            background-color: #dee2e6 !important;
        }
        .app-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
            margin-bottom: 20px;
        }
        .stSelectbox label {
            display: none;
        }
        div[data-testid="stHorizontalBlock"] > div:has(> div:empty) {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("<div class='sidebar-title'>Team Brown</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("📊 Dashboard", use_container_width=True):
        set_page("Dashboard")
    if st.button("👥 Team Members", use_container_width=True):
        set_page("Team Members")
    if st.button("📄 Documents", use_container_width=True):
        set_page("Documents")

# --- CSV File Loader ---
@st.cache_data
def load_data(app_name):
    path = f"{app_name.lower()}.csv"
    if not os.path.exists(path):
        return None
    return pd.read_csv(path)

# --- Page Routing ---
if st.session_state.page == "Team Members":
    st.title("Team Members")
    st.markdown("*We are a team of 13, each contributing uniquely to the success of this project.*")

    team_members = [
        ("Sindhura Patel", "shankesl@mail.uc.edu"),
        ("Sahastra Vadde", "vaddesa@mail.uc.edu"),
        ("Shashidhar Reddy", "gouniksy@mail.uc.edu"),
        ("Akash Nallagonda", "nallagah@mail.uc.edu"),
        ("Lekha Reddy", "surakaly@mail.uc.edu"),
        ("Tharun Medam", "medamtn@mail.uc.edu"),
        ("Pranathi Induri", "induripi@mail.uc.edu"),
        ("Jagan Mohan", "kandukjn@mail.uc.edu"),
        ("Naga Prem Sai Pendela", "pendelni@mail.uc.edu"),
        ("Shraya Bejgum", "bejgumsa@mail.uc.edu"),
        ("Saketh Reddy Nimmala", "nimmalsy@mail.uc.edu"),
        ("Deepak Reddy Yalla", "yallady@mail.uc.edu"),
        ("Ramakrishna Gampa", "gampara@mail.uc.edu"),
    ]

    col1, col2 = st.columns(2)
    for idx, (name, email) in enumerate(team_members):
        with (col1 if idx % 2 == 0 else col2):
            st.markdown(f"""
                <div style="background:#fff;padding:15px 20px;border-radius:15px;box-shadow:0 2px 6px rgba(0,0,0,0.1);margin-bottom:20px;">
                    <div style="font-size:18px;font-weight:600;">🧑🏻‍🎓 {name}</div>
                    <div style="font-size:15px;margin-top:5px;">
                        📧 <a href="mailto:{email}" style="text-decoration:none;color:#0072C6;">{email}</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

elif st.session_state.page == "Documents":
    st.title("📄 Documents")
    st.info("Click a document to preview it below or hide it.")

    pdf_filename = "Team Brown Video Presentation Checkpoint.pdf"

    if st.button(f"📄 {pdf_filename}"):
        if st.session_state.selected_doc == pdf_filename:
            st.session_state.selected_doc = None
        else:
            st.session_state.selected_doc = pdf_filename

    if st.session_state.selected_doc == pdf_filename:
        try:
            with open(pdf_filename, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                preview = f"""
                    <object
                        data="data:application/pdf;base64,{base64_pdf}"
                        type="application/pdf"
                        width="100%" height="700px">
                        <p>Unable to display PDF. <a href="{pdf_filename}">Download instead</a>.</p>
                    </object>
                """
                st.markdown(preview, unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning(f"⚠️ File not found: {pdf_filename}")

# --- Dashboard Page ---
else:
    st.title("📊 Features vs Reviews Dashboard")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🎩 zoom", use_container_width=True):
            st.session_state.selected_app = "zoom"
    if SHOW_WEBEX:
        with col2:
            if st.button("💻 Webex", use_container_width=True):
                st.session_state.selected_app = "webex"
    if SHOW_FIREFOX:
        with col3:
            if st.button("🌐 Firefox", use_container_width=True):
                st.session_state.selected_app = "firefox"

    selected_app = st.session_state.selected_app
    df = load_data(selected_app)

    st.subheader(f"Sentiment Trend for: {selected_app}")

    try:
        if df is None:
            st.error(f"CSV file for '{selected_app}' not found.")
            st.stop()

        required_cols = {"Month", "Positive", "Neutral", "Negative", "Feature Title"}
        if not required_cols.issubset(df.columns):
            st.error(f"The CSV must contain columns: {', '.join(required_cols)}.")
            st.stop()

        df['Month'] = pd.to_datetime(df['Month'])
        total = df[['Positive', 'Neutral', 'Negative']].sum(axis=1)
        df['Positive (%)'] = df['Positive'] / total
        df['Neutral (%)'] = df['Neutral'] / total
        df['Negative (%)'] = df['Negative'] / total

        df_ready = df[["Month", "Feature Title", "Positive (%)", "Neutral (%)", "Negative (%)"]]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_ready["Month"],
            y=df_ready["Positive (%)"],
            name="Positive",
            mode="lines",
            stackgroup="one",
            line=dict(color="green"),
            hoverinfo="skip"
        ))

        fig.add_trace(go.Scatter(
            x=df_ready["Month"],
            y=df_ready["Neutral (%)"],
            name="Neutral",
            mode="lines",
            stackgroup="one",
            line=dict(color="orange"),
            hoverinfo="skip"
        ))

        fig.add_trace(go.Scatter(
            x=df_ready["Month"],
            y=df_ready["Negative (%)"],
            name="Negative",
            mode="lines",
            stackgroup="one",
            line=dict(color="red"),
            hoverinfo="skip"
        ))

        fig.add_trace(go.Scatter(
            x=df_ready["Month"],
            y=[1]*len(df_ready),
            mode="markers",
            marker=dict(opacity=0),
            showlegend=False,
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>" +
                "Feature Title: %{customdata[0]}<br>" +
                "Positive: %{customdata[1]:.0%}<br>" +
                "Neutral: %{customdata[2]:.0%}<br>" +
                "Negative: %{customdata[3]:.0%}<extra></extra>"
            ),
            customdata=df_ready[["Feature Title", "Positive (%)", "Neutral (%)", "Negative (%)"]]
        ))

        fig.update_layout(
            title="Emoji Sentiment Trend with Feature Info",
            yaxis_tickformat=".0%",
            legend_title_text="Sentiment",
            hovermode="x unified",
            margin=dict(t=60, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Data error: {e}")
