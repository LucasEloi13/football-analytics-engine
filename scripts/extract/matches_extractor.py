from scripts.extract.base_extractor import BaseExtractor

class MatchesExtractor(BaseExtractor):
    def get_matches(self):
        # self.logger.info("Obtendo partidas.")
        return self.make_request('matches')
