"""
This is a simple invitation service app that uses awesome HUG framework to do its job.
Please read README.md from application's repo for detailed info.
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
from falcon import HTTP_200, HTTP_201, HTTP_204

from api import create_invitee, retrieve_invitees, update_invitee, delete_invitee


hug_api = hug.API(__name__)  # used also by tests
router = hug.route.API(__name__)


# API for invitation (routing API urls and HTTP methods to appropriate handlers)

api_url = '/invitation'
router.post(api_url, status=HTTP_201)(create_invitee)
router.get(api_url, status=HTTP_200)(retrieve_invitees)
router.put(api_url, status=HTTP_200)(update_invitee)
router.delete(api_url, status=HTTP_204)(delete_invitee)


def serve():
    """Serves API via falcon webserver (hug uses it internally)"""
    hug_api.http.serve(port=8000)
