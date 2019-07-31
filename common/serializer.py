#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import inspect
from sqlalchemy.orm.interfaces import (ONETOMANY, MANYTOMANY)

class Serializer(object):
    def __init__(self, instance, **kwargs):
        meta = self.Meta
        self.instance = instance
        self.depth = kwargs['depth'] if 'depth' in kwargs else meta.depth
        self.include = kwargs[
            'include'] if 'include' in kwargs else meta.include
        self.exclude = kwargs[
            'exclude'] if 'exclude' in kwargs else meta.exclude
        self.extra = kwargs['extra'] if 'extra' in kwargs else meta.extra

    def __new__(self, *args, **kwargs):
        meta = self.Meta
        for _meta in ['include', 'exclude', 'extra']:
            if not hasattr(meta, _meta):
                setattr(meta, _meta, [])
        if not hasattr(meta, 'depth'):
            setattr(meta, 'depth', 2)
        return super(Serializer, self).__new__(self, *args, **kwargs)

    @property
    def data(self):
        if isinstance(self.instance, list):
            return self._serializerlist(self.instance, self.depth)
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
        extra_data = self._serializer_extra(instance)
        result.update(model_data)
        result.update(relation_data)
        result.update(extra_data)
        return result

    def _serializer_extra(self, instance):
        extra = self.extra
        result = {}
        for e in extra:
            # extra_column = getattr(self, e)
            # if isinstance(extra_column, Field):
            #     result[e] = extra_column.data(instance)
            # else:
            extra_column = getattr(instance, e)
            result[e] = extra_column if not callable(
                extra_column) else extra_column()
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
            serializer = Serializer
            if hasattr(self, column):
                serializer = getattr(self, column)
            if relation.direction in [ONETOMANY, MANYTOMANY
                                      ] and relation.uselist:
                children = getattr(instance, column)
                if relation.lazy == 'dynamic':
                    children = children.all()
                result[column] = serializer(
                    children,
                    exclude=[relation.back_populates],
                    depth=depth).data if children else []
            else:
                child = getattr(instance, column)
                if relation.lazy == 'dynamic':
                    child = child.first()
                result[column] = serializer(
                    child,
                    exclude=[relation.back_populates],
                    depth=depth).data if child else {}
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

    class Meta:
        depth = 2
        include = []
        exclude = []
        extra = []
