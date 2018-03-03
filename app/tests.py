"""
Tests that ensures that all endpoints work correctly in sense of API and expected behavior.
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

import hug
import pytest

from falcon import HTTP_200, HTTP_201, HTTP_204, HTTP_400, HTTP_404

from models import Invitee
from app import hug_api as api

# This list is not in alphabetical order, so reverse it before comparing
# with responses as list of invitees in responses is sorted.
test_invitee = [
    {'invitee': 'John Doe (0)', 'email': 'john@email.me'},
    {'invitee': 'Jane Roe (1)', 'email': 'jane@email.me'}
]


class APITest():
    api_url = '/invitation'

    @classmethod
    @pytest.fixture
    def prepare_db_with_test_invitee_0(cls):
        # creates invite record in "db"
        db = Invitee._storage
        db.__init__()  # make db empty ;)
        key = test_invitee[0]['invitee']
        db.set(key, test_invitee[0])
        yield
        db.__init__()  # rollback all changes ;)

    @classmethod
    @pytest.fixture
    def prepare_db_with_both_test_invitees(cls):
        # creates invite record in "db"
        db = Invitee._storage
        db.__init__()  # make db empty ;)
        data = test_invitee[0]
        key = data['invitee']
        db.set(key, data)
        data = test_invitee[1]
        key = data['invitee']
        db.set(key, data)
        yield
        db.__init__()  # rollback all changes ;)

    def assert_invitee(self, invitee_res, invitee_exp=None):
        """Validates if invitee_res (from response) has proper form and same data as optional invite_exp (expected)"""
        assert type(invitee_res) == dict
        assert 'invitee' in invitee_res
        assert len(invitee_res['invitee'])
        assert 'email' in invitee_res
        assert len(invitee_res['email'])
        if invitee_exp:
            assert invitee_res == invitee_exp

    def assert_error(self, res, fields=None):
        """Validates if responce contains expected error messages"""
        fields = fields or []
        assert 'errors' in res.data
        for field in fields:
            assert field in res.data['errors']


class TestInviteeGeneral(APITest):
    """Tests for "general" API issues"""

    def test_invitee_nok_bad_api_url(self):
        for apicall in [hug.test.get, hug.test.put, hug.test.put, hug.test.delete]:
            res = apicall(api, '/bad-api-url')
            assert res.status == HTTP_404


class TestInviteeRetrieve(APITest):
    """Tests for GET /invitation endpoint"""

    @pytest.mark.usefixtures('prepare_db_with_test_invitee_0')
    def test_invitee_retrieve_ok(self):
        test_data = test_invitee[0].copy()
        test_data.pop('email')
        res = hug.test.get(api, self.api_url, test_data)
        assert res.status == HTTP_200
        self.assert_invitee(res.data, test_invitee[0])

    @pytest.mark.usefixtures('prepare_db_with_both_test_invitees')
    def test_invitee_retrieve_ok_multiple_invitees(self):
        for ti in test_invitee:
            test_data = ti.copy()
            test_data.pop('email')
            res = hug.test.get(api, self.api_url, test_data)
            assert res.status == HTTP_200
            self.assert_invitee(res.data, ti)

    @pytest.mark.usefixtures('prepare_db_with_test_invitee_0')
    def test_invitees_list_retrieve_ok(self):
        test_data = None  # catch'em all ;)
        res = hug.test.get(api, self.api_url, test_data)
        assert res.status == HTTP_200
        assert type(res.data) == list
        assert len(res.data) == 1
        self.assert_invitee(res.data[0], test_invitee[0])

    @pytest.mark.usefixtures('prepare_db_with_both_test_invitees')
    def test_invitees_list_retrieve_ok_multiple_invitees(self):
        test_data = None  # catch'em all ;)
        res = hug.test.get(api, self.api_url, test_data)
        assert res.status == HTTP_200
        assert type(res.data) == list
        assert len(res.data) == 2
        for tr, ti in zip(res.data, reversed(test_invitee)):
            self.assert_invitee(tr, ti)


class TestInviteeCreation(APITest):
    """Tests for POST /invitation endpoint"""

    def test_invitee_creation_ok(self):
        test_data = test_invitee[0].copy()
        res = hug.test.post(api, self.api_url, test_data)
        assert res.status == HTTP_201
        self.assert_invitee(res.data, test_invitee[0])

    @pytest.mark.usefixtures('prepare_db_with_test_invitee_0')
    def test_invitee_creation_nok_invitee_already_exists(self):
        test_data = test_invitee.copy()
        res = hug.test.post(api, self.api_url, test_data)
        assert res.status == HTTP_400
        self.assert_error(res, ['invitee'])

    def test_invitee_creation_nok_mising_fields(self):
        for field in ['invitee', 'email']:
            test_data = test_invitee[0].copy()
            test_data.pop(field)
            res = hug.test.post(api, self.api_url, test_data)
            assert res.status == HTTP_400
            self.assert_error(res, [field])

    def test_invitee_creation_nok_bad_email(self):
        for email in ['bademail', None, '', 'bad@em@il']:
            test_data = test_invitee[0].copy()
            test_data['email'] = email
            res = hug.test.post(api, self.api_url, test_data)
            assert res.status == HTTP_400
            self.assert_error(res, ['email'])


class TestInviteeUpdate(APITest):
    """Tests for PUT /invitation endpoint"""

    @pytest.mark.usefixtures('prepare_db_with_test_invitee_0')
    def test_invitee_update_ok(self):
        test_data = test_invitee[0].copy()
        test_data['email'] += '.com'
        res = hug.test.put(api, self.api_url, test_data)
        assert res.status == HTTP_200
        self.assert_invitee(res.data, test_data)

    @pytest.mark.usefixtures('prepare_db_with_test_invitee_0')
    def test_invitee_update_nok__bad_email(self):
        for email in ['bademail', None, '', 'bad@em@il']:
            test_data = test_invitee[0].copy()
            test_data['email'] = email
            res = hug.test.put(api, self.api_url, test_data)
            assert res.status == HTTP_400
            self.assert_error(res, ['email'])


class TestInviteeDelete(APITest):
    """Tests for DELETE /invitation endpoint"""

    @pytest.mark.usefixtures('prepare_db_with_test_invitee_0')
    def test_invitee_delete_ok(self):
        test_data = test_invitee[0].copy()
        test_data.pop('email')
        res = hug.test.delete(api, self.api_url, test_data)
        assert res.status == HTTP_204

    def test_invitee_delete_nok_empty_db(self):
        test_data = test_invitee[0].copy()
        test_data.pop('email')
        res = hug.test.delete(api, self.api_url, test_data)
        assert res.status == HTTP_400  # nothing to delete
        self.assert_error(res, ['invitee'])

    @pytest.mark.usefixtures('prepare_db_with_test_invitee_0')
    def test_invitee_delete_nok_missing_invitee_parameter(self):
        test_data = None
        res = hug.test.delete(api, self.api_url, test_data)
        assert res.status == HTTP_400
        self.assert_error(res, ['invitee'])
