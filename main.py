import math
import random
import subprocess
import time
from mail_sender import Mail
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align
import pyinputplus as inputValidator
from change_exception import ChangeDetectedException
from inputimeout import inputimeout, TimeoutOccurred
from datetime import datetime
import re

"""A Program to monitor Websites and get the specific info about the changes via email.
Does not work on dynamic web-pages, only static ones."""


class Website:

    def __init__(self, link: str, email_address: str, email_password: str,
                 message_to_send: str = "WebsiteChanged!"):
        """
        Initializes the needed data for the program.
        :param link: The link of the site you wish to monitor.
        :type link: str
        :param email_address: the email address you wish to send the info to
        :type email_address: str
        :param email_password: Your email password.
        :type email_password: str
        :param message_to_send: The unique message you want sent.
        :type message_to_send: str
        """
        self._link = link
        self._current_file_name = ""
        self._new_file_name = ""
        self._email_address = email_address
        self._password = email_password
        self._mail_content = message_to_send

    def start_monitoring(self, send_html: bool = False, regular_expression: str = ""):
        """
        The method that starts the monitoring process.
        :param regular_expression: the regex to look for in website
        :type regular_expression: str
        :param send_html: if the mail should contain the html changes
        :type send_html: bool
        :return: None
        :rtype: None
        """

        if regular_expression:
            self.start_monitoring_for_regex(regular_expression)
        else:
            layout_second_variable = BasicLayout()
            layout_second_variable.console.print(f"\nChecking... {self._link}", style="#FFFFFF")

            subprocess.run(f"wget -O file_with_data.html --html-extension {self._link}",
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            current_file_contents = self._convert_to_list_string(False)

            subprocess.run(f"wget -O file_with_new_data.html --html-extension {self._link}",
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            new_file_contents = self._convert_to_list_string(True)

            if current_file_contents == new_file_contents:
                layout_second_variable.console.print(f"No Changes detected\n",
                                                     style=layout_second_variable.get_random_color())
            else:
                layout_second_variable.console.print(f"Change detected\n"
                                                     f"------Sending email-------",
                                                     style=layout_second_variable.get_random_color())
                changes = self._detect_specific_change(current_file_contents,
                                                       new_file_contents, False)
                mail = Mail(self._email_address, self._password)
                content_to_be_sent = f"{self._mail_content}\n\nOLD CONTENT :\n" \
                                     f"{changes[0]}\n\nNEW CONTENT :\n" \
                                     f"{changes[1]}\n\n" \
                                     f"LINES IN HTML:\n" \
                                     f"{self._find_html_line_to_mark(changes[1], new_file_contents)}"
                if send_html:
                    mail.send(self._email_address, "Website Notifier", content_to_be_sent,
                              self._create_full_html_site())
                else:
                    mail.send(self._email_address, "Website Notifier", content_to_be_sent)
                raise ChangeDetectedException("Change detected")

    @staticmethod
    def _convert_to_list_string(is_new_file: bool) -> list[str]:
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

    def _create_full_html_site(self):
        """
        Helper method
        :return: The html page as a single string object
        :rtype: str
        """
        html_page = self._convert_to_list_string(True)
        message = f"""
            <div class="header">
            <h1>{self._mail_content}</h1>
            </div>
            """

        # TODO: Fix Feature of getting red square over change part 2
        # new_file_contents = self._convert_to_string(True)
        # current_file_contents = self._convert_to_string(False)
        # changes = self._detect_specific_change(current_file_contents,
        #                                        new_file_contents, False)
        # html_page = self._create_box_over_changes(self._find_html_line_to_mark(changes[0], current_file_contents),
        #                                           html_page)

        html_page.insert(0, message)
        return "\n".join(html_page)

    # TODO: Fix Feature of getting red square over change part 1
    # @staticmethod
    # def _create_box_over_changes(list_with_indexes: list[int], html_page: list[str]) -> list[str]:
    #     """
    #     Helper method to circle the changes in the html
    #     :param list_with_indexes: the list with the index of the html lines that have changed
    #     :type list_with_indexes: list[int]
    #     :param html_page: the full html page as a list
    #     :type html_page: list[str]
    #     :return: the html page as a list but with the changed lines surrounded by a square
    #     :rtype: list[str]
    #     """
    #     html_to_return = html_page
    #     for index in list_with_indexes:
    #         temp_line = html_to_return[index]
    #         line_with_square = f"""{temp_line[0:2]}style="border:3px; border-style:solid; border-color:#FF0000;
    #         padding: 1em;"{temp_line[2:]}"""
    #         html_to_return[index] = line_with_square
    #
    #     return html_to_return

    def start_monitoring_for_regex(self, regular_expression: str = ""):
        """
        Method to start monitoring for the regex
        :param regular_expression: the regex to search for
        :type regular_expression: str
        :return: None
        :rtype: None
        """

        layout_second_variable = BasicLayout()
        layout_second_variable.console.print(f"\nChecking... {self._link}", style="#FFFFFF")

        subprocess.run(f"wget -O file_with_data.html --html-extension {self._link}",
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        current_file_contents = self._convert_to_list_string(False)

        subprocess.run(f"wget -O file_with_new_data.html --html-extension {self._link}",
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        new_file_contents = self._convert_to_list_string(True)

        was_found = self.does_contain_regex_in_website(regex_to_search_for=regular_expression,
                                                       webpage_as_string_list=new_file_contents)
        if was_found:
            layout_second_variable.console.print(f"Change detected\n"
                                                 f"------Sending email-------",
                                                 style=layout_second_variable.get_random_color())
            changes = self._detect_specific_change(current_file_contents,
                                                   new_file_contents, False)
            mail = Mail(self._email_address, self._password)
            mail.send(self._email_address, "Website Notifier", "Regular Expression found on Webpage: \n"
                                                               f"{self._link}")
            raise ChangeDetectedException("Change detected")
        else:
            layout_second_variable.console.print(f"No Changes detected\n",
                                                 style=layout_second_variable.get_random_color())

    @staticmethod
    def does_contain_regex_in_website(regex_to_search_for: str, webpage_as_string_list: list[str]) -> bool:
        """
        Helper method to search the webpage for the specific regex and return true if it was found
        :param regex_to_search_for: the entered regex to search for
        :type regex_to_search_for: str
        :param webpage_as_string_list: the webpage html to search in
        :type webpage_as_string_list: list[str]
        :return: if found or not
        :rtype: bool
        """
        entered_regex_compiler = re.compile(regex_to_search_for)
        the_search = entered_regex_compiler.search(" ".join(webpage_as_string_list))
        if the_search:
            return True
        return False


class BasicLayout:
    """Basic UI console Layout class"""

    def __init__(self):
        """Initializes the needed console and layout class attributes"""
        self.console = Console()
        self.layout = Layout()
        self._welcome_box_panel_text = "Welcome To Your Web-Monitoring Tool"
        self._link_box_panel_text = "Links to the websites you wish to monitor:"

        self.layout.split_column(
            Layout(name="Up"),
            Layout(name="Down")
        )

        self.layout["Up"].size = 3
        self.layout["Up"].ratio = 1
        self.layout["Down"].ratio = 3

        self.layout["Up"].update(Panel(Align.center(self._welcome_box_panel_text), style="#00FFFF bold"))
        self.layout["Down"].update(Panel(self._link_box_panel_text, style="#FFDAB9"))

    def print_layout(self):
        """Helper method to print layout"""
        self.console.print(self.layout)

    def update_link_box(self, links: list[str]) -> None:
        """
         Function to update the link box
        :param links: the text that should be placed in the box
        :type links: str
        :return: None
        :rtype: None
        """
        text = f"{self._link_box_panel_text}\n"
        for link in links:
            text += f"\n{link}\n"
        self.layout["Down"].update(Panel(f"{text}"))

    @staticmethod
    def get_random_color() -> str:
        """
        Helper function to return random color
        :return:
        :rtype:
        """
        colors = ["#DCDCDC",
                  "#E6E6FA",
                  "#F0FFFF",
                  "#708090",
                  "#FFE4E1",
                  "#FFE4B5",
                  "#BC8F8F",
                  "#D2B48C",
                  "#DEB887",
                  "#F4A460",
                  "#FF69B4"
                  ]
        return colors[random.randint(0, len(colors) - 1)]


if __name__ == '__main__':
    """Initialization Code"""
    start_time_seconds = time.time()
    start_date = datetime.now()

    try:
        layout_variable = BasicLayout()
        layout_variable.print_layout()

        urls_to_monitor = Prompt.ask(
            "[bold blue] Please enter the links to the website you wish to monitor (separate by "
            "space ' ' | max = 15) [""/bold blue]")

        layout_variable.console.print("[bold blue]\n Enter a regular expression to look for in a Website and get "
                                      "notified if it appears (Optional) [""/bold blue]")
        regular_expression_to_monitor = inputValidator.inputRegexStr(prompt=" : ", blank=True)

        layout_variable.console.print("[bold blue]\n Please enter your email [""/bold blue]")
        email = inputValidator.inputEmail(" : ")

        layout_variable.console.print("[bold blue]\n Please enter your password [""/bold blue]")
        password = inputValidator.inputPassword(" : ")

        message = Prompt.ask("[bold blue]\n Please enter the message you want to receive as a notification for a "
                             "change\n [""/bold blue]")

        layout_variable.console.print(
            "[bold blue]\n Please enter the intervals of the check (Seconds) [""/bold blue]")
        intervals = inputValidator.inputInt(" : ")

        if regular_expression_to_monitor:
            pass
        else:
            if_wants_html = Prompt.ask("[bold blue]\n Please state if you wish to be sent the Html boiler as an email "
                                       "attachment (T/F)\n [""/bold blue]").upper()

        if if_wants_html == "T":
            if_wants_html = True
        else:
            if_wants_html = False

        layout_variable.update_link_box(urls_to_monitor.split(" "))
        layout_variable.print_layout()

        do_monitor = True
        while do_monitor:
            try:
                for url in urls_to_monitor.split(" "):
                    file = Website(link=url,
                                   email_address=email, email_password=password,
                                   message_to_send=message)
                    file.start_monitoring(if_wants_html, regular_expression_to_monitor)
                    try:
                        user_input = inputimeout(prompt="Enter 'Exit' to end Monitoring: ", timeout=intervals)
                        if user_input == "Exit":
                            do_monitor = False
                    except TimeoutOccurred:
                        pass

            except ChangeDetectedException:
                break
    except:
        layout_variable.console.print("\n\n Error occurred while running.\n Please check your input and internet "
                                      "connection.\n\n",
                                      style="RED")

    urls_for_output = "\n ".join(urls_to_monitor.split(" "))

    layout_variable.console.print(
        f"\n Monitoring Websites:\n {urls_for_output}\n for "
        f"{math.ceil((time.time() - start_time_seconds) / 60)} "
        f"minutes.",
        style="#FFFF00")

    layout_variable.console.print(f"\n\n Start Time: {start_date.strftime('%d/%m/%Y %H:%M:%S')}\n "
                                  f"End Time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                                  style="#FFFF00")

    layout_variable.console.print("\n\n Thank you for using this Tool.\n Session Terminated.",
                                  style="#FFFF00")
