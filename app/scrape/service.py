from app.config import database, scrape_queue
from .repository.repository import ScrapeRepository


class Service:
    def __init__(self):
        self.database = database
        self.scrape_repository = ScrapeRepository(self.database)
        self.scrape_queue = scrape_queue

    def queue_new_scrape(self, scrape_data):
        self.scrape_queue.put(scrape_data)


def get_service():
    return svc


svc = Service()
