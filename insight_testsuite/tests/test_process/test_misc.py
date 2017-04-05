import unittest, os
import src.process_log as pl

TEST_LOG_PATH = os.path.abspath("insight_testsuite/tests/test_features/log_input/log.txt")
DEFAULT_OUTPUT_PATH = os.path.abspath("insight_testsuite/tests/test_features/log_output/")

class TestMisc(unittest.TestCase):
	
	def test_extraction_pass(self):
		# Is the regex extracting data from input
		test='199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] “POST /login HTTP/1.0” 401 1420\n'
		self.assertEqual(pl.LogProcessor().extract_data(test), ('199.72.81.55', '1420', '01/Jul/1995:00:00:01 -0400', '“POST /login HTTP/1.0” 401'))
		
	def test_extraction_fail(self):
		test = '- - 00:00:01 -0400 POST\n'
		# Is the regex extracting data from input
		self.assertNotEqual(pl.LogProcessor().extract_data(test), ('199.72.81.55', '1420', '01/Jul/1995:00:00:01 -0400'))
		
	def test_calculate_gap(self):
		self.assertEqual(pl.LogProcessor().calculate_gap('01/Jul/1995:00:00:09 -0400', '03/Jul/1995:00:00:09 -0400'),172799)
		
	def test_calculate_gap_small(self):
		self.assertEqual(pl.LogProcessor().calculate_gap('01/Jul/1995:00:00:09 -0400', '01/Jul/1995:00:00:10 -0400'),0)
		
	def test_write_log(self):
		data = "This is a test"
		mode = "string"
		file = pl.LogProcessor().write_log(data, mode, DEFAULT_OUTPUT_PATH, 'test.txt')
		
		f = open(os.path.join(DEFAULT_OUTPUT_PATH,'test.txt'),encoding='latin-1')
		self.assertEqual(f.read(), "This is a test")
		f.close()
		
		os.remove(os.path.join(DEFAULT_OUTPUT_PATH,'test.txt')) 

if __name__ == '__main__':
	unittest.main()