# ReadMe

## Quick Start

To get started with this project, follow the steps below:

### Step 1: Installation

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.

### Step 2: Configuration

1. Open the `config.py` file and update the necessary configuration variables according to your environment.
2. Make sure to provide the correct Kafka brokers and topics, schema registry configuration, and S3 bucket information.

### Step 3: Database Setup

1. Run the following command to set up the database tables:

   ```
   python manage.py db upgrade
   ```

### Step 4: Running the Pipeline

1. Open the `main.py` file and update the necessary pipeline configurations according to your needs.
2. Run the following command to start the pipeline:

   ```
   python main.py
   ```

### Step 5: Testing

1. To run the tests, use the following command:

   ```
   python -m pytest
   ```

## Additional Information

- The project uses SQLAlchemy as the ORM for interacting with the database. The `Doc` model represents a table in the database with various columns.
- The `test_MartydocsProvider` function tests the functionality of the `MartydocsProvider` class, which interacts with the database to insert and retrieve records.
- The `test_TwitterMapper` function tests the functionality of the `TwitterMapper` class, which transforms raw Twitter data into a common schema.
- The project includes a `S3ParquetWriter` class for writing Parquet files to an S3 bucket.
- The project includes a `S3Provider` class for interacting with an S3 bucket.
- The `main` function sets up the pipeline using the provided configurations.

Please refer to the code and comments for more detailed information about each component and its functionality.