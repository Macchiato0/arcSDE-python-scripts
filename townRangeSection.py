'''
TRS attribute value needs to be updated for features with a null TRS value...

Needs to be done on unfrozen feeder IDs and also a tool that will update whole database...

Questions:
  1) What Feature classes need to be updated for TRS?
  
'''

def findTRS(feederID,dataPath):
  
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

    #select by location
    mySelection = arcpy.SelectLayerByLocation_management(TRS,"CONTAINS",dataPathLyr,"","NEW_SELECTION")
    
    #list of TRS polygon object IDs that contain features in the dataPathLyr
    trsList = []
    
    #search cursor used to append list of TRS polygon object IDs that contain features in the dataPathLyr to a list
    cursor = arcpy.da.SearchCursor(mySelection, ["OBJECTID"])
    
    for row in cursor:
      trsList.append(row)
    del cursor
