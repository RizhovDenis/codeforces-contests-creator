import os


class Config:

    db_name = os.environ.get('DB_NAME', 'codeforces')
    db_user = os.environ.get('DB_USER', 'postgres')
    db_password = os.environ.get('DB_PASSWORD', 'postgres')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', 5432)

    parsing_frequency: int = 3600
    num_problems_in_contest: int = 10
    parsing_source: str = 'https://codeforces.com'

    telegram_token: str = 'set_your_token'

    @property
    def alchemy_url(self):
        return f'postgresql+psycopg2://{self.db_user}:{self.db_password}@' \
               f'{self.db_host}:{self.db_port}/{self.db_name}'

    @property
    def codeforce_url(self):
        return 'https://codeforces.com/problemset?order=BY_SOLVED_DESC'


proj_conf = Config()
