import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from scripts.transform.base_transformer import BaseTransformer

class TeamsTransformer(BaseTransformer):
    """
    Input: Teams endpoint JSON
    Output: 3 parquets - coach, player, team
    """
    
    def transform(self):
        """Transforma o JSON em 3 DataFrames diferentes"""
        coach_data = self._transform_coach()
        player_data = self._transform_player()
        team_data = self._transform_team()
        
        return {
            'coach': coach_data,
            'player': player_data,
            'team': team_data
        }
    
    def _transform_coach(self):
        """Extrai dados dos técnicos"""
        data_list = []
        
        for item in self.data['teams']:
            if 'coach' in item and item['coach']:
                data_list.append({
                    'coach_id': item['coach']['id'],
                    'team_id': item['id'],
                    'first_name': item['coach'].get('firstName', None),
                    'last_name': item['coach'].get('lastName', None),
                    'name': item['coach']['name'],
                    'date_of_birth': item['coach'].get('dateOfBirth', None),
                    'nationality': item['coach'].get('nationality', None),
                    'contract_start': item['coach']['contract'].get('start', None) if 'contract' in item['coach'] else None,
                    'contract_until': item['coach']['contract'].get('until', None) if 'contract' in item['coach'] else None
                })
        
        coach_df = pd.DataFrame(data_list)
        return coach_df
    
    def _transform_player(self):
        """Extrai dados dos jogadores"""
        data_list = []
        
        for item in self.data['teams']:
            team_id = item['id']
            if 'squad' in item:
                for player in item['squad']:
                    data_list.append({
                        'player_id': player['id'],
                        'team_id': team_id,
                        'name': player['name'],
                        'position': player.get('position', None),
                        'date_of_birth': player.get('dateOfBirth', None),
                        'nationality': player.get('nationality', None)
                    })
        
        player_df = pd.DataFrame(data_list)
        return player_df
    
    def _transform_team(self):
        """Extrai dados dos times"""
        data_list = []
        
        for item in self.data['teams']:
            data_list.append({
                'team_id': item['id'],
                'area_id': item['area']['id'],
                'name': item['name'],
                'short_name': item.get('shortName', None),
                'tla': item.get('tla', None),
                'crest_url': item.get('crest', None),
                'address': item.get('address', None),
                'website': item.get('website', None),
                'founded': item.get('founded', None),
                'club_colors': item.get('clubColors', None),
                'venue': item.get('venue', None),
                'last_updated': item.get('lastUpdated', None)
            })
        
        team_df = pd.DataFrame(data_list)
        return team_df

    def save_parquets(self, base_path):
        """Salva os 3 DataFrames como parquets separados"""
        dataframes = self.transform()
        
        for table_name, df in dataframes.items():
            filepath = os.path.join(base_path, f"{table_name}.parquet")
            df.to_parquet(filepath, index=False)
            print(f"Parquet salvo: {filepath}")