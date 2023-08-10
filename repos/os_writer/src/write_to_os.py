#!/usr/bin/env python
import asyncio
from typing import List

# Config
from config.os_writer_config import Config

# Shared libs
from peakm.consumer.KafkaConsumer import KafkaConsumer
from peakm.producer.KafkaProducer import KafkaProducer
from peakm.downstream.DownstreamPipeline import DownstreamPipeline

# Schema files
import peakm.proto.core.social.SocialMentionCommon_pb2 as SocialMentionCommon_pb2

# OS Writer custom dependencies
from downstream.os_downstream import OSDownstream
from db_providers.os_provider import OSProvider
from mappers.os_mapper import OSMapper

'''
OS Writer Downstream Pipeline

Consume from Kafka downstream-social topic,
Map common social media schema to marty docs schema,
Write to OS.
'''


async def main():
    pipeline = DownstreamPipeline(
        consumer=KafkaConsumer.instance(
            bootstrap_servers=Config.KAFKA_BROKERS_JSON,
            group_id="os-writer",
            topic=Config.KAFKA_TOPIC_DOWNSTREAM_SOCIAL,
            schemaRegistryConfig=Config.SCHEMA_REGISTRY_CONFIG_JSON,
            protobufModel=SocialMentionCommon_pb2.SocialMentionCommon,
            messages_in_flight=Config.MESSAGES_IN_FLIGHT_OS_WRITER,
            aws=Config.get_msk_credentials() if Config.KAFKA_AWS_CONFIG_JSON else None
        ),
        dlq=KafkaProducer.instance(
            bootstrap_servers=Config.KAFKA_BROKERS_JSON,
            schema="core.social.SocialMentionCommon",
            schemaRegistryConfig=Config.SCHEMA_REGISTRY_CONFIG_JSON,
            topic=Config.KAFKA_TOPIC_DOWNSTREAM_SOCIAL_DLQ,
            aws=Config.get_msk_credentials() if Config.KAFKA_AWS_CONFIG_JSON else None
        ),
        downstream_agent=OSDownstream(
            mapper=OSMapper()
        ),
        db_provider=OSProvider.instance(
            host=Config.OS_CORE_CLUSTER_HOST
        ),
        buffer_time=Config.BUFFER_TIME_OS_WRITER,
    )

    await pipeline.connect()
    await pipeline.downstream()

if __name__ == '__main__':
    asyncio.run(main())
