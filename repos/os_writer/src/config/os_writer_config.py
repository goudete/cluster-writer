import os
from typing import get_type_hints, Union
import json
from peakm.kafka.MSKSecret import get_secret
from aiokafka import helpers


class AppConfigError(Exception):
    pass


def _parse_bool(val: Union[str, bool]) -> bool:  # pylint: disable=E1136
    return val if type(val) == bool else val.lower() in ['true', 'yes', '1']

# AppConfig class with required fields, default values, type checking, and typecasting for int and bool values


class AppConfig:
    # alphabetize fields for readability
    BUFFER_TIME_OS_WRITER: int = 6  # seconds, default value is nice locally
    KAFKA_AWS_CONFIG_JSON: str = 'false'  # only overwritten in production
    KAFKA_BROKERS_JSON: str
    KAFKA_TOPIC_DOWNSTREAM_SOCIAL: str = "downstream-social"  # overridden for tests
    KAFKA_TOPIC_DOWNSTREAM_SOCIAL_DLQ: str = "downstream-social-dlq"  # overridden for tests
    MESSAGES_IN_FLIGHT_OS_WRITER: int = 5  # overridden for prod
    OS_CORE_CLUSTER_HOST: str
    SCHEMA_REGISTRY_CONFIG_JSON: str

    """
    Map environment variables to class fields according to these rules:
      - Field won't be parsed unless it has a type annotation
      - Field will be skipped if not in all caps
      - Class field and environment variable name are the same
    """

    def __init__(self, env):
        for field in self.__annotations__:
            if not field.isupper():
                continue

            # Raise AppConfigError if required field not supplied
            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError('The {} field is required'.format(field))

            # Cast env var value to expected type and raise AppConfigError on failure
            try:
                var_type = get_type_hints(AppConfig)[field]
                if var_type == bool:
                    value = _parse_bool(env.get(field, default_value))
                elif var_type == str and field.endswith('_JSON'):
                    value = json.loads(var_type(env.get(field, default_value)))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError as err:
                raise AppConfigError('Unable to cast value of "{}" to type "{}" for "{}" field. Error: {}'.format(
                    env[field],
                    var_type,
                    field,
                    err
                )
                )

    def __repr__(self):
        return str(self.__dict__)

    def get_msk_credentials(self):
        try:
            creds = json.loads(get_secret())

            return {
                'sasl_mechanism': 'SCRAM-SHA-512',
                'security_protocol': 'SASL_SSL',
                'sasl_plain_password': creds['password'],
                'sasl_plain_username': creds['username'],
                'ssl_context': helpers.create_ssl_context()
            }
        except Exception as err:
            print("get_msk_credentials: error: ", err)
            raise AppConfigError('Unable to get MSK secret. Error: {}'.format(
                err
            ))


# Expose Config object for app to import
Config = AppConfig(os.environ)
