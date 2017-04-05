import unittest, os
import src.process_log as pl

TEST_LOG_PATH = os.path.abspath("insight_testsuite/tests/test_features/log_input/log.txt")
DEFAULT_OUTPUT_PATH = os.path.abspath("insight_testsuite/tests/test_features/log_output/")

class TestFail2Ban(unittest.TestCase):
	
	#data = pl.LogProcessor().fail2ban(TEST_LOG_PATH)
	
	def test_failed_login_detected(self):
		line = pl.LogProcessor().extract_data('221.139.59.83 - - [01/Jul/1995:00:03:31 -0400] “POST /login HTTP/1.0" 401 1420\n')
		self.assertTrue(pl.LogProcessor().failed_login_detected(line[3]))
		
	def test_failed_login_not_detected(self):
		line = pl.LogProcessor().extract_data('219.207.85.53 - - [01/Jul/1995:00:03:34 -0400] “GET / HTTP/1.0" 401 7074\n')
		self.assertFalse(pl.LogProcessor().failed_login_detected(line[3]))
		
	def test_failed_login_not_detected2(self):
		line = pl.LogProcessor().extract_data('221.139.59.83 - - [01/Jul/1995:00:03:31 -0400] “POST /login HTTP/1.0" 200 1420\n')
		self.assertFalse(pl.LogProcessor().failed_login_detected(line[3]))
		
	def test_failed_login_not_detected3(self):
		line = pl.LogProcessor().extract_data('221.139.59.83 - - [01/Jul/1995:00:03:31 -0400] “POST / HTTP/1.0" 401 1420\n')
		self.assertFalse(pl.LogProcessor().failed_login_detected(line[3]))
		
	def test_check_and_ban_less_than_3(self):
		ip = (['01/Jul/1995:00:00:09 -0400', '01/Jul/1995:00:00:19 -0400'], 0)
		time = '01/Jul/1995:00:00:09 -0400'
		self.assertFalse(pl.LogProcessor().check_and_ban(ip,time))
		
	def test_check_and_ban(self):
		ip = (['01/Jul/1995:00:00:09 -0400', '01/Jul/1995:00:00:19 -0400', '01/Jul/1995:00:00:20 -0400'], 0)
		time = '01/Jul/1995:00:00:09 -0400'
		self.assertTrue(pl.LogProcessor().check_and_ban(ip,time))
		
	def test_check_and_ban_already_banned(self):
		ip = (['01/Jul/1995:00:00:09 -0400', '01/Jul/1995:00:00:19 -0400', '01/Jul/1995:00:00:20 -0400'], 1)
		time = '01/Jul/1995:00:00:22 -0400'
		self.assertTrue(pl.LogProcessor().check_and_ban(ip,time))
		
	def test_check_and_ban_expired(self):
		ip = (['01/Jul/1995:00:00:09 -0400', '01/Jul/1995:00:00:19 -0400', '01/Jul/1995:00:00:20 -0400'], 1)
		time = '01/Jul/1995:00:06:22 -0400'
		self.assertEqual(pl.LogProcessor().check_and_ban(ip,time), 2)
		
	def test_check_results(self):
		data = pl.LogProcessor().main(DEFAULT_OUTPUT_PATH, 'fail2ban',TEST_LOG_PATH, 1)
		self.assertEqual(data[0:17],'199.72.81.55 - - ')
		
		
if __name__ == '__main__':
	unittest.main()