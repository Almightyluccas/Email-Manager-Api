class ImapExceptionCust(Exception):
    def __init__(self, status_code: int, detail: str, custom_data: dict = None):
        self.status_code = status_code
        self.detail = detail
        self.custom_data = custom_data
        super().__init__(detail)