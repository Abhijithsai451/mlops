import logging
import os

import pandas as pd
# Pandas Configuration
import plotly.express as px
from plotly.subplots import make_subplots

from mlops_main.project_secrets import plot_path
from mlops_main.src.utils import queries

desired_width = 500
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 25)

logging.basicConfig(
    # filename=os.path.join(home_path,log_path,'running_logs.log'),
    level=logging.DEBUG,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a")


def create_game_count_plot(conn):
    logging.info("Creating the game count plot >>>>>>>>>")
    query = queries.game_count
    df = pd.read_sql(query, conn)
    plot = make_subplots(specs=[[{"secondary_y": True}]])
    team_count_trace = px.bar(df, x="season", y="total_team_count")
    game_count_trace = px.line(df, x="season", y="total_game_count")
    team_count_trace.update_traces(name="team totals", showlegend=True)
    game_count_trace.update_traces(name="game totals", showlegend=True, line_color="red")
    plot.add_trace(team_count_trace.data[0], secondary_y=False)
    plot.add_trace(game_count_trace.data[0], secondary_y=True)
    plot.update_yaxes(title_text="team totals", secondary_y=False)
    plot.update_yaxes(title_text="game totals", secondary_y=True)
    plot.update_layout(
        title_text="1946 to 2020: NBA total team and total game play trend (click legend text to filter)")
    plot.write_image(os.path.join(plot_path + '/game_count_plot.png'))
    logging.info("Creating the game count plot >>>>>>>>> SUCCESS")
    return df


def create_home_game_plot(conn, team_count):
    logging.info("Creating the home game plot >>>>>>>>>")
    query = queries.home_game_stats
    df = pd.read_sql(query, conn)
    df["home_won_percentage"] = round(100 * df["home_win_count"] / team_count["total_game_count"], 2)
    plot = px.line(df, y="home_won_percentage", x="season", title="1946-2020: Overall home game won percentage")
    plot.write_image(os.path.join(plot_path + '/home_game.png'))
    logging.info("Creating the home game plot >>>>>>>>> SUCCESS")


def create_team_level_stats_plot(conn):
    logging.info("Creating the Team level stats plot >>>>>>>>>")
    query = queries.team_level_stats
    df = pd.read_sql(query, conn)
    df["win_percentage"] = round(100 * df["win_count"] / df["team_game_count"], 2)
    plot = px.scatter(df, x="season", y="win_percentage",
                      color="game_location", title="1946-2020: team level game won percentage by game location")
    plot.write_image(os.path.join(plot_path + '/team_level_stats.png'))
    logging.info("Creating the Team level stats plot >>>>>>>>> SUCCESS")


def create_free_throw_plot(conn):
    logging.info("Creating the Free throw stats plot >>>>>>>>>")
    query = queries.free_throw_stats
    df = pd.read_sql(query, conn)
    df = df.dropna().query("free_throw_percentage < 1").reset_index(
        drop=True)

    # calculate median free throw percentage for each year by game location
    cols_to_drop = ["team_id", "team_name", "team_game_count"]
    median_ft_pct = df.drop(cols_to_drop, axis=1).groupby(
        ["season", "game_location"]).median().reset_index()
    plot = px.line(median_ft_pct, x="season", y="free_throw_percentage",
                   color="game_location",
                   title="1946-2020: median of the team level free throw percentage by game location")
    plot.write_image(os.path.join(plot_path + '/free_throw_stats.png'))
    logging.info("Creating the Free throw stats plot >>>>>>>>> SUCCESS")


def create_three_point_field_goal_plot(conn):
    logging.info("Creating the Three point field goals stats plot >>>>>>>>>")
    query = queries.three_point_goal_stats
    df = pd.read_sql(query, conn)
    df = df.dropna().query(
        "three_point_percentage < 1").reset_index(drop=True)

    # calculate median free throw percentage for each year by game location
    cols_to_drop = ["team_id", "team_name", "team_game_count"]
    median_3p_pct = df.drop(cols_to_drop, axis=1).groupby(
        ["season", "game_location"]).median().reset_index()
    plot = px.line(median_3p_pct.query("season > 1986"), x="season", y="three_point_percentage",
                   color="game_location",
                   title="1946-2020: median of the team level three points percentage by game location")
    plot.write_image(os.path.join(plot_path + '/three_point_goal_stats.png'))
    logging.info("Creating the Three point field goals stats plot >>>>>>>>> SUCCESS")


def data_analysis(conn):
    team_count = create_game_count_plot(conn)
    create_home_game_plot(conn, team_count)
    create_team_level_stats_plot(conn)
    create_free_throw_plot(conn)
    create_three_point_field_goal_plot(conn)

    return "EDA on Game Analytics data:SUCCESS"
