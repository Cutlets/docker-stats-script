#!/usr/bin/python3

import os
import os.path
import pprint
import numpy as np
import pandas as pd
import subprocess
from datetime import datetime

def searchList(lst, v):
	i = 0
	for info in lst:
		try:
			idx = info.index(v)
			return i
		except ValueError:
			i = i+1

	if i == len(lst):
		return -1

	return -2

def getFiles(logDir):
	f = os.listdir(logDir)

	f.sort(reverse=True)
	return f

def filesToDf(files, times):
	f = files.sort()
	dinfo = []
	tmp = []

	datelist = []

	for i in range(times+1):
		tmp.append("null")

	for i in range(len(files)):
		date = files[i][35:len(files[i])-4]
		datelist.append(date)
	datelist.sort()

	data = pd.DataFrame()

	data.insert(0, "Container Name", True)
	for d in datelist:
		data.insert(data.shape[1], d, True)

	#	print(data)

	for i in range(len(files)):
		txt = open(files[i], "r")
		strings = txt.readlines()
		for s in strings:
			text = s.split()
			if text[0] == 'CONTAINER':
				continue
			dname = text[0]
			dcpu = text[1]
			dmem = text[2] + text[3] + text[4]
			dstat = dcpu + " // " + dmem

			idx = searchList(dinfo, dname)
	#	print("Index : ", idx, "INFO : ",dname,"\t",dstat)

			if idx == -1:
				tmp2 = tmp[:]
				tmp2[0] = dname
				tmp2[i+1] = dstat
				dinfo.append(tmp2)
			else:
				dinfo[idx][i+1] = dstat

	#	pp = pprint.PrettyPrinter(indent=4)
	#	pp.pprint(dinfo)

	for i in dinfo:
		data.loc[data.shape[0]] = i

	return data


if __name__ == "__main__":
	debugMod = False
	collectTimes = 12
	logDir = "/home/cutlets/dp/log/"
	files = getFiles(logDir)
	files = files[:collectTimes]

	for i in range(collectTimes):
		files[i] = logDir+files[i]

	df = filesToDf(files, collectTimes)
	now = datetime.now()

	fname = "CSV-LOG " + now.strftime(('%Y-%m-%d %H:%M:%S')) + ".csv"
	fname = "./log_csv/"+fname
	df.to_csv(fname)

	shellString =  "echo \"Conatiner Report\" | mailx -s \"Docker Report Arrived\" -A \""  +fname+ "\" cutlets3254@gmail.com"

	subprocess.call(shellString, shell=True)

	if debugMod:
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(files)


