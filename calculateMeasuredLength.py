'''
This script has been developed for the purpose of creating a streamlined, automation solution
for calculating the values for the Measured Length & Length Source fields.

Things to add:
        1) Add workspace paramenter for function
        2) Test as a tool and add necessary GetParameterAsText() variable assignment
        3) Determine proper string formatting for assigning FC data paths to variables
'''
#create function for calculating the value for "Measured Length" field
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
        workspace = 
        
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
priOH = 
priUG = 
secOH = 
secUG = 

#### Call and Execute calculate ML function on ALL necessary FCs####
calculateML(feederID, priOH)
calculateML(feederID, priUG)
calculateML(feederID, secOH)
calculateML(feederID, secUG)
