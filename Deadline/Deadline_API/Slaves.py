from ConnectionProperty import ConnectionProperty
import json

class Subordinates:
    """
        Class used by DeadlineCon to send Subordinate requests, as well as a few Pool and Group requests. 
        Stores the address of the web service for use in sending requests.
    """
    def __init__(self, connectionProperties):
        self.connectionProperties = connectionProperties
        
    def GetSubordinateNames(self):
        """ Gets all the Subordinate names.
            Returns: The list of subordinate names
        """
        return self.connectionProperties.__get__("/api/subordinates?NamesOnly=true")

    def GetSubordinatesInfoSettings(self, names = None):
        """Gets multiple subordinatesubordinates
            Inputs: names: the names of the subordinates to get. If None get all subordinates
            Returns: The list of subordinates' infos and settings
        """
        script = "/api/subordinates?Data=infosettings"
        if names != None:
            script = script +"&Name="+ ArrayToCommaSeperatedString(names).replace(' ','+')
        return self.connectionProperties.__get__(script)

    def GetSubordinateInfoSettings(self, name):
        """ Gets a subordinate.
            Input: name: The subordinate name.
            Returns: The subordinate info and settings
        """
        
        result = self.connectionProperties.__get__("/api/subordinates?Data=infosettings&Name="+name.replace(' ','+'))
        
        if type(result) == list and len(result) > 0:
            result = result[0]
            
        return result

    def GetSubordinateInfo(self, name):
        """ Gets a subordinate info object.
            Input: name: The subordinate name.
            Returns: The subordinate info
        """
        result = self.connectionProperties.__get__("/api/subordinates?Name="+name.replace(' ','+')+"&Data=info")
        
        if type(result) == list and len(result) > 0:
            result = result[0]
            
        return result
        
    def GetSubordinateInfos(self, names = None):
        """ Gets multiple subordinate info objects.
            Input: name: The subordinate names. If None return all info for all subordinates
            Returns: list of the subordinate infos
            """
        script = "/api/subordinates?Data=info"
        if names != None:
            script = script + "&Name="+ArrayToCommaSeperatedString(names).replace(' ','+')
        return self.connectionProperties.__get__(script)

    def SaveSubordinateInfo(self, info):
        """ Saves subordinate info to the database.
            Input:  info: JSon object of the subordinate info
            Returns: Success message
        """
        info = json.dumps(info)
        body = '{"Command":"saveinfo", "SubordinateInfo":'+info+'}'
        return self.connectionProperties.__put__("/api/subordinates", body)

    def GetSubordinateSettings(self, name):
        """ Gets a subordinate settings object.
            Input: name: The subordinate name.
            Returns: The subordinate settings
        """
        
        return self.connectionProperties.__get__("/api/subordinates?Name="+name.replace(' ','+')+"&Data=settings")
    
    def GetSubordinatesSettings(self, names = None):
        """ Gets multiple subordinate settings objects.
            Input: name: The subordinate names. If None return all info for all subordinates
            Returns: list of the subordinate settings's info
        """
        script = "/api/subordinates?Data=settings"
        if names != None:
            script = script + "&Name="+ArrayToCommaSeperatedString(names).replace(' ','+')
            
        return self.connectionProperties.__get__(script)

    def SaveSubordinateSettings(self, info):
        """ Saves subordinate Settings to the database.
            Input:  info: JSon object of the subordinate settings
            Returns: Success message
        """
        info = json.dumps(info)
        body = '{"Command":"savesettings", "SubordinateSettings":'+info+'}'
        
        return self.connectionProperties.__put__("/api/subordinates", body)

    def DeleteSubordinate(self, name):
        """ Removes a subordinate from the repository.
            Input:  name: The name of the subordinate to be removed
            Returns: Success message
        """
        return self.connectionProperties.__delete__("/api/subordinates?Name="+name)

    def AddGroupToSubordinate(self, subordinate, group):
        """ Adds a group to a subordinate.
            Input:  subordinate: The name of the subordinate or subordinates( may be a list )
                    group: The name of the group or groups( may be a list )
            Return: Success message
        """
        body = '{"Subordinate":'+json.dumps(subordinate)+', "Group":'+json.dumps(group)+'}'
        
        return self.connectionProperties.__put__("/api/groups", body)

    def AddPoolToSubordinate(self, subordinate, pool):
        """ Adds a pool to a subordinate.
            Input:  subordinate: The name of the subordinate or subordinates( may be a list )
                    pool: The name of the pool or pools( may be a list )
            Return: Success message
        """
        body = '{"Subordinate":'+json.dumps(subordinate)+', "Pool":'+json.dumps(pool)+'}'
        
        return self.connectionProperties.__put__("/api/pools", body)

    def RemovePoolFromSubordinate(self, subordinate,pool):
        """ Adds a pool from a subordinate.
            Input:  subordinate: The name of the subordinate or subordinates( may be a list )
                    pool: The name of the pool or pools( may be a list )
            Return: Success message
        """
        return self.connectionProperties.__delete__("/api/pools?Subordinates="+ArrayToCommaSeperatedString(subordinate)+"&Pool="+ArrayToCommaSeperatedString(pool))

    def RemoveGroupFromSubordinate(self, subordinate,group):
        """ Adds a group from a subordinate.
            Input:  subordinate: The name of the subordinate or subordinates( may be a list )
                    group: The name of the group or group( may be a list )
            Return: Success message
        """
        return self.connectionProperties.__delete__("/api/groups?Subordinates="+ArrayToCommaSeperatedString(subordinate)+"&Group="+ArrayToCommaSeperatedString(group))

    def GetSubordinateNamesInPool(self, pool):
        """ Gets the names of all subordinates in a specific pool.
            Input:  pool: The name of the pool to search in.( May be a list)
            Returns: a list of all subordinates that are in the pool
        """
        return self.connectionProperties.__get__("/api/pools?Pool="+ArrayToCommaSeperatedString(pool).replace(' ','+'))

    def GetSubordinateNamesInGroup(self, group):
        """ Gets the names of all subordinates in a specific group.
            Input:  group: The name of the group to search in. ( May be a list )
            Returns: a list of all subordinates that are in the groups
        """
        return self.connectionProperties.__get__("/api/groups?Group="+ArrayToCommaSeperatedString(group).replace(' ','+'))

    def SetPoolsForSubordinate(self, subordinate,pool = []):
        """ Sets all of the pools for one or more subordinates overriding their old lists
            Input:  subordinate: Subordinates to be modified (may be a list)
                    pool: list of pools to be used
            Returns: Success message
        """
        body = '{"OverWrite":true, "Subordinate":'+json.dumps(subordinate)+',"Pool":'+json.dumps(pool)+'}'
        
        return self.connectionProperties.__put__("/api/pools", body)

    def SetGroupsForSubordinate(self, subordinate,group = []):
        """ Sets all of the groups for one or more subordinates overriding their old lists
            Input:  subordinate: Subordinates to be modified (may be a list)
                    pool: list of groups to be used
            Returns: Success message
        """
        body = '{"OverWrite":true, "Subordinate":'+json.dumps(subordinate)+',"Group":'+json.dumps(group)+'}'
        
        return self.connectionProperties.__put__("/api/groups", body)

    def GetSubordinateReports(self, name):
        """ Gets the reports for a subordinate.
            Input:  name: The name of the subordinate
            Returns all reports for the subordinate
        """
        return self.connectionProperties.__get__("/api/subordinates?Name="+name.replace(' ','+')+"&Data=reports")
        
    def GetSubordinateReportsContents(self, name):
        """ Gets the reports contents for a subordinate.
            Input:  name: The name of the subordinate
            Returns all reports contents for the subordinate
        """
        
        return self.connectionProperties.__get__("/api/subordinates?Name="+name.replace(' ','+')+"&Data=reportcontents")

    def GetSubordinateHistoryEntries(self, name):
        """ Gets the historyEntries for a subordinate.
            Input:  name: The name of the subordinate
            Returns: all history entries for the subordinate
        """
        return self.connectionProperties.__get__("/api/subordinates?Name="+name.replace(' ','+')+"&Data=history")

#Helper function to seperate arrays into strings
def ArrayToCommaSeperatedString(array):
    if isinstance(array, basestring):
        return array
    else:
        i=0
        script=""
        for i in range(0,len(array)):
            if(i!=0):
                script+=","
            script += str(array[i]);
        return script
