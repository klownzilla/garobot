def get_shop_booking_data(business_id: int) -> dict:
    post_data = {
        'businessID':business_id,
        'shouldIncludePakcage':'True',
        'IsRequestFromOnBoarding':False,
        'loadClasses_Service_Both':False,
        'IsNewWebsiteBuilder':False,
        'IncludededClassId':'',
        'ExcludededClassId':'',
        'IsAllowAllLocation':False
    }
    return post_data

def get_shop_appointment_data(business_id: int, service_id: int, employee_id: int) -> dict:
    post_data = {
        'lAppointmentID':'',
        'businessID':str(business_id),
        'csvServiceID':str(service_id),
        'csvSPID':str(employee_id),
        'AppDate':'Fri May-10-2024',
        'StyleID':None,
        'isPublic':True,
        'isOutcallAppointment':False,
        'strCurrencySymbol':'$',
        'IsFromWidgetPage':'False',
        'isFromShopAdmin':False,
        'isMoveBack':False,
        'BusinessPackageID':0,
        'PromotionID':'',
        'TIME_ZONE':-6,
        'CUSTOM_DAY_LIGHT_SAVING':True,
        'DAY_LIGHT_SAVING':'Y',
        'CountryID':1,
        'CustomerTimezone':-6,
        'Customerzoneid':'',
        'CustomerCulture':'1',
        'CustIsDayLightSaving':True
    }
    return post_data