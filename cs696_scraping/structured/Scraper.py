# #!/usr/bin/env python
# # coding: utf-8
#
# # In[13]:


import numpy as np
import pandas as pd
import sys
import csv
import xlrd
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# In[14]:


sys.path.insert(0, r"/home/kajaltiwari/CS696/CS696_Stock_fundamental_prediction/")

#
# # In[15]:
#

from edgar.stock import Stock
wb = xlrd.open_workbook('ticker_lists.xlsx')
sheet = wb.sheet_by_index(0)
stock_list=[]
for i in range(5,2956):
    stock_list.append(sheet.cell_value(i,0))

# # In[16]:
#
#

with open('Data_2016_3k.csv', mode='w' ,newline='') as file:
  file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  file_writer.writerow(["year",'Company',"CIK", "Revenue", "NetIncomeLoss","Payments to acquire property"])




# In[17]:


revenue=['us-gaap_SalesRevenueNet','us-gaap_Revenues','us-gaap:Revenues','us-gaap:SalesRevenueNet','us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax']
netinc=['us-gaap:NetIncomeLoss','us-gaap_NetIncomeLoss','us-gaap:NetIncomeLoss']
rnd=['us-gaap:ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost','us-gaap_ResearchAndDevelopmentExpense']
prop=['us-gaap_PaymentsToAcquirePropertyPlantAndEquipment','us-gaap_PropertyPlantAndEquipmentNet','us-gaap_PaymentsToAcquireProductiveAssets']


# # In[ ]:
#
#
#
#
#
# # In[18]:
#
#
cik_not_found=[]
year_not_found=[]
income_statements_error=[]
balance_sheets_error=[]
cash_flows_error=[]

for y in range(2017,2018):
    for k in stock_list:

        try:
            stock = Stock(k)
        except:
            cik_not_found.append(k)
            continue
        period = 'quarterly'

        try:
            filing = stock.get_filing('annual',y,1)
        except:
            year_not_found.append([k,y])

        try:
          income_statements = filing.get_income_statements()
          newdict_income_statements = income_statements.reports[0]
        except:
          income_statements_error.append(k)
        try:
          balance_sheets = filing.get_balance_sheets()
          newdict_balance_sheets = balance_sheets.reports[0]




        #print(type(income_statements),type(cash_flows))


        except:


            balance_sheets_error.append(k)
        try:
            cash_flows = filing.get_cash_flows()
            newdict_cash_flows = cash_flows.reports[0]
        except:
            cash_flows_error.append(k)
#         print("\n\n",income_statements)
#         print("\n\n",cash_flows)
        #print(newdict_balance_sheets.map.keys())
        with open('Data_2016_3k.csv', mode='a',newline='') as file:
            file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            if income_statements:
                    print(income_statements)
                    print(newdict_income_statements.map.keys())
                    rev=0
                    rnd='tag not found'
                    for i in revenue:
                          if i in newdict_income_statements.map.keys():

                              rev=newdict_income_statements.map[i].value


                    for m in newdict_income_statements.map.keys():
                          if m in rnd:
                              rnd=newdict_income_statements.map[m].value




            else:
                rev='Income statement not found'
                rnd='Income statement not found'
            if cash_flows:
                    netincome=0
                    paymentProp='tag not found'
                    for j in netinc:
                        if j in newdict_cash_flows.map.keys():
                        #print(i)
                            netincome=newdict_cash_flows.map[j].value



                    for p in prop:
                        if p in newdict_cash_flows.map.keys():
                            paymentProp=newdict_cash_flows.map[p].value





            else:
                netincome='cash flow not found'
                paymentProp='cash flow not found'

            file_writer.writerow([y-1,k,stock.cik, rev,netincome,paymentProp])


f=open("Error_log_2018.txt","w")
f.write("\nCIK not found \n")
f.write(str(cik_not_found))
f.write("\nYEAR not found \n")
f.write(str(year_not_found))
f.write("\nIncome Statement Not found \n")
f.write(str(income_statements_error))
f.write("\nBalance sheet not found \n")
f.write(str(balance_sheets_error))
f.write("\nCash flow not found \n")
f.write(str(cash_flows_error))

f.close()

# In[ ]:


# cash_flows.reports[1]


# In[ ]:


# cash_flows.reports[0]


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




