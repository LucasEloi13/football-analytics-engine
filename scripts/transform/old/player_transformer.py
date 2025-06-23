import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__), '../../')))
from scripts.transform.base_transformer import BaseTransformer

class PlayerTransformer(BaseTransformer):
    """
    input: teams end point json

    ### Tabela: players

    - player_id (PK, INT)
    - team_id (FK, INT)
    - name (VARCHAR)
    - position (VARCHAR)
    - date_of_birth (DATE, NULLABLE)
    - nationality (VARCHAR)
    """

    def transform(self):
        data_list = []

        for item in self.data['teams']:
            team_id = item['id']
            for player in item['squad']:
                data_list.append(
                    {
                        'player_id': player['id'],
                        'team_id': team_id,
                        'name': player['name'],
                        'position': player.get('position', None),
                        'date_of_birth': player.get('dateOfBirth', None),
                        'nationality': player.get('nationality', None)
                    }
                )

        self.df = pd.DataFrame(data_list)
        return self.df
