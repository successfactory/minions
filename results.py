import streamlit as st
import pandas as pd
from helper import *

if st.session_state.players:
    df = pd.DataFrame(st.session_state.players)
    df = df.sort_values(by=DIFF_COLUMN).reset_index(drop=True)
    df.index += 1

    st.header("Rangliste")
    st.dataframe(df, height=500, use_container_width=True)

    df = df[:3].sort_values(by=DIFF_COLUMN, ascending=False)
else:
    st.warning("Keine Spieler hinzugefügt. Bitte füge Spieler hinzu, um die Rangliste anzuzeigen.")
