# import streamlit as st
# import requests

# # URL for the tournament schedule API
# pga_schedule_url = "https://feeds.datagolf.com/get-schedule?tour=pga&file_format=json&key=c8336af0079dd0eeec5576088e1b"

# pga_schedule_response = requests.get(pga_schedule_url)

# st.title("PGA Tour Tournament Leaderboard Predictor")
# st.title("2024 Tournament Schedule")

# if 'selected_tournament' not in st.session_state:
#     st.session_state.selected_tournament = None

# # Parse the response JSON data
# tournaments = pga_schedule_response.json()
# schedule = tournaments['schedule']
# tournament_names = [tournament['event_name'] for tournament in schedule]

# # Display the navbar
# st.markdown("""
# <style>
#     .navbar {
#         overflow-x: auto;
#         white-space: nowrap;
#         background-color: #f1f1f1;
#     }
#     .navbar a {
#         padding: 14px 20px;
#         display: inline-block;
#         color: black;
#         text-align: center;
#         text-decoration: none;
#     }
#     .navbar a:hover {
#         background-color: #ddd;
#     }
# </style>
# <div class="navbar">
# """ + ''.join([f"<a href='#' onclick='set_selected_tournament(\"{tournament['event_name']}\")'>{tournament['event_name']}</a>" for tournament in schedule]) + """
# </div>
# """, unsafe_allow_html=True)

# # JavaScript function to update selected tournament in session state
# st.markdown("""
# <script>
#     function set_selected_tournament(tournament) {
#         const url = new URL(window.location.href);
#         url.searchParams.set('selected_tournament', tournament);
#         window.history.pushState({}, '', url);
#         Streamlit.setComponentValue('selected_tournament', tournament);
#     }
# </script>
# """, unsafe_allow_html=True)

# # Update selected tournament in session state
# if 'selected_tournament' in st.session_state:
#     selected_tournament = st.session_state.selected_tournament
#     if selected_tournament and selected_tournament not in tournament_names:
#         st.session_state.selected_tournament = None
#     elif selected_tournament and selected_tournament in tournament_names:
#         st.session_state.selected_tournament = selected_tournament

# # Display selected tournament information
# if st.session_state.selected_tournament:
#     selected_tournament = st.session_state.selected_tournament
#     tournament_info = next(tournament for tournament in schedule if tournament['event_name'] == selected_tournament)
#     st.write("## Tournament Information")
#     st.write(f"**Name:** {selected_tournament}")
#     st.write(f"**Location:** {tournament_info['location']}")
#     st.write(f"**Start Date:** {tournament_info['start_date']}")
#     st.write(f"**Course:** {tournament_info['course']}")

import streamlit as st
import requests
# import pickle
# import sklearn
import pandas as pd
from model import reg_rf

# Load data
df = pd.read_csv('data/ASA All PGA Raw Data - Tourn Level.csv')

# Load the machine learning model
# with open('/Users/burgefamily/CPSC325/dspl-pga-tour-project/model.pkl', 'rb') as f:
#     model = pickle.load(f)

tournament_field_df = pd.read_csv('data/2024_masters.csv')

# API endpoint for tournament schedule
pga_schedule_url = "https://feeds.datagolf.com/get-schedule?tour=pga&file_format=json&key=c8336af0079dd0eeec5576088e1b"
pga_schedule_response = requests.get(pga_schedule_url)
schedule = pga_schedule_response.json()['schedule']

# Tournament names
tournament_names = [tournament['event_name'] for tournament in schedule]

# Display tournament schedule in a horizontal scrollable navbar
st.title("2024 Tournament Schedule")
selected_tournament = st.selectbox("Select a tournament", tournament_names)

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
        # tournament_test_df = df[df['tournament name'] == 'Masters Tournament']
        # tournament_field_df['player id'] = tournament_field_df.index.astype(int) + 1
    if st.session_state.load > 0:
        features = ['sg_putt', 'sg_arg', 'sg_app', 'sg_ott', 'sg_t2g', 'sg_total', 'player id']
        X_test_df = tournament_field_df.iloc[:, 1:]
        y_pred_df = reg_rf.predict(X_test_df)
        player_map = tournament_field_df.set_index('player id')['player_name'].to_dict()

        predictions = pd.DataFrame({"player id": X_test_df['player id'], "Predicted Strokes": y_pred_df})
        predictions['player_name'] = predictions['player id'].map(player_map)

        predictions_sorted = predictions.sort_values(by="Predicted Strokes")
        if st.button("Make Predictions"):
            st.write(predictions_sorted)
            st.session_state.load = 0

# if st.button("Enter"):
#     chalice_endpoint = st.secrets["endpoint"]
#     data = {'age': age, 'name': name}
#     response = requests.post(chalice_endpoint, json=data)
#     result = response.json()
    
#     # Front end formatting
#     st.title(f"{result['name']} will be {result['new_age']}")
#     st.title("JSON Request")
#     st.text(data)
#     st.title("JSON Response")
#     st.text(result)
