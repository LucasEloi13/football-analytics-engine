import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from scripts.transform.base_transformer import BaseTransformer

class CoachTransformer(BaseTransformer):
    """"
    Recebe como input Teams
    """

    def transform(self):
        self.logger.info("Iniciando transformação de coaches")

        data_list = []

        for item in self.data['teams']:
            data_list.append(
                {
                    'coach_id': item['coach']['id'],
                    'team_id': item['id'],
                    'first_name': item['coach']['firstName'],
                    'last_name': item['coach']['lastName'],
                    'name': item['coach']['name'],
                    'date_of_birth': item['coach']['dateOfBirth'],
                    'nationality': item['coach']['nationality'],
                    'contract_start': item['coach']['contract']['start'],
                    'contract_until': item['coach']['contract']['until']
                }
            )
        self.df = pd.DataFrame(data_list)
        return self.df 

            
