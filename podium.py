import streamlit as st
import pandas as pd
import plotly.express as px
from helper import *

if st.session_state.players:
    df = pd.DataFrame(st.session_state.players)
    df = df.sort_values(by=DIFF_COLUMN).reset_index(drop=True)
    df = df[:3].sort_values(by=DIFF_COLUMN, ascending=False)

    fig = px.bar(
        df,
        y=NAME_COLUMN,
        x=DIFF_COLUMN,
        orientation="h",
        color=DIFF_COLUMN,
        color_continuous_scale="agsunset",
    )

    fig.update_traces(text=None)
    fig.update_layout(
        yaxis_title="",
        xaxis_title=DIFF_COLUMN,
        coloraxis_showscale=False,
    )

    fig.update_layout(yaxis=dict(tickfont=dict(size=25)))

    if len(df) >= 3:
        fig.add_annotation(
            y=df.loc[0, NAME_COLUMN], x=df.loc[0, DIFF_COLUMN], text="🏆", showarrow=False, font=dict(size=60)
        )
        fig.add_annotation(
            y=df.loc[1, NAME_COLUMN], x=df.loc[1, DIFF_COLUMN], text="🥈", showarrow=False, font=dict(size=50)
        )
        fig.add_annotation(
            y=df.loc[2, NAME_COLUMN], x=df.loc[2, DIFF_COLUMN], text="🥉", showarrow=False, font=dict(size=40)
        )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "![Giphy](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2Q0bWp0c2ppN2t1Mmo0dHRqZmt2bHZmNDZ6bTdseHZ6Z25kZGlqaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/4dDN8pehDXYadzZiZ3/giphy.webp)"
    )
else:
    st.warning("Keine Spieler hinzugefügt. Bitte füge Spieler hinzu, um die Rangliste anzuzeigen.")
