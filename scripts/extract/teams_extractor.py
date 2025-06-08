from scripts.extract.base_extractor import BaseExtractor

class TeamsExtractor(BaseExtractor):
    def get_teams(self):
        # self.logger.info("Obtendo times.")
        return self.make_request('teams')
