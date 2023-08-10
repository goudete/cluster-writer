
import json
import pytest
from unittest.mock import patch

from peakm.consumer.KafkaConsumer import MessageToConsume
from downstream.os_downstream import OSDownstream


def generate_test_data():
    '''
    Generate test data to send to OSDownstream
    '''
    # Read message from test data file
    test_data = json.load(open('data/twitter/twitter.json', 'r'))

    transformed_data = [data.get('transformed') for data in test_data]
    messages = [MessageToConsume(future=None, message=m) for m in transformed_data]

    return messages

@pytest.mark.asyncio
async def test_os_downstream():
    '''
    Validate that OSDownstream can take a list of common schema tweets,
    transform them to marty docs schema,
    and write them to OS
    '''

    # Mock test data
    mock_message_buffer = generate_test_data()

    # Mock OS related classes and their methods
    with patch('downstream.os_downstream') as MockOSMapper:

        # Mock the map method to return the same input
        instance_os_mapper = MockOSMapper.return_value
        instance_os_mapper.map.side_effect = lambda x: x

        # Instantiate OSDownstream
        downstream_agent=OSDownstream(mapper=instance_os_mapper)

        # Test connect
        await downstream_agent.connect()

        # Test process
        downstream_agent.downstream(mock_message_buffer)

        # Check if the map method was called for each item in buffer
        assert instance_os_mapper.map.call_count == len(mock_message_buffer)

@pytest.mark.asyncio
async def test_os_downstream_empty_message():
    '''
    Validate that the OSDownstream gracefully handles empty messages
    '''
    mock_message_buffer = []
    # Mock OS related classes and their methods
    with patch('downstream.os_downstream') as MockOSMapper:

        # Mock the map method to return the same input
        instance_os_mapper = MockOSMapper.return_value
        instance_os_mapper.map.side_effect = lambda x: x

        # Instantiate OSDownstream
        downstream_agent = OSDownstream(mapper=instance_os_mapper)

        # Test connect
        await downstream_agent.connect()

        # Test process
        downstream_agent.downstream(mock_message_buffer)

        assert downstream_agent.downstream(mock_message_buffer) is None