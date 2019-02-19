__author__ = 'pascalpoizat'

class NamedElement:
    """
    An element with a name.

    """

    def __init__(self, name: str):
        """
        Constructor.

        :param name: String, name of the named element
        :return:
        """
        self.name: str = name
