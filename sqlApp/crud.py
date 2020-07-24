from sqlalchemy.orm import Session

from modelset import schemas, models


def create_user(db: Session, user: schemas.User):
    q = db.query(models.User).filter(models.User.username == user.username).first()
    if q is None:
        newUser = models.User(username=user.username, password=user.password)
    else:
        newUser = q
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser


def get_user_grades(db: Session, user: schemas.User):
    # username TODO
    print(models.User.grades)
    grades = db.query(models.Grade).filter(models.Grade.owner.username == user.username).all()
    return grades


def create_grade(db: Session, grades: schemas.Grade, user: schemas.User):
    newGrade = models.Grade(**grades.dict())
    newGrade.ownerUsername = user.username
    db.add(newGrade)
    db.commit()
    db.refresh(newGrade)
    return newGrade


def create_notice(db: Session, notice: schemas.Notice):
    oldNotice = db.query(models.Notice).filter_by(url=notice.url).first()
    if oldNotice is None:
        newNotice = models.Notice(**notice.dict())
        newNotice.appendix = str(newNotice.appendix)
    else:
        newNotice = oldNotice
    db.add(newNotice)
    db.flush()
    db.commit()
    db.refresh(newNotice)
    return newNotice


def get_notice(db: Session, skip: int = 0, limit=50):
    notices = db.query(models.Notice).order_by(models.Notice.date).offset(skip).limit(limit).all()
    return notices
