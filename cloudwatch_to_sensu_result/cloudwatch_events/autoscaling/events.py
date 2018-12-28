import json
from cloudwatch_events.event import Event


class EC2InstanceLaunchUnsuccessful(Event):

    def __init__(self, event):
        self.region = event.get('region')
        self.autoscaling_group_name = event.get('detail').get('AutoScalingGroupName')
        self.availability_zone = event.get('detail').get('Availability_Zone')
        self.status_code = event.get('detail').get('StatusCode')
        self.instance_id = event.get('detail').get('EC2InstanceId')
        self.cause = event.get('detail').get('Cause')

    def sensu_result(self):

        sensu_result = None
        if self.status_code == 'Failed':
            sensu_result = {
                'source': 'autoscaling.aws',
                'output': 'Autoscaling:{} instance:{} status:{} cause:{}'.format(self.autoscaling_group_name, self.instance_id, self.status_code, self.cause),
                'status': '2',
                'name': 'asg_{}'.format(self.autoscaling_group_name)
            }

        return sensu_result

    class Factory:
        @staticmethod
        def create(json): return EC2InstanceLaunchUnsuccessful(json)
