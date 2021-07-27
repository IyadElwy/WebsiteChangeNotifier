class ChangeDetectedException(Exception):
    """
    An exception class representing a Web-Site change detection
    """

    def __init__(self, message: str):
        """
        Initializing the exception
        :param message: the message to be returned
        :type message: str
        """
        self.message = message
        super(ChangeDetectedException, self).__init__(self.message)

    def __str__(self):
        """The overridden str function"""
        return self.message
