from enum import Enum


class AIPAOURLEnum(Enum):
    ROOT_URL = 'http://client3.aipao.me'

    CHECK_IMEI_CODE_URL = ROOT_URL + '/api/%7Btoken%7D/QM_Users/Login_AndroidSchool'

    VALID_URL = ROOT_URL + '/api/%7Btoken%7D/QM_Runs/getResultsofValidByUser'
    INVALID_URL = ROOT_URL + '/api/%7Btoken%7D/QM_Runs/getResultsofInValidByUser'

    GET_STU_REGULATION_URL = ROOT_URL + '/api/{token}/QM_Users/GS'
    START_RUN_URL = ROOT_URL + '/api/{token}/QM_Runs/SRS'
    FINISHED_RUN_URL = ROOT_URL + '/api/{token}/QM_Runs/ES'

    def __str__(self):
        return self.value
