import sys

#sys.path.append('../..')
import unittest, json
from cloudwatch_events.event_factory import EventFactory

class TestEventFactory(unittest.TestCase):
    def test_batch_event(self):
        event_json = '''
        {
          "version": "0",
          "id": "c8f9c4b5-76e5-d76a-f980-7011e206042b",
          "detail-type": "Batch Job State Change",
          "source": "aws.batch",
          "account": "aws_account_id",
          "time": "2017-10-23T17:56:03Z",
          "region": "us-east-1",
          "resources": [
            "arn:aws:batch:us-east-1:aws_account_id:job/4c7599ae-0a82-49aa-ba5a-4727fcce14a8"
          ],
          "detail": {
            "jobName": "event-test",
            "jobId": "4c7599ae-0a82-49aa-ba5a-4727fcce14a8",
            "jobQueue": "arn:aws:batch:us-east-1:aws_account_id:job-queue/HighPriority",
            "status": "RUNNABLE",
            "attempts": [],
            "createdAt": 1508781340401,
            "retryStrategy": {
              "attempts": 1
            },
            "dependsOn": [],
            "jobDefinition": "arn:aws:batch:us-east-1:aws_account_id:job-definition/first-run-job-definition:1",
            "parameters": {},
            "container": {
              "image": "busybox",
              "vcpus": 2,
              "memory": 2000,
              "command": [
                "echo",
                "'hello world'"
              ],
              "volumes": [],
              "environment": [],
              "mountPoints": [],
              "ulimits": []
            }
          }
        }
        '''
        event_input = json.loads(event_json)
        factroy_id = EventFactory.getFactoryId(event_input)
        event = EventFactory.createEvent(factroy_id, event_input)
        print(json.dumps(event.sensu_result()))

    def test_ssm_command_status_event(self):
        raw_json = '''
        {
            "version": "0",
            "id": "51c0891d-0e34-45b1-83d6-95db273d1602",
            "detail-type": "EC2 Command Status-change Notification",
            "source": "aws.ssm",
            "account": "123456789012",
            "time": "2016-07-10T21:51:32Z",
            "region": "us-east-1",
            "resources": ["arn:aws:ec2:us-east-1:123456789012:instance/i-abcd1111"],
            "detail": {
                "command-id": "e8d3c0e4-71f7-4491-898f-c9b35bee5f3b",
                "document-name": "AWS-RunPowerShellScript",
                "expire-after": "2016-07-14T22:01:30.049Z",
                "parameters": {
                    "executionTimeout": ["3600"],
                    "commands": ["date"]
                },
                "requested-date-time": "2016-07-10T21:51:30.049Z",
                "status": "Success"
            }
        }'''
        event_input =json.loads(raw_json)
        factory_id = EventFactory.getFactoryId(event_input)
        event = EventFactory.createEvent(factory_id, event_input)
        print(json.dumps(event.sensu_result()))

    def test_ssm_command_iovocation_status_event(self):
        raw_json = '''
                {
            "version": "0",
            "id": "4780e1b8-f56b-4de5-95f2-95db273d1602",
            "detail-type": "EC2 Command Invocation Status-change Notification",
            "source": "aws.ssm",
            "account": "123456789012",
            "time": "2016-07-10T21:51:32Z",
            "region": "us-east-1",
            "resources": ["arn:aws:ec2:us-east-1:123456789012:instance/i-abcd1111"],
            "detail": {
                "command-id": "e8d3c0e4-71f7-4491-898f-c9b35bee5f3b",
                "document-name": "AWS-RunPowerShellScript",
                "instance-id": "i-9bb89e2b",
                "requested-date-time": "2016-07-10T21:51:30.049Z",
                "status": "Success"
            }
        }'''
        event_input = json.loads(raw_json)
        factory_id = EventFactory.getFactoryId(event_input)
        event = EventFactory.createEvent(factory_id, event_input)
        print(json.dumps(event.sensu_result()))
    def test_ssm_automation_step_status_event(self):
        raw_json = '''
        {
          "version": "0",
          "id": "eeca120b-a321-433e-9635-dab369006a6b",
          "detail-type": "EC2 Automation Step Status-change Notification",
          "source": "aws.ssm",
          "account": "123456789012",
          "time": "2016-11-29T19:43:35Z",
          "region": "us-east-1",
          "resources": ["arn:aws:ssm:us-east-1:123456789012:automation-execution/333ba70b-2333-48db-b17e-a5e69c6f4d1c", 
            "arn:aws:ssm:us-east-1:123456789012:automation-definition/runcommand1:1"],
          "detail": {
            "ExecutionId": "333ba70b-2333-48db-b17e-a5e69c6f4d1c",
            "Definition": "runcommand1",
            "DefinitionVersion": 1.0,
            "Status": "Success",
            "EndTime": "Nov 29, 2016 7:43:25 PM",
            "StartTime": "Nov 29, 2016 7:43:23 PM",
            "Time": 2630.0,
            "StepName": "runFixedCmds",
            "Action": "aws:runCommand"
          }
        }'''
        event_input = json.loads(raw_json)
        factory_id = EventFactory.getFactoryId(event_input)
        event = EventFactory.createEvent(factory_id, event_input)
        print(json.dumps(event.sensu_result()))
    def test_ssm_automation_execution_status_event(self):
        raw_json = '''
        {
          "version": "0",
          "id": "d290ece9-1088-4383-9df6-cd5b4ac42b99",
          "detail-type": "EC2 Automation Execution Status-change Notification",
          "source": "aws.ssm",
          "account": "123456789012",
          "time": "2016-11-29T19:43:35Z",
          "region": "us-east-1",
          "resources": ["arn:aws:ssm:us-east-1:123456789012:automation-execution/333ba70b-2333-48db-b17e-a5e69c6f4d1c", 
            "arn:aws:ssm:us-east-1:123456789012:automation-definition/runcommand1:1"],
          "detail": {
            "ExecutionId": "333ba70b-2333-48db-b17e-a5e69c6f4d1c",
            "Definition": "runcommand1",
            "DefinitionVersion": 1.0,
            "Status": "Success",
            "StartTime": "Nov 29, 2016 7:43:20 PM",
            "EndTime": "Nov 29, 2016 7:43:26 PM",
            "Time": 5753.0,
            "ExecutedBy": "arn:aws:iam::123456789012:user/userName"
          }
        }'''
        event_input = json.loads(raw_json)
        factory_id = EventFactory.getFactoryId(event_input)
        event = EventFactory.createEvent(factory_id, event_input)
        print(json.dumps(event.sensu_result()))

    def test_health_event(self):
        raw_json = '''
        {
          "version": "0",
          "id": "121345678-1234-1234-1234-123456789012",
          "detail-type": "AWS Health Event",
          "source": "aws.health",
          "account": "123456789012",
          "time": "2016-06-05T06:27:57Z",
          "region": "ap-southeast-2",
          "resources": [],
          "detail": {
            "eventArn": "arn:aws:health:ap-southeast-2::event/AWS_ELASTICLOADBALANCING_API_ISSUE_90353408594353980",
            "service": "ELASTICLOADBALANCING",
            "eventTypeCode": "AWS_ELASTICLOADBALANCING_API_ISSUE",
            "eventTypeCategory": "issue",
            "startTime": "Sat, 11 Jun 2016 05:01:10 GMT",
            "endTime": "Sat, 11 Jun 2016 05:30:57 GMT",
            "eventDescription": [{
              "language": "en_US",
              "latestDescription": "A description of the event will be provided here"
            }]
          }
        }'''
        event_input = json.loads(raw_json)
        factory_id = EventFactory.getFactoryId(event_input)
        event = EventFactory.createEvent(factory_id, event_input)
        print(json.dumps(event.sensu_result()))

    def test_autoscaling_failure(self):
        raw_json = '''
        {
          "version": "0",
          "id": "12345678-1234-1234-1234-123456789012",
          "detail-type": "EC2 Instance Launch Unsuccessful",
          "source": "aws.autoscaling",
          "account": "123456789012",
          "time": "yyyy-mm-ddThh:mm:ssZ",
          "region": "us-west-2",
          "resources": [
            "auto-scaling-group-arn",
            "instance-arn"
          ],
          "detail": {
              "StatusCode": "Failed",
              "AutoScalingGroupName": "my-auto-scaling-group",
              "ActivityId": "87654321-4321-4321-4321-210987654321",
              "Details": {
                  "Availability Zone": "us-west-2b",
                  "Subnet ID": "subnet-12345678"
              },
              "RequestId": "12345678-1234-1234-1234-123456789012",
              "StatusMessage": "message-text",
              "EndTime": "yyyy-mm-ddThh:mm:ssZ",
              "EC2InstanceId": "i-1234567890abcdef0",
              "StartTime": "yyyy-mm-ddThh:mm:ssZ",
              "Cause": "description-text"
          }
        }'''
        event_input = json.loads(raw_json)
        factory_id = EventFactory.getFactoryId(event_input)
        event = EventFactory.createEvent(factory_id, event_input)
        print(json.dumps(event.sensu_result()))
    def test_unknown_event(self):
        raw_json = '''
        {
          "version": "0",
          "id": "12345678-1234-1234-1234-123456789012",
          "detail-type": "EC2 Instance Launch Unsuccessful",
          "source": "aws.unknown",
          "account": "123456789012",
          "time": "yyyy-mm-ddThh:mm:ssZ",
          "region": "us-west-2",
          "resources": [
            "auto-scaling-group-arn",
            "instance-arn"
          ],
          "detail": {
              "StatusCode": "Failed",
              "AutoScalingGroupName": "my-auto-scaling-group",
              "ActivityId": "87654321-4321-4321-4321-210987654321",
              "Details": {
                  "Availability Zone": "us-west-2b",
                  "Subnet ID": "subnet-12345678"
              },
              "RequestId": "12345678-1234-1234-1234-123456789012",
              "StatusMessage": "message-text",
              "EndTime": "yyyy-mm-ddThh:mm:ssZ",
              "EC2InstanceId": "i-1234567890abcdef0",
              "StartTime": "yyyy-mm-ddThh:mm:ssZ",
              "Cause": "description-text"
          }
        }'''
        event_input = json.loads(raw_json)
        factory_id = EventFactory.getFactoryId(event_input)
        event = EventFactory.createEvent(factory_id, event_input)
        assert event is None

if __name__ == '__main__':
    unittest.main()