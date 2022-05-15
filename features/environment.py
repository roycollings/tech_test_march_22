"""
A place to define hooks and pre-tag processing (such as fixture loading etc...)
"""


def before_all(_):
    """
    Actions to be taken before any scenarios run.
    WARNING: This is executed before *each* parallel process.
    """


def after_all(_):
    """
    Actions to be taken after all scenarios ran.
    WARNING: This is executed after *each* parallel process.
    """
