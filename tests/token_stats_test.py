import pytest
from datetime import date, datetime
from analyzers import AnalyzeTokens
import os

pytestmark = pytest.mark.usefixtures("spark")


def test_token_stat(spark):
    path = os.getcwd() + "/tests/fixtures/token_stats"
    start_date = date(2017, 1, 15)
    end_date = date(2017, 1, 16)

    analyzer = AnalyzeTokens(storage_path=path, start_date=start_date, end_date=end_date, spark_session=spark,
                             database=None, current_datetime=datetime(2017, 2, 15, 15, 10))

    files = analyzer.get_files_to_analyze()

    expected_files = [path + '/2017/01/15/token_stat.json.log', path + '/2017/01/16/token_stat.json.log']

    assert len(files) == len(expected_files)
    assert len(set(files) - set(expected_files)) == 0

    results = analyzer.get_data()
    expected_results = [(u'token:2', date(2017, 1, 15), 1),
                        (u'token:2', date(2017, 1, 16), 1),
                        (u'token:3', date(2017, 1, 15), 6),
                        (u'token:1', date(2017, 1, 15), 2),
                        (u'token:1', date(2017, 1, 16), 2)]
    
    assert len(results) == len(expected_results)
    assert results == expected_results
    assert analyzer.get_log_analyzer_stats(datetime(2017, 2, 15, 15, 12)) == \
           "[OK] [2017-02-15 15:12:00] [2017-02-15 15:10:00] [TokenStatsUpdater] [120]"


def test_token_stat_empty_file(spark):
    path = os.getcwd() + "/tests/fixtures/token_stats"
    start_date = date(2017, 1, 17)
    end_date = date(2017, 1, 17)
    analyzer = AnalyzeTokens(storage_path=path, start_date=start_date, end_date=end_date, spark_session=spark,
                             database=None)

    files = analyzer.get_files_to_analyze()
    expected_files = [path + '/2017/01/17/token_stat.json.log']
    assert len(files) == len(expected_files)
    results = analyzer.get_data()
    assert len(results) == 0
