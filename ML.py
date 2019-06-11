#Primary Overhead dataset
priOH = r'Primary Lines\Primary Overhead Conductor'

#Primary Underground dataset
priUG = r'Primary Lines\Primary Underground Conductor'

#Secondary Overhead dataset
secOH = r'Customers & Transformers\Secondary Overhead Conductor'

#Secondary Underground dataset
secUG = r'Customers & Transformers\Secondary Underground Conductor'

#Complete list of data paths
calcDataList = [priOH, priUG, secOH, secUG]

#list of feeder IDs to iterate through
feederID = ['008507']

#fields for search cursor
searchFields = ["OBJECTID","SHAPE@LENGTH"]

#fields for update cursor
updateFields = ["OBJECTID","MEASUREDLENGTH","LENGTHSOURCE"]

#for SQL delimiter variable
feederField = "FEEDERID"

measureField = "MEASUREDLENGTH"

for feeder in feederID:
    for FC in calcDataList:
        SQL = """{0} = '{1}' AND {2} IS NULL""".format(arcpy.AddFieldDelimiters(FC,feederField),feeder,arcpy.AddFieldDelimiters(FC,measureField))
        searchCursor = arcpy.da.SearchCursor(FC,searchFields,SQL)
        myDict = {}
        for row in searchCursor:
            objID = row[0]
            objLength = row[1]
            myDict[objID] = objLength
            updateCursor = arcpy.da.UpdateCursor(FC,updateFields,SQL)
            for item in updateCursor:
                myLength = myDict[item[0]]
                item[1] = myLength*3.28084
                item[2] = "FM"
                updateCursor.updateRow(item)
