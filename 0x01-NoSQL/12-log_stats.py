#!/usr/bin/env python3
"""
Aggregation operations
"""
from pymongo import MongoClient
from typing import Tuple


def get_nginx_stats() -> Tuple:
    """
    Queries nginx collection for specific data
    - Returns:
        - count of all documents
        - count of each method in the collection
        - count of each GET calls to /status path
    """
    client: MongoClient = MongoClient()
    db = client.logs
    collection = db.nginx
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    method_stats = []
    for method in methods:
        method_count = collection.count_documents({'method': method})
        method_stats.append({'method': method, 'count': method_count})
    doc_count = collection.estimated_document_count()
    status_path_stats = collection.count_documents({'method': 'GET',
                                                    'path': '/status'})
    client.close()
    return doc_count, method_stats, status_path_stats


def print_nginx_stats() -> None:
    """
    Prints stats from nginx query
    """
    doc_count, method_stats, status_path_stats = get_nginx_stats()
    print(f'{doc_count} logs')
    print('Methods:')
    for method in method_stats:
        print(f'\tmethod {method.get("method")}: {method.get("count")}')
    print(f'{status_path_stats} status check')


if __name__ == '__main__':
    print_nginx_stats()
