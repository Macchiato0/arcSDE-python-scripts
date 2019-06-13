def calculateML(feederID,datapath):
    searchFields = ["OBJECTID","SHAPE@LENGTH"]
    updateFields = ["OBJECTID","MEASUREDLENGTH","LENGTHSOURCE"]
    feederField = "FEEDERID"
    measureField = "MEASUREDLENGTH"
    for feeder in feederID:
        print feeder
        SQL = """{0} = '{1}' AND {2} IS NULL""".format(arcpy.AddFieldDelimiters(secOH,feederField),feeder,arcpy.AddFieldDelimiters(secOH,measureField))
        print SQL
        myDict = {}
        searchCursor = arcpy.da.SearchCursor(secOH,searchFields,SQL)
        for row in searchCursor:
            objID = row[0]
            objLength =row[1]
            myDict[objID] = objLength
        print myDict
        del searchCursor

        updateCursor = arcpy.da.UpdateCursor(secOH,updateFields,SQL)
        for item in updateCursor:
            myLength = myDict[item[0]]
            item[1] = myLength*3.28084
            item[2] = "FM"
            updateCursor.updateRow(item)
        del updateCursor
#### Function Parameters ####
feederID = ['001901']
secOH = r'E:\Data\EROlson\test.gdb\SecOH'
calculateML(feederID, secOH)
