def calculateMeasuredLength(feederIDs):
    ####### Set Data Sources #######
    #Primary Overhead dataset
    priOH = r'Primary Lines\Primary Overhead Conductor'

    #Primary Underground dataset
    priUG = r'Primary Lines\Primary Underground Conductor'

    #Secondary Overhead dataset
    secOH = r'Customers & Transformers\Secondary Overhead Conductor'

    #Secondary Underground dataset
    secUG = r'Customers & Transformers\Secondary Underground Conductor'
    
    ####### Variable Assignment #######
    #fields for search cursor
    searchFields = ["OBJECTID","SHAPE@LENGTH"]

    #fields for update cursor
    updateFields = ["OBJECTID","MEASUREDLENGTH","LENGTHSOURCE"]

    #for SQL delimiter variable
    feederField = "FEEDERID"

    measureField = "MEASUREDLENGTH"

    for feeder in feederIDs:

        ####### Start Process for Secondary OH #######
    
        #create proper SQL where clause
        SQL = """{0} = '{1}' AND {2} IS NULL""".format(arcpy.AddFieldDelimiters(secOH,feederField),feeder,arcpy.AddFieldDelimiters(secOH,measureField))

        #dictionary to store queried features' object ID, and shape length
        myDict = {}

        #create search cursor
        searchCursor = arcpy.da.SearchCursor(secOH,searchFields,SQL)

        #loop through search cursor and place values into dictionary to be called later in the update cursor
        for row in searchCursor:
            objID = row[0]
            objLength = row[1]
            myDict[objID] = objLength
        #delete cursor when finished
        del searchCursor

        #create update cursor
        updateCursor = arcpy.da.UpdateCursor(secOH,updateFields,SQL)

        #loop through cursor and update row values from key/value pair in dictionary
        for item in updateCursor:
            myLength = myDict[item[0]]
            item[1] = myLength*3.28084
            item[2] = "FM"
            updateCursor.updateRow(item)
        #delete cursor when finished
        del updateCursor

        ####### Need blocks of code that mirror one above, but for individual FC's being updated #######
