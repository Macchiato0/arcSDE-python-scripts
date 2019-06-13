'''
This script is being developed for the purpose of automating the QA Email
process as it is described in the QA Email Process Job aid developed by
Tierney O'Keefe and Shelly Jeltema

            ***All of these processes must be done per Feeder ID***

            1)  Update attribute fields with missing information
                    -Switch FC (SQL queries previously developed)
                        -Switch Symbol Type
                        - CYME Equip. ID

            2)  Return total number of added and deleted features for:
                    -Service Points
                    -Transformers

            3)  Return total number of added fuses

            4)  Return total number of Service Points with "ACTIVE" meter status
                that were removed
                    -SQL code previously developed for this process
'''

'''
SQL Code for step 1:

FEEDERID ='XXXXXX' AND SUBTYPECD = 4 AND SWITCHSYMBOLTYPE is NULL

'''

###Testing step 1###

myData = 
fieldNames = ["SWITCHSYMBOLTYPE", "EQUIPMENTID"]
feederID = [150701,150702]
for ID in feederID:
    cursor = arcpy.da.UpdateCursor(myData, fieldNames, "FEEDERID = '{0}' AND SUBTYPECD = 4 AND SWITCHSYMBOLTYPE IS NULL".format(ID))
    for row in cursor:
        row[0] = "LBEC"
        row[1] = "LBREAK_SW"
        cursor.updateRow(row)
    del cursor

    cursor = arcpy.da.UpdateCursor(myData, fieldNames, "FEEDERID = '{0}' AND SUBTYPECD = 3 AND SWITCHSYMBOLTYPE IS NULL".format(ID))
    for row in cursor:
        row[0] = "LC"
        row[1] = "DIS_SW-600A"
        cursor.updateRow(row)
    del cursor

###Testing step 2###
'''
This portion of the process has been covered/completed in the QA Test script.
'''

###Testing step 3###
'''
We need to report the total number of added/removed Service Points and Secondary
Transformers per Feeder ID.
'''
servicePoints = 
cursor = arcpy.da.SearchCursor(servicePoints,"*","FEEDERID = '150701' AND CONSTRUCTIONSTATUS=50")
count = 0
for row in cursor:
    count += 1
print ('Total added service points: ' + str(count))


###Testing step 4###
'''
Calculate number of removed service points with active meter status.
1)create join and preform sql query on matching joined data.
SQL Code:
( DRG_xxx.xxx.ServicePoint.FEEDERID = '154301' AND DRG_xxx.xxx.ServicePoint.CONSTRUCTIONSTATUS = 55 ) AND ( DRG_xxx.xxx.ServiceAddress.METERSTATUS = 'ACTIVE' )
***Total number of rows returned provides number we need to report***
'''

###Testing step 5###
'''
Need total number of added fuses.
'''
fuse = 
cursor = arcpy.da.SearchCursor(servicePoints,"*","FEEDERID = '150701' AND CONSTRUCTIONSTATUS=50")
count = 0
for row in cursor:
    count += 1
print ('Total added Fuses: ' + str(count))

### EOlson 05/2019 ###
### rosemary.erin.o@gmail.com ###
