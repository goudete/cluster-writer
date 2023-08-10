# Project Quick Start Guide

This guide will walk you through the steps to set up and run the project. Please follow the instructions below to get started.

## Prerequisites
Before you begin, make sure you have the following installed on your machine:
- Python 3.8 or higher
- Kafka
- Protobuf compiler (protoc)

## Installation
1. Clone the project repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment for the project:
   ```
   python3 -m venv env
   ```
4. Activate the virtual environment:
   - For Windows:
     ```
     .\env\Scripts\activate
     ```
   - For Unix/Linux:
     ```
     source env/bin/activate
     ```
5. Install the project dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration
1. Open the `config/os_writer_config.py` file.
2. Modify the configuration variables according to your environment.
3. Save and close the file.

## Running the Project
1. Start the Kafka server.
2. Generate the protobuf classes by running the following command:
   ```
   protoc -I=peakm/proto/core/social --python_out=. peakm/proto/core/social/SocialMentionCommon.proto
   ```
3. Run the project using the following command:
   ```
   python main.py
   ```

## Testing the Project
1. Make sure the Kafka server is running.
2. Run the tests using the following command:
   ```
   pytest
   ```

## Troubleshooting
If you encounter any issues while setting up or running the project, please refer to the project documentation or consult the project team for assistance. 