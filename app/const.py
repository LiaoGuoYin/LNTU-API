from app import exceptions

semester_dict = {'2008-秋': 636, '2009-春': 637,
                 '2009-秋': 643, '2010-春': 635,
                 '2010-秋': 639, '2011-春': 632,
                 '2011-秋': 628, '2012-春': 641,
                 '2012-秋': 629, '2013-春': 640,
                 '2013-秋': 645, '2014-春': 630,
                 '2014-秋': 634, '2015-春': 631,
                 '2015-秋': 623, '2016-春': 621,
                 '2016-秋': 624, '2017-春': 619,
                 '2017-秋': 625, '2018-春': 622,
                 '2018-秋': 633, '2019-春': 642,
                 '2019-秋': 620, '2020-春': 626,
                 '2020-秋': 627, '2021-春': 662,
                 '2021-秋': 663, '2022-春': 664,
                 '2022-秋': 665, '2023-春': 666,
                 '2023-秋': 667, '2024-春': 668}

# building_dict = {'fuxin': {'博文楼': 7, '博雅楼': 13, '新华楼': 19, '中和楼': 17, '致远楼': 18, '知行楼': 8, '物理实验室': 15, '主楼机房': 9},
#                  'huludao': {'尔雅楼': 20, '静远楼': 11, '葫芦岛物理实验室': 16, '葫芦岛机房': 21, '耘慧楼': 14}}
building_dict = {'eyl': 20, 'jyl': 11, 'hldwlsys': 16, 'hldjf': 21, 'yhl': 14, 'bwl': 7, 'byl': 13, 'xhl': 19,
                 'zhl': 17, 'zyl': 18, 'zxl': 8, 'wlsys': 15, 'zljf': 9}


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
        raise exceptions.FormException('请检查学期参数是否正确')
    return semester_dict.get(semester, default_semester_id)
