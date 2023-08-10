# DB
import datetime
import json

from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk


class OSProvider:
    def __init__(self, os):
        self.os = os
        self.owner = "7166c64f-418b-4424-b53c-b8fb7855a352"

    @staticmethod
    def instance(host):
        os = OpenSearch(hosts=host)
        return OSProvider(
            os=os
        )

    def write(self, documents):
        try:
            bulk_actions = self.construct_bulk_actions(documents)
            success, errors = bulk(self.os, bulk_actions)
            if len(bulk_actions) == success:
                print(f'Successfully indexed {success} documents')
            else:
                print(f'Failed to index {len(errors)} documents')
                for error in errors:
                    print(error)
                raise Exception(errors)

        except Exception as e:
            print("Indexing failed:", e)
            raise e

    def construct_bulk_actions(self, documents):
        actions = []
        for doc in documents:
            if "id" not in doc:
                continue

            index = self.construct_index(doc)

            action = {
                "_op_type": "update",
                "_index": index,
                "_id": doc["id"],
                "doc": doc,
                "doc_as_upsert": True
            }

            actions.append(action)

        return actions

    def construct_index(self, doc):
        dt_object = datetime.datetime.fromtimestamp(doc["created"])
        formatted_date = dt_object.strftime("%Y-%m")

        index = f"doc_{formatted_date}_{self.owner}"
        print('Indexing to:', index)
        return index

    def get(self, id, index):
        try:
            res = self.os.get(index=index, id=id)
            return res
        except Exception as e:
            print("Get failed:", e)
            return None

    def check_connection(self):
        try:
            return self.os.ping()
        except Exception as e:
            print("Connection failed:", e)
            return False
