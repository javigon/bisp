'''
Created on Jan 28, 2013

@author: Matias Bjorling
'''
import urllib
import json

# Points to the root of the bisp external interface
SERVER_ADDRESS = 'http://localhost:8000/api/user/'
QUERY_BUILDING_BID = 0
TEST_SERVICE_ID = 'room-1-light-2-gain'

def read_url(url_path):
    raw = urllib.urlopen(url_path)
    
    js = raw.readlines()
    
    return json.loads(js[0])

def get_buildings():
    ''' Everything from http://django-tastypie.readthedocs.org/en/latest/interacting.html#fetching-data is supported. '''
    
    url = SERVER_ADDRESS + 'buildinginfo/'
    js_object = read_url(url)
    
    # Meta data for the query
    print 'All meta data available:', json.dumps(js_object['meta'], indent = 4)
    
    # Number of buildings available 
    print 'Total number of buildings:', js_object['meta']['total_count']

    # Retrieved building objects
    print 'Buildings:', json.dumps(js_object['objects'], indent = 4)
    
    # Retrieve building id for further queueries
    for b in js_object['objects']:
        print 'Building found with ID', b['bid'], 'and description', b['description']
    

def get_all_building_info(bid):
    url = SERVER_ADDRESS + 'building/entry/description/' + str(bid)
    js_object = read_url(url)
    
    print json.dumps(js_object['value'], indent = 4)
    
    # Number of rooms in the building
    print 'Rooms:', len(js_object['value']['rooms'])
    
    # Query a single room for its unique ID
    print 'Room ids', json.dumps(js_object['value']['rooms'].keys(), indent = 4)
    
    # Query information for a specific room
    print 'Information on lights in first room', json.dumps(js_object['value']['rooms']['floor-0-room-1']['lights'], indent = 4)
    
    
def get_service_value(service_id):
    ''' Everything from http://django-tastypie.readthedocs.org/en/latest/interacting.html#fetching-data is supported. 

     Get the value of some service (light, heater, ac, water, etc.) in the system. 
     You need the unique that identify each service.
    
     The variables available to read is found in the "outputs" section of the service definition. For example
     for lights. Outputs are state, production and gain. You append .output name to the light to retrieve its value.
    
     Ex. For light, with ID room-1-light-2 and you wish to know if it is on or off. You query room-1-light-2.gain
     
     Use the http://django-tastypie.readthedocs.org/en/latest/interacting.html#fetching-data guide to form more
     advance queries. 
    '''
    # We use the following
    light_url = SERVER_ADDRESS + 'measurement/?uuid=' + str(service_id) + '&limit=2&order_by=-timestamp'
    js_object = read_url(light_url)
    
    # Retrieve the last 20 samples of the light.
    print json.dumps(js_object, indent = 4)
    
def set_service_value(service_id, value):
    '''
        To set a value for a service. We use the following format:
          /api/user/building/entry/set/service_id/value where service_id is the 
            service id and value is the value that you wish to set for the actuator/service.
            
        The attributes available, follows the same schema as possible outputs. 
        But only input attributes are possible when setting a value.
    '''
    
    # We use the following to turn of the light. 
    url = SERVER_ADDRESS + 'building/entry/set/' + str(QUERY_BUILDING_BID) + '/'+ str(service_id) +'/' + str(value)
    read_url(url)
    
    
if __name__ == '__main__':
    
    # Retrieve a list of registered buildings
    print 'Retrieve all buildings available in the simulator.'
    get_buildings()
    input()
    
    # Get all information about a specific building
    print 'Retrieve the blueprint for the building with id:', QUERY_BUILDING_BID
    get_all_building_info(QUERY_BUILDING_BID)
    input()

    # Get information for a specific service (water, ac, light, etc)
    print 'Get the value for the specific light with id:', TEST_SERVICE_ID
    get_service_value(TEST_SERVICE_ID)
    input()    

    # Set information for a specific service
    print 'Turn the light off for service:', TEST_SERVICE_ID
    set_service_value(TEST_SERVICE_ID, 0)

    pass
