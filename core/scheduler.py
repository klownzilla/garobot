import logging, time
from core.garobot import Garobot
from core.shop import Appointment
from core.webhook import Webhook

class Scheduler:
    def __init__(self, garobot: Garobot, frequency: int) -> None:
        self.logger = logging.getLogger(__name__)
        self.garobot = garobot
        self.frequency = frequency
        self._watch_appointments()

    def _watch_appointments(self) -> None:
        first = True
        while True:
            found_appointment = self._get_garobot().populate_appointments()
            if found_appointment:
                best_appointment = self._get_garobot().determine_best_appointment()
                if first or best_appointment != self._get_best_appointment():
                    first = False
                    self.logger.info('Found new best appointment!')
                    self._set_best_appointment(best_appointment)
                    self.logger.info('{}'.format(self._get_best_appointment()))
                    Webhook().notify_channel(self._get_best_appointment())
            else:
                self.logger.info('Keeping appointment...')
                self.logger.info('{}'.format(self._get_best_appointment()))

            try:
                self.logger.info('Sleeping for {} seconds...'.format(self._get_frequency()))
                time.sleep(self._get_frequency())
                self.logger.info('Done sleeping!')
            except KeyboardInterrupt:
                self.logger.info('Keyboard interrupt! Exiting...')
                self._get_garobot().get_api().close_session()
                raise SystemExit()

    def _get_garobot(self) -> Garobot:
        return self.garobot
    
    def _get_best_appointment(self) -> Appointment:
        return self.best_appointment

    def _set_best_appointment(self, best_appointment: Appointment) -> None:
        self.best_appointment = best_appointment
    
    def _get_frequency(self) -> int:
        return self.frequency