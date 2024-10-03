import pandas as pd
import altair as alt
import streamlit as st
from streamlit_keycloak import login

from utils.config import KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID

pd.set_option('display.max_columns', None)

st.set_page_config(page_title="Tidsrejsen", layout="wide")

keycloak = login(
    url=KEYCLOAK_URL,
    realm=KEYCLOAK_REALM,
    client_id=KEYCLOAK_CLIENT_ID
)

if keycloak.authenticated:
    st.title("Tidsrejsen")
    tidsrejsen_link = 'https://tidsrejsen.dk/om-tidsrejsen/'
    st.link_button("Gå til Tidsrejsen", tidsrejsen_link, type='primary')
    device_tab, unique_user_tab, completed_missions_tab, chapter_tab, overview_tab, device_overview_tab = st.tabs(
        ["Top 5 Anvendte Enheder", "Unikke brugere", ' Missioner', 'Kapitler', 'Oversigt over Brugere', 'Overblik over Enheder']
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
            st.altair_chart(device_chart, use_container_width=True)

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
            st.altair_chart(device_chart, use_container_width=True)

    with unique_user_tab:
        unique_user_df = pd.read_csv('tidsrejsen_updated.csv', sep=';')
        unique_users_count = unique_user_df['MemberEmail'].nunique()

        st.write("## Unikke brugere")
        st.markdown(f'''Antal af unikke brugere: :green-background[{unique_users_count}] ''')

        anonymous_users_df = unique_user_df[unique_user_df['MemberEmail'].isna()]
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

    with completed_missions_tab:
        mission_names = {
            1437: "Tidsrejsen",
            1148: "De FE'E Dyr",
            1268: "Verdens Tammeste Dyr",
            1278: "Menneskedyrets Myretuer",
            1399: "I lortens Fodspor",
            1438: "De Byduelige Dyr",
            1280: "Isens Kraft",
            1400: "Ude i Skoven",
            1439: "Fremtiden - Hvad Synes Du?"
        }

        completed_missions_df = pd.read_csv('tidsrejsen_updated.csv', sep=';')
        completed_missions_df = completed_missions_df[completed_missions_df['Type'] == 'missionEnd']
        completed_missions_df['Mission'] = completed_missions_df['Mission'].map(mission_names)
        completed_missions_df = completed_missions_df[['Mission']]

        chart_col, table_col = st.columns(2)
        with chart_col:
            st.write("## Gennemførte missioner")
            completed_missions_chart = alt.Chart(completed_missions_df).mark_bar().encode(
                x=alt.X('Mission', title='Missioner'),
                y=alt.Y('count()', title='Antal af gennemførte missioner'),
                color=alt.Color('Mission', title='Missioner'),
                tooltip=[alt.Tooltip('count()', title='Antal af gennemførte missioner'), alt.Tooltip('Mission', title='Mission')]
            ).properties(
                width=500,
                height=500
            )
            st.altair_chart(completed_missions_chart, use_container_width=True)

    with completed_missions_tab:
        mission_names = {
            1437: "Tidsrejsen",
            1148: "De FE'E Dyr",
            1268: "Verdens Tammeste Dyr",
            1278: "Menneskedyrets Myretuer",
            1399: "I lortens Fodspor",
            1438: "De Byduelige Dyr",
            1280: "Isens Kraft",
            1400: "Ude i Skoven",
            1439: "Fremtiden - Hvad Synes Du?"
        }

        completed_missions_df = pd.read_csv('tidsrejsen_updated.csv', sep=';')
        completed_missions_df = completed_missions_df[completed_missions_df['Type'] == 'missionEnd']
        completed_missions_df['Mission'] = completed_missions_df['Mission'].map(mission_names)

        missions_per_user_df = completed_missions_df.groupby(['MemberEmail', 'Mission']).size().reset_index(name='CompletedMissions')

        chart_col, table_col = st.columns(2)

        with chart_col:
            st.write("## Gennemførte missioner pr. bruger")
            completed_missions_chart = alt.Chart(missions_per_user_df).mark_bar().encode(
                x=alt.X('MemberEmail', title='Bruger'),
                y=alt.Y('CompletedMissions', title='Antal af gennemførte missioner'),
                color=alt.Color('Mission', title='Missioner'),
                tooltip=[alt.Tooltip('MemberEmail', title='Bruger'), alt.Tooltip('Mission', title='Mission'), alt.Tooltip('CompletedMissions', title='Antal af gennemførte missioner')]
            ).properties(
                width=500,
                height=500
            )
            st.altair_chart(completed_missions_chart, use_container_width=True)

    with completed_missions_tab:
        completed_missions_df = pd.read_csv('statistics_formatted_cleaned.csv', sep=';')
        completed_missions_df = completed_missions_df[['Mission']]
        chart_col, table_col = st.columns(2)

        with chart_col:
            st.write("## Antal missioner")
            completed_missions_chart = alt.Chart(completed_missions_df).mark_bar().encode(
                x=alt.X('Mission', title='Missioner'),
                y=alt.Y('count()', title='Antal af missioner'),
                color=alt.Color('Mission', title='Missioner'),
                tooltip=[alt.Tooltip('count()', title='Antal af missioner'), alt.Tooltip('Mission', title='Mission')]
            ).properties(
                width=500,
                height=500
            )
            st.altair_chart(completed_missions_chart, use_container_width=True)

    with chapter_tab:
        chapter_names = {
            1147: "RANDERS REGNSKOV",
            1279: "RANDERS BY",
            1281: "FUSSINGØ"
        }

        chapter_df = pd.read_csv('tidsrejsen_updated.csv', sep=';')
        chapter_df = chapter_df[chapter_df['Type'].isin(['missionStep'])]
        chapter_df['Chapter'] = chapter_df['Chapter'].map(chapter_names)
        unique_chapter_df = chapter_df[['MemberEmail', 'Chapter']].drop_duplicates()
        chapter_count_df = unique_chapter_df.groupby('MemberEmail').size().reset_index(name='ChapterCount')
        unique_chapter_df = unique_chapter_df.merge(chapter_count_df, on='MemberEmail')

        chart_col, table_col = st.columns(2)
        with chart_col:
            st.write("## Kapitler")
            chapter_chart = alt.Chart(unique_chapter_df).mark_bar().encode(
                x=alt.X('MemberEmail', title='Bruger'),
                y=alt.Y('Chapter', title='Kapitel', sort=list(chapter_names.values())),
                color=alt.Color('Chapter', title='Kapitel'),
                tooltip=[
                    alt.Tooltip('MemberEmail', title='Bruger'),
                    alt.Tooltip('Chapter', title='Kapitel'),
                    alt.Tooltip('ChapterCount', title='Antal Kapitler')
                ]
            ).properties(
                width=500,
                height=500
            )
            st.altair_chart(chapter_chart, use_container_width=True)

else:
    st.markdown('''<span style="color:red">Du er ikke logget ind</span>''', unsafe_allow_html=True)
