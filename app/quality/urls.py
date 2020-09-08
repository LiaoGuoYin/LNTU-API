from enum import Enum


class QualityExpansionURLEnum(Enum):
    URL_ROOT = 'http://202.199.224.19:8080'

    LOGIN = URL_ROOT + '/'
    INFO = URL_ROOT + '/SutuoSoft_htgl/Student/XSGL_xsxx_view.aspx'
    REPORT = URL_ROOT + '/SutuoSoft_htgl/Student/XSGL_grcjd.aspx'

    SCHOLARSHIP = URL_ROOT + '/SutuoSoft_htgl/Student/jxjsqb/sqb2017.aspx'  # TODO

    MIND = URL_ROOT + '/SutuoSoft_htgl/Student/HDJL_ztsxjyhd_index.aspx'
    COMPETITION = URL_ROOT + '/SutuoSoft_htgl/Student/HDJL_xskydclw_index.aspx'
    SOCIAL = URL_ROOT + '/SutuoSoft_htgl/Student/HDJL_shsjzysj_index.aspx'
    READING = URL_ROOT + '/SutuoSoft_htgl/Student/HDJL_pdjdzzdhg_index.aspx'
    EMPLOYMENT = URL_ROOT + '/SutuoSoft_htgl/Student/HDJL_xsgbrz_index.aspx'
    SKILL = URL_ROOT + '/SutuoSoft_htgl/Student/HDJL_jinengrenzheng_index.aspx'

    @classmethod
    def get_activity(self):
        return {
            'mind': self.MIND,
            'competition': self.COMPETITION,
            'social': self.SOCIAL,
            'reading': self.READING,
            'employment': self.EMPLOYMENT,
            'skill': self.SKILL,
        }
