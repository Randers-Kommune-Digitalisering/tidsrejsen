import pandas as pd
import altair as alt
import streamlit as st

pd.set_option('display.max_columns', None)

st.set_page_config(page_title="Tidsrejsen", layout="wide")

st.title("Tidsrejsen")
tidsrejsen_link = 'https://tidsrejsen.dk/om-tidsrejsen/'
st.link_button("Gå til Tidsrejsen", tidsrejsen_link, type='primary')
device_tab, unique_user_tab, completed_missions_tab, chapter_tab, overview_tab, device_overview_tab = st.tabs(
    ["Top 5 Anvendte Enheder", "Unikke brugere", ' Gennemførte missioner', 'Kapitler', 'Oversigt over Brugere', 'Overblik over Enheder']
)

with device_tab:
    device_df = pd.read_csv('statistics_formatted_cleaned.csv', sep=';')
    device_df = device_df[['Device']]
    device_counts = device_df['Device'].value_counts().reset_index()
    device_counts.columns = ['Device', 'Count']
    top_5_devices = device_counts.nlargest(5, 'Count')

    chart_col, table_col = st.columns(2)
    with chart_col:
        st.write("## Top 5 Anvendte Enheder")
        device_chart = alt.Chart(top_5_devices).mark_bar().encode(
            x=alt.X('Device', title='Enheder'),
            y=alt.Y('Count', title='Antal af enheder'),
            color=alt.Color('Device', title='Enheder'),
            tooltip=[alt.Tooltip('Device', title='Enhed'), alt.Tooltip('Count', title='Antal af enheder')]
        ).properties(
            width=500,
            height=500
        )
        st.altair_chart(device_chart, use_container_width=True, theme=None)

    top_10_devices = device_counts.nlargest(10, 'Count')

    with chart_col:
        st.write("## Top 10 Anvendte Enheder")
        device_chart = alt.Chart(top_10_devices).mark_arc().encode(
            theta=alt.Theta(field="Count", type="quantitative", title="Antal af enheder"),
            color=alt.Color(field="Device", type="nominal", title="Enheder"),
            tooltip=[alt.Tooltip('Count', title='Antal af enheder'), alt.Tooltip('Device', title='Enhed')]
        ).properties(
            width=500,
            height=500
        )
        st.altair_chart(device_chart, use_container_width=True, theme=None)

with unique_user_tab:
    statistics_df = pd.read_csv('statistics_cleaned.csv', sep=';')
    unique_users_count = statistics_df['MemberEmail'].nunique()

    st.write("## Unikke brugere")
    st.markdown(f'''Antal af unikke brugere: :green-background[{unique_users_count}] ''')

    anonymous_users_df = statistics_df[statistics_df['MemberEmail'].isna()]
    unique_anonymous_sessions_count = anonymous_users_df['Session'].nunique()

    st.write("## Unikke anonyme brugere")
    st.markdown(f'''Antal af unikke anonyme brugere: :red-background[{unique_anonymous_sessions_count}] ''')

    unique_users_df = pd.DataFrame({
        'Metric': ['Unikke brugere', 'Unikke anonyme brugere'],
        'Count': [unique_users_count, unique_anonymous_sessions_count]
    })

    chart_col, table_col = st.columns(2)
    with chart_col:
        unique_users_chart = alt.Chart(unique_users_df).mark_bar().encode(
            x=alt.X('Metric', title='Brugere'),
            y=alt.Y('Count', title='Antal af brugere'),
            color=alt.Color('Metric', title='Brugere'),
            tooltip=[alt.Tooltip('Count', title='Antal af brugere'), alt.Tooltip('Metric', title='Brugere')]
        ).properties(
            width=500,
            height=500
        )
        st.altair_chart(unique_users_chart, use_container_width=True)
