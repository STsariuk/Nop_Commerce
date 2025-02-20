from src.locustfiles.tasksets.base import BaseTaskSet


class HomePage(BaseTaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    def get_main_page(self):
        request_path = '/'

        with self.client.get(
            url=request_path,
            headers=self.client.headers,
            cookies=self.cookies,
            catch_response=True,
            name=request_path
        ) as response:
            self.validate_response(response)
        return
