# Game Data Stats Queries >>>>>>>>
game_count = """
        SELECT 
            SEASON_ID-20000 AS season,
            COUNT(DISTINCT TEAM_ID_HOME) AS total_team_count,
            COUNT(DISTINCT GAME_ID) AS total_game_count
        FROM Game
        GROUP BY season
        """
home_game_stats = """
    SELECT 
        SEASON_ID-20000 AS season,
        SUM(CASE WL_HOME 
                WHEN'W' THEN 1
                ELSE 0
            END) AS home_win_count
    FROM Game
    GROUP BY SEASON_ID
    """
team_level_stats = """
    SELECT 
        SEASON_ID-20000 AS season,
        TEAM_ID_HOME AS team_id,
        TEAM_NAME_HOME AS team_name,
        SUM(CASE WL_HOME 
                WHEN'W' THEN 1
                ELSE 0
            END) AS win_count,
        COUNT(TEAM_ID_HOME) AS team_game_count,
        "home" AS game_location
    FROM Game
    GROUP BY SEASON_ID, TEAM_ID_HOME 

    UNION

    SELECT 
        SEASON_ID-20000 AS season,
        TEAM_ID_AWAY AS team_id,
        TEAM_NAME_AWAY AS team_name,
        SUM(CASE WL_AWAY 
                WHEN'W' THEN 1
                ELSE 0
            END) AS win_count,
        COUNT(TEAM_ID_AWAY) AS team_game_count,
        "away" AS game_location
    FROM Game
    GROUP BY SEASON_ID, TEAM_ID_AWAY
"""
free_throw_stats = """
    SELECT 
        SEASON_ID-20000 AS season,
        TEAM_ID_HOME AS team_id,
        TEAM_NAME_HOME AS team_name,
        FT_PCT_HOME AS free_throw_percentage,
        COUNT(TEAM_ID_HOME) AS team_game_count,
        "home" AS game_location
    FROM Game
    GROUP BY SEASON_ID, TEAM_ID_HOME 

    UNION

    SELECT 
        SEASON_ID-20000 AS season,
        TEAM_ID_AWAY AS team_id,
        TEAM_NAME_AWAY AS team_name,
        FT_PCT_AWAY AS free_throw_percentage,
        COUNT(TEAM_ID_AWAY) AS team_game_count,
        "away" AS game_location
    FROM Game
    GROUP BY SEASON_ID, TEAM_ID_AWAY
"""
three_point_goal_stats = """
    SELECT 
        SEASON_ID-20000 AS season,
        TEAM_ID_HOME AS team_id,
        TEAM_NAME_HOME AS team_name,
        FG3_PCT_HOME AS three_point_percentage,
        COUNT(TEAM_ID_HOME) AS team_game_count,
        "home" AS game_location
    FROM Game
    GROUP BY SEASON_ID, TEAM_ID_HOME 
    
    UNION
    
    SELECT 
        SEASON_ID-20000 AS season,
        TEAM_ID_AWAY AS team_id,
        TEAM_NAME_AWAY AS team_name,
        FG3_PCT_AWAY AS three_point_percentage,
        COUNT(TEAM_ID_AWAY) AS team_game_count,
        "away" AS game_location
    FROM Game
    GROUP BY SEASON_ID, TEAM_ID_AWAY
"""
# <<<<<<<<<<<<<<<<<<<<
# Player Dats Stats Queries >>>>>>>>
player_salary_stats = """
    SELECT 
        namePlayer AS player_name,
        nameTeam AS team_name,
        2021 - strftime('%Y', Player_Attributes.BIRTHDATE) AS age,
        Player_Attributes.DRAFT_YEAR AS draft_year,
        2021 - Player_Attributes.DRAFT_YEAR AS years_in_NBA,
        Player_Attributes.POSITION AS game_position,
        ROUND(value/1000000) AS salary_in_millions
    FROM Player_Salary
    JOIN Player ON
        Player_Salary.namePlayer = Player.full_name
    JOIN Player_Attributes ON
        Player.ID = Player_Attributes.ID
    WHERE slugSeason = '2020-21'
    ORDER BY salary_in_millions DESC

"""
player_salary_stats_top_10 = """
    SELECT 
        namePlayer AS player_name,
        nameTeam AS team_name,
        Player_Attributes.DRAFT_YEAR AS draft_year,
        Player_Attributes.POSITION AS game_position,
        Player_Attributes.PTS AS points,
        Player_Attributes.AST AS assists,
        Player_Attributes.REB AS rebounds,
        ROUND(value/1000000) AS salary_in_millions
    FROM Player_Salary
    JOIN Player ON
        Player_Salary.namePlayer = Player.full_name
    JOIN Player_Attributes ON
        Player.ID = Player_Attributes.ID
    WHERE slugSeason = '2020-21'
    ORDER BY salary_in_millions DESC

"""
# <<<<<<<<<<
# Background data stats Queries >>>>>>>>
background_data_stats = """
    SELECT 
        nameTeam AS team_name,
        ROUND(AVG(value/1000000), 2) AS avg_salary_in_millions
    FROM Player_Salary
    WHERE slugSeason = '2020-21'
    GROUP BY team_name
    ORDER BY avg_salary_in_millions DESC
    LIMIT 10;
"""
# <<<<<<<<<<<<<<
