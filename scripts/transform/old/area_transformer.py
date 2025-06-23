import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from scripts.transform.base_transformer import BaseTransformer

class AreaTransformer(BaseTransformer):
    """
    Input: competition details end point json

    ### Tabela: areas

    - area_id (PK, INT)
    - name (VARCHAR)
    - code (VARCHAR)
    - flag_url (TEXT)

    """
    def transform(self):
        self.logger.info("Iniciando transformação de Area")
        data_list = []

        area = self.data['area']
        data_list.append(
            {
            'area_id': area['id'],
            'name': area['name'],
            'code': area.get('code', None),
            'flag_url': area.get('flag', None)
            }
        )

        self.df = pd.DataFrame(data_list)
        return self.df
    