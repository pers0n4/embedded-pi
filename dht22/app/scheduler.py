import logging

from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session

from .models import Record

logger = logging.getLogger("apscheduler")


try:
    import adafruit_dht
    import board
except Exception as error:
    logger.error(str(error))


class Scheduler:
    def __init__(self, engine):
        self.engine = engine
        self.scheduler = BackgroundScheduler()
        self.device = adafruit_dht.DHT22(board.D18)

        self.scheduler.add_job(self.store_dht, "interval", seconds=2)

    def store_dht(self):
        data = Record.parse_obj(self.read_dht())
        with Session(self.engine) as session:
            session.add(data)
            session.commit()

    def read_dht(self):
        try:
            temperature = self.device.temperature
            humidity = self.device.humidity
            return {
                "temperature": temperature,
                "humidity": humidity,
            }
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        except Exception as error:
            self.device.exit()
            raise error

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()
