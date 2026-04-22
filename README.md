# reviews_vs_features

This project contains a **Streamlit dashboard** for exploring how user reviews relate to product features across multiple collaboration apps such as Zoom, Webex, and Firefox-based data samples.

## What Is Included

- dashboard.py builds the interactive Streamlit app
- zoom.csv, webex.csv, and irefox.csv provide the review datasets
- equirements.txt lists the Python dependencies

## Features

- Sidebar-based page navigation
- Review dataset loading by application
- Plotly-powered data visualization
- Team and document sections embedded in the app

## Run Locally

`ash
pip install -r requirements.txt
streamlit run dashboard.py
`

## Notes

The app expects the CSV files to be available in the same directory as dashboard.py.
