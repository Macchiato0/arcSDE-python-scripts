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
####Required Data Paths####
switch = r'E:\Data\EROlson\test.gdb\Switch'
servicePoints = r'E:\Data\EROlson\test.gdb\ServicePoint'
transformer = r'E:\Data\EROlson\test.gdb\Transformer'
fuse = r'E:\Data\EROlson\test.gdb\Fuse'

####Feeder ID(s)####
feederID = [150701,150702]
###Testing step 1###


fieldNames = ["SWITCHSYMBOLTYPE", "EQUIPMENTID"]

for ID in feederID:
    cursor = arcpy.da.UpdateCursor(switch, fieldNames, "FEEDERID = '{0}' AND SUBTYPECD = 4 AND SWITCHSYMBOLTYPE IS NULL".format(ID))
    for row in cursor:
        row[0] = "LBEC"
        row[1] = "LBREAK_SW"
        cursor.updateRow(row)
    del cursor

    cursor = arcpy.da.UpdateCursor(switch, fieldNames, "FEEDERID = '{0}' AND SUBTYPECD = 3 AND SWITCHSYMBOLTYPE IS NULL".format(ID))
    for row in cursor:
        row[0] = "LC"
        row[1] = "DIS_SW-600A"
        cursor.updateRow(row)
    del cursor

###Testing step 2###
'''
We need to report the total number of added/removed Service Points and Secondary
Transformers per Feeder ID.
'''
servicePoints = r'E:\Data\EROlson\test.gdb\ServicePoint'
for ID in feederID:
    cursor = arcpy.da.SearchCursor(servicePoints,"*","FEEDERID = '{0}' AND CONSTRUCTIONSTATUS=50".format(ID))
    count = 0
    for row in cursor:
        count += 1

print ('Total added service points: ' + str(count))

transformer = r'E:\Data\EROlson\test.gdb\Transformer'
for ID in feederID:
    cursor = arcpy.da.SearchCursor(transformer,"*","FEEDERID = '{0}' AND CONSTRUCTIONSTATUS=50".format(ID))
    count = 0
    for row in cursor:
        count += 1

print ('Total added transformers: ' + str(count))
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
