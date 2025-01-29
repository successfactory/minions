import streamlit as st
import pandas as pd
import time
from helper import *


def save_results(data):
    df = pd.DataFrame(data)
    df.to_csv(FILE_PATH, index=False)


if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "player" not in st.session_state:
    st.session_state.player = ""


with st.form("Eingabeformular"):
    st.header("Neuen Player")
    name = st.text_input("Name:")
    estimated_time = st.text_input("Geschätzte Zeit:", placeholder="z.B. 3:45")
    submit = st.form_submit_button("Los geht's")

    if submit:
        if st.session_state.player == "":
            st.session_state.players.append(
                {
                    "Name": name,
                    "Geschätzte Zeit": estimated_time,
                    "Tatsächliche Zeit": "0:00",
                }
            )
            save_results(st.session_state.players)
        st.session_state.player = name


def start():
    if not st.session_state.is_running:
        st.session_state.start_time = time.time() - st.session_state.elapsed_time
        st.session_state.is_running = True


def stop():
    if st.session_state.is_running:
        st.session_state.elapsed_time = time.time() - st.session_state.start_time
        st.session_state.is_running = False

        for player in st.session_state.players:
            if player[NAME_COLUMN] == st.session_state.player:
                player[ACTUAL_COLUMN] = format_time(st.session_state.elapsed_time)
                player[DIFF_COLUMN] = calculate_diff(player[ESTIMATED_COLUMN], player[ACTUAL_COLUMN])
        save_results(st.session_state.players)


if st.session_state.player:
    if st.session_state.start_time is None:
        st.button("Start", on_click=start, disabled=st.session_state.is_running)
    if not st.session_state.start_time is None:
        st.button("Stop", on_click=stop)

    my_bar = st.progress(0, text="Stoppuhr")

    time_placeholder = st.empty()
    max_seconds = mmss_to_seconds(estimated_time)
    run_seconds = max_seconds

    while st.session_state.is_running:
        run_seconds -= 1 if run_seconds > 0 else 0
        my_bar.progress(int(100 / max_seconds * run_seconds), text="Bananaaaa!")
        st.session_state.elapsed_time = time.time() - st.session_state.start_time
        time_placeholder.subheader(f"Verstrichene Zeit: {format_time(st.session_state.elapsed_time)}")
        time.sleep(1)

    if not st.session_state.is_running and st.session_state.elapsed_time > 0:
        time_placeholder.subheader(f"Verstrichene Zeit: {format_time(st.session_state.elapsed_time)}")
        st.text(f"Differenz in Sekunden: {calculate_diff(estimated_time, format_time(st.session_state.elapsed_time))}")
        st.session_state.start_time = None
        st.session_state.elapsed_time = 0
        st.session_state.is_running = False
        st.session_state.player = ""
