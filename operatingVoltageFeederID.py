'''
This script has been developed for the purpose of:
                                                    1) Making a list of FeederIDs that have null values in ANY of the input data FCs
                                                    2) Making a list of FeederIDs that have null values AND Isolators associated with
                                                       the given FeederIDs
                                                  
'''
#input data
transformer = r'Customers & Transformers\Secondary Transformers'

priOH = r'Primary Lines\Primary Overhead Conductor'

priUG = r'Primary Lines\Primary Underground Conductor'

misc = r'Misc Network Features\Tap Dots, T-points, & Wire Changes'

fuse = r'Devices\Protective Devices & Switches\Fuse'

isolator = r'Devices\Primary Devices\Isolator'

dataList = [transformer, priOH, priUG, misc, fuse]
fields = ["FEEDERID"]
allFeederID = []
nullFeederID = []
isolatorFeederID = []
  
for i in dataList:
    delim = arcpy.AddFieldDelimiters(i,"OPERATINGVOLTAGE") + ' IS NULL'
    cursor = arcpy.da.SearchCursor(i,fields,delim)
    for row in cursor:
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
