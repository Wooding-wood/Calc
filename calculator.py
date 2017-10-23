#!/usr/bin/env python3

import sys
import os
import copy
import csv
from multiprocessing import Process, Queue
import getopt
import configparser
from datetime import date, datetime


#Class
class Config(object):
	def __init__(self, configfile, city):
		self.file = configfile
		self._config = []
		self.city = city.upper()
	# def get_config(self):
	# 	if os.path.exists(self.file):
	# 		with open(self.file) as config:
	# 			# for line in config:                          
	# 			for line in config:
	# 				line_split = line.strip().split(' = ')
	# 				#print(line_split)
	# 				if len(line_split) != 2:
	# 					print("Config File Parameter Error")
	# 				else:
	# 					try:
	# 						self._config[line_split[0]] = float(line_split[1])
	# 					except:
	# 						print("Config Parameter Error")
	# 			return self._config
	# 	else:			
	# 		print("Can't found file,Please try again")
	# 		sys.exit()
	def get_config(self):
		if os.path.exists(self.file):
			config = configparser.ConfigParser()
			config.read(self.file)

			lists_header = config.sections()
			if self.city in config:
				conf = config.items(self.city)
				#return conf
			else:
				conf = config['DEFAULT']
				conf = config.items('DEFAULT')
				#return conf
			#print(conf)
			return conf
		else:
			print("Can't found confing file, Please try again")
			exit()


class UserData(object):
	def __init__(self, userdatafile):
		self.file = userdatafile
		####################################self.userdata = self.get_userdata()     why

	def get_userdata(self):
		user_dict = {}
		if os.path.exists(self.file):
			try:
				with open (self.file, 'r') as data:
					reade = csv.reader(data)
					for row in reade:
						if len(row) != 2:
							print("% File Data Error" %self.file)
							exit()
						else:
							user_dict[row[0].strip()] = int(row[1])
					#print(user_dict)
					return user_dict
			except:
				print("Please check CSV File Format")
				exit()
		else:
			print ("Can't found csv file,Please try again")
			exit()



class calac(object):
	def __init__(self, userdata, config, output):
		self.data = userdata
		self.Config = config
		self.Output = output
		self.result = {}
		self.FormatResult = []
		self.Calacultor()
		self.OutputFile()

	def Calacultor(self):
		for name, salary in self.data.items():
			insurance = self.Cala_enhance(salary, self.Config)
			tax = self.TAX(salary - insurance)
			self.result[name] = ["{:.2f}".format(i) for i in [salary, insurance, tax, (salary - insurance - tax)]]
			t = datetime.now()
			self.FormatResult.append("%s,%s,%s,%s,%s,%s" % (name, self.result[name][0],self.result[name][1], self.result[name][2], self.result[name][3], datetime.strftime(t, '%Y-%m-%d %H:%M:%S')))
		#print(self.FormatResult)


	def OutputFile(self):
		with open(self.Output, 'w') as file:
			#print (self.FormatResult)
			for str in self.FormatResult:
				#print(str)
				writer = csv.writer(file)
				writer.writerow([str])


	def TAX(self, salary):
			# Base
			Base = 3500
			salary -= Base

			if salary <= 0:
				return 0
			TAX_TABLE = [
				(80000, 0.45, 13505),
				(55000, 0.35, 5505),
				(35000, 0.30, 2755),
				(9000, 0.25, 1005),
				(4500, 0.2, 555),
				(1500, 0.1, 105),
				(0, 0.03, 0)
			]
			for item in TAX_TABLE:
				if salary > item[0]:
					return (salary * item[1] - item[2])

	def Cala_enhance(self, salary, config):
		total_insurance = 0
		for i in range(6):
			total_insurance += float(config[i+2][1])

		if salary > float(config[1][1]):
			social_insurance = float(config[1][1]) * total_insurance
		elif salary > float(config[0][1]):
			social_insurance = salary * total_insurance
		else:
			social_insurance = float(config[0][1]) * total_insurance

		return social_insurance



#
def argv_input():
	para = {'-c':'test.cfg', '-d':'UserData.csv', '-o':'gongzi.csv', '-C':''}
	#print(sys.argv)
	try:
		args = sys.argv[1:]
		optlist, args= getopt.getopt(args, 'C:c:d:o:h', ["help"])
		#print (optlist)
		for a in optlist:
			if(a[0] in ('-h', "--help")):
				usage()
				exit()
			else:
				para[a[0]] = a[1]
		#print (para)
		return para
	except:
		print('Parament Error')
		usage()
		exit()

def usage():
	print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')

UserData_Queue = Queue()
def User_Data(input_dic):
	userdata = UserData(input_dic['-d'])
	data_dic = userdata.get_userdata()
	UserData_Queue.put(data_dic)

def Out_Put(config_dic, input_dic):
	output_file = input_dic['-o']
	data_dic = UserData_Queue.get()
	Calac = calac(data_dic, config_dic, output_file)

def main():
	input_dic = argv_input()

	CONFIG = Config(input_dic['-c'], input_dic['-C'])
	config_dic = CONFIG.get_config()
	#############################################a = UserData(input_dic['-d'])      class return not a dict
	Process(target=User_Data, args=(input_dic, )).start()
	Process(target=Out_Put, args=(config_dic, input_dic, )).start()


	# salary_rm_base = salary - Cala_enhance(salary) - Base
	# TAX = Cala_Tax(salary_rm_base)
    #
	# format(TAX, ".2f")
	# print("%.2f" %TAX)

if __name__ == "__main__":
	main()