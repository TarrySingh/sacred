#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from sacred.utils import convert_camel_case_to_snake_case, get_inheritors


class CommandLineOption(object):

    """
    Base class for all command-line options.

    To implement a new command-line option just inherit from this class.
    Then add the `flag` class-attribute to specify the name and a class
    docstring with the description.
    If your command-line option should take an argument you must also provide
    its name via the `arg` class attribute and its description as
    `arg_description`.
    Finally you need to implement the `execute` classmethod. It receives the
    value of the argument (if applicable) and the current run. You can modify
    the run object in any way.
    """

    short_flag = None
    """ The (one-letter) short form (defaults to first letter of flag) """

    arg = None
    """ Name of the argument (optional) """

    arg_description = None
    """ Description of the argument (optional) """

    @classmethod
    def get_flag(cls):
        # Get the flag name from the class name
        flag = cls.__name__
        if flag.endswith("Option"):
            flag = flag[:-6]
        flag = convert_camel_case_to_snake_case(flag)

        if cls.short_flag is None:
            return flag[:1], flag
        else:
            return cls.short_flag, flag

    @classmethod
    def execute(cls, args, run):
        """
        Modify the current Run base on this command-line option.

        This function is executed after contstructing the Run object, but
        before actually starting it.
        :param args: If this command-line option accepts an argument this will
                     be value of that argument if set or None.
                     Otherwise it is either True or False.
        :type args: bool | str
        :param run: The current run to be modified
        :type run: sacred.run.Run
        """
        pass


def gather_command_line_options():
    return sorted(get_inheritors(CommandLineOption), key=lambda x: x.__name__)


class HelpOption(CommandLineOption):

    """Print this help message and exit."""


class DebugOption(CommandLineOption):

    """
    Run in debug mode.

    Don't filter the stacktrace and automatically enter post-mortem debugging
    with pdb.
    """

    @classmethod
    def execute(cls, args, run):
        run.debug = True


class LoglevelOption(CommandLineOption):

    """Adjust the loglevel."""

    arg = 'LEVEL'
    arg_description = 'Loglevel either as 0 - 50 or as string: DEBUG(10), ' \
                      'INFO(20), WARNING(30), ERROR(40), CRITICAL(50)'

    @classmethod
    def execute(cls, args, run):
        try:
            lvl = int(args)
        except ValueError:
            lvl = args
        run.root_logger.setLevel(lvl)


class CommentOption(CommandLineOption):

    """Adds a message to the run."""

    arg = 'COMMENT'
    arg_description = 'A comment that should be stored along with the run.'

    @classmethod
    def execute(cls, args, run):
        run.comment = args


class BeatIntervalOption(CommandLineOption):

    """Control the rate of heartbeat events."""

    arg = 'BEAT_INTERVAL'
    arg_description = "Time between two heartbeat events measured in seconds."

    @classmethod
    def execute(cls, args, run):
        run.beat_interval = float(args)
