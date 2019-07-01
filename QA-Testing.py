'''
Python script to automate the QA process when SDEs are recieved back from DRG.

Initial process thoughts:
1)  Only select features within boundary of feederID
1)  Do initial scrape of SDE to remove all features marked remove/delete from the
following feature classes:
            -Primary OH & UG
            -Secondary OH & UG
            -OH Connector line
            -UG Connector line
            -Misc. Network features

2)  Conduct "Select By Location" geoprocessing to find any "floating"
geometric network features & Taps and delete "floating" ones.

    ***geometric network junctions are only on linear features!!!***

3)  Then the gReady will be run to find any remaining errors that need to be looked
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

#Misc. Network Features dataset
miscNetFeat = 

#Geometric Network junctions dataset
geoNetJunct = 


#Complete list of data paths
delDataList = [priOH, priUG, secOH, secUG, miscNetFeat]

#for loop to iterate through delDataList and delete items marked remove/delete
for i in delDataList:
    
   #create update cursor
   cursor = arcpy.da.UpdateCursor(i,"*","CONSTRUCTIONSTATUS=55")

   for row in cursor:
      cursor.deleteRow()

#delete cursor when finished
del cursor

###Find stranded Tap points###


#list of feature classes used in select by location analysis to find stranded tap points
selectByList = [priOH, priUG, secOH, secUG]

#List of tap points that are intersected by a layer in selectByList
tapsIntersectedList = []

#Start looping through FCs

for i in selectByList:

    #create layer to select from
    myLyr = arcpy.MakeFeatureLayer_management(miscNetFeat, 'miscNetFeat_lyr')
    
    #select by location
    mySelection = arcpy.SelectLayerByLocation_management(myLyr,"INTERSECT",i,"","NEW_SELECTION")

    #search cursor used to append list of tap dot object IDs that are intersected by line feature to list
    cursor = arcpy.da.SearchCursor(mySelection, ["OBJECTID"])
    
    for row in cursor:
        if row[0] not in tapsIntersectedList:
            tapsIntersectedList.append(row[0])
    
    del cursor

#now we need to delete any rows whose OBJ IDs are NOT in the tapsIntersectedList
    
with arcpy.da.UpdateCursor(miscNetFeat, ["OBJECTID"]) as cursor:
    #for each row evaluate if the Object ID is in the tapsIntersectedList
    #if not in list --> then delete!
    for row in cursor:
        if row[0] not in tapsIntersectedList:
            print row[0]
            cursor.deleteRow()

###Find geometric network junctions attached to lines --> delete all others###

#list of geometric network junctions that are intersected by a layer in selectByList
geoNetJunctIntersectedList = []

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

#now we need to delete any rows whose OBJ IDs are NOT in the geoNetJunctIntersectedList
    
with arcpy.da.UpdateCursor(geoNetJunct, ["OBJECTID"]) as cursor:
    #for each row evaluate if the Object ID is in the geoNetJunctIntersectedList
    #if not in list --> then delete!
    for row in cursor:
        if row[0] not in geoNetJunctIntersectedList:
            print row[0]
            cursor.deleteRow()

### EOlson 05/2019 ###
### rosemary.erin.o@gmail.com ###
