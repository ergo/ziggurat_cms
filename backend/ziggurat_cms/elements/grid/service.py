# -*- coding: utf-8 -*-

import uuid

from ziggurat_cms.services.node_element import NodeElementService
from ziggurat_cms.services.elements import BaseElementService


class ZigguratCMSGridService(BaseElementService):
    @classmethod
    def set_defaults(cls, instance):
        instance.config = {'rows': []}
        row = cls.add_row(instance)

    @classmethod
    def add_row(cls, instance):
        row = {
            'uuid': str(uuid.uuid4()),
            'config': {'className': ''},
            'position': len(instance.config['rows']) + 1,
            'columns': []
        }
        instance.config['rows'].append(row)
        cls.add_column(row['uuid'], instance)
        instance.config.changed()
        return row

    @classmethod
    def add_column(cls, row_uuid, instance):
        for row in instance.config['rows']:
            if row['uuid'] == row_uuid and len(row['columns']) < 12:
                column = {
                    'config': {'className': '', 'span': 12},
                    'position': len(row['columns']) + 1,
                    'uuid': str(uuid.uuid4()),
                    'element_uuids': []
                }
                row['columns'].append(column)
                instance.config.changed()
                return column
        return None

    @classmethod
    def delete_column(cls, instance, column_uuid, db_session):
        for row in instance.config['rows']:
            for column in row['columns']:
                if column['uuid'] == column_uuid:
                    row['columns'].remove(column)
                    for elem_uuid in column['element_uuids']:
                        elem = NodeElementService.by_uuid(
                            elem_uuid, db_session=db_session)
                        elem.delete(db_session=db_session)
        for i, row in enumerate(instance.config['rows'], start=1):
            row['position'] = i
            for j, column in enumerate(row['columns'], start=1):
                column['position'] = j
        instance.config.changed()
        return ''

    @classmethod
    def delete_row(cls, instance, row_uuid, db_session):
        for row in instance.config['rows']:
            if row['uuid'] == row_uuid:
                instance.config['rows'].remove(row)
                for column in row['columns']:
                    for elem_uuid in column['element_uuids']:
                        elem = NodeElementService.by_uuid(
                            elem_uuid, db_session=db_session)
                        elem.delete(db_session=db_session)
        for i, row in enumerate(instance.config['rows'], start=1):
            row['position'] = i
        instance.config.changed()
        return ''

    @classmethod
    def patch_row(cls, instance, row_uuid, data, db_session):
        found_row = None
        for row in instance.config['rows']:
            if row['uuid'] == row_uuid:
                found_row = row
                instance.config['rows'].remove(row)

        instance.config['rows'].insert(data['position'] - 1, found_row)
        for i, row in enumerate(instance.config['rows'], start=1):
            row['position'] = i
        instance.config.changed()
        return found_row

    @classmethod
    def patch_column(cls, instance, column_uuid, data, db_session):
        found_row = None
        found_column = None
        for row in instance.config['rows']:
            for column in row['columns']:
                if column['uuid'] == column_uuid:
                    found_row = row
                    found_column = column
                    row['columns'].remove(column)
                    break
                if found_column:
                    break
        found_row['columns'].insert(data['position'] - 1, found_column)
        found_column['config']['span'] = data['config']['span']
        for i, column in enumerate(found_row['columns'], start=1):
            column['position'] = i
        instance.config.changed()
        return found_column
