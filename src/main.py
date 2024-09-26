import pandas as pd
import altair as alt
import streamlit as st

pd.set_option('display.max_columns', None)


st.set_page_config(page_title="Tidsrejsen", layout="wide")

st.title("Tidsrejsen")

disk_tab, other_tab = st.tabs(["Tidsrejsen", "Other"])


