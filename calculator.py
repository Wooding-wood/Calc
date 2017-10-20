#!/usr/bin/env python3

import sys
import os
import copy
import csv

#Class
class Config(object):
	def __init__(self, configfile):
		self.file = configfile
		self._config = {}
	def get_config(self):
		if os.path.exists(self.file):
			with open(self.file) as config:
				# for line in config:                          
				for line in config:
					line_split = line.strip().split(' = ')
					#print(line_split)
					if len(line_split) != 2:
						print("Config File Parameter Error")
					else:
						try:
							self._config[line_split[0]] = float(line_split[1])
						except:
							print("Config Parameter Error")
				return self._config
		else:			
			print("Can't found file,Please try again")
			sys.exit()


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
			self.FormatResult.append("%s,%s,%s,%s,%s" % (name, self.result[name][0],self.result[name][1], self.result[name][2], self.result[name][3]))
		#print(self.FormatResult)


	def OutputFile(self):
		with open(self.Output, 'w') as file:
			print (self.FormatResult)
			for str in self.FormatResult:
				print(str)
				writer = csv.writer(file)
				writer.writerow(str)


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
		SOCIAL_INSURANCE = {}
		SOCIAL_INSURANCE = copy.deepcopy(config)
		SOCIAL_INSURANCE.pop('JiShuH')
		SOCIAL_INSURANCE.pop('JiShuL')

		if salary > config['JiShuH']:
			social_insurance = config['JiShuH'] * sum(SOCIAL_INSURANCE.values())
		elif salary > config['JiShuL']:
			social_insurance = salary * sum(SOCIAL_INSURANCE.values())
		else:
			social_insurance = config['JiShuL'] * sum(SOCIAL_INSURANCE.values())

		return social_insurance



#
def argv_input():
	para = {'-c':'', '-d':'', '-o':''}
	#print(sys.argv)
	if len(sys.argv) != 7:
		print('Parameter Error')
	else:
		try:
			args = sys.argv[1:]
			for index in para.keys():
				index_num = args.index(index)
				para[index] = args[index_num + 1]
			return para
		except:
			print('Parameter Error')



def main():
	input_dic = argv_input()

	CONFIG = Config(input_dic['-c'])
	config_dic = CONFIG.get_config()
	#############################################a = UserData(input_dic['-d'])      class return not a dict
	userdata = UserData(input_dic['-d'])
	data_dic = userdata.get_userdata()
	output_file = input_dic['-o']
	Calac = calac(data_dic, config_dic, output_file)
	# salary_rm_base = salary - Cala_enhance(salary) - Base
	# TAX = Cala_Tax(salary_rm_base)
    #
	# format(TAX, ".2f")
	# print("%.2f" %TAX)

if __name__ == "__main__":
	main()