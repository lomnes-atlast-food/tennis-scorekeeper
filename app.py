import streamlit as st

from helpers.tennis import TennisMatch, TennisPlayer


def main():
    st.title("Tennis Match Tracker")
    if "match" not in st.session_state:
        player1_name = "Alice"
        player2_name = "Bob"
        player1 = TennisPlayer(name=player1_name)
        player2 = TennisPlayer(name=player2_name)
        match = TennisMatch(players=(player1, player2))
        match.new_set()
    else:
        match = st.session_state["match"]

    player1_name = st.text_input("Player 1 Name", "Alice")
    player2_name = st.text_input("Player 2 Name", "Bob")

    player1_games = st.number_input(
        f"{match.players[0].name} Games",
        min_value=0,
        max_value=None,
        value=match.sets[-1].scores[0],
        key="player1_games",
    )
    player2_games = st.number_input(
        f"{match.players[1].name} Games",
        min_value=0,
        max_value=None,
        value=match.sets[-1].scores[1],
        key="player2_games",
    )
    scores = (player1_games, player2_games)
    match.update_scores(scores=scores)

    if st.button("New Match"):
        player1 = TennisPlayer(name=player1_name)
        player2 = TennisPlayer(name=player2_name)
        match = TennisMatch(players=(player1, player2))
        match.new_set()
    if match.sets[-1].status == "Complete":
        disable_new_set = False
    else:
        disable_new_set = True

    if st.button("New Set", disabled=disable_new_set):
        match.new_set()

    for set in match.sets:
        st.write(f"{set.id}: {set.scores[0]} to {set.scores[1]}")

    st.session_state["match"] = match


if __name__ == "__main__":
    main()
