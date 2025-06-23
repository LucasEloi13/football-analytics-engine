import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from scripts.transform.base_transformer import BaseTransformer

from datetime import datetime
import pandas as pd

class CompetitionTransformer(BaseTransformer):
    """"
    recebe como input Competition details end point json
    """
    def transform(self):
        self.logger.info("Iniciando transformação de Competition")

        data_list = []

        for item in self.data: 
            data_list.append(
                {
                    'competition_id': item['id'],
                    'area_id': item['area']['id'],
                    'name': item['name'],
                    'code': item['code'],
                    'type': item['type'],
                    'emblem_url': item['emblem'],
                    'plan': item['plan'],
                    'current_season': item['currentSeason']['id'],
                    'number_of_available_seasons': item['numberOfAvailableSeasons'],
                    'last_updated': item['lastUpdated']
                }
            )
        self.df = pd.DataFrame(data_list)
        return self.df 