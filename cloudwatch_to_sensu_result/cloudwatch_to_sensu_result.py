import os
import sys
sys.path.insert(0, "./")
from cloudwatch_events.event_factory import EventFactory

import boto3
import json

import logging, aws_lambda_logging

AWS_REGON = os.getenv('AWS_REGION', 'us-east-1')
SERVICE = os.getenv('SERVICE', 'default')
APP_TIER = os.getenv('APP_TIER', 'default')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
SNS_ARN = os.getenv('SNS_TOPIC_ARN', None)

EXTRA_SENSU_CHECK_PROPS = os.getenv('EXTRA_SENSU_CHECK_PROPS', '{}')

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))
aws_lambda_logging.setup(level=LOG_LEVEL.upper(), service =SERVICE, app_tier = APP_TIER)


def handler(event, context):
    if SNS_ARN:
        factroy_id = EventFactory.getFactoryId(event)
        event = EventFactory.createEvent(factroy_id, event)
        sensu_result = event.sensu_result()
        extra_props = {}
        try:
            extra_props = json.loads(EXTRA_SENSU_CHECK_PROPS)
        except ValueError:
            logger.error('cannot parse as jsn: {}'.format(EXTRA_SENSU_CHECK_PROPS))

        if sensu_result:
            sensu_result.update(extra_props)
            sns = boto3.client('sns', region=AWS_REGON)
            response = sns.publish(
                TargetArn = SNS_ARN,
                Message = json.dumps(sensu_result)
            )
    else:
        logger.error('No sns topic configured')


def test_logging():
    logger.info({'detail':'test', 'code': '2'})


if __name__ == '__main__':
    test_logging()
