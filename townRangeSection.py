def calculateTownRangeSection():
  ####Some basic steps####
  '''
  SectionName is a feature class in the LandBase SDE connection. There is a 6-digit numeric sequence that is a unique ID for each polygon
  in the sectionname attribut field.
  
  We need the section name code transfered for the following feature classes for a specific feederID:
    -Misc. Network Features
    -Fuse
    -Switch
    
  Some sort of "select by location" analysis will need to be done to identify which feederIDs are within a given section.
  '''
