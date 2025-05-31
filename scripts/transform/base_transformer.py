import pandas as pd
import json

class BaseTransformer:
    def __init__(self, input_data):
        # self.data = json.load(input_data) 
        self.data = input_data
        self.df = None  

    def validate(self):
        """Valida se o DataFrame foi criado corretamente."""
        if self.df is None or self.df.empty:
            raise ValueError("O DataFrame está vazio ou não foi criado.")

    def save_to_parquet(self, filepath):
        """Salva o DataFrame em formato parquet."""
        self.validate()
        self.df.to_parquet(filepath)
