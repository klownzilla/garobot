# Base URL
BASE_URL = 'https://www.vagaro.com/'

# HIT ME
# Site wide API
API_URL = 'https://www.vagaro.com/us04/websiteapi/homepage/'

# FOR BOT CHECK
# Mock a browser to bypass bot detection
HEADER = {
        'Content-Type':'application/json; charset=utf-8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
}

# API endpoint definitions
ENDPOINTS = {
    'get_bookings':'getonlinebookingtabdetail',
    'get_appointments':'getavailablemultiappointments'
}

# Hidden HTML class id which contains business id
BUSINESS_ID_CLASS_ID = 'hdnSiteBuilderBusinessID'

# Discord webhook URL
WEBHOOK_URL = '[webhook here]'

# Discord bot username
WEBHOOK_USERNAME = 'garobot_py_bot'

# RGB in int representation of webhook embed
WEBHOOK_RGB_INT = 13387588

# Length of webhook notification reference
WEBHOOK_NOTIFICATION_REF_LENGTH = 16