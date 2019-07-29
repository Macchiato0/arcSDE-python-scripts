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

####This has been run in the test GDB and appears to be working quite nicely. Integration into a replica QA GDB needs to be closely 
asessed before implementation.
####
'''

import arcpy

#Arcmap settings
arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

#assign workspace
arcpy.env.workspace = #do I need to hvae this???

###input data paths###

#OH Connector Line
OHline = r'Customers & Transformers\Transformer Connector Lines\OH Connector Line'

#UG Connector Line
UGline = r'Customers & Transformers\Transformer Connector Lines\UG Connector Line'

#Primary Overhead dataset
priOH = r'Primary Lines\Primary Overhead Conductor'

#Primary Underground dataset
priUG = r'Primary Lines\Primary Underground Conductor'

#Secondary Overhead dataset
secOH = r'Customers & Transformers\Secondary Overhead Conductor'

#Secondary Underground dataset
secUG = r'Customers & Transformers\Secondary Underground Conductor'

#Geometric Network junctions dataset
geoNetJunct = r'Misc Network Features\ELECDIST.ElectricGeomNetwork_Junctions'

#Boundary Feeder Go dataset
circuitBoundary = r'Org Bounds\Circuit Boundaries'

####SQL expression for feeder boundary####

#FeederID being QA'd
feeder = '012701'

feederField = "FEEDERID"

SQL = """{0} = '{1}'""".format(arcpy.AddFieldDelimiters(circuitBoundary,feederField),feeder)

###Find gemetric network junctions that overlap with proper circuit boundary layer###

#list of geometric network junctions that are intersected by circuit boundary layer
circuitGeoNetJunctList = []

#create layer to select from
myBoundaryLyr = arcpy.MakeFeatureLayer_management(geoNetJunct, 'boundaryGeoNetJunct_lyr')

#create circuit boundary layer w/SQL to select from
myCircuitBoundaryLyr = arcpy.MakeFeatureLayer_management(circuitBoundary, 'boundaryCircuit_lyr',SQL)

#select by location
myBoundarySelection = arcpy.SelectLayerByLocation_management(myBoundaryLyr,"COMPLETELY_WITHIN",myCircuitBoundaryLyr,"","NEW_SELECTION")

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
selectByList = [OHline, UGline, priOH, priUG, secOH, secUG]

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

### EOlson 07/2019 ###
### rosemary.erin.o@gmail.com ###
