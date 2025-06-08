from scripts.extract.base_extractor import BaseExtractor
import logging

class CompetitionDetailsExtractor(BaseExtractor):
    def get_competition_details(self):
        logging.info("Obtendo detalhes da competição.")
        return self.make_request('competition_details')
