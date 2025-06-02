from scripts.extract.base_extractor import BaseExtractor

class CompetitionDetailsExtractor(BaseExtractor):
    def get_competition_details(self):
        self.logger.info("Obtendo detalhes da competição.")
        return self.make_request('competition_details')
