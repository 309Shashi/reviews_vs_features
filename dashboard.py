import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Page Config ---
st.set_page_config(page_title="Features vs Reviews Dashboard", layout="wide")

# --- Session State Init ---
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "selected_app" not in st.session_state:
    st.session_state.selected_app = "zoom"

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
                    <div style="font-size:15px;margin-top:5px;">📧 {email}</div>
                </div>
            """, unsafe_allow_html=True)

elif st.session_state.page == "Documents":
    st.title("Documents")
    st.info("This section is under construction.")

# --- Dashboard Page ---
else:
    st.title("📊 Features vs Reviews Dashboard")

    # App selector buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("📹 zoom", use_container_width=True):
            st.session_state.selected_app = "zoom"
    with col2:
        if st.button("💻 Webex", use_container_width=True):
            st.session_state.selected_app = "webex"
    with col3:
        if st.button("🌐 Firefox", use_container_width=True):
            st.session_state.selected_app = "firefox"

    selected_app = st.session_state.selected_app
    df = load_data(selected_app)

    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.subheader(f"Sentiment Trend for: {selected_app}")

    try:
        if df is None:
            st.error(f"CSV file for '{selected_app}' not found.")
            st.stop()

        required_cols = {"Month", "Positive", "Neutral", "Negative", "Feature Title", "Feature Description", "Feature Type"}
        if not required_cols.issubset(df.columns):
            st.error(f"The CSV must contain columns: {', '.join(required_cols)}.")
            st.stop()

        df['Month'] = pd.to_datetime(df['Month'])
        total = df[['Positive', 'Neutral', 'Negative']].sum(axis=1)
        df['Positive (%)'] = df['Positive'] / total
        df['Neutral (%)'] = df['Neutral'] / total
        df['Negative (%)'] = df['Negative'] / total

        melted = df.melt(
            id_vars=['Month', 'Feature Title'],
            value_vars=['Positive (%)', 'Neutral (%)', 'Negative (%)'],
            var_name='Sentiment',
            value_name='Proportion'
        )

        fig = px.area(
            melted,
            x="Month",
            y="Proportion",
            color="Sentiment",
            custom_data=["Feature Title"],
            color_discrete_map={
                "Positive (%)": "green",
                "Neutral (%)": "orange",
                "Negative (%)": "red"
            }
        )

        fig.update_traces(
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>" +
                "Sentiment: %{fullData.name}<br>" +
                "Proportion: %{y:.0%}<br><br>" +
                "<b>%{customdata[0]}</b><extra></extra>"
            ),
            mode="none"
        )

        fig.update_layout(
            title="Emoji Sentiment Trend with Feature Info",
            yaxis_tickformat=".0%",
            legend_title_text="Sentiment",
            legend=dict(orientation="h", y=1.1, x=0.3),
            margin=dict(t=60, b=40),
            hovermode="x",
            xaxis_showspikes=True,
            yaxis_showspikes=True,
            xaxis_spikemode='across',
            yaxis_spikemode='across',
            xaxis_spikesnap='cursor',
            yaxis_spikesnap='cursor',
            xaxis_spikethickness=1,
            yaxis_spikethickness=1,
            xaxis_spikecolor='blue',
            yaxis_spikecolor='blue'
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Data error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
