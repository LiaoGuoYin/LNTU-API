from api.models import Score


def calculateGPA(user, semester="2018秋"):
    # TODO 有bug，重修有学分折半
    """GPA计算规则不同：
    2016级：
        "二级制: 合格(85),不合格(0)"
        "五级制: 优秀(94),良(84),中(74),及格(64),不及格(0)"
    2017级及其以后：
        "二级制: 合格(85),不合格(0)"
        "五级制: 优秀(95),良(85),中(75),及格(65),不及格(0)"
    """
    results = {"GPA": 0,
               "WAM": 0,
               "count": 0,
               "score_total": 0,
               "credit_total": 0,
               "grade_point_total": 0,
               }
    rules_2016 = {"合格": 74, "不合格": 0, "": 0,  # 异常成绩重置为0
                  "优秀": 94, "良": 84, "中": 74, "及格": 64, "不及格": 0}
    rules_2017 = {"合格": 85, "不合格": 0, "": 0,
                  "优秀": 95, "良": 85, "中": 75, "及格": 65, "不及格": 0}
    if user.username[:2] in ('17', '18', '19'):  # 判断年级
        rules = rules_2017
        print('2017')
    else:
        rules = rules_2016
        print('2016')
    scores = Score.objects.filter(username=user, semester=semester)
    scores = Score.objects.filter(username=user)
    for each in scores:
        each.scores = rules.get(each.scores, each.scores)
        if each.scores:
            print(F"{each.name}：{each.scores} -> {each.scores}")
        else:
            print(F"{each.name}: None -> {each.scores}(异常)")
            continue

        # 计算GPA
        results['count'] += 1
        point = float(each.scores)
        results['credit_total'] += each.credit
        results['score_total'] += point * each.credit
        if 95 <= point <= 100:
            results['grade_point_total'] += each.credit * 4.5
        elif point >= 90:
            results['grade_point_total'] += each.credit * 4.0
        elif point >= 85:
            results['grade_point_total'] += each.credit * 3.5
        elif point >= 80:
            results['grade_point_total'] += each.credit * 3.0
        elif point >= 75:
            results['grade_point_total'] += each.credit * 2.5
        elif point >= 70:
            results['grade_point_total'] += each.credit * 2.0
        elif point >= 65:
            results['grade_point_total'] += each.credit * 1.5
        elif point >= 60:
            results['grade_point_total'] += each.credit * 1.0
        else:
            results['grade_point_total'] += 0

    if results['count'] == 0:
        return
    results['GPA'] = round(results['grade_point_total'] / results['credit_total'], 4)  # 绩点
    results['WAM'] = round(results['score_total'] / results['credit_total'], 4)  # 加权平均分
    print(results)
    return results['GPA']
