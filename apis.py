import json
import logging
import os
import subprocess
from tempfile import NamedTemporaryFile

from flask import make_response, current_app
from flask_restplus import Namespace, Resource

from domain.portfolioSuggestor import Sector

logger = logging.getLogger(__name__)


portfolio = Namespace('portfolio', __name__)


def matrix_loader(data):
    result = {}
    methods = [item for item in data[1].split(' ') if len(item) > 0]
    for row in data[2:-1]:
        row = [item for item in row.split(' ') if len(item) > 0]
        result[row[0]] = {}
        for i in range(1, len(row)):
            result[row[0]][methods[i - 1]] = eval(row[i])
        for (key, value) in result.items():
            result[key]['averse'] = (0.2 * result[key]['maxdec'] + 0.25 * (result[key]['ercp'] + result[key]['mvol']) +
                                     0.2 * result[key]['EW'] + 0.1 * result[key]['maxsharpe']) / 5
            result[key]['moderate'] = sum(value.values()) / len(value)
            result[key]['aggressive'] = (0.6 * result[key]['maxsharpe'] + 0.1 * (result[key]['maxdec'] +
                                                                               result[key]['ercp'] + result[key]['mvol']
                                                                               + result[key]['EW']))

    return json.dumps(result)


@portfolio.route('')
class Portfolio(Resource):
    @staticmethod
    def get():
        main = current_app.main
        fin_cnt = 3
        non_fin_cnt = 7
        main.select(fin_cnt, Sector.FINANCIAL)
        main.select(non_fin_cnt, Sector.NON_FINANCIAL)
        f = NamedTemporaryFile()
        f.name = f'{f.name}.csv'
        r_file = os.path.join(os.getcwd(), "domain\\service\\porfolio.r")
        main.save_returns_matrix_to_csv(f.name)
        res = subprocess.check_output(f'"C:\\Program Files\\R\\R-3.6.0\\bin\\Rscript.exe" "{r_file}" "{f.name}"',
                                      shell=True)
        main.reset()
        return make_response(matrix_loader(res.decode('utf-8').split('\r\n')))
