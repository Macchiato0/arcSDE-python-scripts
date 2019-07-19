'''
Need script to update TRS

-need landbase sde connection for spatial selection (brock sent in email)
-section name FC has section name attribute field. needs to be moved to...misc. net feature,fuse,switch (will be done by feederID) 
to town range section (string value) in provided FCs

'''

def calculateTownRangeSection():
  updateFields = "TRS"
  feederField = "FEEDERID"
  trsSearchField = "SECTIONNAME"
  for feeder in feederID:
    
    SQL = """{0} = '{1}' AND {2} IS NULL""".format(arcpy.AddFieldDelimiters(dataPath,feederField),feeder,arcpy.AddFieldDelimiters(dataPath,workHQField))

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
    for row in updateCursor:
        row[0] = workHeadquarters
        updateCursor.updateRow(row)
    del updateCursor

    # Stop the edit operation.
    edit.stopOperation()

    # Stop the edit session and save the changes
    edit.stopEditing(True)
