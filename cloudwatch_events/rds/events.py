import json
from cloudwatch_events.event import Event

class RDSDBInstanceEvent(Event):
    def __init__(self, event):
        self.region = event.get('region')
        self.resources = event.get('resources')
        self.time = event.get('time')
        self.event_categories = event.get('detail').get('EventCategories')
        self.message = event.get('detail').get('Message')
        self.source = event.get('detail').get('SourceIdentifier')

    def sensu_result(self):
        status_map = {
            'failover': 2,
        }

        sensu_check = {
            'name':  'rds_{}'.format(self.source),
            'source': 'rds.aws',
            'status': '{}'.format(status_map.get(self.event_categories[0]),1),
            'output': 'RDS event:{} from {} at {}, manually resolve alert when recovered.'.format(self.event_categories[0], self.soruce, self.time)
        }

        return sensu_check

    class Factory:
        @staticmethod
        def create(json): return RDSDBInstanceEvent(json)

