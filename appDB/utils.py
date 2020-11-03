import os

from sqlalchemy import inspect
from sqlalchemy.orm.base import ONETOMANY, MANYTOMANY

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
        test_db_name = sql['test_db_name']
        db_url_dict['production'] = F"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8"
        db_url_dict['test'] = F"mysql+pymysql://{user}:{password}@{host}:{port}/{test_db_name}?charset=utf8"
    return db_url_dict


class Serializer(object):

    def __init__(self, instance, many=False, include=[], exclude=[], depth=2):
        self.instance = instance
        self.many = many
        self.include = include
        self.exclude = exclude
        self.depth = depth

    @property
    def data(self):
        if self.include and self.exclude:
            raise ValueError('include and exclude can\'t work together')
        if self.many:
            if isinstance(self.instance, list):
                return self._serializerlist(self.instance, self.depth)
            pageinfo = {
                'items': True,
                'pages': self.instance.pages,
                'has_prev': self.instance.has_prev,
                'page': self.instance.page,
                'has_next': self.instance.has_next,
                'iter_pages': list(self.instance.iter_pages(left_edge=1,
                                                            left_current=2,
                                                            right_current=3,
                                                            right_edge=1))
            }
            return {'data': self._serializerlist(self.instance.items,
                                                 self.depth),
                    'pageinfo': pageinfo}
        return self._serializer(self.instance, self.depth)

    def _serializerlist(self, instances, depth):
        results = []
        for instance in instances:
            result = self._serializer(instance, depth)
            if result:
                results.append(result)
        return results

    def _serializer(self, instance, depth):
        result = {}
        if depth == 0:
            return result
        depth -= 1
        model_class = self.get_model_class(instance)
        inp = self.get_inspect(model_class)
        model_data = self._serializer_model(inp, instance, depth)
        relation_data = self._serializer_relation(inp, instance, depth)
        result.update(model_data)
        result.update(relation_data)
        return result

    def _serializer_model(self, inp, instance, depth):
        result = {}
        model_columns = self.get_model_columns(inp)
        for column in model_columns:
            result[column] = getattr(instance, column)
        return result

    def _serializer_relation(self, inp, instance, depth):
        result = {}
        relation_columns = self.get_relation_columns(inp)
        for relation in relation_columns:
            column = relation.key
            if relation.direction in [ONETOMANY, MANYTOMANY]:
                children = getattr(instance, column)
                if relation.lazy == 'dynamic':
                    children = children.all()
                result[column] = Serializer(
                    children,
                    many=True,
                    exclude=[relation.back_populates],
                    depth=depth).data
            else:
                child = getattr(instance, column)
                if relation.lazy == 'dynamic':
                    child = child.first()
                result[column] = Serializer(
                    child,
                    many=False,
                    exclude=[relation.back_populates],
                    depth=depth).data
        return result

    def get_model_class(self, instance):
        return getattr(instance, '__class__')

    def get_inspect(self, model_class):
        return inspect(model_class)

    def get_model_columns(self, inp):
        if self.include:
            model_columns = [
                column.name for column in inp.columns
                if column.name in self.include
            ]
        elif self.exclude:
            model_columns = [
                column.name for column in inp.columns
                if column.name not in self.exclude
            ]
        else:
            model_columns = [column.name for column in inp.columns]

        return model_columns

    def get_relation_columns(self, inp):
        if self.include:
            relation_columns = [
                relation for relation in inp.relationships
                if relation.key in self.include
            ]
        elif self.exclude:
            relation_columns = [
                relation for relation in inp.relationships
                if relation.key not in self.exclude
            ]
        else:
            relation_columns = [relation for relation in inp.relationships]
        return relation_columns
