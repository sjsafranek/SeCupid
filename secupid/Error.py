#!/usr/bin/python

class SeCupidError(Exception):
	"""Base class for exceptions in this module."""
	pass

class DriverTypeError(SeCupidError):
    """  """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
