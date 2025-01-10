import streamlit as st
import pandas as pd
import plotly.express as px
import random
import os

FILE_PATH = "results.csv"


def save_results(data):
    df = pd.DataFrame(data)
    df.to_csv(FILE_PATH, index=False)


def load_results():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH).to_dict(orient="records")
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
                "Name": name,
                "Geschätzte Zeit": seconds_to_mmss(estimated),
                "Tatsächliche Zeit": seconds_to_mmss(actual),
                "Differenz (Sekunden)": diff,
            }
        )
    return data


def seconds_to_mmss(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"


def mmss_to_seconds(mmss):
    try:
        minutes, seconds = map(int, mmss.split(":"))
        return minutes * 60 + seconds
    except ValueError:
        return None


st.title("Minions LEGO Schätzspiel")

if "players" not in st.session_state:
    st.session_state.players = load_results() or generate_demo_data()

with st.form("Eingabeformular"):
    st.header("Neuen Spieler hinzufügen")
    name = st.text_input("Name:")
    estimated_time = st.text_input("Geschätzte Zeit:", placeholder="z.B. 3:45")
    actual_time = st.text_input("Tatsächliche Zeit:", placeholder="z.B. 4:15")
    submit = st.form_submit_button("Hinzufügen")

    if submit:
        est_seconds = mmss_to_seconds(estimated_time)
        act_seconds = mmss_to_seconds(actual_time)

        if name and est_seconds is not None and act_seconds is not None:
            diff = abs(est_seconds - act_seconds)
            st.session_state.players.append(
                {
                    "Name": name,
                    "Geschätzte Zeit": seconds_to_mmss(est_seconds),
                    "Tatsächliche Zeit": seconds_to_mmss(act_seconds),
                    "Differenz (Sekunden)": diff,
                }
            )
            save_results(st.session_state.players)
            st.success(f"Spieler {name} wurde hinzugefügt!")
        else:
            st.error("Bitte alle Felder korrekt im Format MM:SS ausfüllen!")

if st.session_state.players:
    df = pd.DataFrame(st.session_state.players)
    df = df.sort_values(by="Differenz (Sekunden)").reset_index(drop=True)

    st.header("Rangliste (Top 10)")
    st.dataframe(df[:10])

    df = df[:3].sort_values(by="Differenz (Sekunden)", ascending=False)

    fig = px.bar(
        df,
        y="Name",
        x="Differenz (Sekunden)",
        orientation="h",
        color="Differenz (Sekunden)",
        color_continuous_scale="agsunset",
    )

    fig.update_traces(text=None)
    fig.update_layout(
        yaxis_title="",
        xaxis_title="Differenz (Sekunden)",
        coloraxis_showscale=False,
    )

    fig.update_layout(yaxis=dict(tickfont=dict(size=25)))

    if len(df) >= 3:
        fig.add_annotation(
            y=df.loc[0, "Name"], x=df.loc[0, "Differenz (Sekunden)"], text="🏆", showarrow=False, font=dict(size=60)
        )
        fig.add_annotation(
            y=df.loc[1, "Name"], x=df.loc[1, "Differenz (Sekunden)"], text="🥈", showarrow=False, font=dict(size=50)
        )
        fig.add_annotation(
            y=df.loc[2, "Name"], x=df.loc[2, "Differenz (Sekunden)"], text="🥉", showarrow=False, font=dict(size=40)
        )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "![Giphy](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2Q0bWp0c2ppN2t1Mmo0dHRqZmt2bHZmNDZ6bTdseHZ6Z25kZGlqaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/4dDN8pehDXYadzZiZ3/giphy.webp)"
    )
else:
    st.warning("Keine Spieler hinzugefügt. Bitte füge Spieler hinzu, um die Rangliste anzuzeigen.")
