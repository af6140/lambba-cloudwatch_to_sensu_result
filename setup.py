import configparser
from setuptools import setup

config = configparser.ConfigParser()
config.read('./local_setup.cfg')

pkg_name = config['setup']['name'].strip('"\'')
pkg_version = config['setup']['version'].strip('"\'')

setup(name=pkg_name,
      version=pkg_version,
      description='lambda transform cloudwatch event to sensu result',
      url='https://github.com/af6140/lambda-cloudwatch_to_sensu_result',
      author='Dawei Wang',
      author_email='daweiwang.gatekeeper@gmail.com',
      license="Apache 2.0",
      zip_safe=True,
      setup_requires=['lambda_setuptools'],
      packages=[pkg_name],
      install_requires=[
          'certifi==2018.1.18',
          'chardet==3.0.4',
          'idna==2.6',
          'jsonpickle==0.9.6',
          'jsonschema==2.6.0',
          'urllib3==1.23',
          'requests==2.20.0',
          'wrapt==1.10.11',
          'aws_lambda_logging==0.1.1'
      ],
      lambda_package=pkg_name,
      )
