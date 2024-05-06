#!/usr/bin/env python3
""" Python function that inserts a new document
    in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """Returns the new _id after inserting a new document"""

    return mongo_collection.insert_one(kwargs).inserted_id
