feederID = '150701'
miscNetFeat = #update with data path
TRS = #update with data path

def findTRS():
#create layer to select from
myLyr = arcpy.MakeFeatureLayer_management(miscNetFeat, 'miscNetFeat_lyr')

#select by location
mySelection = arcpy.SelectLayerByLocation_management(myLyr,"COMPLETELY_WITHIN",TRS,"","NEW_SELECTION")

#search cursor used to append list of geometric network junction object IDs that are within feeder boundary to list
cursor = arcpy.da.SearchCursor(mySelection, ["OBJECTID"])
