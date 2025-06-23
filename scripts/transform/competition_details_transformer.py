import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from scripts.transform.base_transformer import BaseTransformer

class CompetitionDetailsTransformer(BaseTransformer):
    """
    Input: Competition details endpoint JSON
    Output: 3 parquets - area, competition, season
    """
    
    def transform(self):
        """Transforma o JSON em 3 DataFrames diferentes"""
        area_data = self._transform_area()
        competition_data = self._transform_competition()
        season_data = self._transform_season()
        
        return {
            'area': area_data,
            'competition': competition_data,
            'season': season_data
        }
    
    def _transform_area(self):
        """Extrai dados da área"""
        area = self.data['area']
        area_df = pd.DataFrame([{
            'area_id': area['id'],
            'name': area['name'],
            'code': area.get('code', None),
            'flag_url': area.get('flag', None)
        }])
        return area_df
    
    def _transform_competition(self):
        """Extrai dados da competição"""
        competition_df = pd.DataFrame([{
            'competition_id': self.data['id'],
            'area_id': self.data['area']['id'],
            'name': self.data['name'],
            'code': self.data['code'],
            'type': self.data['type'],
            'emblem_url': self.data['emblem'],
            'plan': self.data['plan'],
            'current_season': self.data['currentSeason']['id'],
            'number_of_available_seasons': self.data['numberOfAvailableSeasons'],
            'last_updated': self.data['lastUpdated']
        }])
        return competition_df
    
    def _transform_season(self):
        """Extrai dados das temporadas"""
        season_list = []
        for item in self.data['seasons']:
            winner = item.get('winner')
            winner_team_id = winner.get('id') if winner is not None else None
            season_list.append({
                'season_id': item['id'],
                'competition_id': self.data['id'],
                'start_date': item['startDate'],
                'end_date': item['endDate'],
                'current_matchday': item.get('currentMatchday', None),
                'winner_team_id': winner_team_id
            })
        season_df = pd.DataFrame(season_list)
        return season_df

    def save_parquets(self, base_path):
        """Salva os 3 DataFrames como parquets separados"""
        dataframes = self.transform()
        
        for table_name, df in dataframes.items():
            filepath = os.path.join(base_path, f"{table_name}.parquet")
            df.to_parquet(filepath, index=False)
            print(f"Parquet salvo: {filepath}")