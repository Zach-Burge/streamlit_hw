import streamlit as st
import requests
import pandas as pd
from model import reg_rf
import datetime

date_cutoff = datetime.date.today()

# Load data
df = pd.read_csv('data/ASA All PGA Raw Data - Tourn Level.csv')

tournament_field_df = pd.read_csv('data/2024_masters.csv')

# API endpoint for tournament schedule
pga_schedule_url = "https://feeds.datagolf.com/get-schedule?tour=pga&file_format=json&key=c8336af0079dd0eeec5576088e1b"
pga_schedule_response = requests.get(pga_schedule_url)
schedule = pga_schedule_response.json()['schedule']

# Tournament names
for tournament in schedule:
    tournament_date = datetime.datetime.strptime(tournament['start_date'], '%Y-%m-%d').date()
    tournament['start_date'] = tournament_date
upcoming_tournament_names = [tournament['event_name'] for tournament in schedule if tournament['start_date'] < date_cutoff]

# Display tournament schedule in a horizontal scrollable navbar
st.title("2024 Tournament Schedule")
selected_tournament = st.selectbox("Select a tournament", upcoming_tournament_names)

# Display selected tournament information
if selected_tournament:
    tournament_info = next((tournament for tournament in schedule if tournament['event_name'] == selected_tournament), None)
    if tournament_info:
        st.write("## Tournament Information")
        st.write(f"**Name:** {tournament_info['event_name']}")
        st.write(f"**Location:** {tournament_info['location']}")
        st.write(f"**Start Date:** {tournament_info['start_date']}")
        st.write(f"**Course:** {tournament_info['course']}")
    else:
        st.write("Tournament information not found.")
    if 'load' not in st.session_state:
        st.session_state.load = 0
    def set_state(state):
        st.session_state.load = state
    if st.button("Load Field"):
        set_state(1)
        st.write("## Field Data")
        st.write(tournament_field_df)
    if st.session_state.load > 0:
        features = ['sg_putt', 'sg_arg', 'sg_app', 'sg_ott', 'sg_t2g', 'sg_total', 'player id']
        X_test_df = tournament_field_df.iloc[:, 1:]
        y_pred_df = reg_rf.predict(X_test_df)
        player_map = tournament_field_df.set_index('player id')['player_name'].to_dict()

        predictions = pd.DataFrame({"player id": X_test_df['player id'], "Predicted Strokes": y_pred_df})
        predictions['player_name'] = predictions['player id'].map(player_map)
        predictions["Predicted Strokes"] = round(predictions["Predicted Strokes"])

        predictions_sorted = predictions.sort_values(by="Predicted Strokes")
        if st.button("Make Predictions"):
            rows = st.columns(2)
            rows[0].write("## Predicted ")
            rows[0].dataframe(predictions_sorted, hide_index=True)
            tourney_actual = pd.read_csv("/Users/burgefamily/CPSC325/dspl-pga-tour-project/streamlit_hw/data/2024_masters_actual.csv")
            rows[1].write("## Actual ")
            rows[1].dataframe(tourney_actual, hide_index=True)
            # F1 at 10
            common_players = predictions_sorted.head(10).merge(tourney_actual.head(10), on='player_name')
            precision = len(common_players) / len(predictions_sorted.head(10))
            recall = len(common_players) / len(tourney_actual.head(10))
            f1_score = 2 * (precision * recall) / (precision + recall)
            st.write("## F1-Score for Top 10")
            st.write(f1_score)
            # F1 at 30
            common_players = predictions_sorted.head(30).merge(tourney_actual.head(30), on='player_name')
            precision = len(common_players) / len(predictions_sorted.head(30))
            recall = len(common_players) / len(tourney_actual.head(30))
            f1_score = 2 * (precision * recall) / (precision + recall)
            st.write("## F1-Score for Top 30")
            st.write(f1_score)
            st.session_state.load = 0