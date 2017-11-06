import os, tempfile, subprocess, socket
from collections import OrderedDict

class Deadline(object):
	MAYA_JOB_INFO_ATTRS=				(("ArchiveOnComplete"										, "False"),
													 ("BatchName"												, ""),
													 ("Blacklist"													, ""),
													 ("ChunkSize"													, ""),
													 ("ClearNotificationTargets"								, "False"),
													 ("Comment"													, ""),
													 ("ConcurrentTasks"											, ""),
													 ("DeleteOnComplete"										, "False"),
													 ("Department"												, ""),
													 ("EmailNotification"										, "False"),
													 ("EnableAutoTimeout"										, "False"),
													 ("EnableTimeoutsForScriptTasks"						, "False"),
													 ("FailureDetectionTaskErrors"							, 0),
													 ("FailureDetectionJobErrors"								, 0),
													 ("ForceReloadPlugin"										, "False"),
													 ("Frames"														, ""),
													 ("Group"														, ""),
													 ("GrowlNotification"										, "False"),
													 ("IgnoreBadJobDetection"								, "False"),
													 ("InitialStatus"												, ""),
													 ("Interruptible"												, "False"),
													 ("IsFrameDependent"										, "False"),
													 ("JobDependencies"										, ""),
													 ("JobDependencyPercentage"							, -1),
													 ("LimitGroups"												, ""),
													 ("LimitConcurrentTasksToNumberOfCpus"			, "True"),
													 ("MachineLimit"												, 0),
													 ("MachineLimitProgress"									, -1.0),
													 ("Name"														, ""),
													 ("NetsendNotification"									, "False"),
													 ("NotificationEmails"										, ""),
													 ("NotificationNote"											, ""),
													 ("MachineName"												, socket.gethostname()),
													 ("MinRenderTimeSeconds"								, 0),
													 ("MinRenderTimeMinutes"								, 0),
													 ("NotificationTargets"										, ""),
													 ("OnJobComplete"											, "Nothing"),
													 ("OnTaskTimeout"											, "Error"),
													 ("OutputFilename0" 										, ""),
													 ("OutputDirectory0"										, ""),
													 ("OutputFilename1"										, ""),
													 ("OutputDirectory1"										, ""),
													 ("OutputFilename2"										, ""),
													 ("OutputDirectory2"										, ""),
													 ("OutputFilename3"										, ""),
													 ("OutputDirectory3"										, ""),
													 ("OutputFilename4"										, ""),
													 ("OutputDirectory4"										, ""),
													 ("OutputFilename5" 										, ""),
													 ("OutputDirectory5" 										, ""),
													 ("OutputFilename6" 										, ""),
													 ("OutputDirectory6" 										, ""),
													 ("OverrideJobFailureDetection"							, "False"),
													 ("OverrideNotificationMethod"							, "False"),
													 ("OverrideTaskFailureDetection"						, "False"),
													 ("Plugin" 														, "MayaCmd"),
													 ("Pool" 															, ""),
													 ("PostJobScript"												, ""),
													 ("PostTaskScript" 											, ""),
													 ("PreJobScript"												, ""),
													 ("PreTaskScript"												, ""),
													 ("Priority" 														, ""),
													 ("ResumeOnCompleteDependencies" 				, "True"),
													 ("ResumeOnDeletedDependencies"					, "False"),
													 ("ResumeOnFailedDependencies"						, "False"),
													 ("SecondaryPool"												, "none"),
													 ("SendJobErrorWarning"									, "True"),
													 ("Sequential" 												, "False"),
													 ("SynchronizeAllAuxiliaryFiles"							, "False"),
													 ("SuppressEvents"											, "False"),
													 ("TaskTimeoutSeconds"									, 0),
													 ("TaskTimeoutMinutes"									, ""),
													 ("TileJob"														, "False"),
													 ("TileJobFrame"												, 0),
													 ("TileJobTilesInX"											, 0),
													 ("TileJobTilesInY"											, 0),
													 ("UserName"													, ""),
													 ("Whitelist" 													, ""))

	MAYA_PLUGIN_INFO_ATTRS=		(("Animation"													, 1),
													 ("Build"															, "64bit"),
													 ("IgnoreError211"											, 1),
													 ("ImageHeight"												, ""),
													 ("ImageWidth"												, ""),
													 ("LocalRendering"											, 1),
													 ("MaxProcessors"											, 24),
													 ("OutputFilePath"											, ""),
													 ("OutputFilePrefix"											, ""),
													 ("ProjectPath"												, ""),
													 ("RenderHalfFrames"										, 0),
													 ("RenderLayer"												, ""),
													 ("Renderer"													, "vray"),
													 ("SceneFile"													, ""),
													 ("StrictErrorChecking"										, 0),
													 ("UsingRenderLayers"										, 1),
													 ("Version"														, ""))


	MAYA_JOB_INFO_ATTRS    = OrderedDict(MAYA_JOB_INFO_ATTRS)
	MAYA_PLUGIN_INFO_ATTRS = OrderedDict(MAYA_PLUGIN_INFO_ATTRS)

	def __init__(self):
		for key, val in self.MAYA_JOB_INFO_ATTRS.iteritems():
			setattr(self, key, val)

		for key, val in self.MAYA_PLUGIN_INFO_ATTRS.iteritems():
			setattr(self, key, val)

	def _create_job_file(self, path = "", orderedDict = None):
		if orderedDict:
			job_file = open(path, mode = "w")
			for key, val in orderedDict.iteritems():
				job_file.write( "%s=%s\n" %( key, val ) )

			job_file.close()

	def _getAttr(self, orderedDict = None):
		if orderedDict:
			myDict = ()
			for key in orderedDict:
				myDict += ( ( key, eval("self.%s" % key) ), )

			return OrderedDict(myDict)

	def build_maya_job_info( self, name = "maya_job_info.job", path = tempfile.gettempdir() ):
		attrs       = self._getAttr(self.MAYA_JOB_INFO_ATTRS)
		job_path    = os.path.join(path, name).replace("\\", "/")
		self._create_job_file(job_path, attrs)

		return job_path

	def build_maya_plugin_info( self, name = "maya_plugin_info.job", path = tempfile.gettempdir() ):
		attrs       = self._getAttr(self.MAYA_PLUGIN_INFO_ATTRS)
		job_path    = os.path.join(path, name).replace("\\", "/")
		self._create_job_file(job_path, attrs)

		return job_path

	def build_maya_job_xml(self):
		pass

	def build_maya_plugin_xml(self):
		pass

	def make_dirs(self, path = ""):
		if path:
			if not os.path.exists(path):
				os.makedirs(path)

	def submit_to_deadline(self, *args):
		if self.OutputDirectory0:
			if not os.path.exists(self.OutputDirectory0):
				self.make_dirs(self.OutputDirectory0)
				
		startupinfo = subprocess.STARTUPINFO()
		startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW		
		subprocess.call( 'C:/Program Files/Thinkbox/Deadline7/bin/deadlinecommand.exe "%s" "%s"' %(args[0], args[1]) , startupinfo=startupinfo)