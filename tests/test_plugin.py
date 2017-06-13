#!/usr/bin/env python
import pytest

from plugin import instVHDL

def test_port_creation():
    p_name = "p_name"
    p_type = "p_type"
    p = instVHDL.port(p_name, p_type)
    assert p.getName() == p_name
    assert p.getType() == p_type


def test_generic_port_creation():
    p_name = "p_name"
    p_type = "p_type"
    p_default = "p_default"
    p = instVHDL.genericPort(p_name, p_type, p_default)
    assert p.getName() == p_name
    assert p.getType() == p_type
    assert p.getDefault() == p_default
