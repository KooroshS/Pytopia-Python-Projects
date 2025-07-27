import streamlit as st
from src.monty_hall import simulate_game # Note: This import might need adjustment if src is not available locally
import time

st.title(":zap: Monty Hall Simulation")

num_games = st.number_input(
    "Enter number of games to simulate",
    min_value=1,
    max_value=100000,
    value=100,
)

col1, col2 = st.columns(2)
col1.subheader("Win Percentage Without Switching")
col2.subheader("Win Percentage With Switching")

chart1 = col1.line_chart(x=None, y=None)
chart2 = col2.lin_chart(x=None, y=None) # Note: There was a typo here, should be line_chart

wins_no_switch = 0
wins_switch = 0

for i in range(num_games):
  wins_with_switching, wins_without_switching = simulate_game(1)
  wins_switch += wins_with_switching
  wins_no_switch += wins_without_switching

  chart1.add_rows # Note: This needs arguments to add data
  chart2.add_rows # Note: This needs arguments to add data

  time.sleep(0.01)
