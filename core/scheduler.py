import logging, time
from core.garobot import Garobot
from core.shop import Appointment

class Scheduler:
    def __init__(self, garobot: Garobot, frequency: int) -> None:
        self.logger = logging.getLogger(__name__)
        self.garobot = garobot
        self.frequency = frequency
        self.watch_appointments()

    def watch_appointments(self) -> None:
        self._get_garobot().populate_appointments()
        self._set_best_appointment(self._get_garobot().determine_best_appointment())
        self.logger.info('Current best appointment...')
        self.logger.info('{}'.format(self._get_best_appointment()))

        while True:
            self.logger.info('Sleeping for {} seconds...'.format(self._get_frequency()))
            time.sleep(self._get_frequency())

            self._get_garobot().populate_appointments()
            best_appointment = self._get_garobot().determine_best_appointment()
            if best_appointment != self._get_best_appointment():
                self.logger.info('Setting new best appointment...')
                self._set_best_appointment(best_appointment)
            else:
                self.logger.info('Found no new best appointment...')

    def _get_garobot(self) -> Garobot:
        return self.garobot
    
    def _get_best_appointment(self) -> Appointment:
        return self.best_appointment

    def _set_best_appointment(self, best_appointment: Appointment) -> None:
        self.best_appointment = best_appointment
    
    def _get_frequency(self) -> int:
        return self.frequency