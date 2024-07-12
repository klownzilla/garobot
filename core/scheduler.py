import logging, time
from core.garobot import Garobot
from core.shop import Appointment
from api.notification import Notification
from core.constants import FREQUENCY, FREQUENCY_VARIATION
from core.utils import generate_frequency_variation

logger = logging.getLogger(__name__)

class Scheduler:
    def __init__(self, garobot: Garobot) -> None:
        self.garobot = garobot
        self.frequency = FREQUENCY
        self.frequency_variation = FREQUENCY_VARIATION
        self.notification_service = Notification()
        self._watch_appointments()

    def _watch_appointments(self) -> None:
        first = True
        while True:
            found_appointment = self._get_garobot().populate_appointments()
            if found_appointment:
                best_appointment = self._get_garobot().determine_best_appointment()
                if first or best_appointment != self._get_best_appointment():
                    first = False
                    logger.info('Found new best appointment!')
                    self._set_best_appointment(best_appointment)
                    logger.info('{}'.format(self._get_best_appointment()))
                    self._get_notification_service().notify_channel(self._get_best_appointment())
            else:
                logger.info('Keeping appointment...')
                logger.info('{}'.format(self._get_best_appointment()))

            try:
                generated_frequency_variation = generate_frequency_variation(self._get_frequency_variation())
                logger.info('Sleeping for {} seconds...'.format(self._get_frequency() + generated_frequency_variation))
                time.sleep(self._get_frequency() + generated_frequency_variation)
                logger.info('Done sleeping!')
            except KeyboardInterrupt:
                logger.info('Keyboard interrupt! Exiting...')
                self._get_garobot().get_api().close_session()
                raise SystemExit()

    def _get_garobot(self) -> Garobot:
        return self.garobot
    
    def _get_notification_service(self) -> Notification:
        return self.notification_service
    
    def _get_best_appointment(self) -> Appointment:
        return self.best_appointment

    def _set_best_appointment(self, best_appointment: Appointment) -> None:
        self.best_appointment = best_appointment
    
    def _get_frequency(self) -> int:
        return self.frequency
    
    def _get_frequency_variation(self) -> int:
        return self.frequency_variation