import argparse, re, os
import datetime as dt
from itertools import islice

DEFAULT_LOG_PATH = os.path.abspath("log_input/log.txt")
DEFAULT_OUTPUT_PATH = os.path.abspath("log_output/")
LOG_DATA = re.compile(r"^(?P<ip>.*)\s-\s-\s\[(?P<time>[A-Za-z0-9\/:\-\s]*)\]\s?(?P<target>.*)\s(?P<bits>\d*|-)\n")

class LogProcessor():
	
	def topten(self, path):
		ips = []
		c = {}
		with open(path,encoding='latin-1') as f:
			for line in f:
				ip, bits, time, target = self.extract_data(line)
				# increment ip
				if ip in c:
					idx = c[ip]
					ips[idx] = ((ips[idx][0]+1),ip)
				else:
					c[ip] = len(ips)
					ips.append((1,ip))
		
		ips.sort(reverse=True) #Used tuples because it allows us to store multiple values and easily sort by the first one.
					
		#Format Results
		return ips[:10]
	
	
	def bandwidth(self, path):
		bit_totals = []
		c = {}
		resource = re.compile(r"[A-Z]*\s(?P<resource>[A-Za-z0-9\/\.\-_]*)\s?[A-Z]*\s?.*")
		
		with open(path,encoding='latin-1') as f:
			for line in f:
				ip, bits, time, target = self.extract_data(line)
				if bits != '-':
					resource_matches = re.search(resource, target)
					r = resource_matches.group('resource')
					if r in c:
						idx = c[r]
						bit_totals[idx] = ((bit_totals[idx][0]+int(bits)),r)
					else:
						c[r] = len(bit_totals)
						bit_totals.append((int(bits),r))
		bit_totals.sort(reverse=True)
		
		return bit_totals[:10]
	
	def traffic(self, path):
		past = []
		time_range = []
		c = {}
		time_list = []
		with open(path,encoding='latin-1') as f:
			for line in f:
				ip, bits, time, target = self.extract_data(line)
				
				if not past:
					past = time
				else:
					gap = self.calculate_gap(past, time)
					# Fill in missing time periods
					time_range.extend([(0,'')]*gap)
					time_list.extend([0]*gap)
					past = time
				
				if time in c:
					idx = c[time]
					time_range[idx] = ((time_range[idx][0]+1),time)
					time_list[idx] = time_list[idx]+1
				else:
					c[time] = len(time_range)
					time_range.append((1,time))
					time_list.append(1)
				
		t = self.time_periods(60, time_range, time_list, c)
		t.sort(reverse=True)
		return t[:10]
	
	def fail2ban(self, path):
		ips = {}
		blocked = ''
		with open(path,encoding='latin-1') as f:
			for line in f:
				ip, bits, time, target = self.extract_data(line)
				
				#Is line a login failure?
				if self.failed_login_detected(target):
					# increment ip
					if ip in ips:
						lst = ips[ip][0]
						lst.append(time)
						ips[ip] = (lst,ips[ip][1])
					else:
						ips[ip] = ([time], 0)
				
				#Check if ip is blocked
				if ip in ips:
					banned = self.check_and_ban(ips[ip], time)
					if banned:
						ips[ip] = (ips[ip][0], 1)
						blocked += line
					elif banned == 2:# Ban has expired
						ips[ip] = ([],0)

		return blocked
	
	def check_and_ban(self, ip, time):
		if len(ip[0]) < 3:
			return 0
		elif len(ip[0]) > 1 and time == ip[0][2]:
			return 0
		elif ip[1] == 1:
			if self.calculate_gap(ip[0][2],time) > 250:
				return 2
			else:
				return 1
		elif self.calculate_gap(ip[0][0], ip[0][2]) <= 20:
				return 1
		return 0
			
	
	def failed_login_detected(self, target):
		target=target.encode('ascii', 'ignore').decode()
		if target[0] == '"':
			target = target[1:]	
		if target[0:4] != 'POST':
			return False
		if int(target[-3:]) != 401: # Funny story, software like Wordpress will actually log failed logins with POST - 200
			return False
		if target[5:11] != '/login':
			return False
		return True
	
	def time_periods(self, unit, data, dlst, m):
		sums = []
		secs = unit*60
		#Find the ten highest bars
		peaks = list(data) # Creating copies of things in Python is sometimes dumb, but this is faster than the copy module
		peaks.sort(reverse=True)
		peaks = [x for x in islice([p for i, p in enumerate(peaks) if self.filter_peaks(peaks, i)], 10)]
		#Build lists based on the 3600 greatest consecutive values either to left or right
		for p in peaks:
			idx = m[p[1]] #index of the peak in the original unsort list
			start = idx-secs if idx-secs >= 0 else 0
			end = idx+secs if idx+secs <= (len(data)-1) else (len(data)-1)
			segment = data[start:end]
			lst = dlst[start:end]
			tsums = self.compare_sums(segment, lst, secs, end)
			sums.append(tsums)
		return sums
	
	def calculate_gap(self, past, present):
		months = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun': 6,'Jul': 7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12} # For this volume of data, would rather not bother with conventional string to datetime. ;) 
		
		if not past or not present:
			return 0
		past,present = past[:-6].split(":"), present[:-6].split(":") #Trim timezones
		past_date = past[0].split('/')
		pres_date = present[0].split('/')
		
		if past[0] == present[0] and ((int(present[3]) - int(past[3])) <= 1 or (present[3] == '00' and past[3] == '59')):
			return 0
		x = dt.datetime(int(past_date[2]),months[past_date[1]],int(past_date[0]),int(past[1]),int(past[2]),int(past[3]))
		y = dt.datetime(int(pres_date[2]),months[pres_date[1]],int(pres_date[0]),int(present[1]),int(present[2]),int(present[3]))
		return int((y-x).total_seconds())-1
	
	def filter_peaks(self, peaks, index):
		if index == 0:
			return peaks[index]
		if self.calculate_gap(peaks[(index-1)][1], peaks[index][1]) > 3600:
			return peaks[index]
		return False
	
	def compare_sums(self, tlst, lst, secs, end):
		tsums = (0,'')
		
		for i, l in enumerate(tlst):
			if len(tlst) < secs or i+secs <= end:
				if l[0] == 0: #Skip placeholder seconds
				 	continue
				curr_sum = self.sum_sublist(i, secs, lst)
				
				#Identify timestamp of first value
				if curr_sum > tsums[0]:
					tsums = (curr_sum, l[1])
		return tsums	
	
	def sum_sublist(self, start, unit, lst):
		return sum(lst[start:start+unit])
		
	def extract_data(self, line):
		matches = re.search(LOG_DATA, line)
		try:
			return matches.group('ip'), matches.group('bits'), matches.group('time'), matches.group('target')
		except:
			return ('',0,0,'')

	def write_log(self, data, mode, path, filename):
		with open(os.path.join(path,filename),'a') as f:
			if mode == 'string':
				f.write(data)
			elif mode == 'no count':
				for d in data:
					f.write(d[1]+'\n')
			else:
				for d in data:
					f.write(d[1]+','+str(d[0])+'\n')
		return True
				
		
	def main(self, path=DEFAULT_OUTPUT_PATH, mode=None, filepath=DEFAULT_LOG_PATH, test=0):
		data = ''
		if not filepath:
			filepath = DEFAULT_LOG_PATH
		if mode.lower() == 'top10' or mode.lower() == 'topten':
			data = self.topten(filepath)
			mode = 'tuple list'
			filename = 'hosts.txt'
		if mode.lower() == 'bandwidth':
			data = self.bandwidth(filepath)
			mode = 'no count'
			filename = 'resources.txt'
		if mode.lower() == 'traffic':
			data = self.traffic(filepath)
			mode = 'tuple list'
			filename = 'hours.txt'
		if mode.lower() == 'fail2ban':
			data = self.fail2ban(filepath)
			mode = 'string'
			filename = 'blocked.txt'
		if mode.lower() == 'all':
			print('Calculating the Top Ten IPs Addresses...')
			self.write_log(self.topten(filepath), 'tuple list', path, 'hosts.txt')
			print('Calculating the Top Ten Resources...')
			self.write_log(self.bandwidth(filepath), 'tuple list', path,  'resources.txt')
			print('Calculating the Ten Busiest Hours...')
			self.write_log(self.traffic(filepath), 'tuple list', path, 'hours.txt')
			print('Logging Blocked Requests...')
			self.write_log(self.fail2ban(filepath), 'string', path, 'blocked.txt')
			
		if test:
			return data
		elif not test and mode.lower() == 'all':
			return
		else:
			self.write_log(data, mode, path, filename)
		
if __name__ == '__main__':
	p = argparse.ArgumentParser()
	p.add_argument('-m', '--mode', help='Select the mode processor will run in. Options: top10, bandwidth, traffic ,fail2ban')
	p.add_argument('-f', '--filepath', help='The location of log file to process')
	args = p.parse_args()
	LogProcessor().main(DEFAULT_OUTPUT_PATH, args.mode, args.filepath)