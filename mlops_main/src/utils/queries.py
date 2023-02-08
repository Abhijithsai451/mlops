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
