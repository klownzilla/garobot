import logging, requests, json
from datetime import datetime
from core.shop import Appointment
from api.constants import WEBHOOK_URL, WEBHOOK_USERNAME, WEBHOOK_RGB_INT, WEBHOOK_NOTIFICATION_REF_LENGTH
from core.utils import *

logger = logging.getLogger(__name__)

class Notification:

    def notify_channel(self, appointment: Appointment) -> None:
        post_data = self._prepare_data(appointment)
        logger.info('Sending notification to channel...')
        webhook_response = requests.post(WEBHOOK_URL, json=post_data)
        try:
            webhook_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error(e)
            raise SystemExit(e)
        else:
            logger.info('Notification successfully sent!')

    def _prepare_data(self, appointment: Appointment) -> dict:
        appointment_dict = json.loads(str(appointment))
        webhook_description = 'Date: {}\nService: [${:2.2f}] {}\nEmployee: {}\nAppointment ID: {}'.format(
            appointment_dict['appointment_date_time'],
            appointment_dict['service']['service_price'],
            appointment_dict['service']['service_name'],
            appointment_dict['employee']['employee_name'],
            appointment_dict['appointment_id']
        )
        post_data = {
            'username':WEBHOOK_USERNAME,
            'embeds':[
                {
                    'description':webhook_description,
                    'title':'**Found new best appointment!**',
                    'color':WEBHOOK_RGB_INT,
                    'footer':{
                        'text':'Notificaton sent on {}\nNotif. Ref.: {}'.format(
                            datetime.now().strftime('%a %b %d %H:%M:%S %Y'),
                            generate_unique_id(WEBHOOK_NOTIFICATION_REF_LENGTH)
                            )
                    }
                }
            ]
        }
        return post_data