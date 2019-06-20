import logging
import sys
from datetime import datetime

from flask import Flask
from flask_cors import CORS
from flask_restplus import Api

from apis import portfolio
from domain.portfolioSuggestor import Suggestor


def set_up_logger():
    log_formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)-5.5s]  %(message)s")
    root_logger = logging.getLogger()

    file_handler = logging.FileHandler(f'logs\\portfolioTrader.{datetime.now().strftime("%Y-%m-%d.%H.%M.%S")}.log')
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)


def dispatch_for_main():
    pass


if __name__ == '__main__':
    set_up_logger()
    logger = logging.getLogger(__name__)
    logger.info("Start Flask Application")
    app = Flask(__name__)
    app.main = Suggestor()
    CORS(app)
    api = Api(app)
    api.add_namespace(portfolio)
    app.run()
