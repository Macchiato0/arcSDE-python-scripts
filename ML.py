def calculateML(feederID,dataPath):
    searchFields = ["OBJECTID","SHAPE@LENGTH"]
    updateFields = ["OBJECTID","MEASUREDLENGTH","LENGTHSOURCE"]
    feederField = "FEEDERID"
    measureField = "MEASUREDLENGTH"
    for feeder in feederID:
        SQL = """{0} = '{1}' AND {2} IS NULL""".format(arcpy.AddFieldDelimiters(dataPath,feederField),feeder,arcpy.AddFieldDelimiters(dataPath,measureField))
        myDict = {}
        searchCursor = arcpy.da.SearchCursor(dataPath,searchFields,SQL)
        for row in searchCursor:
            objID = row[0]
            objLength =row[1]
            myDict[objID] = objLength
        del searchCursor

        #set workspace
        workspace = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde'
        
        # Start an edit session. Must provide the worksapce.
        edit = arcpy.da.Editor(workspace)
        
        # Edit session is started without an undo/redo stack for versioned data
        #  (for second argument, use False for unversioned data)
        edit.startEditing(False, True)
        
        # Start an edit operation
        edit.startOperation()
        
        updateCursor = arcpy.da.UpdateCursor(dataPath,updateFields,SQL)
        for item in updateCursor:
            myLength = myDict[item[0]]
            item[1] = myLength*3.28084
            item[2] = "FM"
            updateCursor.updateRow(item)
        del updateCursor
        
        # Stop the edit operation.
        edit.stopOperation()
        
        # Stop the edit session and save the changes
        edit.stopEditing(True)
        
        
#### Function Parameters ####
feederID = ['001901']
priOH = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.PriOHElectricLineSegment'
priUG = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.PriUGElectricLineSegment'
secOH = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.SecOHElectricLineSegment'
secUG = r'E:\Data\EROlson\PROD_ DGSEP011AsEROlson.sde\ELECDIST.ElectricDist\ELECDIST.SecUGElectricLineSegment'

#### Call and Execute calculate ML function ####
calculateML(feederID, priOH)
calculateML(feederID, priUG)
calculateML(feederID, secOH)
calculateML(feederID, secUG)
