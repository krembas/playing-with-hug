"""
Models definitions used by application (to provide persistence layer and abstract data I/O into common interface
used by handlers "views").
"""
# Copyright (C) 2017 Krystian Rembas
# -----------------------------------------------------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# -----------------------------------------------------------------------------------------------------------------------

from hug.store import InMemoryStore


class Model():
    """Simple generic "model" with runtime storage"""
    _storage = InMemoryStore()  # actually it's just an "opaqued" dict but thanks hug ;)

    def __init__(self, **fields):
        """Instrumentates a model with appropriate field attributes and runtime storage"""
        super().__init__()
        # filter out non-model fields and pk field
        model_fields = {field: fields[field] for field in fields if field in self.fields}
        for field in model_fields:
            setattr(self, field, fields[field])

    def save(self):
        """
        Saves model instance. If instance exist will be just updated.
        :return: Saved instance data
        """
        key = getattr(self, self.pk)
        if self._storage.exists(key):
            # update existing invitee data (only given fields)
            data = self._storage.get(key)
            data.update({field: getattr(self, field)
                         for field in self.fields if getattr(self, field, None) != data[field]})
            self._storage.set(key, data)
        else:
            # create new invitee data
            data = {field: getattr(self, field) for field in self.fields}
            self._storage.set(key, data)
        return self._storage.get(key)

    def get(self):
        """
        Retrieves model instance for given pk
        :return: Retrieved instance data or None if no instance found.
        """
        key = getattr(self, self.pk)
        if key is None:
            # special case - sorted (by pk field) list of instance data
            return sorted([v for k, v in self._storage._data.items()], key=lambda data: data[self.pk])
        return self._storage.get(key) if self._storage.exists(key) else None

    def delete(self):
        """
        Deletes model instance.
        :return: Deleted object data or None if model instance didn't exist (so nothing to delete)
        """
        key = getattr(self, self.pk)
        data = self._storage.get(key) if self._storage.exists(key) else None
        self._storage.delete(key)  # handles missing key, don't worry
        return data

    @property
    def as_dict(self):
        """Returns a dict with all model instance fields and its values"""
        return {field: getattr(self, field, None) for field in self.fields}


class Invitee(Model):
    """Model for Invitee"""
    fields = ['invitee', 'email']
    pk = fields[0]

    def __init__(self, **fields):
        super().__init__(**fields)
