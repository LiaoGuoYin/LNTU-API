from app import schemas
from app.education import core
from app.quality import core as quality_core
from app.constants import constantsShared


def refresh_helper_message() -> schemas.HelperMessage:
    helper_message = schemas.HelperMessage(
        notice=constantsShared.config.message,
        semester=constantsShared.current_semester,
        week=constantsShared.current_week,
    )
    helper_message.educationServerStatus = '正常' if core.is_education_online() else '离线'
    helper_message.qualityServerStatus = '正常' if quality_core.is_quality_online() else '离线'
    helper_message.helperServerStatus = '正常'
    return helper_message
