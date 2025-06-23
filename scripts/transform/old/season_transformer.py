import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from scripts.transform.base_transformer import BaseTransformer

class SeasonTransformer(BaseTransformer):
    """
    Input: competitions details end point json
    ### Tabela: seasons
    - season_id (PK, INT)
    - competition_id (FK, INT)
    - start_date (DATE)
    - end_date (DATE)
    - current_matchday (INT)
    - winner_team_id (FK, INT, NULLABLE)
    """

    def transform(self):
        data_list = []

        for item in self.data['seasons']:
            winner = item.get('winner')
            winner_team_id = winner.get('id') if winner is not None else None
            data_list.append(
                {
                'season_id': item['id'],
                'competition_id': self.data['id'],
                'start_date': item['startDate'],
                'end_date': item['endDate'],
                'current_matchday': item.get('currentMatchday', None),
                'winner_team_id': winner_team_id
                }
            )   

        self.df = pd.DataFrame(data_list)
        return self.df

