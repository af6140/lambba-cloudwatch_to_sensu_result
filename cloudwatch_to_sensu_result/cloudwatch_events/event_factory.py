#import generators
import random
#https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html
import importlib

class EventFactory:
    factories = {}

    def addFactory(id, eventFactory):
        EventFactory.factories.put[id] = eventFactory
    
    addFactory = staticmethod(addFactory)

    def createEvent(id, json):
        if not id in EventFactory.factories:
            class_name_specs  = id.split('.')
            print(class_name_specs)
            class_name = class_name_specs[-1]
            class_name_specs.pop()
            module_name = '.'.join(class_name_specs)
            module = importlib.import_module(module_name)
            factory  = getattr(getattr(module, class_name), 'Factory')
            print('module:{} class:{}'.format(module_name,class_name))
            EventFactory.factories[id] = factory()
        return EventFactory.factories[id].create(json)
    
    createEvent = staticmethod(createEvent)


    def getFactoryId(event):
        event_source = event.get('source').replace('aws.', 'cloudwatch_events.')
        detail_type =event.get('detail-type').replace(' ', '').replace('-', '')
        return '{}.events.{}'.format(event_source, detail_type)
