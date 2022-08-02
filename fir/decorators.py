# -*- coding: utf-8 -*-
from functools import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from fir.config.base import TF_INSTALLED, ENFORCE_2FA


def fir_auth_required(view=None, redirect_field_name=None, login_url=None):
    if not TF_INSTALLED:
        return login_required(
            function=view,
            redirect_field_name=REDIRECT_FIELD_NAME,
            login_url=None,
        )


    from django_otp.decorators import otp_required
    return (
        otp_required(
            view=view,
            redirect_field_name=REDIRECT_FIELD_NAME,
            login_url=login_url,
            if_configured=False,
        )
        if ENFORCE_2FA
        else otp_required(
            view=view,
            redirect_field_name=REDIRECT_FIELD_NAME,
            login_url=login_url,
            if_configured=True,
        )
    )
