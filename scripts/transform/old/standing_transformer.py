import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from scripts.transform.base_transformer import BaseTransformer

class StandingTransformer(BaseTransformer):

    def transform(self):
        data_list = []

        """"
        Input: Standings end point json

        ### Tabela: standings

        - standing_id (PK, INT, AUTO_INCREMENT)
        - season_id (FK, INT)
        - team_id (FK, INT)
        - position (INT)
        - played_games (INT)
        - won (INT)
        - draw (INT)
        - lost (INT)
        - points (INT)
        - goals_for (INT)
        - goals_against (INT)
        - goal_difference (INT)
        - stage (VARCHAR)
        - type (VARCHAR)
        - group_name (VARCHAR, NULLABLE)

        """
        for standings in self.data['standings']:
            stage = standings['stage']
            type_ = standings['type']
            group_name = standings.get('group', None)
            for team in standings['table']:
                data_list.append(
                    {
                        'competition_id': self.data['competition']['id'],
                        'season_id': self.data['season']['id'],
                        'team_id': team['team']['id'],
                        'position': team['position'],
                        'played_games': team['playedGames'],
                        'won': team['won'],
                        'draw': team['draw'],
                        'lost': team['lost'],
                        'points': team['points'],
                        'goals_for': team['goalsFor'],
                        'goals_against': team['goalsAgainst'],
                        'goal_difference': team['goalDifference'],
                        'stage': stage,
                        'type': type_,
                        'group_name': group_name  # group can be null
                    }
                )
        self.df = pd.DataFrame(data_list)
        return self.df