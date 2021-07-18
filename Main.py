import os
import time


class Website:
    def __init__(self, link: str):
        self._link = link
        self._current_file_name = ""
        self._new_file_name = ""

    def start_monitoring(self, monitoring_intervals_in_seconds=60):
        os.system(f"wget -O file_with_data.html --html-extension {self._link}")
        current_file_contents = self._convert_to_string(False)
        while True:
            os.system(f"wget -O file_with_new_data.html --html-extension {self._link}")
            new_file_contents = self._convert_to_string(True)

            if current_file_contents == new_file_contents:
                print("Nothing Changed.")
            else:
                print("Website Changed!")
                break

            time.sleep(monitoring_intervals_in_seconds)

    @staticmethod
    def _convert_to_string(is_new_file: bool) -> list[str]:
        if is_new_file:
            file_name = "file_with_new_data.html"
        else:
            file_name = "file_with_data.html"
        html_file_as_string = ""
        with open(file_name, "r", encoding="utf8") as html_file:
            html_file_as_string = html_file.readlines()

        return html_file_as_string


if __name__ == '__main__':
    file = Website("https://www.w3schools.com/python/ref_string_rindex.asp")
    file.start_monitoring(60)
