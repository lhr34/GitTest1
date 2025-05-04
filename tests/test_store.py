import os
import tempfile
from app.data_store import append_log, read_logs


def test_log_operations():
    with tempfile.TemporaryDirectory() as tmpdir:

        os.environ['LOG_FILE'] = os.path.join(tmpdir, "test_log.csv")

        test_data = {'timestamp': '2023-01-01T12:00:00', 'PowerSensor': 250,
                     'TemperatureSensor': 22, 'HumiditySensor': 60, 'LightSensor': 500}
        append_log(test_data)

        logs = read_logs()
        assert len(logs) == 1
        assert logs[0]['PowerSensor'] == '250'

