def gpa_util(grade_list) -> dict:
    # TODO bug，重修有学分折半
    """GPA计算规则:
        "二级制: 合格(85),不合格(0)"
        "五级制: 优秀(95),良(85),中(75),及格(65),不及格(0)"
    """
    results = {"gradePointAverage": 0,
               "weightedAverage": 0,
               "scoreTotal": 0,
               "creditTotal": 0,
               "gradePointTotal": 0,
               "courseCount": 0,
               }
    rule_dict = {"合格": 85, "不合格": 0,
                 "优秀": 95, "良": 85, "中": 75, "及格": 65, "不及格": 0}
    for grade in grade_list:
        # 分数等级置换
        print(F"{grade.name}：{grade.score} ", end='')
        grade.score = rule_dict.get(grade.score, grade.score)
        if grade.score:
            print(F" -> {grade.score}")
        else:
            print(F" None -> {grade.score}(异常)")
            continue

        # 计算GPA
        point = float(grade.score)
        grade.credit = float(grade.credit)
        results['courseCount'] += 1
        results['creditTotal'] += grade.credit
        results['scoreTotal'] += point * grade.credit

        # 计算学分绩
        if 95 <= point <= 100:
            results['gradePointTotal'] += grade.credit * 4.5
        elif 90 <= point < 95:
            results['gradePointTotal'] += grade.credit * 4.0
        elif 85 <= point < 90:
            results['gradePointTotal'] += grade.credit * 3.5
        elif 80 <= point < 85:
            results['gradePointTotal'] += grade.credit * 3.0
        elif 75 <= point < 80:
            results['gradePointTotal'] += grade.credit * 2.5
        elif 70 <= point < 75:
            results['gradePointTotal'] += grade.credit * 2.0
        elif 65 <= point < 70:
            results['gradePointTotal'] += grade.credit * 1.5
        elif 60 <= point < 65:
            results['gradePointTotal'] += grade.credit * 1.0
        else:
            results['gradePointTotal'] += 0

    if results['courseCount'] == 0:
        return {}

    # 计算平均学分绩 GPA
    results['gradePointAverage'] = round(results['gradePointTotal'] / results['creditTotal'], 4)  # 绩点
    results['weightedAverage'] = round(results['scoreTotal'] / results['creditTotal'], 4)  # 加权平均分
    return results
