'''
base - Python abstract building interface - bif base

Created on Dec 5, 2012

@author: Javier Gonzalez

Base2 uses the Services (enum) Class for making methods in the bif interface more extensible

Defined Services:
    - LIGHT      - Lightning Services
    - WATER      - Watering Services
    - AIR        - Air Conditioning Services
    - HEATING    - Heating Serivices
    - BLINDS     - Windows and Roller-blinder Services

'''
import abc
from building.lib import services
from userapi import api_fields

class BifBase(object):
    "Building Interface Abstract Class"
    __metaclass__ = abc.ABCMeta

    '''
        Definition of mandatory services in the building.
        Here we define the services that MUST be instantiated.
        The concrete implementations of this abstract class can implement
        more services, but are enforced to implement the services listed here.
        Defined Services:

            "LIGHT"  - Lightning
            "WATER"  - Watering
            "AIR"    - Air Conditioning
            "BLINDS" - Roller Blinders
            "HEATING" - Heaters

    '''
    ##New service definition MUST be added here
    defServices = ['LIGHT', 'WATER', 'AIR', 'BLINDS', 'HEATING']

    ##Services implemented in all class instances
    buildServClass = []

    def __init__(self):
        ##Initialize services in bif instantiation
        self.buildServ = services.Services()

    ##Add services to bif instantiation
    def implService(self, serviceName):
        if serviceName not in self.defServices:
            raise ValueError("Trying to implement a non-defined building service in the BifBase abstract interface")
        self.buildServ.addService(serviceName.lower())
        #Make class aware of which services its instances implement
        if serviceName.lower() not in self.__class__.buildServClass:
            self.__class__.buildServClass.append(serviceName.lower())



    '''
        #######################################
        Semi-Implemented abstract methods for building services
        #######################################
    '''

    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getNumFloors(self):
        '''    getNumFloors(self)

               Description:
                   Returns number of floors in a given building

        '''

        method_name = "_getNumFloors"
        return method_name

    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getNumRooms(self):
        '''    getNumRooms(self)

               Description:
                   Returns number of rooms in a given building/Floor

        '''

        method_name = "_getNumRooms"
        return method_name

    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getRooms(self):
        '''    getNumRooms(self)

               Description:
                   Returns rooms in a given building/Floor

        '''

        method_name = "_getRooms"
        return method_name

    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getRoomFloor(self, roomID):
        '''    getRoomFloor(self, roomID)

               Description:
                   Returns the FloorID where the Room is Located

        '''

        method_name = "_getRoomFloor"
        return method_name



    ###      Room adjacency    ###

    ###
    ### Each room is adjacent to other rooms (the hall
    ### is also considered as a room. Adjacency exists
    ### between floors
    ###

    ### RoomA ---edge--- RoomB ###

    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getNumRoomPairs(self):
        '''    getNumEdges(self)

               Description:
                   Returns the number of edges in a given building

        '''

        method_name = "_getNumRoomPairs"
        return method_name

    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getRoomPairList(self):
        '''    getEdgeList(self)

               Description:
                   Returns RoomA---edge---RoomB tuple
                   We assume that always int(RoomA) < int(RoomB) to avoid duplicates

        '''

        method_name = "_getRoomPairList"
        return method_name

    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getRoomList(self):
        '''    getNodeList(self)

               Description:
                   Returns all rooms

        '''

        method_name = "_getRoomList"
        return method_name


    ### Service-specific Methods ###
    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getRoomHasServ(self, service, roomID):
        '''    getRoomServ(self, service, roomID)

               Description:
                   Returns the existance of a service in a given room

        '''

        if service not in vars(self.buildServ).keys():
            raise ValueError("Trying to access a non-defined building service")

        #serv = vars(self.buildServ).get(service)    #serv contains the key of the service attribute

        method_name ='_servRoomHas_' + str(service)
        return method_name


    @abc.abstractmethod
    @api_fields.is_exported_float
    def getNumBuildingServ(self, service):
        '''     getNumBuildingServ(self, service)

                Description:
                    Number of service instances in a building

                    We mark it as abstractmethod since it must be implemented in the
                    child class

                Parameters:
                    service - name of the service

        '''

        if service not in vars(self.buildServ).keys():
            raise ValueError("Trying to access a non-defined building service")

        #serv = vars(self.buildServ).get(service)    #serv contains the key of the service attribute

        method_name ='_servNumBuilding_' + str(service)
        return method_name


    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getNumFloorServ(self, service, floorID):
        '''     getNumFloorServ(self, service, FloorID)

                Description:
                    Number of services instances in a floor

                    We mark it as abstractmethod since it has to be implemented in the
                    child class

                Parameters:
                    service - name of the service
                    floorID - ID of the floor

        '''
        if service not in vars(self.buildServ).keys():
            raise ValueError("Trying to access a non-defined building service")

        #serv = vars(self.buildServ).get(service)    #serv contains the key of the service attribute

        method_name ='_servNumFloor_' + str(service)
        return method_name

    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getNumRoomServ(self, service, roomID):
        '''     getNumRoomServ(self, service, roomID)

                Description:
                    Number of services instances in a room

                    We mark it as abstractmethod since it has to be implemented in the
                    child class

                Parameters:
                    service - name of the service
                    roomID - ID of the floor

        '''
        if service not in vars(self.buildServ).keys():
            raise ValueError("Trying to access a non-defined building service")

        #serv = vars(self.buildServ).get(service)    #serv contains the key of the service attribute

        method_name ='_servNumRoom_' + str(service)
        return method_name

    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getBuildingServ(self, service):
        '''     getBuildingServ(self, service)

                Description:
                    List of a service instances in a Building

                    We mark it as abstractmethod since it has to be implemented in the
                    child class

                Parameters:
                    service - name of the service
        '''
        if service not in vars(self.buildServ).keys():
            raise ValueError("Trying to access a non-defined building service")

        #serv = vars(self.buildServ).get(service)    #serv contains the key of the service attribute

        method_name ='_servListBuilding_' + str(service)
        return method_name

    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getFloorServ(self, service, floorID):
        '''     getFloorServ(self, service, roomID)

                Description:
                    List of a service instances in a Floor

                    We mark it as abstractmethod since it has to be implemented in the
                    child class

                Parameters:
                    service - name of the service
                    floorID - ID of floor
        '''
        if service not in vars(self.buildServ).keys():
            raise ValueError("Trying to access a non-defined building service")

        #serv = vars(self.buildServ).get(service)    #serv contains the key of the service attribute

        method_name ='_servListFloor_' + str(service)
        return method_name

    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getRoomServ(self, service, roomID):
        '''     getRoomServ(self, service, roomID)

                Description:
                    List of a service instances in a Room

                    We mark it as abstractmethod since it has to be implemented in the
                    child class

                Parameters:
                    service - name of the service
                    roomID - ID of room
        '''
        if service not in vars(self.buildServ).keys():
            raise ValueError("Trying to access a non-defined building service. Try any of ["+(",".join(vars(self.buildServ).keys()))+"]")

        #serv = vars(self.buildServ).get(service)    #serv contains the key of the service attribute

        method_name ='_servListRoom_' + str(service)
        return method_name

    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getEfficiencyServ(self, service, serviceID):
        '''     getEfficiencyServ(self, service, serviceID)

                Description:
                    Efficiency of a given service specified by its serviceID

                    We mark it as abstractmethod since it has to be implemented in the
                    child class

                Parameters:
                    service - name of the service
                    serviceID - ID of a service
        '''
        if service not in vars(self.buildServ).keys():
            raise ValueError("Trying to access a non-defined building service")

        #serv = vars(self.buildServ).get(service)    #serv contains the key of the service attribute

        method_name ='_servEfficiency_' + str(service)
        return method_name

    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getExpenditureServ(self, service, serviceID):
        '''     getExpenditureServ(self, service, serviceID)

                Description:
                    Expenditure of a given service specified by its serviceID.
                    Expenditure is e.g. Wattage in terms of Electric Power

                    We mark it as abstractmethod since it has to be implemented in the
                    child class

                Parameters:
                    service - name of the service
                    serviceID - ID of a service
        '''
        if service not in vars(self.buildServ).keys():
            raise ValueError("Trying to access a non-defined building service. Try any of ["+(",".join(vars(self.buildServ).keys()))+"]")

        #serv = vars(self.buildServ).get(service)    #serv contains the key of the service attribute

        method_name ='_servExpenditure_' + str(service)
        return method_name

    @abc.abstractmethod
    @api_fields.is_exported_integer
    def getSizeServ(self, service, serviceID):
        '''     getSizeServ(self, service, serviceID)

                Description:
                    Size of a given service specified by its serviceID.

                    We mark it as abstractmethod since it has to be implemented in the
                    child class

                Parameters:
                    service - name of the service
                    serviceID - ID of a service
        '''
        if service not in vars(self.buildServ).keys():
            raise ValueError("Trying to access a non-defined building service")

        #serv = vars(self.buildServ).get(service)    #serv contains the key of the service attribute

        method_name ='_servSize_' + str(service)
        return method_name



    '''
        ##################################################
        Abstract private methods for building architecture
        ##################################################
    '''

    @abc.abstractmethod
    def _getNumFloors(self):
        return

    @abc.abstractmethod
    def _getNumRooms(self):
        return

    @abc.abstractmethod
    def _getRoomFloor(self, roomID):
        return

    @abc.abstractmethod
    def _getNumRoomPairs(self):
        return

    @abc.abstractmethod
    def _getRoomPairList(self):
        return

    @abc.abstractmethod
    def _getRoomList(self):
        return

    @abc.abstractmethod
    def _getRooms(self):
        return

    '''
        ##################################################
        Abstract private methods for building services
        ##################################################
    '''

    ##Lightning
    if 'LIGHT' in defServices:
        @abc.abstractmethod
        def _servNumBuilding_light(self):
            return

        @abc.abstractmethod
        def _servNumFloor_light(self, floorID):
            return

        @abc.abstractmethod
        def _servNumRoom_light(self, roomID):
            return

        @abc.abstractmethod
        def _servRoomHas_light(self, roomID):
            return


    ##Watering
    if 'WATER' in defServices:
        @abc.abstractmethod
        def _servNumBuilding_water(self):
            return

        @abc.abstractmethod
        def _servNumFloor_water(self, floorID):
            return

        @abc.abstractmethod
        def _servNumRoom_water(self, roomID):
            return

        @abc.abstractmethod
        def _servRoomHas_water(self, roomID):
            return

    ##Air Conditioning

    if 'AIR' in defServices:
        @abc.abstractmethod
        def _servNumBuilding_air(self):
            return

        @abc.abstractmethod
        def _servNumFloor_air(self, floorID):
            return

        @abc.abstractmethod
        def _servNumRoom_air(self, roomID):
            return

        @abc.abstractmethod
        def _servRoomHas_air(self, roomID):
            return

    ##Roller Blinders

    if 'BLINDS' in defServices:
        @abc.abstractmethod
        def _servNumBuilding_blinds(self):
            return

        @abc.abstractmethod
        def _servNumFloor_blinds(self, floorID):
            return

        @abc.abstractmethod
        def _servNumRoom_blinds(self, roomID):
            return

        @abc.abstractmethod
        def _servRoomHas_blinds(self, roomID):
            return


    if 'HEATING' in defServices:
        @abc.abstractmethod
        def _servNumBuilding_heating(self):
            return

        @abc.abstractmethod
        def _servNumFloor_heating(self, floorID):
            return

        @abc.abstractmethod
        def _servNumRoom_heating(self, roomID):
            return

        @abc.abstractmethod
        def _servRoomHas_heating(self, roomID):
            return
