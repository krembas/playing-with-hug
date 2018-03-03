"""
Validators definitions used by request handlers (to ensure data provided by request are proper).
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

from models import Invitee


@hug.type(extend=hug.types.text)
def _email_validator(value):
    """Email address."""
    # ridiculously yet robust simple email validator ;)
    if value.count('@') != 1:
        raise ValueError('Incorrect email format: {}'.format(value))
    return value


@hug.type(extend=hug.types.text)
def _nonexisting_invitee_validator(value):
    """New invitee name."""
    if Invitee(invitee=value).get():
        raise ValueError("Invitee '{}' already exists, probably you tried create it instead update.".format(value))
    return value


@hug.type(extend=hug.types.text)
def _exisitng_invitee_validator(value):
    """Existing invitee name."""
    if not Invitee(invitee=value).get():
        raise ValueError("Invitee '{}' not found, probably not invited yet or removed.".format(value))
    return value


# exported validators

nonexisting_invitee = _nonexisting_invitee_validator
existing_invitee = _exisitng_invitee_validator
email = _email_validator
