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

salary = int( sys.argv[1])
print(salary)
salary_rm_base = salary - Base

for cnt in range(6):
    if(TAX_table[cnt] <= salary_rm_base <= TAX_table[cnt+1]):
        print(cnt)
        break
