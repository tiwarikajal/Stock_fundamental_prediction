import xlrd
import sys
import csv
# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = "all"
sys.path.insert(0, r"C:\Umass spring 20\696\nikitas\sec-edgar-financials")
from edgar.stock import Stock

wb = xlrd.open_workbook('ticker_lists.xlsx')
sheet = wb.sheet_by_index(0)
stock_list = []
for i in range(11, 985):
    stock_list.append(sheet.cell_value(i, 0))

with open('Data.csv', mode='w') as file:
    file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(
        ["year", 'Company', "CIK", "Revenue", "NetIncomeLoss", "R&D Expense", "Payments to acquire property"])

cik_not_found = []
year_not_found = []
income_statements_error = []
balance_sheets_error = []
cash_flows_error = []

for y in range(2013, 2014):
    for i in stock_list[1:10]:

        try:
            stock = Stock(i)
        except:
            cik_not_found.append(i)
            continue
        period = 'annual'

        try:
            filing = stock.get_filing('annual', y, 1)
        except:
            year_not_found.append([i, y])

        income_statements = filing.get_income_statements()
        balance_sheets = filing.get_balance_sheets()
        cash_flows = filing.get_cash_flows()
        # print(type(income_statements),type(cash_flows))
        try:
            newdict_income_statements = income_statements.reports[0]
        except:
            income_statements_error.append(i)
        try:
            newdict_balance_sheets = balance_sheets.reports[0]
        except:
            balance_sheets_error.append(i)
        try:
            newdict_cash_flows = cash_flows.reports[0]
        except:
            cash_flows_error.append(i)
        #         print("\n\n",income_statements)
        #         print("\n\n",cash_flows)

        with open('Data.csv', mode='a') as file:
            file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            if income_statements:
                try:
                    rev = newdict_income_statements.map['us-gaap_Revenues'].value

                except:
                    rev = 'ERROR'
                try:
                    rnd = newdict_income_statements.map['us-gaap_ResearchAndDevelopmentExpense'].value
                except:
                    rnd = 'ERROR'
            else:
                rev = 'ERROR'
                rnd = 'ERROR'
            if cash_flows:
                try:
                    netincome = newdict_cash_flows.map['us-gaap_NetIncomeLoss'].value

                except:
                    netincome = 'ERROR'
                try:
                    paymentProp = newdict_cash_flows.map['us-gaap_PaymentsToAcquirePropertyPlantAndEquipment'].value
                except:
                    paymentProp = 'ERROR'
            else:
                netincome = 'ERROR'
                paymentProp = 'ERROR'

            file_writer.writerow([y, i, stock.cik, rev, netincome, rnd, paymentProp])

