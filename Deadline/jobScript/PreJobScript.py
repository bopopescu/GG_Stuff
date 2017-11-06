import re, os, subprocess
from System.IO import *
from Deadline.Scripting import *

deadlineEXE = "C:/Program Files/Thinkbox/Deadline7/bin/deadlinecommand.exe"

def __main__( *args ):
	deadlinePlugin = args[0]
	job = deadlinePlugin.GetJob()
	outputDirectories = job.OutputDirectories
	outputFilenames = job.OutputFileNames
	paddingRegex = re.compile("[^\\?#]*([\\?#]+).*")
	for i in range( 0, len(outputDirectories) ):
		outputDirectory = outputDirectories[i]
		
		### remove existed file
		def communicate_with_deadline(*args):
			communicateWithDeadline = subprocess.Popen([deadlineEXE, args[0], args[1]], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
			getDatas = communicateWithDeadline.communicate()
			getData = getDatas[0]
			return getData
		
		fileOutput = os.listdir(outputDirectory)
		getJobID = communicate_with_deadline('GetJobIdsFilter', 'JobName=%s'%job)
		status = communicate_with_deadline('GetJobTasks', getJobID)
		splitStatus = status.split("\r\n")
		frameDatas = [frameDatas for frameDatas in splitStatus if frameDatas.startswith("TaskFrameList")==True]
		statusDatas = [statusDatas for statusDatas in splitStatus if statusDatas.startswith("Status")==True]
		
		for frameData, statusData in zip(frameDatas, statusDatas):
			if statusData.split("=")[-1] == "Queued":
				deleteFrame = frameData.split("=")[-1]
				deleteFrameReformat = ('{:04d}'.format(int(deleteFrame))) 
				for output in fileOutput:
					if output.split(".")[-2] == deleteFrameReformat:
						deadlinePlugin.LogInfo(outputDirectory + "\%s"%output)
						os.remove(outputDirectory + "\%s"%output)