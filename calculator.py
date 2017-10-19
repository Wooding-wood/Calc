#!/usr/bin/env python3

import sys


#Base
Base = 3500

#
def Cala_Tax(salary):
#Table
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

def Cala_enhance(salary):
	SOCIAL_INSURANCE = (0.08, 0.02, 0.005, 0, 0, 0.06)
	social_insurance = salary * sum(SOCIAL_INSURANCE)
	return social_insurance

def main():
	if len(sys.argv) != 2:
		print('Parameter Error')
	try:
		salary = int(sys.argv[1])
	except:
		print("Value ERROR")

	salary_rm_base = salary - Cala_enhance(salary) - Base
	TAX = Cala_Tax(salary_rm_base)

	format(TAX, ".2f")
	print("%.2f" %TAX)

if __name__ == "__main__":
	main()