import pandas as pd 
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from scripts.transform.base_transformer import BaseTransformer

class MatchTransformer(BaseTransformer):
    """"
    Input: Matches end point json

    ### Tabela: matches

    - match_id (PK, INT)
    - season_id (FK, INT)
    - home_team_id (FK, INT)
    - away_team_id (FK, INT)
    - utc_date (TIMESTAMP)
    - status (VARCHAR)
    - matchday (INT)
    - stage (VARCHAR)
    - group_name (VARCHAR, NULLABLE)
    - score_winner (VARCHAR, NULLABLE)
    - score_duration (VARCHAR)
    - score_home_full (INT, NULLABLE)
    - score_away_full (INT, NULLABLE)
    - score_home_half (INT, NULLABLE)
    - score_away_half (INT, NULLABLE)
    - last_updated (TIMESTAMP)
    """

    def transform(self):
        data_list = []

        for item in self.data['matches']:
            data_list.append(
                {
                    'match_id': item['id'],
                    'season_id': item['season']['id'],
                    'home_team_id': item['homeTeam']['id'],
                    'away_team_id': item['awayTeam']['id'],
                    'utc_date': item['utcDate'],
                    'status': item['status'],
                    'matchday': item.get('matchday', None),
                    'stage': item.get('stage', None),
                    'group_name': item.get('group', None),  # group can be null
                    'score_winner': item['score'].get('winner', None),
                    'score_duration': item['score']['duration'],
                    'score_home_full': item['score']['fullTime'].get('home', None),
                    'score_away_full': item['score']['fullTime'].get('away', None),
                    'score_home_half': item['score']['halfTime'].get('home', None),
                    'score_away_half': item['score']['halfTime'].get('away', None),
                    'last_updated': item.get('lastUpdated', None)
                }
            )
        self.df = pd.DataFrame(data_list)
        return self.df