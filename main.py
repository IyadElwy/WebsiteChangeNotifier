import os
import time
from mail_sender import Mail

"""A Program to monitor Websites and get the specific info about the changes via email."""


class Website:

    def __init__(self, link: str, email_address: str, password: str,
                 message_to_send: str = "WebsiteChanged!"):
        """
        Initializes the needed data for the program.
        :param link: The link of the site you wish to monitor.
        :type link: str
        :param email_address: the email address you wish to send the info to
        :type email_address: str
        :param password: Your email password.
        :type password: str
        :param message_to_send: The unique message you want sent.
        :type message_to_send: str
        """
        self._link = link
        self._current_file_name = ""
        self._new_file_name = ""
        self._email_address = email_address
        self._password = password
        self._mail_content = message_to_send

    def start_monitoring(self, monitoring_intervals_in_seconds=60):
        """
        The method that starts the monitoring process.
        :param monitoring_intervals_in_seconds: The intervals of time for monitoring the website (seconds).
        :type monitoring_intervals_in_seconds: int
        :return: None
        :rtype: None
        """
        os.system(f"wget -O file_with_data.html --html-extension {self._link}")
        current_file_contents = self._convert_to_string(False)
        while True:
            os.system(f"wget -O file_with_new_data.html --html-extension {self._link}")
            new_file_contents = self._convert_to_string(True)

            if current_file_contents == new_file_contents:
                pass
            else:
                changes = self._detect_specific_change(current_file_contents,
                                                       new_file_contents, False)
                mail = Mail(self._email_address, self._password)
                content_to_be_sent = f"{self._mail_content}\n\nOLD CONTENT :\n" \
                                     f"{changes[0]}\n\nNEW CONTENT :\n" \
                                     f"{changes[1]}\n\n" \
                                     f"LINES IN HTML:\n" \
                                     f"{self._find_html_line_to_mark(changes[1], new_file_contents)}"
                mail.send(self._email_address, "Website Notifier", content_to_be_sent)
                break

            time.sleep(monitoring_intervals_in_seconds)

    @staticmethod
    def _convert_to_string(is_new_file: bool) -> list[str]:
        """
        Helper function.
        :param is_new_file: To check if the file is the new one or the old one.
        :type is_new_file: bool
        :return: the files as a list where every entry in the list contains a line of html
        :rtype: list[str]
        """
        if is_new_file:
            file_name = "file_with_new_data.html"
        else:
            file_name = "file_with_data.html"
        html_file_as_string = ""

        with open(file_name, "r", encoding="utf8") as html_file:
            html_file_as_string = html_file.readlines()

            # TODO: remove debugging code here
            # with open("C:/Users/iyade/PycharmProjects/TestStuff/testWebsite.html",
            #           "r", encoding="utf8") as html_file:

            html_file_as_string = html_file.readlines()

        return html_file_as_string

    @staticmethod
    def _detect_specific_change(current_file_contents: list[str],
                                new_file_contents: list[str], strip_away_newline: bool) -> list[list[str]]:
        """
        Helper functipm
        :param current_file_contents: the current file contents.
        :type current_file_contents: list[str]
        :param new_file_contents: the new file contents.
        :type new_file_contents: list[str]
        :param strip_away_newline: value to check if the `\n` character should be removed.
        :type strip_away_newline: bool
        :return: A list containg the a list with the old lines and a list with the new lines.
        :rtype: list[list[str]]
        """
        list_with_before_contents = list(
            set(current_file_contents).difference(new_file_contents))

        list_with_after_contents = list(
            set(new_file_contents).difference(current_file_contents))

        if strip_away_newline:
            for index, content in enumerate(list_with_before_contents):
                list_with_before_contents[index] = content.strip("\n")
            for index, content in enumerate(list_with_after_contents):
                list_with_after_contents[index] = content.strip("\n")
            return [list_with_before_contents, list_with_after_contents]
        else:
            return [list_with_before_contents, list_with_after_contents]

    @staticmethod
    def _find_html_line_to_mark(lines_to_search_for: list[str], file_to_search_in: list[str]) -> list[int]:
        """
        Helper function.
        :param lines_to_search_for: a list of lines to get the index of in a file.
        :type lines_to_search_for: list[str]
        :param file_to_search_in: a list containing all the file contents in which we search for.
        :type file_to_search_in: list[str]
        :return: a list containing the indexes of the lines that have been found in the file.
        :rtype: list[str]
        """
        list_with_changed_lines_indexes = list()
        for line in lines_to_search_for:
            list_with_changed_lines_indexes.append(file_to_search_in.index(line) + 1)
        return list_with_changed_lines_indexes


if __name__ == '__main__':
    file = Website(link="https://www.w3schools.com/python/ref_string_rindex.asp",
                   email_address="TEST@gmail.com", password="PASSWORD",
                   message_to_send="Your site changed!")
    file.start_monitoring(5)

# TODO: use the html of the original site to send an html view of the website via email
# TODO: but with changes highlighted using the indexes of the changed lines
# TODO: Add input option to quit with the input validation module and use the time
# TODO: out module to check for when the program should continue instead of the sleep function
