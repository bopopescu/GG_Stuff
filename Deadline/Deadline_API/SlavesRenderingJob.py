from ConnectionProperty import ConnectionProperty

class SubordinatesRenderingJob:
    """
        Class used by DeadlineCon to send Subordinates Rendering Job requests. 
        Stores the address of the web service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetSubordinatesRenderingJob(self, id, getIpAddress=False):
        """    Gets the list of subordinates that are currently rendering a job.
            Input:  id: The job ID.
                getIpAddress: If True, the IP address of the subordinates will be returned instead
            Returns: The list of subordinate names, or the list of subordinate IP addresses if getIpAddress is True
        """
        
        return self.connectionProperties.__get__("/api/subordinatesrenderingjob?JobID="+id+"&GetIpAddress="+str(getIpAddress))