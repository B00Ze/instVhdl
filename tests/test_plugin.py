#!/usr/bin/env python
import pytest
import string
import random

from plugin import instVHDL

ALIGNMENT_SIGN = " "
TEST_JOIN_SIGN = " "

def get_alignment(name, alignment):
    colon_position = alignment + 1
    if len(name) > alignment:
        colon_position = len(name) + 1
    return colon_position

def test_port_creation():
    p_name = "p_name"
    p_type = "p_type"
    p = instVHDL.port(p_name, p_type)
    assert p.getName() == p_name
    assert p.getType() == p_type


DEFAULT_P_NAME    = "p_name"
DEFAULT_P_TYPE    = "p_type"
DEFAULT_P_DEFAULT = "p_default"

@pytest.fixture()
def generic_port():
    p_name    = DEFAULT_P_NAME
    p_type    = DEFAULT_P_TYPE
    p_default = DEFAULT_P_DEFAULT
    p = instVHDL.genericPort(p_name, p_type, p_default)
    return p

def test_generic_port_creation(generic_port):
    p = generic_port
    assert p.getName() == DEFAULT_P_NAME
    assert p.getType() == DEFAULT_P_TYPE
    assert p.getDefault() == DEFAULT_P_DEFAULT

@pytest.fixture()
def generic_port_vhdl():
    p_name    = DEFAULT_P_NAME
    p_type    = DEFAULT_P_TYPE
    p_default = DEFAULT_P_DEFAULT
    p = instVHDL.genericPortVHDL(p_name, p_type, p_default)
    return p

def test_generic_port_vhdl_creation(generic_port_vhdl):
    p = generic_port_vhdl
    assert len(p.getStrList()) != 0
    assert DEFAULT_P_NAME in TEST_JOIN_SIGN.join(p.getStrList())
    assert DEFAULT_P_TYPE in TEST_JOIN_SIGN.join(p.getStrList())

def test_generic_port_vhdl_alignment(generic_port_vhdl):
    p = generic_port_vhdl
    alignments = (0, 5, 33, len(DEFAULT_P_NAME), len(DEFAULT_P_NAME)-1)
    for alignment in alignments:
        colon_position = get_alignment(DEFAULT_P_NAME, alignment)
        aligned = TEST_JOIN_SIGN.join(p.getStrAligned(alignment))
        assert aligned[colon_position] == ':'

def test_generic_port_vhdl_default(generic_port_vhdl):
    p = generic_port_vhdl
    alignment = 0

    test_str = TEST_JOIN_SIGN.join(p.getStrAligned(alignment))
    assert DEFAULT_P_DEFAULT in test_str

    default = "tmp"
    p.setDefault(default)
    test_str = TEST_JOIN_SIGN.join(p.getStrAligned(alignment))
    assert default in test_str

    default = ""
    p.setDefault(default)
    test_str = TEST_JOIN_SIGN.join(p.getStrAligned(alignment))
    assert ":=" not in test_str

def tests_port_inout():
    p_name = "p_name"
    p_type = "p_type"
    p_inout = "p_inout"
    p = instVHDL.inoutPort(p_name, p_type, p_inout)
    assert p.getName() == p_name
    assert p.getType() == p_type
    assert p.getInout() == p_inout

def tests_port_inout_vhdl_aligned():
    p_name = "p_name"
    p_type = "p_type"
    p_inout = "p_inout"

    p = instVHDL.inoutPortVHDL(p_name, p_type, p_inout)

    alignments = (0,  33,  len(p_inout), len(p_inout)-1)
    inout_alignments = (0,  33, len(p_name), len(p_name)-1,  len(p_inout), len(p_inout)-1)
    for alignment  in alignments:
        colon_position = get_alignment(p_name, alignment)
        for inout_alignment in inout_alignments:
            inout_colon_offset = get_alignment(p_inout, inout_alignment)

            aligned = TEST_JOIN_SIGN.join(p.getStrAligned(alignment, inout_alignment))

            assert p_name in aligned
            assert aligned[colon_position] == ':'
            assert p_inout in aligned

            inout_position = aligned.find(p_inout)
            assert inout_position > 0
            assert aligned[inout_position+inout_colon_offset - 1] == ' '

DEFAULT_C_NAME = "c_name"
@pytest.fixture()
def dummy_component():
    c_name = DEFAULT_C_NAME
    c = instVHDL.component(c_name)
    return c

def tests_component_creation(dummy_component):
    c_name = DEFAULT_C_NAME

    c = dummy_component

    assert c.getName() == c_name
    assert len(c.getLib()) > 0
    assert len(c.getGeneric()) == 0

    c_name = "new_name"
    c.setName(c_name)
    assert c.getName() == c_name

    c_lib = "c_lib"
    c.setLib(c_lib)
    assert c.getLib() == c_lib

DEFAULT_MAX_NAME_LENGTH = 30

def random_name():
    valid_sumbols = string.ascii_letters + string.digits + "_"
    name_length = random.randint(1, DEFAULT_MAX_NAME_LENGTH)
    return ''.join(random.choice(valid_sumbols) for x in range(name_length))

@pytest.fixture()
def generic_list():
    MAX_LIST_LENGTH = 20
    out = []
    for _ in range(random.randint(3, MAX_LIST_LENGTH)):
        p_name    = random_name()
        p_type    = random_name()
        p_default = random_name()
        p = instVHDL.genericPort(p_name, p_type, p_default)
        out.append(p)
    return out

def tests_component_generic_add(generic_list):
    pass
#    for generic in generic_list:
#        assert generic.getName() in

