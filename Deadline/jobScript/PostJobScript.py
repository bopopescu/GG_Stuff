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
		outputFilename = outputFilenames[i]
		startFrame = deadlinePlugin.GetStartFrame()
		endFrame = deadlinePlugin.GetEndFrame()
		for frameNum in range(startFrame, endFrame+1):
			outputPath = Path.Combine(outputDirectory,outputFilename)
			outputPath = outputPath.replace("//","/")
			m = re.match(paddingRegex,outputPath)
			if( m != None):
				padding = m.group(1)
				frame = StringUtils.ToZeroPaddedString(frameNum,len(padding),False)
				outputPath = outputPath.replace( padding, frame )
			
			getFilePath = os.listdir(outputPath)
			outputFrame = []
			for filePath in getFilePath:
				outputFrame.append(int(filePath.split(".")[-2]))
			outputFrameSorted = sorted(outputFrame)
			#deadlinePlugin.LogInfo( "Output file: " + outputPath )
			
			
			### requeue missing frame
			def communicate_with_deadline(*args):
				communicateWithDeadline = subprocess.Popen([deadlineEXE, args[0], args[1]], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
				getDatas = communicateWithDeadline.communicate()
				getData = getDatas[0]
				return getData
			
			print "TARA"
				
			"""getJobID = communicate_with_deadline('GetJobIdsFilter', 'JobName=%s'%job)
			getJob = communicate_with_deadline('GetJob', getJobID)
			splitJob = getJob.split("\r\n")
			firstFrameData = [firstFrameData for firstFrameData in splitJob if firstFrameData.startswith("FirstFrame")==True]
			lastFrameData = [lastFrameData for lastFrameData in splitJob if lastFrameData.startswith("LastFrame")==True]
			firstFrame = firstFrameData[0].split("=")[1]
			lastFrame = lastFrameData[0].split("=")[1]
			frameRange = range(int(firstFrame), (int((lastFrame)))+1)
			frameMinMax = firstFrame + ("-") + lastFrame
			missingFrames = list(set(frameRange) - set(outputFrameSorted))
			if missingFrames:
				subprocess.Popen([deadlineEXE, 'SetJobFrameRange', getJobID, frameMinMax, '1'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
				for missingFrame in sorted(missingFrames):
					jobTask = communicate_with_deadline('GetJobTasks', getJobID)
					splitJobTask = jobTask.split("\r\n")
					names = [nameDatas for nameDatas in splitJobTask if nameDatas.startswith("Name=")==True]
					for name in names:
						taskIDS = name.split("=")[1]
						if taskIDS.endswith(str(missingFrame) + '-' + str(missingFrame)):
							taskID = taskIDS.split("_")[0]
							subprocess.Popen([deadlineEXE, 'RequeueJobTask', getJobID, taskID], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)"""

