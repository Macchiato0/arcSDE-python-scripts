'''
Python script to automate a portion of the QA process when SDEs are recieved back from DRG.

Initial process thoughts:
1)  Only select features within boundary of feederID

2)  Conduct "Select By Location" geoprocessing to find any "floating"
geometric network features & Taps and delete "floating" ones.
***try using a set for OBJIDs instead of list?***

    ***geometric network junctions are only on linear features!!!***

3)  Then gReady will be run to find any remaining errors that need to be looked
at maually by an analyst.
'''

import arcpy

#Arcmap settings
arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

#assign workspace
arcpy.env.workspace = 

###input data paths###

#Primary Overhead dataset
priOH = 

#Primary Underground dataset
priUG = 

#Secondary Overhead dataset
secOH = 

#Secondary Underground dataset
secUG = 

#Geometric Network junctions dataset
geoNetJunct = 

#Boundary Feeder Go dataset
circuitBoundary = 

###Find gemetric network junctions that overlap with proper circuit boundary layer###

#list of geometric network junctions that are intersected by circuit boundary layer
circuitGeoNetJunctList = []

#list of feature classes used in select by location analysis to find stranded geometric network junctions
selectByList = [circuitBoundary]

#Start looping through FCs

for i in selectByList:

    #create layer to select from
    myBoundaryLyr = arcpy.MakeFeatureLayer_management(geoNetJunct, 'boundaryGeoNetJunct_lyr')
    
    #select by location
    myBoundarySelection = arcpy.SelectLayerByLocation_management(myBoundaryLyr,"COMPLETELY_WITHIN",i,"","NEW_SELECTION")

    #search cursor used to append list of geometric network junction object IDs that are within feeder boundary to list
    cursor = arcpy.da.SearchCursor(myBoundarySelection, ["OBJECTID"])
    
    for row in cursor:
        if row[0] not in circuitGeoNetJunctList:
            circuitGeoNetJunctList.append(row[0])
    
    del cursor
###Find geometric network junctions attached to lines --> delete all others###

#list of geometric network junctions that are intersected by a layer in selectByList
geoNetJunctIntersectedList = []

#list of feature classes used in select by location analysis to find stranded geometric network junctions
selectByList = [priOH, priUG, secOH, secUG]

#Start looping through FCs

for i in selectByList:

    #create layer to select from
    myLyr = arcpy.MakeFeatureLayer_management(geoNetJunct, 'geoNetJunct_lyr')
    
    #select by location
    mySelection = arcpy.SelectLayerByLocation_management(myLyr,"INTERSECT",i,"","NEW_SELECTION")

    #search cursor used to append list of tap dot object IDs that are intersected by line feature to list
    cursor = arcpy.da.SearchCursor(mySelection, ["OBJECTID"])
    
    for row in cursor:
        if row[0] not in geoNetJunctIntersectedList:
            geoNetJunctIntersectedList.append(row[0])
    
    del cursor

#now we need to delete any rows whose OBJ IDs are NOT in the geoNetJunctIntersectedList BUT ARE IN the circuitGeoNetJunctList
    
with arcpy.da.UpdateCursor(geoNetJunct, ["OBJECTID"]) as cursor:
    #for each row evaluate if the Object ID is in the geoNetJunctIntersectedList
    #if not in list --> then delete!
    for row in cursor:
        if row[0] not in geoNetJunctIntersectedList and row[0] in circuitGeoNetJunctList:
            print row[0]
            cursor.deleteRow()

### EOlson 05/2019 ###
### rosemary.erin.o@gmail.com ###
