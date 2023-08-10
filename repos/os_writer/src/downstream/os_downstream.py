from typing import List

# Shared libs
from peakm.downstream.IDownstream import IDownstream, DownstreamMessage


class OSDownstream(IDownstream):
    def __init__(self, mapper) -> None:
        self.os_mapper = mapper

    async def connect(self):
        ...

    async def disconnect(self):
        ...

    def downstream(self, messages: List[DownstreamMessage]):
        '''
        Process kafka message with the following steps:
        1. Map common social mention schema to marty docs schema
        2. Write mapped message to OS

        params:
            message: Kafka message to process
        '''
        if not messages:
            return

        try:
            '''
            Transform message to marty docs schema

            NOTES: 
            - This code currently assumes message is a list of tweets in the common social mention schema

            TODO: Update this code to handle other social media types
            '''
            print("OSDownstream::downstream: downstream - messages", messages)
            mapped_data = [ self.os_mapper.map(m) for m in messages ]
            return mapped_data
        except Exception as e:
            print("Error occurred while transforming message")
            raise


