import csv
import statistics 
import datetime
#a=[1,2]
#print(statistics.mean(a))
filename='sample.csv'

def convertmonth(month):
	if month.upper()=='JAN':
		return 1
	if month.upper()=='FEB':
		return 2
	if month.upper()=='MAR':
		return 3
	if month.upper()=='APR':
		return 4
	if month.upper()=='MAY':
		return 5 
	if month.upper()=='JUN':
		return 6
	if month.upper()=='JUL':
		return 7 
	if month.upper()=='AUG':
		return 8
	if month.upper()=='SEP':
		return 9
	if month.upper()=='OCT':
		return 10
	if month.upper()=='NOV':
		return 11
	if month.upper()=='DEC':
		return 12
def checkmonth(month):
	if (month.upper()=='JAN' or month.upper()=='FEB' or month.upper()=='MAR' or month.upper()=='APR' or
		 month.upper()=='MAY' or month.upper()=='JUN' or month.upper()=='JUL' or month.upper()=='AUG' or 
		 month.upper()=='SEP' or month.upper()=='OCT' or month.upper()=='NOV' or month.upper()=='DEC'):
		return 1
	else:
		return 0

def formatdate(message):
	dat=input(message)
	if (len(dat.split('-')))==3:
		for value in dat.split('-'):
			if len(value)<=2:
				if len(value)==1:
					date='0'+str(value)
				else:
					date=value
			elif len(value)==4:
				year=value
			elif len(value)==3:
				if checkmonth(str(value))==1:
					month=convertmonth(value)
				else:
					print("Invalid Month, Please Use first 3 letters of month")
					return formatdate(message)
	else:
		print("\nInvalid input. Please Enter Date in correct format seperated by '-'\nEg: 'Date/year/month - Date/year/month - Date/year/month'\n")
		return formatdate(message)
	try:
			return datetime.date(int(year),int(month),int(date))
	except UnboundLocalError:
		print("\nInvalid Input. Please Enter Date in correct format seperated by '-'\nEg: 'Date/year/month - Date/year/month - Date/year/month'\n")
		return formatdate(message)
	except ValueError:
		print("\nInvalid Input. Please Enter Date in correct format seperated by '-'\nEg: 'Date/year/month - Date/year/month - Date/year/month'\n")
		return formatdate(message)


def searchcode(code):
	with open(filename) as csv_file:
		output=[]
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if row[0]==code:
				return 1
			else:
				if line_count == 0:
					line_count += 1
				elif line_count>0:
					if (row[0].find(code.upper()) != -1):
						if row[0] not in output:
							return row[0]
					line_count += 1

def codeinput():
	code=input("Enter The STOCK CODE : ")
	if (searchcode(code))!=None:
		if(searchcode(code))==1:
			return code
		else:
			k=input("Did You Mean : "+searchcode(code)+" (Y/N) : ")
			if k=='Y':
				return searchcode(code)
			else:
				return codeinput()
	else:
		print ("Code Not Found")
		return codeinput()

def findstatistics(start,end,symbol):
	stats=[]
	prices=[]
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
			else:
				chkdate=datetime.date(int(row[1][7:11]),convertmonth(row[1][3:6]),int(row[1][0:2]))
				#chkdate=chkdate.strftime("%d-%b-%Y")
				if (row[0]==symbol and chkdate>=startdate and chkdate<=enddate):
					prices.append(float(row[2]))
				line_count += 1
	stats.append(statistics.mean(prices))
	stats.append(statistics.stdev(prices))
	return stats

def checkprice(startdate,enddate,symbol):
	with open(filename) as csv_file:
		low=[]
		high=[]
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
			else:
				chkdate=datetime.date(int(row[1][7:11]),convertmonth(row[1][3:6]),int(row[1][0:2]))
				#chkdate=chkdate.strftime("%d-%b-%Y")
				if (row[0]==symbol and chkdate>=startdate and chkdate<=enddate):
					if(low!=[] and high!=[]):
						if low[1]>float(row[2]):
							low.clear()
							low.append(row[1])
							low.append(float(row[2]))
						elif high[1]<float(row[2]):
							high.clear()
							high.append(row[1])
							high.append(float(row[2]))
					else:
						low.append(row[1])
						low.append(float(row[2]))
						high.append(row[1])
						high.append(float(row[2]))
					line_count+=1
		return (low+high)



#print(checkmonth("dec"))
symbol=codeinput()
startdate=formatdate("Enter Start Date. Seperate Fields by '-'")
#print(startdate)
enddate=formatdate("Enter End Date. Seperate Fields by '-'")
#print(enddate)
if startdate>enddate:
	print("Startdate can't be greater than enddate")
else:
	stats=findstatistics(startdate,enddate,symbol)
	profit=checkprice(startdate,enddate,symbol)
	print("\n\nHere is your Result :\nMean : "+str(stats[0])+"\nStd : "+str(stats[1])+"\nBuy Date : "+
		profit[0]+"\nSell Date : "+profit[2]+"\nProfit : Rs"+str((float(profit[3])-float(profit[1]))*100))
#print(codeinput())
#print(stats)
#print(startdate)
#print(enddate)  