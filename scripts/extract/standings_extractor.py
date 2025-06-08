from scripts.extract.base_extractor import BaseExtractor

class StandingsExtractor(BaseExtractor):
    def get_standings(self):
        # self.logger.info("Obtendo tabela de classificação.")
        return self.make_request('standings')
