import os

PROJECT_ABSOLUTE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_ABSOLUTE_PATH = PROJECT_ABSOLUTE_PATH + '/config.yaml'


def get_db_url_dict(config_path=CONFIG_ABSOLUTE_PATH) -> dict:
    import yaml
    db_url_dict = {}
    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)

        sql = config['mysql']
        user = sql['user']
        password = sql['password']
        host = sql['host']
        port = sql['port']
        db_name = sql['db_name']
        db_url_dict['production'] = F"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

        sql = config['test-mysql']
        user = sql['user']
        password = sql['password']
        host = sql['host']
        port = sql['port']
        db_name = sql['db_name']
        db_url_dict['test'] = F"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

    return db_url_dict

# {
#     yearDom: "<tr><td class='calendar-bar-td-blankBorder' index='0'>2007-2008</td><td class='calendar-bar-td-blankBorder' index='1'>2008-2009</td><td class='calendar-bar-td-blankBorder' index='2'>2009-2010</td></tr><tr><td class='calendar-bar-td-blankBorder' index='3'>2010-2011</td><td class='calendar-bar-td-blankBorder' index='4'>2011-2012</td><td class='calendar-bar-td-blankBorder' index='5'>2012-2013</td></tr><tr><td class='calendar-bar-td-blankBorder' index='6'>2013-2014</td><td class='calendar-bar-td-blankBorder' index='7'>2014-2015</td><td class='calendar-bar-td-blankBorder' index='8'>2015-2016</td></tr><tr><td class='calendar-bar-td-blankBorder' index='9'>2016-2017</td><td class='calendar-bar-td-blankBorder' index='10'>2017-2018</td><td class='calendar-bar-td-blankBorder' index='11'>2018-2019</td></tr><tr><td class='calendar-bar-td-blankBorder' index='12'>2019-2020</td><td class='calendar-bar-td-blankBorder' index='13'>2020-2021</td><td class='calendar-bar-td-blankBorder' index='14'>2021-2022</td></tr><tr><td class='calendar-bar-td-blankBorder' index='15'>2022-2023</td><td class='calendar-bar-td-blankBorder' index='16'>2023-2024</td><td class='calendar-bar-td-blankBorder'></td><td class='calendar-bar-td-blankBorder'></td></tr><td class='calendar-bar-td-blankBorder'></td>",
#     termDom: "<tr><td class='calendar-bar-td-blankBorder' val='620'>学期<span>1</span></td></tr><tr><td class='calendar-bar-td-blankBorder' val='626'>学期<span>2</span></td></tr>",
#     semesters: {y0: [{id: 644, schoolYear: "2007-2008", name: "1"}, {id: 638, schoolYear: "2007-2008", name: "2"}],
#                 y1: [{id: 636, schoolYear: "2008-2009", name: "1"}, {id: 637, schoolYear: "2008-2009", name: "2"}],
#                 y2: [{id: 643, schoolYear: "2009-2010", name: "1"}, {id: 635, schoolYear: "2009-2010", name: "2"}],
#                 y3: [{id: 639, schoolYear: "2010-2011", name: "1"}, {id: 632, schoolYear: "2010-2011", name: "2"}],
#                 y4: [{id: 628, schoolYear: "2011-2012", name: "1"}, {id: 641, schoolYear: "2011-2012", name: "2"}],
#                 y5: [{id: 629, schoolYear: "2012-2013", name: "1"}, {id: 640, schoolYear: "2012-2013", name: "2"}],
#                 y6: [{id: 645, schoolYear: "2013-2014", name: "1"}, {id: 630, schoolYear: "2013-2014", name: "2"}],
#                 y7: [{id: 634, schoolYear: "2014-2015", name: "1"}, {id: 631, schoolYear: "2014-2015", name: "2"}],
#                 y8: [{id: 623, schoolYear: "2015-2016", name: "1"}, {id: 621, schoolYear: "2015-2016", name: "2"}],
#                 y9: [{id: 624, schoolYear: "2016-2017", name: "1"}, {id: 619, schoolYear: "2016-2017", name: "2"}],
#                 y10: [{id: 625, schoolYear: "2017-2018", name: "1"}, {id: 622, schoolYear: "2017-2018", name: "2"}],
#                 y11: [{id: 633, schoolYear: "2018-2019", name: "1"}, {id: 642, schoolYear: "2018-2019", name: "2"}],
#                 y12: [{id: 620, schoolYear: "2019-2020", name: "1"}, {id: 626, schoolYear: "2019-2020", name: "2"}],
#                 y13: [{id: 627, schoolYear: "2020-2021", name: "1"}, {id: 662, schoolYear: "2020-2021", name: "2"}],
#                 y14: [{id: 663, schoolYear: "2021-2022", name: "1"}, {id: 664, schoolYear: "2021-2022", name: "2"}],
#                 y15: [{id: 665, schoolYear: "2022-2023", name: "1"}, {id: 666, schoolYear: "2022-2023", name: "2"}],
#                 y16: [{id: 667, schoolYear: "2023-2024", name: "1"}, {id: 668, schoolYear: "2023-2024", name: "2"}]},
#     yearIndex: "12", termIndex: "1", semesterId: "626"}
