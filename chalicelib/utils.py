import logging
import json
import boto3
from chalicelib import config
from functools import wraps
from itsdangerous import URLSafeSerializer, BadSignature
from chalice import ForbiddenError
from botocore.exceptions import ClientError

logger = logging.getLogger('my-app')


def get_secret(secret_name):
    service_name = 'secretsmanager'
    region_name = 'us-east-1'
    client = get_aws_client(service_name, region_name)
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            logger.error("The requested secret {} was not found".format(secret_name))
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            logger.error("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            logger.error("The request had invalid params:", e)
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = json.loads(get_secret_value_response['SecretString'])
            return secret['username'], secret['password']
        else:
            raise Exception("no secretstring found under secret id {}".format(secret_name))

def get_aws_client(service_name, region_name):
    logger.debug("Creating boto3 service client for {} in region {}".format(service_name, region_name))
    session = boto3.session.Session()
    client = session.client(
        service_name=service_name,
        region_name=region_name
    )
    return client

def signature_check(_meth):
    @wraps(_meth)
    def sig_check(*args, **kwargs):
        priv_path = None
        try:
            priv_path = dangerous_world.loads(kwargs['signature'])
        except BadSignature as err:
            logger.warn(err)
            raise ForbiddenError("Insufficient privileges")
        else:
            if priv_path != config.private_path:
                raise ForbiddenError("Insufficient privileges")
        return _meth(*args, **kwargs)
    return sig_check

logger.debug("retrieving credentials from secrets manager")
username, password = get_secret(config.rh_credentials)
logger.debug("retrieved credentials from secrets manager")
r_username = username
r_password = password
dangerous_world = URLSafeSerializer(r_password)
