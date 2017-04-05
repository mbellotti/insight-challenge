import unittest, os
import src.process_log as pl

TEST_LOG_PATH = os.path.abspath("insight_testsuite/tests/test_features/log_input/log.txt")
DEFAULT_OUTPUT_PATH = os.path.abspath("insight_testsuite/tests/test_features/log_output/")

class TestTraffic(unittest.TestCase):
	
	def test_compare_sums_short(self):
		tlst = [(10, '01/Jul/1995:00:00:01 -0400'), (2, '01/Jul/1995:00:00:01 -0400'), (1, '01/Jul/1995:00:00:01 -0400'), (3, '01/Jul/1995:00:00:01 -0400')]
		lst = [10, 2, 1, 3]
		secs = 10
		end = 3
		self.assertEqual(pl.LogProcessor().compare_sums(tlst, lst, secs, end), (16,'01/Jul/1995:00:00:01 -0400'))
		
	def test_compare_sums_long(self):
			tlst = [(10, '01/Jul/1995:00:00:01 -0400'), (2, '01/Jul/1995:00:00:02 -0400'), (1, '01/Jul/1995:00:00:03 -0400'), (3, '01/Jul/1995:00:00:04 -0400'), (10, '01/Jul/1995:00:00:05 -0400'), (7, '01/Jul/1995:00:00:06 -0400'), (1, '01/Jul/1995:00:00:07 -0400'), (4, '01/Jul/1995:00:00:08 -0400'), (10, '01/Jul/1995:00:00:09 -0400'), (5, '01/Jul/1995:00:00:10 -0400'), (1, '01/Jul/1995:00:00:11 -0400'), (1, '01/Jul/1995:00:00:12 -0400'), (10, '01/Jul/1995:00:00:13 -0400'), (8, '01/Jul/1995:00:00:14 -0400'), (1, '01/Jul/1995:00:00:15 -0400'), (10, '01/Jul/1995:00:00:16 -0400')]
			lst = [x[0] for x in tlst]
			secs = 5
			end = 15
			self.assertEqual(pl.LogProcessor().compare_sums(tlst, lst, secs, end), (32,'01/Jul/1995:00:00:05 -0400'))

	def test_sum_sublist_full(self):
		lst = [1,2,3,4]
		self.assertEqual(pl.LogProcessor().sum_sublist(0,4,lst), 10)

	def test_sum_sublist_partial(self):
		lst = [1,2,3,4,5,6,7,8,9]
		self.assertEqual(pl.LogProcessor().sum_sublist(0,4,lst), 10)

	def test_filter_peaks_fail(self):
		lst = [(10, '01/Jul/1995:00:00:01 -0400'), (2, '01/Jul/1995:00:00:02 -0400'), (1, '01/Jul/1995:00:00:03 -0400'), (3, '01/Jul/1995:00:00:04 -0400'), (10, '01/Jul/1995:00:00:05 -0400'), (7, '01/Jul/1995:00:00:06 -0400'), (1, '01/Jul/1995:00:00:07 -0400'), (4, '01/Jul/1995:00:20:08 -0400'), (10, '01/Jul/1995:00:00:09 -0400'), (5, '01/Jul/1995:00:00:10 -0400'), (1, '01/Jul/1995:20:00:11 -0400'), (1, '01/Jul/1995:00:00:12 -0400'), (10, '01/Jul/1995:00:00:13 -0400'), (8, '01/Jul/1995:00:00:14 -0400'), (1, '01/Jul/1995:00:00:15 -0400'), (10, '01/Jul/1995:10:00:16 -0400')]
		self.assertEqual(pl.LogProcessor().filter_peaks(lst, 1), False)
		
	def test_filter_peaks_pass(self):
		lst = [(1, '01/Jul/1995:20:00:11 -0400'), (1, '01/Jul/1995:00:00:12 -0400')]
		self.assertEqual(pl.LogProcessor().filter_peaks(lst, 0), (1, '01/Jul/1995:20:00:11 -0400'))

	def test_check_results(self):
		data = pl.LogProcessor().main(DEFAULT_OUTPUT_PATH, 'traffic', TEST_LOG_PATH, 1)
		self.assertEqual(data, [(8, '01/Jul/1995:00:00:01 -0400')])
		
		
if __name__ == '__main__':
	unittest.main()