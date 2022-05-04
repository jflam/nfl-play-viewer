import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

TEMP_ANIMATION_FILENAME = "game_animation.html"

st.write("# NFL Game Play Analysis")
st.write("## Games")

# Read the table that contains the game information (teams, date, home, away)
df_games = pd.read_csv("./games.csv")

# Extract out a list of the unique game_ids to use to populate game selector
game_ids = df_games["gameId"].unique()

# Populate the selectbox with a VISITOR at HOME on DATE
def print_game_info(game_id):
    game = df_games.loc[df_games["gameId"] == game_id]
    return (f"{game['visitorTeamAbbr'].values[0]} "
        f"at {game['homeTeamAbbr'].values[0]} "
        f"on {game['gameDate'].values[0]}")

# Read the master table of game data into pandas (for week 1)
df = pd.read_csv("./week1.csv")

# User selects the game to view
game_id = st.selectbox("Select a game", 
                       game_ids, 
                       format_func=print_game_info)

st.write(f"## Plays for: {print_game_info(game_id)}")

GAME_COLUMNS = ['time', 'x', 'y', 'team', 'playId', 'jerseyNumber', 
    'displayName']
df_game = df.loc[df["gameId"] == game_id][GAME_COLUMNS]

# Populate the selectbox with a list of plays and let user select play to view
# Ideally the outcome of the play is here somewhere?
play_ids = df_game["playId"].unique()
play_id = st.selectbox("Select a play", play_ids)

# When user has selected the play to view, render the plays and a plot
df_plays = df_game.loc[df_game["playId"] == play_id]

# Display the plays for the selected game (useful for browsing the data)
st.dataframe(df_plays)

# Helper function to generate the playing field
# Source: Miranda Auhl: https://github.com/mirandaauhl/nfl-animation
def generate_field(ax):
    rect = patches.Rectangle((0, 0), 120, 53.3, linewidth=2,
                            edgecolor='black', facecolor='#BDD9BF', zorder=0)
    ax.add_patch(rect)

    # plot line numbers
    for a in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]:
        ax.axvline(x=a, color='white', zorder=1)
    # added to set y-axis up for the numbers
    ax.axhline(y=0, color='white', zorder=1)
    ax.axhline(y=53.3, color='white', zorder=1)

    # plot numbers
    for x in range(20, 110, 10):
        numb = x
        if x > 50:
            numb = 120-x
        ax.text(x, 4, str(numb - 10), horizontalalignment='center', fontsize=15, color='white', zorder=1)
        ax.text(x-0.95, 53.3-4, str(numb-10), 
                horizontalalignment='center', fontsize=15, color='white',rotation=180, zorder=1)

    # hash marks
    for x in range(11, 110):
        ax.plot([x, x], [0.4, 0.7], color='white', zorder=1)
        ax.plot([x, x], [53.0, 52.5], color='white', zorder=1)
        ax.plot([x, x], [23, 23.66], color='white', zorder=1)
        ax.plot([x, x], [29.66, 30.33], color='white', zorder=1)

    # hide axis
    plt.axis('off')

    # create base scatter plots for the players location, allows for legend creation
    ax.scatter([], [], c= '#0069D1', label = 'Home team', zorder=2)
    ax.scatter([], [], c= '#D92F38', label = 'Away team', zorder=2)
    ax.scatter([], [], c='#E89B00' , label = 'Football', zorder=2)
    ax.legend(loc='upper right')

    # # statistics overview tables 
    # plt.table(cellText=data, 
    #                 colWidths=[0.1]*4,
    #                 colLabels=list(stat_overview.columns),
    #                 loc='right',
    #                 )
    # plt.table(cellText=data2, 
    #                 colWidths=[0.1]*2,
    #                 colLabels=list(percentile_cal.columns),
    #                 loc='bottom')
                    
    # # initial plots for jersey numbers
    # for x in range(0, 14):
    #     d["label{0}".format(x)] = ax.text(0, 0, '', fontsize = 'small', fontweight = 700, zorder=4)

    # plot legend
    ax.legend(loc='upper right')

def plot_tick(ax, play):
    """Plot player and ball positions for a single tick (100ms) in the play"""
    for _, row in play.iterrows():
        if row['team'] == 'home':
            ax.plot(row['x'], row['y'], linestyle='None', marker='o', mfc='#0069D1',mec='#0069D1', label = 'Home team', zorder=2)
        elif row['team'] == 'away':
            ax.plot(row['x'], row['y'], linestyle='None',marker='o', mfc='#D92F38',mec='#D92F38', label = 'Away team', zorder=2)
        elif row['team'] == 'football':
            ax.plot(row['x'], row['y'], linestyle='None',marker='o', mfc='#E89B00',mec='#E89B00', label = 'Football', zorder=3)

def plot_animation_play(df_events, fig, ax):
    """Plot the animation for a single play"""
    generate_field(ax)
    def plot_play(df_play):
        plot_tick(ax, df_play[1])

    anim = FuncAnimation(fig, plot_play, frames=df_events, interval=100)

    with open(TEMP_ANIMATION_FILENAME, "w") as f:
        print(anim.to_html5_video(), file=f)

    HtmlFile = open(TEMP_ANIMATION_FILENAME, "r")
    source_code = HtmlFile.read() 
    components.html(source_code, height = 900,width=1900)

def plot_static_play(df_events, fig, ax):
    """Plot the static image for a single play"""
    generate_field(ax)
    for _, play in df_events:
        plot_tick(ax, play)
    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(14, 6.5)) 
df_play_ticks = df_plays.groupby("time")
plot_static_play(df_play_ticks, fig, ax)

fig, ax = plt.subplots(figsize=(14, 6.5)) 
plot_animation_play(df_play_ticks, fig, ax)