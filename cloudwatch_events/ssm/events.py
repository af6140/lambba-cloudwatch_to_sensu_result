from cloudwatch_events.event import Event

class EC2CommandStatuschangeNotification(Event):
    def __init__(self, event):
        self.region = event.get('region')
        self.resources = event.get('resources')
        self.time = event.get('time')
        self.command_id = event.get('detail').get('command-id')
        self.document_name = event.get('detail').get('document-name')
        self.status = event.get('detail').get('status')

    def sensu_result(self):
        status_map = {
            'Pending': 1,
            'In Progress': 1,
            'Delayed': 1,
            'Success': 0,
            'Delievery Timed Out': 2,
            'Execution Timed Out': 2,
            'Failed': 2,
            'Canceled': 1,
            'Undeliverable': 2,
            'Terminated': 1
        }
        resource_id = self.resources[0]
        resource_id = resource_id.split('/')[-1]
        sensu_check = {
            'name':  'command_status_{}_{}'.format(self.document_name,resource_id),
            'source': 'ssm.aws',
            'status': '{}'.format(status_map.get(self.status, 1)),
            'output': 'Command:{} document:{} status:{}'.format(self.command_id, self.document_name, self.status)
        }

        return sensu_check
    class Factory:
        @staticmethod
        def create( json): return EC2CommandStatuschangeNotification(json)


class EC2CommandInvocationStatuschangeNotification(Event):
    def __init__(self, event):
        self.region = event.get('region')
        self.resources = event.get('resources')
        self.time = event.get('time')
        self.command_id = event.get('detail').get('command-id')
        self.document_name = event.get('detail').get('document-name')
        self.status = event.get('detail').get('status')
        self.instance_id = event.get('detail').get('instance-id')
    def sensu_result(self):
        status_map = {
            'Pending': 1,
            'In Progress': 1,
            'Delayed': 1,
            'Success': 0,
            'Delievery Timed Out': 2,
            'Execution Timed Out': 2,
            'Failed': 2,
            'Canceled': 1,
            'Undeliverable': 2,
            'Terminated': 1
        }
        sensu_check = {
            'name':  'command_invocation_{}'.format(self.document_name),
            'source': 'ssm.aws',
            'status': '{}'.format(status_map.get(self.status, 1)),
            'output': 'Command:{} document:{} status:{} instance:{}'.format(self.command_id, self.document_name, self.status, self.instance_id)
        }
        return sensu_check
    class Factory:
        @staticmethod
        def create(json): return EC2CommandInvocationStatuschangeNotification(json)


class EC2AutomationStepStatuschangeNotification(Event):
    def __init__(self, event):
        self.region = event.get('region')
        self.resources = event.get('resources')
        self.time = event.get('time')
        self.execution_id = event.get('detail').get('ExecutionId')
        self.definition = event.get('detail').get('Definition')
        self.definition_version = event.get('detail').get('DefinitionVersion')
        self.status = event.get('detail').get('status')
        self.step_name = event.get('detail').get('StepName')
        self.action = event.get('detail').get('Action')
    def sensu_result(self):
        status_map = {
            'Pending': 1,
            'In Progress': 1,
            'Delayed': 1,
            'Success': 0,
            'Delievery Timed Out': 2,
            'Execution Timed Out': 2,
            'Failed': 2,
            'Canceled': 1,
            'Undeliverable': 2,
            'Terminated': 1
        }
        sensu_check = {
            'name':  'automation_step_{}:{}_step_{}'.format(self.definition,self.definition_version, self.step_name),
            'source': 'ssm.aws',
            'status': '{}'.format(status_map.get(self.status, 1)),
            'output': 'AutomationStep:{}:{} step:{} status:{}'.format(self.definition, self.definition_version, self.step_name, self.status)
        }
        return sensu_check
    class Factory:
        @staticmethod
        def create(json): return EC2AutomationStepStatuschangeNotification(json)



class EC2AutomationExecutionStatuschangeNotification(Event):
    def __init__(self, event):
        self.region = event.get('region')
        self.resources = event.get('resources')
        self.time = event.get('time')
        self.execution_id = event.get('detail').get('ExecutionId')
        self.definition = event.get('detail').get('Definition')
        self.definition_version = event.get('detail').get('DefinitionVersion')
        self.status = event.get('detail').get('status')
    def sensu_result(self):
        status_map = {
            'Pending': 1,
            'In Progress': 1,
            'Delayed': 1,
            'Success': 0,
            'Delievery Timed Out': 2,
            'Execution Timed Out': 2,
            'Failed': 2,
            'Canceled': 1,
            'Undeliverable': 2,
            'Terminated': 1
        }
        sensu_check = {
            'name':  'automation_execution_{}:{}'.format(self.definition, self.definition_version),
            'source': 'ssm.aws',
            'status': '{}'.format(status_map.get(self.status, 1)),
            'output': 'AutomationExecution:{}:{} execution:{} status:{}'.format(self.definition, self.definition_version, self.execution_id, self.status)
        }
        return sensu_check
    class Factory:
        @staticmethod
        def create(json): return EC2AutomationExecutionStatuschangeNotification(json)
