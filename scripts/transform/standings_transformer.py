import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from scripts.transform.base_transformer import BaseTransformer

class StandingsTransformer(BaseTransformer):
    """
    Input: Standings endpoint JSON
    Output: 1 parquet - standings
    """
    
    def transform(self):
        """Transforma o JSON em DataFrame de standings"""
        standings_data = self._transform_standings()
        return {'standings': standings_data}
    
    def _transform_standings(self):
        """Extrai dados da classificação"""
        data_list = []
        
        for standings in self.data['standings']:
            stage = standings['stage']
            type_ = standings['type']
            group_name = standings.get('group', None)
            
            for team in standings['table']:
                data_list.append({
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
                    'group_name': group_name
                })
        
        standings_df = pd.DataFrame(data_list)
        return standings_df

    def save_parquets(self, base_path):
        """Salva o DataFrame como parquet"""
        dataframes = self.transform()
        
        for table_name, df in dataframes.items():
            filepath = os.path.join(base_path, f"{table_name}.parquet")
            df.to_parquet(filepath, index=False)
            print(f"Parquet salvo: {filepath}")