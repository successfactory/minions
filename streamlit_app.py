import streamlit as st
import pandas as pd
import random
import os
from helper import *


def load_results():
    if os.path.exists(FILE_PATH):
        results = pd.read_csv(FILE_PATH)

        results[DIFF_COLUMN] = results.apply(
            lambda x: calculate_diff(x[ESTIMATED_COLUMN], x[ACTUAL_COLUMN]), axis=1
        )
        return results.to_dict(orient="records")
    else:
        return []


def generate_demo_data():
    names = [f"Spieler {i}" for i in range(1, 21)]
    data = []
    for name in names:
        estimated = random.randint(30, 540)
        actual = random.randint(30, 540)
        diff = abs(estimated - actual)
        data.append(
            {
                NAME_COLUMN: name,
                ESTIMATED_COLUMN: seconds_to_mmss(estimated),
                ACTUAL_COLUMN: seconds_to_mmss(actual),
                DIFF_COLUMN: diff,
            }
        )
    return data


if "players" not in st.session_state:
    st.session_state.players = load_results() or generate_demo_data()

new_player = st.Page("form.py", title="Neu", icon=":material/add_circle:")
results = st.Page("results.py", title="Rangliste", icon=":material/format_list_numbered:")
podium = st.Page("podium.py", title="Podium", icon=":material/trophy:")


pg = st.navigation([new_player, results, podium])
st.set_page_config(page_title="Minions LEGO Schätzspiel", page_icon=":material/trophy:")
st.title("Minions LEGO Schätzspiel")

pg.run()
