"""Test utilities.
"""

from pylint.testutils import tokenize_str, CheckerTestCase

import astroid

# constants for single quote types
Q_SING = "'"
Q_DOUB = '"'

# constants for triple quote types
TRI_Q_SING = "'''"
TRI_Q_DOUB = '"""'


class StringQuiteCheckerTestCase(CheckerTestCase):
    """A class which extends the pylint CheckerTestCase by wrapping
    some common code used in testing.
    """

    def _check(self, test_str, visiter, *messages):
        """Method to perform the actual test check for those methods
        that utilize a visitor.
        """
        stmt = astroid.extract_node(test_str)

        if messages:
            ctx = self.assertAddsMessages(*messages)
        else:
            ctx = self.assertNoMessages()

        with ctx:
            self.checker.process_tokens(tokenize_str(test_str))
            visiter(stmt)

    def check_module(self, test_str, *messages):
        """Test that the module-level docstring is linted correctly.
        """
        stmt = astroid.parse(test_str)

        if messages:
            ctx = self.assertAddsMessages(*messages)
        else:
            ctx = self.assertNoMessages()

        with ctx:
            self.checker.process_tokens(tokenize_str(test_str))
            self.checker.visit_module(stmt)

    def check_class(self, test_str, *messages):
        """Test that the class-level docstring is linted correctly.
        """
        self._check(
            test_str,
            self.checker.visit_classdef,
            *messages
        )

    def check_function(self, test_str, *messages):
        """Test that the function-level docstring is linted correctly.
        """
        self._check(
            test_str,
            self.checker.visit_functiondef,
            *messages
        )