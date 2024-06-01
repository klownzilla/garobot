import logging, time
import garobot as garobot_core
import shop as garobot_shop

class Scheduler():
    def __init__(self, garobot: garobot_core.Garobot, frequency: int) -> None:
        self.logger = logging.getLogger(__name__)
        self.garobot = garobot
        self.frequency = frequency
        self.watch_appointments()

    def watch_appointments(self) -> None:
        self.get_garobot().populate_appointments()
        self._set_best_appointment(self.get_garobot().determine_best_appointment())
        self.logger.info('Current best appointment:{}'.format(self._get_best_appointment()))

        while True:
            self.logger.info('Sleeping for {} seconds...'.format(self._get_frequency()))
            time.sleep(self._get_frequency())

            self.get_garobot().populate_appointments()
            best_appointment = self.get_garobot().determine_best_appointment()
            if best_appointment != self._get_best_appointment():
                self.logger.info('Setting new best appointment...')
                self._set_best_appointment(best_appointment)
            else:
                self.logger.info('Found no new best appointment...')

    def get_garobot(self) -> garobot_core.Garobot:
        return self.garobot
    
    def _get_best_appointment(self) -> garobot_shop.Appointment:
        return self.best_appointment

    def _set_best_appointment(self, best_appointment: garobot_shop.Appointment) -> None:
        self.best_appointment = best_appointment

    def _refresh_appointments(self) -> set[garobot_shop.Appointment]:
        appointment_set = set()
        return appointment_set
    
    def _get_frequency(self) -> int:
        return self.frequency