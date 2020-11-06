semester_dict = {'2008-秋': 638, '2008-春': 636,
                 '2009-秋': 637, '2009-春': 643,
                 '2010-秋': 635, '2010-春': 639,
                 '2011-秋': 632, '2011-春': 628,
                 '2012-秋': 641, '2012-春': 629,
                 '2013-秋': 640, '2013-春': 645,
                 '2014-秋': 630, '2014-春': 634,
                 '2015-秋': 631, '2015-春': 623,
                 '2016-秋': 621, '2016-春': 624,
                 '2017-秋': 619, '2017-春': 625,
                 '2018-秋': 622, '2018-春': 633,
                 '2019-秋': 642, '2019-春': 620,
                 '2020-秋': 626, '2020-春': 627,
                 '2021-秋': 662, '2021-春': 663,
                 '2022-秋': 664, '2022-春': 665,
                 '2023-秋': 666, '2023-春': 667,
                 '2024-秋': 668}


def choose_semester_id(semester: str) -> int:
    import yaml
    import os
    APP_ABSOLUTE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # TODO App absolute directory
    with open(os.path.join(APP_ABSOLUTE_PATH, 'config.yaml')) as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
        default_semester = config['default']['semester']
        default_semester_id = semester_dict[default_semester]
    if semester not in semester_dict:
        return semester_dict['2024-秋']
    return semester_dict.get(semester, default_semester_id)
