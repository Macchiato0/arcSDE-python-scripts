'''
Useful Links:
https://gis.stackexchange.com/questions/230536/adding-values-from-list-to-field-in-feature-class-using-arcpy
'''
import arcpy

arcpy.env.workspace = 

#input data
transformer = 

priOH = 

priUG = 

misc = 

fuse = 

isolator = 

dataList = [transformer, priOH, priUG, misc, fuse]
fields = ["FEEDERID"]
allFeederID = []
nullFeederID = []
isolatorFeederID = []
  
for i in dataList:
    delim = arcpy.AddFieldDelimiters(i,"OPERATINGVOLTAGE") + ' IS NULL'
    cursor = arcpy.da.SearchCursor(i,fields,delim)
    for row in cursor:
        #check to see if feeder ID associated with isolator

        #if associated with isolator:
        #put in different list from nulls
        if row[0] not in allFeederID:
            allFeederID.append(row[0])

del cursor

for feeder in allFeederID:
    cursor = arcpy.da.SearchCursor(isolator,"*","SUBTYPECD = 10 AND FEEDERID = '{}'".format(feeder))
    for row in cursor:
        isolatorFeederID.append(row[0])
    else:
        nullFeederID.append(feeder)

del cursor




