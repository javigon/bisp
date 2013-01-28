'''
Created on Dec 6, 2012

@author: Matias Bjorling
'''

import inspect
from tastypie.resources import ModelResource, ModelDeclarativeMetaclass
from tastypie.resources import Resource
from tastypie import fields
from repo.models import Building, Measurement
from copy import deepcopy
from tastypie.exceptions import NotFound, BadRequest
from tastypie.constants import ALL
from building.bif import BifBase
from building.bmanager import Manager
from building.impl.room import Room


class BuildingDataResource(ModelResource):
    class Meta:
        resource_name = 'buildinginfo'
        queryset = Building.objects.all()
        
class MeasurementsResource(ModelResource):
    class Meta:
        resource_name = 'measurement'
        queryset = Measurement.objects.all()
        filtering = {
            'bid': ALL,
            'timestamp': ALL,
            'uuid': ALL
        }

class BuildingValue():
    _query = None
    _value = None

class BuildingResource(Resource):

    __metaclass__ = ModelDeclarativeMetaclass

    PATH_START_IDX = 4;

    class Meta:
        resource_name = 'building'
        object_class = BifBase

    @classmethod
    def get_fields(cls, f=None, e=None):
        """
        Look up Meta object_class variable and export their associated methods.
        """
        final_fields = {}

        if not cls._meta.object_class:
            return final_fields
        # We export all methods
        for f in dir(cls._meta.object_class):

            if not f.startswith('get'):
                continue;

        final_fields['query'] = fields.CharField()
        final_fields['query'].attribute = '_query'
        final_fields['query'].null = True
        final_fields['value'] = fields.DictField()
        final_fields['value'].attribute = '_value'
        final_fields['value'].null = True

        cls.fields = deepcopy(final_fields)

        return final_fields

    @classmethod
    def obj_get(self, request=None, **kwargs):
        """
        This method is called when using the /api/user/building/entry/query/... interface
        """

        data = BuildingValue()
        path = None
        methodtype = None

        if hasattr(request, "path"):
            path = request.path.split('/') # unicode: /api/user/building/entry/lights/1/1/1/
        else:
            return None

        if (len(path) < self.PATH_START_IDX):
            raise BadRequest('You need to specify all variables on the form /api/user/building/entry/QUERY/SERVICE/BUILDINGID/FLOORID/ROOMID')

        # Create our arguments from the query path.
        if len(path) > self.PATH_START_IDX:
            methodtype = path[self.PATH_START_IDX+1];

        if methodtype.lower() == 'description':
            data._value = self.get_building_description(path)
        elif methodtype.lower() == 'set':
            data._value = self.set_service(path)
        else:
            raise NotFound

        data._query = methodtype.lower();

        return data

    @classmethod
    def obj_get_list(self, request=None, **kwargs):
        filters = {}

        print Manager.get_available_buildings()
        b = Manager.lookup(1)

        if hasattr(request, 'GET'):
            # Grab a mutable copy.
            filters = request.GET.copy()

        print request
        print filters
        # Update with the provided kwargs.
        filters.update(kwargs)

        t = inspect.getmembers(BifBase, predicate=inspect.ismethod)

        return t

    @classmethod
    def _get_buildingID(self, path):
        return int(path[self.PATH_START_IDX+2])

    @classmethod
    def _get_serviceID(self, path):
        return path[self.PATH_START_IDX+3]
    
    @classmethod
    def _get_value(self, path):
        return path[self.PATH_START_IDX+4]

    @classmethod
    def get_building_description(self, path):
        """ format /api/user/building/entry/description/1 where 1 is the building id """
        if len(path) < self.PATH_START_IDX + 2:
            raise BadRequest("To retrieve building services. You must supply a building id. Ex. /api/user/building/entry/description/1 for retrieving it for building where id = 1")

        buildingID = self._get_buildingID(path)
        b = Manager.lookup(buildingID)

        # Hint pyDev about our type
        assert isinstance(b, BifBase)

        floor = dict()
        floor['numFloors'] = b.getNumFloors()

        rooms = dict()

        for r in b.getRooms():
            print type(r)

            assert isinstance(r, Room)
            rooms[str(r.getLogicalID())] = r.getFullRepresentation()

        root = dict()
        root['rooms'] = rooms
        return root

    @classmethod
    def set_service(self, path):
        ''' format /api/user/building/entry/set/buildingid/service_id/value where service_id is the 
            service id and value is the value that you wish to set for the actuator/service.'''
        
        if len(path) < self.PATH_START_IDX + 4:
            raise BadRequest("To set building services. You must supply a service id and its new value. Ex. /api/user/building/entry/set/buildingid/serviceid/0.")

        buildingID = self._get_buildingID(path)
        serviceID = self._get_serviceID(path)
        value = self._get_value(path)

        # Instantiate building if its not already done so
        Manager.lookup(buildingID) 
        
        Manager.set_building_service(buildingID, serviceID, value)

        r = dict()
        r['returnvalue'] = True
        return r


