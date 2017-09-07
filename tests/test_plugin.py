#!/usr/bin/env python
import pytest

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


def test_generic_port_creation():
    p_name = "p_name"
    p_type = "p_type"
    p_default = "p_default"
    p = instVHDL.genericPort(p_name, p_type, p_default)
    assert p.getName() == p_name
    assert p.getType() == p_type
    assert p.getDefault() == p_default

def test_generic_port_vhdl_creation():
    p_name = "p_name"
    p_type = "p_type"
    p_default = "p_default"
    p = instVHDL.genericPortVHDL(p_name, p_type, p_default)
    assert len(p.getStrList()) != 0
    assert p_name in TEST_JOIN_SIGN.join(p.getStrList())
    assert p_type in TEST_JOIN_SIGN.join(p.getStrList())
    
def test_generic_port_vhdl_alignment():
    p_name = "p_name"
    p_type = "p_type"
    p_default = "p_default"
    p = instVHDL.genericPortVHDL(p_name, p_type, p_default)
    alignments = (0, 5, 33, len(p_name), len(p_name)-1)
    for alignment in alignments:
        colon_position = get_alignment(p_name, alignment)
        aligned = TEST_JOIN_SIGN.join(p.getStrAligned(alignment))
        assert aligned[colon_position] == ':'

def test_generic_port_vhdl_default():
    p_name = "p_name"
    p_type = "p_type"
    p_default = "p_default"
    alignment = 0
    p = instVHDL.genericPortVHDL(p_name, p_type, p_default)

    test_str = TEST_JOIN_SIGN.join(p.getStrAligned(alignment))
    assert p_default in test_str

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

def tests_component_creation():
    c_name = "c_name"

    c = instVHDL.component(c_name)

    assert c.getName() == c_name
    assert len(c.getLib()) > 0 
    assert len(c.getGeneric()) == 0

    c_name = "new_name"
    c.setName(c_name)
    assert c.getName() == c_name

    c_lib = "c_lib"
    c.setLib(c_lib)
    assert c.getLib() == c_lib
