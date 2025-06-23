import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from scripts.transform.base_transformer import BaseTransformer

class MatchesTransformer(BaseTransformer):
    """
    Input: Matches endpoint JSON
    Output: 1 parquet - matches
    """
    
    def transform(self):
        """Transforma o JSON em DataFrame de matches"""
        matches_data = self._transform_matches()
        return {'matches': matches_data}
    
    def _transform_matches(self):
        """Extrai dados das partidas"""
        data_list = []
        
        for item in self.data['matches']:
            data_list.append({
                'match_id': item['id'],
                'season_id': item['season']['id'],
                'home_team_id': item['homeTeam']['id'],
                'away_team_id': item['awayTeam']['id'],
                'utc_date': item['utcDate'],
                'status': item['status'],
                'matchday': item.get('matchday', None),
                'stage': item.get('stage', None),
                'group_name': item.get('group', None),
                'score_winner': item['score'].get('winner', None),
                'score_duration': item['score']['duration'],
                'score_home_full': item['score']['fullTime'].get('home', None),
                'score_away_full': item['score']['fullTime'].get('away', None),
                'score_home_half': item['score']['halfTime'].get('home', None),
                'score_away_half': item['score']['halfTime'].get('away', None),
                'last_updated': item.get('lastUpdated', None)
            })
        
        matches_df = pd.DataFrame(data_list)
        return matches_df

    def save_parquets(self, base_path):
        """Salva o DataFrame como parquet"""
        dataframes = self.transform()
        
        for table_name, df in dataframes.items():
            filepath = os.path.join(base_path, f"{table_name}.parquet")
            df.to_parquet(filepath, index=False)
            print(f"Parquet salvo: {filepath}")