import streamlit as st

from helpers.tennis import TennisMatch, TennisPlayer


def main():
    if "match" not in st.session_state:
        player1_name = "Alice"
        player2_name = "Bob"
        player1 = TennisPlayer(name=player1_name)
        player2 = TennisPlayer(name=player2_name)
        match = TennisMatch(players=(player1, player2))
        match.new_set()
        st.session_state.player1_games = 0
        st.session_state.player2_games = 0
    else:
        match = st.session_state["match"]

    message_bar = st.empty()
    col0, col1, col2 = st.columns(3)
    col0.text_input("", "Player Name", disabled=True)
    player1_name = col1.text_input("", "Alice")
    player2_name = col2.text_input("", "Bob")
    match.players[0].name = player1_name
    match.players[1].name = player2_name

    col0.text_input("", "Games", disabled=True)
    player1_games = col1.number_input(
        f"",
        min_value=0,
        max_value=None,
        key="player1_games",
    )
    player2_games = col2.number_input(
        f"",
        min_value=0,
        max_value=None,
        key="player2_games",
    )
    scores = (player1_games, player2_games)
    match.update_scores(scores=scores)

    st.write(match.scoreboard())
    message = f"{match.players[0].name} {match.sets_won[0]} - {match.sets_won[1]} {match.players[1].name}"
    message_bar.title(message)

    st.sidebar.header("Tennis Match Tracker")
    if match.sets[-1].status == "Complete":
        disable_new_set = False
    else:
        disable_new_set = True
    if match.status == "Complete":
        disable_new_set = True
    new_match_button = st.sidebar.button("New Match", key="new_match_button")
    new_set_button = st.sidebar.button(
        "New Set", key="new_set_button", disabled=disable_new_set
    )
    submit_scores_button = st.sidebar.button(
        "Submit Scores", key="submit_scores_button"
    )

    if new_match_button:
        player1 = TennisPlayer(name=player1_name)
        player2 = TennisPlayer(name=player2_name)
        match = TennisMatch(players=(player1, player2))
        match.new_set()

    if new_set_button:
        match.new_set()

    st.session_state["match"] = match


if __name__ == "__main__":
    main()
