'''
TRS attribute value needs to be updated for features with a null TRS value...

Needs to be done on unfrozen feeder IDs and also a tool that will update whole database...

  1) What Feature classes need to be updated for TRS?
        -Fuse
        -Dynamic protective device
        -Switch
        -Capacitors
        -Isolators
        -VoltageRegulators
'''

def findTRS(feederID,dataPath): #instead of this user should input list of feederIDs and DB connection to their version def findTRS(feederID,workspacePath)
                                # set workspace to user input DB connection arcpy.env.workspace = workspacePath
                                # then set code to loop through all required FC's to be updated
  ####PDM_PROD.mxd data paths ####
  #fuse = r'Devices\Protective Devices & Switches\Fuse'
  #DPD = r'Devices\Protective Devices & Switches\Dynamic Protective Device'
  #switch = r'Devices\Protective Devices & Switches\Switch'
  #capacitors = r'Devices\Primary Devices\Capacitors'
  #isolator = r'Devices\Primary Devices\Isolator'
  #R&B = r'Devices\Primary Devices\Regulators & Boosters'
  ############################
  
  #variables used for SQL statement
  feederField = arcpy.AddFieldDelimiters(dataPath,"FEEDERID")
  trsField = arcpy.AddFieldDelimiters(dataPath,"TRS")
  
  #Town Range Section feature class
  TRS = r'E:\Data\EROlson\test.gdb\TownRangeSection'
  
  for feeder in feederID:
    #create SQL clause for feature layer selection
    SQL = """{0} = '{1}' AND {2} IS NULL""".format(feederField,feeder,trsField)

    #create layer from input datapath to select from
    dataPathLyr = arcpy.MakeFeatureLayer_management(dataPath, 'output_lyr', SQL)

    #select by location - select TRS polygons that contain objects from dataPathLyr 
    mySelection = arcpy.SelectLayerByLocation_management(TRS,"CONTAINS",dataPathLyr,"","NEW_SELECTION")
    
    #list of TRS polygon object IDs that contain features in the dataPathLyr
    trsList = []
    
    #search cursor used to append list of TRS polygon object IDs that contain features in the dataPathLyr to a list
    cursor = arcpy.da.SearchCursor(mySelection, ["OBJECTID"])
    
    for row in cursor:
      trsList.append(row) #or is it row[0]???
    del cursor
    
    ####Now another Select By Location of dataPath FC to individual TRS polygons####
    #variable for SQL statement
    objIDField = arcpy.AddFieldDelimiters(TRS,"OBJECTID")
    
    # i is an objectID for a specific polygon in the TRS FC
    for i in trsList:
      SQL = """{0} = {1}""".format(objIDField, i)
      
      #create layer w/specific object ID from TRS FC to clip from
      trsLyr = arcpy.MakeFeatureLayer_management(TRS, 'trs_lyr', SQL)
      
      #find section name value for trsLyr using a Search Cursor
      cursor = arcpy.da.SearchCursor(trsLyr, ["SECTIONNAME"])
      for row in cursor:
        sectionName = row[0]
      del cursor
      
      #select by location
      mySelection = arcpy.SelectLayerByLocation_management(dataPathLyr,"COMPLETELY_WITHIN",trsLyr,"","NEW_SELECTION")
      
      #dictionary to store TRS ["SECTIONNAME"] value as key and all selected object IDs from dataPathLyr as values
      myDict = {} #myDict{key:[value1,value2,value3]}
      
      #loop through mySelection and assign all selected object IDs as a value to TRS ["SECTIONNAME"] key
      cursor = arcpy.da.SearchCursor(mySelection, ["OBJECTID"])
      for row in cursor:
        myDict
      del cursor
      
      
    
    
