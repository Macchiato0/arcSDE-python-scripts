'''
This script is being developed for the purpose of reporting DRG contract metrics per SDE to be input into 
the master google sheet tacker for billing purposes.
'''

#### HVD Pole Photos ####
'''
1) Access the Support Structure FC in desired SDE
2) Find all HVD Pole photos
    -SQL expression: SUBSTATIONID = '%SubstationID%' AND CIRCUITID = '%CircuitID%' AND USAGETYPE = 'URB'
    -Total number of returned records equals the value for HVD Pole Photos
'''

#### Delivered Poles ####
'''
1) Access the Support Structure FC in desired SDE
2) Find all HVD Pole photos
    -SQL expression: SUBSTATIONID = '%SubstationID%' AND CIRCUITID = '%CircuitID%'
    -Total number of returned records equals the value for HVD Pole Photos
'''

#### Delivered UG ####
'''
1) Access Surface Structure FC
2) Find "Surface Enclosures"
    - SQL expression: (SUBSTATIONID = '%SubstationID%' AND CIRCUITID = '%CircuitID%') AND SUBTYPECD = 7
    - Get count of total number of returned records
3) Find "UG TLMs"
    - SQL expression: FEEDERID = '%FeederID%' AND( SUBTYPECD = 4 OR SUBTYPECD = 6 )
    - Get count of total number of returned records
4) Add values together for total of "Delivered UG"
'''

#### Poles with JU ####
'''
1) Access Support Structure FC
2) Execute selection
    - SQL expression: SUBSTATIONID = '%SubstationID%' AND CIRCUITID = '%CircuitID%'
3) Initiate "Join" w/ Attachment FC (by ObjectID, Keep only matching records)
    - Get count of total number of returned records for "Poles with JU"
4) Remove join
'''

#### Streetlight ####
'''
1) Access Streetlight FC
2) Execute selection
    - SQL expression: "SUBSTATIONID" = '%SubstationID%' AND "CIRCUITID" = '%CircuitID%'
3) Get count of total number of records returned
'''

#### Transformers Added or Removed ####
'''
1) Access Transformer FC
2) Execute selection
    - SQL expression: FEEDERID = '%FeederID%' AND (CONSTRUCTIONSTATUS = 50)
    - SQL expression: FEEDERID = '%FeederID%' AND (CONSTRUCTIONSTATUS = 55)
3) Get count of total number of records returned from each selection
'''

#### RePhased Transformers ####
'''
1) Access Transformer FC
2) Execute selection
    - SQL expression: FEEDERID = '%FeederID%' AND FLAG_FOR_EXCEPTION = 'Wrong Phase'
3) Get count of total number of records returned 
'''

#### RePhased Customers ####
'''
1) Access Service Points FC
2) Execute selection
    - SQL expression: FEEDERID = '%FeederID%' AND (FLAG_FOR_EXCEPTION = 'Wrong Phase' OR COMMENTS = 'FED BY ANOTHER CIRCUIT')
3) Get count of total number of records returned 
'''

#### Customers Added or Removed ####
'''
1) Access Service Points FC
2) Execute selection
    - SQL expression: FEEDERID = '%FeederID%' AND CONSTRUCTIONSTATUS = 50
    - SQL expression: FEEDERID = '%FeederID%' AND CONSTRUCTIONSTATUS = 55
3) Get count of total number of records returned for both selections
'''

#### Number of Service Points ####
'''
1) Access Service Points FC
2) Execute selection
    - SQL expression: FEEDERID = '%FeederID%'
3) Get count of total number of records returned 
'''
