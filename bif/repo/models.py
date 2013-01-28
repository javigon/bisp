from django.db import models

class Building(models.Model):
    bid = models.IntegerField("Unique building ID")
    description = models.CharField(max_length=512) # "Short description of the building"
    bri = models.IntegerField("building representation id. 0 - Debug, 2 - IFC, 3 - Revit")
    active = models.BooleanField()
    # Add other aux attributes here. 
    def __unicode__(self):
        return str(self.bid) + ' ' + str(self.description)

class Entity(models.Model):
    bid = models.ForeignKey(Building)
    uuid = models.CharField(max_length=50) # Unique Identifier for each entity in a building.
    description = models.CharField(max_length=512) #"Short description of the entity"
    
    def __unicode__(self):
        return self.id

class Measurement(models.Model):
    bid = models.IntegerField("Unique building ID")
    uuid = models.CharField(max_length=256) #models.ForeignKey(Entity);
    timestamp = models.DateTimeField("Current time the value was recorded")
    val = models.FloatField("Value to be stored")
    
    def __unicode__(self):
        return str(self.id)


