from cloudwatch_events.event import Event

class AWSHealthEvent(Event):

    # interested event type
    target_types = [
        'AWS_EC2_PERSISTENT_INSTANCE_RETIREMENT_SCHEDULED',
        'AWS_EC2_INSTANCE_REBOOT_MAINTENANCE_SCHEDULED'
    ]

    def __init__(self, event):
        self.region = event.get('region')
        self.service = event.get('detail').get('service')
        self.event_type_code = event.get('detail').get('eventTypeCode')
        # one of issue, accountNotification, scheduledChange
        self.event_type_category = event.get('detail').get('eventTypeCategory')
        self.start_time = event.get('detail').get('startTime')
        self.end_time = event.get('detail').get('endTime')
        event_descriptions = event.get('detail').get('eventDescription', [{}])
        print(event_descriptions)
        self.descriptions = list(map(lambda x: x.get('latestDescription', 'NA'), event_descriptions))
        #open, closed, upcoming
        self.status_code = event.get('detail').get('statusCode', 'NA')
        self.last_updated_time = str(event.get('lastUpdatedTime', 'NA'))

    def sensu_result(self):
        status_map = {
            'issue': 2,
            'accountNotification': 0,
            'scheduledChange': 1
        }

        sensu_status = '0'

        if self.event_type_category == 'issue':
            if self.status_code == 'open':
                sensu_status = '2'
            elif self.status_code == 'closed':
                sensu_status = '0'
            else:
                sensu_status = '2'
        elif self.event_type_category == 'accountNotification':
            if self.status_code == 'open':
                sensu_status = '1'
            elif self.status_code == 'closed':
                sensu_status = '0'
            else:
                sensu_status = '1'
        elif self.event_type_category == 'scheduledChange':
            if self.status_code == 'open':
                sensu_status = '1'
            elif self.status_code == 'closed':
                sensu_status = '0'
            else:
                sensu_status = '1'


        sensu_check = {
            'name':  'health_{}_{}'.format(self.service, self.event_type_category),
            'source': '{}.health.aws'.format(self.service),
            'status': sensu_status,
            'output': 'AWS health:{} event_type:{} status:{} description:{}'.format(self.service,self.event_type_code, self.status_code, self.descriptions)
        }

        return sensu_check

    class Factory:
        @staticmethod
        def create(json): return AWSHealthEvent(json)
