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
  
  #Town Range Section Feature Layer
  myTrsLyr = arcpy.MakeFeatureLayer_management(TRS, 'trsOutput_lyr')
  
  for feeder in feederID:
    #create SQL clause for feature layer selection
    SQL = """{0} = '{1}' AND {2} IS NULL""".format(feederField,feeder,trsField)

    #create layer from input datapath to select from
    dataPathLyr = arcpy.MakeFeatureLayer_management(dataPath, 'output_lyr', SQL)

    #select by location - select TRS polygons that contain objects from dataPathLyr 
    mySelection = arcpy.SelectLayerByLocation_management(myTrsLyr,"CONTAINS",dataPathLyr,"","NEW_SELECTION")
    
    #list of TRS polygon object IDs that contain features in the dataPathLyr
    trsList = []
    
    #search cursor used to append list of TRS polygon object IDs that contain features in the dataPathLyr to a list
    cursor = arcpy.da.SearchCursor(mySelection, ["OBJECTID"])
    
    for row in cursor:
      trsList.append(row[0]) 
    del cursor
    
    #data check
    print ("TRS OBJID List: {}".format(trsList)) 
    
    ####Now another Select By Location of dataPath FC to individual TRS polygons####
    #variable for SQL statement
    objIDField = arcpy.AddFieldDelimiters(TRS,"OBJECTID")
    
    # i is an objectID for a specific polygon in the TRS FC
    for i in trsList:
      
      #data check
      print ("TRS Polygon OBJID: {0}".format(i))
      
      SQL = """{0} = {1}""".format(objIDField, i)
      
      #create layer w/specific object ID from TRS FC to conduct select by location from
      trsLyr = arcpy.MakeFeatureLayer_management(TRS, 'trs_lyr', SQL)
      
      #find section name value for trsLyr using a Search Cursor
      cursor = arcpy.da.SearchCursor(trsLyr, ["SECTIONNAME"])
      for row in cursor:
        sectionName = str(row[0])
      del cursor
      
      #data check
      print ("Section Name: {0}".format(sectionName))
      print type(sectionName)
      
      #select by location
      mySelection2 = arcpy.SelectLayerByLocation_management(dataPathLyr,"COMPLETELY_WITHIN",trsLyr,"","NEW_SELECTION")
      
      '''
      I am having some trouble right here... 
      The code below updates a layer file and not a FC so it does nothing for me...
      Should I loop through the selected objects, append the objIDs to a list,
      then loop through the list you just created and create a cursor object 
      on the actual FC that only updates the object IDs in the list.....
      '''
      
      #loop through mySelection and update with sectionName variable value
      cursor = arcpy.da.UpdateCursor(mySelection2, ["TRS"])
      for row in cursor:
        #data check
        print ("Update Cursor row: ".format(row[0]))
        row[0]= sectionName
      del cursor
   
