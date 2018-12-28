#!/bin/bash
docker run -it --rm \
 -v ${PWD}:/lambda \
 python_aws_lambda:latest
