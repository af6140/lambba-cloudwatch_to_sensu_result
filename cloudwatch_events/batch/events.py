import json
from cloudwatch_events.event import Event

class BatchJobStateChange(Event):
    def __init__(self, event):
        self.region = event.get('region')
        self.resources = event.get('resources')
        self.job_name = event.get('detail').get('jobName')
        self.job_id = event.get('detail').get('jobId')
        job_queue = event.get('detail').get('jobQueue')
        queque_specs = job_queue.split('/')
        self.job_queue = queque_specs[-1]
        self.status = event.get('detail').get('status')
        self.created = event.get('detail').get('createdAt')
        self.jobDefinition = event.get('detail').get('jobDefinition')

    def sensu_result(self):
        status_map = {
            'SUCCEEDED': 0,
            'FAILED': 2,
            'SUBMITTED': 1,
            'PENDING': 1,
            'RUNNABLE': 1,
            'STARTING': 1,
            'RUNNING': 1,
        }

        sensu_check = {
            'name':  'job_{}_{}'.format(self.job_queue,self.job_name),
            'source': 'batch.aws',
            'status': '{}'.format(status_map.get(self.status, 1)),
            'output': 'Job:{} of execution:{} with status:{}'.format(self.job_name, self.job_id, self.status)
        }

        return sensu_check

    class Factory:
        @staticmethod
        def create(json): return BatchJobStateChange(json)

