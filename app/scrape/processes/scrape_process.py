import asyncio
import structlog
from datetime import datetime
import json
from pymongo import MongoClient

from multiprocessing import Process, Queue

from ..utils.scraper import fetch_html_selenium, save_raw_data, format_data, save_formatted_data, calculate_price, html_to_markdown_with_readability, create_dynamic_listing_model, create_listings_container_model


class ScrapeProcess(Process):
    def __init__(self, scrape_queue: Queue, env) -> None:
        Process.__init__(self)
        self.scrape_queue = scrape_queue
        self.env = env
        self.logger = structlog.get_logger()

    async def process_queue_events(self):
        # Initialize DB in this new process
        # MongoDB connection
        client = MongoClient(self.env.MONGO_URL)

        # MongoDB database
        database = client[self.env.MONGO_DATABASE]

        while True:
            if self.scrape_queue.qsize() > 0:
                scrape_data = self.scrape_queue.get()
                new_scrape = await self.scrape_event(scrape_data)
                self.save_scrape_data(database, scrape_data, new_scrape)
            await asyncio.sleep(0.1)

    async def scrape_event(self, scrape_data):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        raw_html = fetch_html_selenium(scrape_data.scrape_url)
        markdown = html_to_markdown_with_readability(raw_html)
        save_raw_data(markdown, timestamp)
        DynamicListingModel = create_dynamic_listing_model(scrape_data.column_list)
        DynamicListingsContainer = create_listings_container_model(DynamicListingModel)
        formatted_data = format_data(markdown, DynamicListingsContainer, self.env.OPEN_API_KEY)
        formatted_data_text = json.dumps(formatted_data.dict())
        input_tokens, output_tokens, total_cost = calculate_price(markdown, formatted_data_text, model="gpt-4o-mini")
        df = save_formatted_data(formatted_data, timestamp)

        return formatted_data

    def save_scrape_data(self, database, scrape_data, new_scrape):
        data_dict = new_scrape.dict() if hasattr(new_scrape, 'dict') else new_scrape
        final_data = {
            "scrape_id": scrape_data.scrape_id,
            "scrape_url": scrape_data.scrape_url,
            "column_list": scrape_data.column_list,
            "data": data_dict["listings"],
            "created_at": datetime.utcnow()
        }

        database["scrape_data"].insert_one(final_data)

    def run(self):
        asyncio.run(self.process_queue_events())
