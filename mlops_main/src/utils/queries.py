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
three_point_goal_stats =  """
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