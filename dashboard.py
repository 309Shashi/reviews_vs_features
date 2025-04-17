import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import base64

SHOW_WEBEX = False  # Set to True to show Webex app
SHOW_FIREFOX = False  # Set to True to show Firefox app

# --- Page Config ---
st.set_page_config(page_title="Features vs Reviews Dashboard", layout="wide")

# --- Session State ---
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "selected_app" not in st.session_state:
    st.session_state.selected_app = "zoom"
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

@st.cache_data
def load_data(app_name):
    path = f"{app_name.lower()}_with_versions.csv"
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path, encoding="latin1")
    # clean up any BOMs or stray whitespace in the headers
    df.columns = df.columns.str.replace('\ufeff', '').str.strip()
    return df

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
        header[data-testid="stHeader"], [data-testid="stSidebar"] {
            background-color: #ced4da !important;
            color: black !important;
        }
        .sidebar-title {
            font-family: 'Trebuchet MS', sans-serif;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 1rem;
            color: black;
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

# --- Team Page ---
if st.session_state.page == "Team Members":
    st.title("Team Members")
    st.markdown("*We are a team of 13, each contributing uniquely to the success of this project.*")

    groups = [
        ("Data Cleaning", [
            ("Shraya Bejgum", "bejgumsa@mail.uc.edu"),
            ("Jagan Mohan", "kandukjn@mail.uc.edu"),
        ]),
        ("Exploratory Data Analysis", [
            ("Lekha Reddy", "surakaly@mail.uc.edu"),
            ("Pranathi Induri", "induripi@mail.uc.edu"),
            ("Tharun Medam", "medamtn@mail.uc.edu"),
        ]),
        ("Sentiment Analysis", [
            ("Ramakrishna Gampa", "gampara@mail.uc.edu"),
            ("Naga Prem Sai Pendela", "pendelni@mail.uc.edu"),
        ]),
        ("Dashboard Development", [
            ("Shashidhar Reddy", "gouniksy@mail.uc.edu"),
            ("Akash Nallagonda", "nallagah@mail.uc.edu"),
        ]),
        ("Timeline & Area Graph Design", [
            ("Saketh Reddy Nimmala", "nimmalsy@mail.uc.edu"),
            ("Deepak Reddy Yalla", "yallady@mail.uc.edu"),
        ]),
        ("Presentation & Video Compilation", [
            ("Sahastra Vadde", "vaddesa@mail.uc.edu"),
            ("Sindhura Patel", "shankesl@mail.uc.edu"),
        ]),
    ]

    for title, members in groups:
        st.markdown(f"#### 🔹 {title}")
        cols = st.columns(len(members))
        for col, (name, email) in zip(cols, members):
            with col:
                st.markdown(f"""
                    <div style="
                        background: #fff;
                        padding: 15px 20px;
                        border-radius: 15px;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                        margin-bottom: 20px;
                    ">
                        <div style="font-size:18px; font-weight:600;">
                            🧑🏻‍🎓 {name}
                        </div>
                        <div style="font-size:15px; margin-top:5px;">
                            📧 <a href="mailto:{email}" style="text-decoration:none; color:#0072C6;">
                                {email}
                            </a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

# --- Documents Page ---
elif st.session_state.page == "Documents":
    st.title("📄 Documents")
    for pdf_filename in ["Team Brown Video Presentation Checkpoint.pdf", "Team_Brown_Demo.pdf"]:
        if st.button(f"📄 {pdf_filename}"):
            st.session_state.selected_doc = (
                None if st.session_state.selected_doc == pdf_filename else pdf_filename
            )
        if st.session_state.selected_doc == pdf_filename:
            try:
                with open(pdf_filename, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("utf-8")
                st.markdown(f"""
                    <iframe src="data:application/pdf;base64,{b64}" width="100%" height="700px" style="border:none;"></iframe>
                    <p style="margin-top:10px;">
                        📥 <a href="data:application/pdf;base64,{b64}" download="{pdf_filename}">Download PDF</a>
                    </p>
                """, unsafe_allow_html=True)
            except FileNotFoundError:
                st.warning(f"⚠️ File not found: {pdf_filename}")

# --- Dashboard Page ---
else:
    st.title("📊 Features vs Reviews Dashboard")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🎩 zoom", use_container_width=True):
            st.session_state.selected_app = "zoom"
    with col2:
        if SHOW_WEBEX and st.button("💻 Webex", use_container_width=True):
            st.session_state.selected_app = "webex"
    with col3:
        if SHOW_FIREFOX and st.button("🌐 Firefox", use_container_width=True):
            st.session_state.selected_app = "firefox"

    df = load_data(st.session_state.selected_app)
    if df is None:
        st.error("CSV file not found.")
        st.stop()

    # verify required columns
    required = {"Month","Positive","Neutral","Negative","Feature Title","Version","Feature Description"}
    if not required.issubset(df.columns):
        missing = required - set(df.columns)
        st.error(f"Missing columns in CSV: {missing}")
        st.stop()

    # parse dates & compute totals/percentages
    df["Month"] = pd.to_datetime(df["Month"])
    df["Total Reviews"] = df[["Positive","Neutral","Negative"]].sum(axis=1)
    df["Positive (%)"] = df["Positive"] / df["Total Reviews"]
    df["Neutral (%)"]  = df["Neutral"]  / df["Total Reviews"]
    df["Negative (%)"] = df["Negative"] / df["Total Reviews"]

    # --- Area Chart ---
    df_ready = df[["Month","Version","Positive (%)","Neutral (%)","Negative (%)"]].sort_values("Month")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_ready["Month"], y=df_ready["Positive (%)"], name="Positive",
        mode="lines", stackgroup="one", line=dict(color="green"), hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=df_ready["Month"], y=df_ready["Neutral (%)"], name="Neutral",
        mode="lines", stackgroup="one", line=dict(color="orange"), hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=df_ready["Month"], y=df_ready["Negative (%)"], name="Negative",
        mode="lines", stackgroup="one", line=dict(color="red"), hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=df_ready["Month"], y=[1]*len(df_ready),
        mode="markers", marker=dict(opacity=0), showlegend=False,
        hovertemplate=(
            "Version: %{customdata[0]}<br>"
            "Positive: %{customdata[1]:.0%}<br>"
            "Neutral: %{customdata[2]:.0%}<br>"
            "Negative: %{customdata[3]:.0%}<extra></extra>"
        ),
        customdata=df_ready[["Version","Positive (%)","Neutral (%)","Negative (%)"]]
    ))
    fig.update_layout(
        title="Emoji Sentiment Trend by Version",
        yaxis_tickformat=".0%",
        hovermode="x unified",
        margin=dict(t=60,b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Pie Chart ---
    st.markdown("### 🥧 Overall Review Sentiment Distribution")
    pie = go.Figure(data=[go.Pie(
        labels=["Good (Positive)","Neutral","Bad (Negative)"],
        values=[df["Positive"].sum(),df["Neutral"].sum(),df["Negative"].sum()],
        marker=dict(colors=["green","orange","red"]), hole=0.3
    )])
    pie.update_layout(margin=dict(t=10,b=10), legend_title_text="Sentiment Type")
    st.plotly_chart(pie, use_container_width=True)

    # --- Line Chart (resampled to fill missing months) ---
    st.markdown("### 📈 Total Reviews Over Time")
    df_line = (
        df.set_index("Month")["Total Reviews"]
          .resample("MS")
          .sum()
          .fillna(0)
          .reset_index()
    )
    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(
        x=df_line["Month"],
        y=df_line["Total Reviews"],
        mode="lines+markers",
        line=dict(color="#1f77b4", width=3),
        name="Total Reviews"
    ))
    line_fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Review Count",
        title="Total Reviews Trend",
        margin=dict(t=40,b=40)
    )
    st.plotly_chart(line_fig, use_container_width=True)

    # --- Features Table by Version ---
    st.markdown("### 📋 Features for Selected Version")
    versions = sorted(df["Version"].dropna().unique(), reverse=True)
    sel_ver = st.selectbox("Select Version", versions)
    feats = (
        df[df["Version"] == sel_ver]
          [["Feature Title","Feature Description"]]
          .drop_duplicates()
          .reset_index(drop=True)
    )
    if not feats.empty:
        st.dataframe(feats, use_container_width=True)
    else:
        st.info("No features found for this version.")
