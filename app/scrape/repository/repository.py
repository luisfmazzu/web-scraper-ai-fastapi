from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database


class ScrapeRepository:
    def __init__(self, database: Database):
        self.database = database
        self.collection = "scrape_data"

    def create_scrape_data(self, scrape_data: dict):
        scrape_data["created_at"] = datetime.utcnow()

        self.database[self.collection].insert_one(scrape_data)

    def get_scrape_data(self, scrape_id: str):
        scrape_data = self.database[self.collection].find_one(
            {
                "scrape_id": scrape_id
            },
            {
                '_id': 0
            }
        )
        return scrape_data
