def findTRS(feederID,dataPath):
  feederField = "FEEDERID"
  TRS = #Town Range Section feature class
  for feeder in feederID:
    #create SQL clause for feature layer selection
    SQL = """{0} = '{1}'""".format(arcpy.AddFieldDelimiters(dataPath,feederField),feeder)

    #create layer from input datapath to select from
    dataPathLyr = arcpy.MakeFeatureLayer_management(dataPath, 'output_lyr', SQL)

    #select by location
    ####I think this selection is wrong. Read the documentation on this tool before proceeding####
    #http://desktop.arcgis.com/en/arcmap/10.3/tools/data-management-toolbox/select-layer-by-location.htm
    mySelection = arcpy.SelectLayerByLocation_management(dataPathLyr,"COMPLETELY_WITHIN",TRS,"","NEW_SELECTION")

    #search cursor used to append list of geometric network junction object IDs that are within feeder boundary to list
    cursor = arcpy.da.SearchCursor(mySelection, ["OBJECTID"])
