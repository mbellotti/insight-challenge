import unittest, os
import src.process_log as pl

TEST_LOG_PATH = os.path.abspath("insight_testsuite/tests/test_features/log_input/log.txt")
DEFAULT_OUTPUT_PATH = os.path.abspath("insight_testsuite/tests/test_features/log_output/")

class TestBandwidth(unittest.TestCase):
	
	data = pl.LogProcessor().main(DEFAULT_OUTPUT_PATH, 'bandwidth', TEST_LOG_PATH, 1)
	
	def test_tenresults(self):
		# Parse test file and make sure format is correct
		self.assertEqual(len(self.data),3)
	
	def test_tenformat(self):
		self.assertEqual(self.data,[(8520, '/login'), (7970, '/shuttle/countdown/'), (0, '/shuttle/countdown/liftoff.html')])

if __name__ == '__main__':
	unittest.main()