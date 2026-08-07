from pathlib import Path

from bot.config import Settings
from bot.database.repositories import CatalogRepository


class CatalogService:
    def __init__(self, catalog: CatalogRepository, settings: Settings):
        self.catalog = catalog
        self.settings = settings

    def list_categories(self):
        return self.catalog.list_categories()

    def get_category(self, title: str):
        return self.catalog.get_category(title)

    def list_subcategories(self, category_title: str):
        return self.catalog.list_subcategories(category_title)

    def get_subcategory(self, title: str):
        return self.catalog.get_subcategory(title)

    def list_products(self, subcategory_title: str):
        return self.catalog.list_products(subcategory_title)

    def get_product(self, title: str):
        return self.catalog.get_product(title)

    def get_product_picture_path(self, product) -> Path | None:
        if not product.file_name:
            return None
        return self.settings.picture_dir / f"{product.file_name}.jpg"
