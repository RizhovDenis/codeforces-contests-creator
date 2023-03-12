import click


@click.group(name='parser')
def parser_group():
    """ Parser service """


@parser_group.command(name='run')
def parse_codeforces_problems():
    import time
    import requests

    from datetime import datetime, timedelta
    from settings import proj_conf

    from apps.parser.utils.logic import parsing_pages

    interval = datetime.utcnow()
    time_expired = interval

    while True:
        if interval < time_expired:
            time.sleep(proj_conf.parsing_frequency // 10)
            interval = datetime.utcnow()
            continue

        req = requests.get(url=proj_conf.codeforce_url)

        while req.status_code != 200:
            req = requests.get(url=proj_conf.codeforce_url)

        parsing_pages(page=req.text)

        interval = interval + timedelta(seconds=proj_conf.parsing_frequency)
        time_expired = interval + timedelta(seconds=proj_conf.parsing_frequency)
