# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()


class NewsScraperPipeline:

    def open_spider(self, spider):
            self.connection = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
            )

        

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        spider.logger.info(f"ITEM RECEIVED: {dict(adapter)}")

        try:
            self.cursor.execute(
                """
                INSERT INTO "News_app_news"
                (title, content, date, author, url)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    adapter.get("title"),
                    None,
                    None,
                    None,
                    None,
                )
            )

            self.connection.commit()

            spider.logger.info("INSERT SUCCESSFUL")

        except Exception as e:
            self.connection.rollback()
            spider.logger.error(f"INSERT FAILED: {e}")

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
