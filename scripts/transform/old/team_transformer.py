import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from scripts.transform.base_transformer import BaseTransformer

class TeamTransformer(BaseTransformer):
    """
    INPUT: Teams end point json
    """

    def transform(self):
        data_list = []

        for item in self.data['teams']:
            data_list.append(
                {
                    'team_id': item['id'],
                    'area_id': item['area']['id'],
                    'name': item['name'],
                    'short_name': item['shortName'],
                    'tla': item['tla'],
                    'crest_url': item['crest'],
                    'address': item['address'],
                    'website': item['website'],
                    'founded': item['founded'],
                    'club_colors': item['clubColors'],
                    'venue': item['venue'],
                    'last_updated': item['lastUpdated']
                }
            )
        self.df = pd.DataFrame(data_list)
        return self.df
        