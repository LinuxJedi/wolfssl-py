# -*- coding: utf-8 -*-
#
# _methods.py
#
# Copyright (C) 2006-2022 wolfSSL Inc.
#
# This file is part of wolfSSL. (formerly known as CyaSSL)
#
# wolfSSL is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# wolfSSL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

# pylint: disable=missing-docstring, invalid-name

try:
    from wolfssl._ffi import lib as _lib
    from wolfssl._ffi import ffi as _ffi
except ImportError:
    pass


PROTOCOL_SSLv23 = 1
PROTOCOL_SSLv3 = 2
PROTOCOL_TLS = 1
PROTOCOL_TLSv1 = 3
PROTOCOL_TLSv1_1 = 4
PROTOCOL_TLSv1_2 = 5
PROTOCOL_TLSv1_3 = 6

_PROTOCOL_LIST = [PROTOCOL_SSLv23, PROTOCOL_SSLv3, PROTOCOL_TLS,
                  PROTOCOL_TLSv1, PROTOCOL_TLSv1_1, PROTOCOL_TLSv1_2,
                  PROTOCOL_TLSv1_3]

_DYNAMIC_TYPE_METHOD = 11


def _native_free(native_object, dynamic_type):
    _lib.wolfSSL_Free(native_object)


class WolfSSLMethod(object):  # pylint: disable=too-few-public-methods
    """
    An SSLMethod holds SSL-related configuration options such as
    protocol version and communication side.
    """

    def __init__(self, protocol, server_side):
        if protocol not in _PROTOCOL_LIST:
            raise ValueError("this protocol is not supported")

        elif protocol == PROTOCOL_SSLv3:
            raise ValueError("this protocol is not supported")

        elif protocol == PROTOCOL_TLSv1:
            raise ValueError("this protocol is not supported")

        elif protocol == PROTOCOL_TLSv1_1:
            self.native_object =                                     \
                _lib.wolfTLSv1_1_server_method() if server_side else \
                _lib.wolfTLSv1_1_client_method()

        elif protocol == PROTOCOL_TLSv1_2:
            self.native_object =                                     \
                _lib.wolfTLSv1_2_server_method() if server_side else \
                _lib.wolfTLSv1_2_client_method()

        elif protocol == PROTOCOL_TLSv1_3:
            self.native_object =                                     \
                _lib.wolfTLSv1_3_server_method() if server_side else \
                _lib.wolfTLSv1_3_client_method()

        elif protocol in [PROTOCOL_SSLv23, PROTOCOL_TLS]:
            self.native_object =                                    \
                _lib.wolfSSLv23_server_method() if server_side else \
                _lib.wolfSSLv23_client_method()

        if self.native_object == _ffi.NULL:
            raise MemoryError("Unnable to allocate method object")

    def __del__(self):
        if getattr(self, 'native_object', _ffi.NULL) != _ffi.NULL:
            _native_free(self.native_object, _DYNAMIC_TYPE_METHOD)
