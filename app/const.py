semester_dict = {'2008-1': 638, '2008-2': 636,
                 '2009-1': 637, '2009-2': 643,
                 '2010-1': 635, '2010-2': 639,
                 '2011-1': 632, '2011-2': 628,
                 '2012-1': 641, '2012-2': 629,
                 '2013-1': 640, '2013-2': 645,
                 '2014-1': 630, '2014-2': 634,
                 '2015-1': 631, '2015-2': 623,
                 '2016-1': 621, '2016-2': 624,
                 '2017-1': 619, '2017-2': 625,
                 '2018-1': 622, '2018-2': 633,
                 '2019-1': 642, '2019-2': 620,
                 '2020-1': 626, '2020-2': 627,
                 '2021-1': 662, '2021-2': 663,
                 '2022-1': 664, '2022-2': 665,
                 '2023-1': 666, '2023-2': 667,
                 '2024-1': 668}


def choose_semester_id(semester: str) -> int:
    import yaml
    import os
    APP_ABSOLUTE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # TODO App absolute directory
    with open(f'{APP_ABSOLUTE_PATH}/config.yaml') as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
        default_semester = config['default']['semester']
        default_semester_id = semester_dict[default_semester]
    if semester not in semester_dict:
        return semester_dict['2024-1']
    return semester_dict.get(semester, default_semester_id)
