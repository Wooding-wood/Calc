#!/usr/bin/env python3

import sys

#Table
TAX_table = [0,1500,4500,9000,35000,55000,80000]
TAX_RATE = [0,0.03,0.1,0.2,0.25,0.30,0.35,0.45]
TAX_De = [0,0,105,555,1005,2755,5505,13505]
#Base
Base = 3500

#
Taxrate = 0

try:
	salary = int(sys.argv[1])
except:
	print("Value ERROR")

salary_rm_base = salary - Base

if salary_rm_base <= 0:
	cnt = 0
elif 0 < salary_rm_base <= 1500:
    cnt = 1
elif 1500 < salary_rm_base <= 4500:
    cnt = 2
elif 4500 < salary_rm_base <= 9000:
    cnt = 3
elif 9000 < salary_rm_base <= 35000:
	cnt = 4
elif 35000 < salary_rm_base <= 55000:
	cnt = 5
elif 55000 < salary_rm_base <= 80000:
	cnt = 6
elif salary_rm_base > 80000:
	cnt = 7

#print(TAX_RATE[cnt])
#print(TAX_De[cnt])
TAX = (salary_rm_base * TAX_RATE[cnt]) - TAX_De[cnt]

format(TAX, ".2f")
print("%.2f" %TAX)

