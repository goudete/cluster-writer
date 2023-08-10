from google.protobuf import json_format
import json
import pytest
import asyncio
import time

from config.os_writer_config import Config
from db_providers.os_provider import OSProvider
from peakm.producer.KafkaProducer import KafkaProducer, MessageToProduce
import peakm.proto.core.social.SocialMentionCommon_pb2 as SocialMentionCommon_pb2

'''
OS Writer Service Test Flow

SETUP
- create social-mention-common messages
    - read messages from test data file
    - convert messages to protobuf object

EXECUTE
- produce social-mention-common messages to Kafka topic
- wait for messages to be processed by pipeline

ASSERT
- assert that documents are in OS
'''

tweets = [
    {
        "transformed": {
            "id": 1,
            "author": "bipin38349109",
            "text": "@sanghaviharsh ધર્મો રક્ષતિ રક્ષિત: જે ધર્મ ની રક્ષા કરેછે તેમની રક્ષા ધર્મકર છે, માન.મંત્રી શ્રી હર્ષ સંઘવી સાહેબે ચાતુરમાસ ની સાધુઓ ની અમદાવાદમા  પાલખીયાત્રામા જોડાઇ ને લોકોમા સંસ્કારને શ્રધાવધે તેમાટે પ્રેરણાદાયકધર્મનુ કાર્યકરવા બદલ ધન્યવાદ ઉધોગવીકાસ મંડળ રાજકોટ બીપીન સી ગઢીયા",
            "url": "https://twitter.com/879840665265258497/status/1675303898918055936",
            "publish_date": 1688258549,
            "created_date": 1688258549,
            "domain": "twitter.com",
            "topimage": "",
            "entities": [],
            "language": "en",
            "sentiment_v1": {
                "polarity": -66,
                "label": "negative",
                "confidence": 89
            },
            "metadata": {
                "username": "bipin38349109",
                "user_id": "879840665265258497",
                "quote_count": 0,
                "reply_count": 0,
                "retweet_count": 0,
                "favorite_count": 0,
                "in_reply_to_user_id": "879840665265258496",
                "is_retweet": False
            }
        }
    },
    {
        "transformed": {
            "id": 2,
            "author": "Flfawless",
            "text": "RT @infodrakor_id: Cast drama ENA #LiesHiddenInMyGarden: #KimTaeHee #LimJiYeon #KimSungOh #ChoiJaeRim untuk ELLE Thailand 📸💜\n\nDramanya slow…",
            "url": "https://twitter.com/1594348797047369728/status/1675303899337736199",
            "publish_date": 1688258549,
            "created_date": 1688258549,
            "domain": "twitter.com",
            "topimage": "",
            "entities": [],
            "language": "en",
            "sentiment_v1": {
                "polarity": 66,
                "label": "positive",
                "confidence": 23
            },
            "metadata": {
                "username": "Flfawless",
                "user_id": "1594348797047369728",
                "quote_count": 0,
                "reply_count": 0,
                "retweet_count": 0,
                "favorite_count": 0,
                "in_reply_to_user_id": "",
                "is_retweet": True
            }
        }
    },
    {
        "transformed": {
            "id": 3,
            "author": "GregMonroe54321",
            "text": "RT @BillSimmons: A 9-player 3-teamer that gets Dame to Philly and Harden to LAC….\n\nPort gets Maxey, Mann, Zubac + Tobias expiring + dumps N…",
            "url": "https://twitter.com/895287399005118465/status/1675303900595777536",
            "publish_date": 1688258550,
            "created_date": 1688258550,
            "domain": "twitter.com",
            "topimage": "",
            "entities": [],
            "language": "en",
            "sentiment_v1": {
                "polarity": 11,
                "label": "neutral",
                "confidence": 0
            },
            "metadata": {
                "username": "GregMonroe54321",
                "user_id": "895287399005118465",
                "quote_count": 0,
                "reply_count": 0,
                "retweet_count": 0,
                "favorite_count": 0,
                "in_reply_to_user_id": "",
                "is_retweet": True
            }
        }
    }
]


async def wait_for_os(os_provider, mention_id, os_index, timeout_seconds=30, polling_interval_seconds=1):
    """
    Continuously queries OS with the given parameters until a result is returned or the timeout is reached.

    :param os_provider: The OS provider instance
    :param mention_id: The mention ID to query
    :param os_index: The OS index to query
    :param timeout_seconds: The maximum number of seconds to wait before timing out
    :param polling_interval_seconds: The number of seconds to wait between queries
    :return: The result from the OS, or None if the query timed out
    """
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        result = os_provider.get(mention_id, os_index)
        if result is not None:
            return result
        await asyncio.sleep(polling_interval_seconds)
    return None


@pytest.mark.asyncio
async def test_os_writer():
    print("test_os_writer")
    '''
    SETUP
    - create social-mention-common messages
        - read messages from test data file
        - convert messages to protobuf object
    '''

    # tweets = json.load(open('data/twitter/twitter.json', 'r'))
    # convert tweet id to string
    for tweet in tweets:
        tweet["transformed"]["id"] = str(tweet["transformed"]["id"])

    social_mention_common = [data["transformed"] for data in tweets]

    social_mention_common_messages = [
        json_format.ParseDict(
            data["transformed"],
            SocialMentionCommon_pb2.SocialMentionCommon(),
            ignore_unknown_fields=False
        )
        for data in tweets
    ]

    '''
    EXECUTE
    - produce social-mention-common messages to Kafka topic
    - wait for messages to be processed by pipeline
    '''

    kafka_producer = KafkaProducer.instance(
        bootstrap_servers=Config.KAFKA_BROKERS_JSON,
        schema="core.social.SocialMentionCommon",
        schemaRegistryConfig=Config.SCHEMA_REGISTRY_CONFIG_JSON,
        topic=Config.KAFKA_TOPIC_DOWNSTREAM_SOCIAL
    )
    await kafka_producer.connect()

    # produce social-mention-common messages to Kafka topic
    for common in social_mention_common_messages:
        message = MessageToProduce(
            common.id,
            common
        )
        await kafka_producer.produce(message)

    '''
    ASSERT
    - assert that documents are in OS
    '''
    # initialize OS Provider
    os_provider = OSProvider.instance(
        host=Config.OS_CORE_CLUSTER_HOST
    )

    # assert os connection
    assert os_provider.check_connection()

    for mention in social_mention_common:
        mention["created"] = mention["created_date"]  # to match legacy schema
        os_index = os_provider.construct_index(mention)
        result = await wait_for_os(os_provider, mention["id"], os_index)
        assert result is not None, "Timed out waiting for OS to process mention[id]: " + mention["id"]
        print("result", result)
        assert result.get('_source').get('sentiment_v1').get(
            'polarity') == mention["sentiment_v1"]["polarity"] / 100
        assert result.get('_source').get('sentiment_v1').get(
            'confidence') == mention["sentiment_v1"]["confidence"] / 100
        assert len(result.get('_source').get('tags')) == 3
    await kafka_producer.disconnect()
