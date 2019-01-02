import json
import logging
import os.path
import re
import requests

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
op_file = os.path.abspath('./merged_results.json')
as_file = os.path.abspath('./app_store/data/app_store_results.json')
ps_file = os.path.abspath('./play_store/data/play_store_results.json')

merged_dict = {}


def main():
    parse_app_store_results()
    parse_play_store_results()
    closed()


def parse_app_store_results():
    with open(as_file, 'r') as f:
        app_store = json.load(f)

    for obj in app_store['results']:
        app_name = obj['appName']

        item = {
            'agencyFullName': obj['agencyFullName'],
            'appStore': {
                'appViewUrl': obj['appViewUrl'],
                'developerViewUrl': obj['developerViewUrl'],
                'averageUserRating': obj['averageUserRating'],
                'userRatingCount': obj['userRatingCount']
            }
        }

        merged_dict[app_name] = item


def parse_play_store_results():
    with open(ps_file, 'r') as f:
        play_store = json.load(f)

    for obj in play_store['results']:
        app_name = obj['appName']

        item = {
            'agencyFullName': obj['agencyFullName'],
            'playStore': {
                'appViewUrl': obj['appViewUrl'],
                'developerViewUrl': obj['developerViewUrl'],
                'averageUserRating': obj['averageUserRating'],
                'userRatingCount': obj['userRatingCount']
            }
        }

        if app_name in merged_dict:
            merged_dict[app_name].update(item)
        else:
            merged_dict[app_name] = item


def closed():
    merged = {
        'results': [],
        'resultCount': 0,
    }

    for k, v in merged_dict.iteritems():
        item = {
            'appName': k,
        }

        item.update(v)
        merged['results'].append(item)

    merged['resultCount'] = len(merged_dict)

    with open(op_file, 'w') as f:
        f.write(json.dumps(merged))

        logging.info('Saved file %s' % op_file)


if __name__ == '__main__':
    main()