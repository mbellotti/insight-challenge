import unittest, os
import src.process_log as pl

TEST_LOG_PATH = os.path.abspath("insight_testsuite/tests/test_features/log_input/log.txt")
DEFAULT_OUTPUT_PATH = os.path.abspath("insight_testsuite/tests/test_features/log_output/")

class TestTopTen(unittest.TestCase):
	
	data = pl.LogProcessor().main(DEFAULT_OUTPUT_PATH, 'top10', TEST_LOG_PATH, 1)
	
	def test_tenresults(self):
		# Parse test file and make sure format is correct
		self.assertEqual(len(self.data),3)
	
	def test_tenformat(self):
		self.assertEqual(self.data,[(6,'199.72.81.55'), (3,'burger.letters.com'), (1,'unicomp6.unicomp.net')])

if __name__ == '__main__':
	unittest.main()