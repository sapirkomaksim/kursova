from repositories.report_repo import ReportRepository


class ReportService:

    def __init__(self):
        self.repo = ReportRepository()

    def sales(self):
        return self.repo.sales_report()

    def stock(self):
        return self.repo.stock_report()

    def expired(self):
        return self.repo.expired_report()

    def top_sales(self):
        return self.repo.top_sales_report()