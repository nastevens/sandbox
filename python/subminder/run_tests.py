import unittest
import test.test_parser as test_parser

parser_test_suite = test_parser.suite()

aggregate_suite = unittest.TestSuite()
aggregate_suite.addTest(parser_test_suite)

unittest.TextTestRunner(verbosity = 2).run(aggregate_suite)
