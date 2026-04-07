import logging
from repositories.batch_repo import BatchRepository
from repositories.sale_repo import SaleRepository


# 🔥 Налаштування логування
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("sales.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


class SalesService:

    def __init__(self):
        self.batch_repo = BatchRepository()
        self.sale_repo = SaleRepository()
        logging.debug("SalesService initialized")

    def sell(self, user_id: int, customer_id: int, medicine_id: int, qty: int):
        """
        FEFO списання (First Expired First Out)
        """

        logging.info(
            f"START SELL | user={user_id} "
            f"customer={customer_id} medicine={medicine_id} qty={qty}"
        )

        qty = int(qty)
        remaining = qty

        # 🔍 Отримуємо партії
        batches = self.batch_repo.get_fefo_batches(medicine_id)
        logging.debug(f"FEFO batches found: {batches}")

        if not batches:
            logging.warning("NO BATCHES FOUND")
            raise Exception("Немає доступних партій для продажу")

        # 🔍 Загальний залишок
        total_available = sum(b[1] for b in batches)
        logging.debug(f"TOTAL AVAILABLE: {total_available}")

        if total_available < qty:
            logging.warning(
                f"NOT ENOUGH STOCK | requested={qty} available={total_available}"
            )
            raise Exception(
                f"Недостатньо товару. Доступно: {total_available}"
            )

        # ✅ Створюємо продаж
        sale_id = self.sale_repo.create_sale(user_id, customer_id)
        logging.info(f"SALE CREATED | id={sale_id}")

        # 🔥 FEFO списання
        for batch_id, available_qty, price, exp in batches:

            if remaining <= 0:
                break

            take = min(available_qty, remaining)

            logging.debug(
                f"TAKE FROM BATCH | batch={batch_id} "
                f"available={available_qty} take={take}"
            )

            # додаємо позицію
            self.sale_repo.add_item(
                sale_id,
                batch_id,
                take,
                price
            )

            # зменшуємо залишок
            self.batch_repo.decrease_quantity(batch_id, take)

            remaining -= take

        # 🔍 Контроль
        if remaining > 0:
            logging.error(
                f"ERROR: remaining qty not zero | remaining={remaining}"
            )

        # Перерахунок total
        self.sale_repo.update_total(sale_id)
        logging.info(f"SALE COMPLETED | id={sale_id}")

        return sale_id

    def sell_from_batch(self, user_id, customer_id, batch_id, qty):

        batch = self.batch_repo.get_batch(batch_id)

        if not batch:
            raise Exception("Партію не знайдено")

        (
            batch_id,
            medicine_id,
            supplier_id,
            batch_number,
            manufacture_date,
            exp,
            available,
            price
        ) = batch

        if available < qty:
            raise Exception(f"Недостатній залишок. Доступно {available}")

        sale_id = self.sale_repo.create_sale(user_id, customer_id)

        self.sale_repo.add_item(
            sale_id,
            batch_id,
            qty,
            price
        )

        self.batch_repo.decrease_quantity(batch_id, qty)

        self.sale_repo.update_total(sale_id)

        return sale_id