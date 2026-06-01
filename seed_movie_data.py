import utils
import pandas as pd
from weaviate.util import generate_uuid5
from weaviate.classes.data import DataObject, DataReference


CSV_PATH = "data/movies_data.csv"

INSERT_MOVIES = True

def clean(value):
    return None if pd.isna(value) else value


def as_int(value):
    value = clean(value)
    return None if value is None else int(value)


def as_float(value):
    value = clean(value)
    return None if value is None else float(value)


def insert_many_or_print_errors(collection, objects, label):
    if not objects:
        print(f"No {label} objects to insert.")
        return

    response = collection.data.insert_many(objects)

    if response.has_errors:
        print(f"Some {label} objects failed to insert:")
        print(response.errors)
    else:
        print(f"Inserted {len(response.uuids)} {label} objects")