# -*- coding: utf-8 -*-

import requests

from ziggurat_cms.celery import celery


@celery.task
def test_task(subreddit, dt, d, td):
    print('task started', subreddit, dt, d, td)
    result = requests.get('https://www.reddit.com/r/{}.json'.format(subreddit))
    if result.status_code == requests.codes.ok:
        data = result.json()
        print(data)
    else:
        print(result)
