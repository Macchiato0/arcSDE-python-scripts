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

'''
