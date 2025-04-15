import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import base64

SHOW_WEBEX = True  # Set to True to show Webex app
SHOW_FIREFOX = True  # Set to True to show Firefox app

# --- Page Config ---
st.set_page_config(page_title="Features vs Reviews Dashboard", layout="wide")

# --- Session State ---
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "selected_app" not in st.session_state:
    st.session_state.selected_app = "zoom"
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

# --- Load Data ---
@st.cache_data
def load_data(app_name):
    path = f"{app_name.lower()}.csv"
    if not os.path.exists(path):
        return None
    return pd.read_csv(path)

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
    members = [
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
    for idx, (name, email) in enumerate(members):
        with (col1 if idx % 2 == 0 else col2):
            st.markdown(f"""
                <div style="background:#fff;padding:15px 20px;border-radius:15px;box-shadow:0 2px 6px rgba(0,0,0,0.1);margin-bottom:20px;">
                    <div style="font-size:18px;font-weight:600;">🧑🏻‍🎓 {name}</div>
                    <div style="font-size:15px;margin-top:5px;">
                        📧 <a href="mailto:{email}" style="text-decoration:none;color:#0072C6;">{email}</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# --- Documents Page ---
elif st.session_state.page == "Documents":
    st.title("📄 Documents")
    pdf_filename = "Team Brown Video Presentation Checkpoint.pdf"
    if st.button(f"📄 {pdf_filename}"):
        st.session_state.selected_doc = (
            None if st.session_state.selected_doc == pdf_filename else pdf_filename
        )
    if st.session_state.selected_doc == pdf_filename:
        try:
            with open(pdf_filename, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                st.markdown(f"""
                    <a href="data:application/pdf;base64,{base64_pdf}" target="_blank">📄 Open Team Brown Video Presentation Checkpoint.pdf in new tab</a>
                    <p style="margin-top:10px;">
                        📥 <a href="data:application/pdf;base64,{base64_pdf}" download="{pdf_filename}">Click here to download the PDF</a>
                    </p>
                """, unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning(f"⚠️ File not found: {pdf_filename}")


    pdf_filename2 = "Team_Brown_Demo.pdf"
    if st.button(f"📄 {pdf_filename2}"):
        st.session_state.selected_doc = (
            None if st.session_state.selected_doc == pdf_filename2 else pdf_filename2
        )
    if st.session_state.selected_doc == pdf_filename2:
        try:
            with open(pdf_filename2, "rb") as f:
                base64_pdf2 = base64.b64encode(f.read()).decode('utf-8')
                st.markdown(f"""
                    <a href="data:application/pdf;base64,{base64_pdf2}" target="_blank">📄 Open Team_Brown_Demo.pdf in new tab</a>
                    <p style="margin-top:10px;">
                        📥 <a href="data:application/pdf;base64,{base64_pdf2}" download="{pdf_filename2}">Click here to download the PDF</a>
                    </p>
                """, unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning(f"⚠️ File not found: {pdf_filename2}")


# --- Dashboard Page ---
else:
    st.title("📊 Features vs Reviews Dashboard")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🎩 zoom", use_container_width=True):
            st.session_state.selected_app = "zoom"
    with col2:
        if SHOW_WEBEX:
            if st.button("💻 Webex", use_container_width=True):
                st.session_state.selected_app = "webex"
    with col3:
        if SHOW_FIREFOX:
            if st.button("🌐 Firefox", use_container_width=True):
                st.session_state.selected_app = "firefox"

    df = load_data(st.session_state.selected_app)
    st.subheader(f"Sentiment Trend for: {st.session_state.selected_app}")

    if df is None:
        st.error("CSV file not found.")
        st.stop()

    try:
        required_cols = {"Month", "Positive", "Neutral", "Negative", "Feature Title"}
        if not required_cols.issubset(df.columns):
            st.error("Missing columns in CSV.")
            st.stop()

        df['Month'] = pd.to_datetime(df['Month'])
        total = df[['Positive', 'Neutral', 'Negative']].sum(axis=1)
        df['Positive (%)'] = df['Positive'] / total
        df['Neutral (%)'] = df['Neutral'] / total
        df['Negative (%)'] = df['Negative'] / total

        df_ready = df[["Month", "Feature Title", "Positive (%)", "Neutral (%)", "Negative (%)"]]

        # --- Area Chart ---
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_ready["Month"], y=df_ready["Positive (%)"],
            name="Positive", mode="lines", stackgroup="one", line=dict(color="green"), hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=df_ready["Month"], y=df_ready["Neutral (%)"],
            name="Neutral", mode="lines", stackgroup="one", line=dict(color="orange"), hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=df_ready["Month"], y=df_ready["Negative (%)"],
            name="Negative", mode="lines", stackgroup="one", line=dict(color="red"), hoverinfo="skip"))

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
            hovermode="x unified",
            margin=dict(t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- Pie Chart ---
        st.markdown("### 🥧 Overall Review Sentiment Distribution")
        pie_fig = go.Figure(data=[
            go.Pie(labels=["Good (Positive)", "Neutral", "Bad (Negative)"],
                   values=[df['Positive'].sum(), df['Neutral'].sum(), df['Negative'].sum()],
                   marker=dict(colors=["green", "orange", "red"]), hole=0.3)
        ])
        pie_fig.update_layout(margin=dict(t=10, b=10), legend_title_text="Sentiment Type")
        st.plotly_chart(pie_fig, use_container_width=True)

        # --- Line Chart ---
        st.markdown("### 📈 Total Reviews Over Time")
        df['Total Reviews'] = df['Positive'] + df['Neutral'] + df['Negative']
        line_fig = go.Figure()
        line_fig.add_trace(go.Scatter(
            x=df['Month'],
            y=df['Total Reviews'],
            mode='lines+markers',
            line=dict(color="#1f77b4", width=3),
            name="Total Reviews"
        ))
        line_fig.update_layout(
            xaxis_title="Month", yaxis_title="Review Count",
            title="Total Reviews Trend", margin=dict(t=40, b=40)
        )
        st.plotly_chart(line_fig, use_container_width=True)

        # --- Feature Sentiment Table Filtered by Month ---
        st.markdown("### 📋 Feature Sentiment Table for Selected Month")
        unique_months = df['Month'].dt.strftime("%B %Y").unique()
        selected_month = st.selectbox("Select Month", unique_months)

        selected_df = df[df['Month'].dt.strftime("%B %Y") == selected_month]
        if not selected_df.empty:
            feature_table = (
                selected_df.groupby("Feature Title")[["Positive", "Neutral", "Negative"]]
                .mean()
                .reset_index()
                .sort_values("Positive", ascending=False)
            )
            st.dataframe(feature_table.reset_index(drop=True), use_container_width=True)
        else:
            st.info("No data available for selected month.")

    except Exception as e:
        st.error(f"Data error: {e}")
