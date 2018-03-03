"""
API handlers definition (de-coupled from request handlers, can be used for CLI API as well).
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


from validators import existing_invitee, nonexisting_invitee, email
from models import Invitee


# Request handlers

def retrieve_invitees(invitee: existing_invitee=None):
    """
    Retrieves invitees data.

    If parameter 'invitee' is provided (with proper invitee name, existing in system) then as a result invitee data
    is returned, otherwise list of all invitee data records is returned or None if no data exists in system.
    """
    return Invitee(invitee=invitee).get()


def create_invitee(invitee: nonexisting_invitee, email: email):
    """
    Creates invitee data.

    Validates if invitee is a text and email format is proper (and then stores new invitee record) then returns
    appropriate response with HTTP status code & response data.
    """
    return Invitee(invitee=invitee, email=email).save()


def update_invitee(invitee: existing_invitee, email: email):
    """
    Updates invitee data.

    Validates if invitee does not existing yet and email format is proper (and then stores new invitee record)
    then returns appropriate response with HTTP status code & response data.
    """
    return Invitee(invitee=invitee, email=email).save()


def delete_invitee(invitee: existing_invitee):
    """
    Deletes invitee data.

    Validates if invitee exists (and if so removes it from the system) then returns
    appropriate response with HTTP status code & response data.
    """
    Invitee(invitee=invitee).delete()
