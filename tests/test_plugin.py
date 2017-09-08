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

@pytest.fixture
def port_inout():
    p_name  = DEFAULT_P_NAME
    p_type  = DEFAULT_P_TYPE
    p_inout = DEFAULT_P_DEFAULT
    p = instVHDL.inoutPort(p_name, p_type, p_inout)
    return p


def tests_port_inout(port_inout):
    p = port_inout
    assert p.getName()  == DEFAULT_P_NAME
    assert p.getType()  == DEFAULT_P_TYPE
    assert p.getInout() == DEFAULT_P_DEFAULT

@pytest.fixture
def port_inout_vhdl():
    p_name  = DEFAULT_P_NAME
    p_type  = DEFAULT_P_TYPE
    p_inout = DEFAULT_P_DEFAULT
    p = instVHDL.inoutPortVHDL(p_name, p_type, p_inout)
    return p

def tests_port_inout_vhdl_aligned(port_inout_vhdl):
    p = port_inout_vhdl
    p_name  = DEFAULT_P_NAME
    p_inout = DEFAULT_P_DEFAULT

    alignments = (0,  33,  len(p_inout), len(p_inout)-1)
    inout_alignments = (0,  33, len(p_name), len(p_name)-1,  len(p_inout), len(p_inout)-1)
    for alignment  in alignments:
        colon_position = get_alignment(p_name, alignment)
        for inout_alignment in inout_alignments:
            inout_colon_offset = get_alignment(p_inout, inout_alignment)

            aligned = TEST_JOIN_SIGN.join(p.getStrAligned(alignment, inout_alignment))

            assert p_name in aligned
            assert aligned[colon_position] == ':', \
                    "Port name not aligned: {}, {}".format(p_name, alignment)
            assert p_inout in aligned

            inout_position = aligned.find(p_inout)
            assert inout_position > 0, \
                    "Port name not found in aligned representation: {}, {}".format(p_inout, aligned)
            assert aligned[inout_position+inout_colon_offset - 1] == ' ', \
                    "Inout not aligned to {}".format(inout_alignment)

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
def random_generic_list():
    MAX_LIST_LENGTH = 20
    out = []
    for _ in range(random.randint(3, MAX_LIST_LENGTH)):
        p_name    = random_name()
        p_type    = random_name()
        p_default = random_name()
        p = instVHDL.genericPort(p_name, p_type, p_default)
        out.append(p)
    return out

def tests_component_generic_add(dummy_component, random_generic_list):
    for port in random_generic_list:
        dummy_component.addGeneric(port)
    ports  =  dummy_component.getGeneric()

    assert len(ports) == len(random_generic_list)
    for port in random_generic_list:
        assert port in ports

    dummy_component.setGeneric([])
    assert len(dummy_component.getGeneric()) == 0

    for port in random_generic_list:
        dummy_component.addGenericStr(port.getName(), port.getType(), port.getDefault())

    port_names  =  []
    for port in dummy_component.getGeneric():
        port_names.append(port.getName())

    assert len(ports) == len(random_generic_list)
    for port in random_generic_list:
        assert port.getName() in port_names

NOT_ELEMENT_TEXT =  """ 
entity not_element is
    port (
        A : in std_logic;
        nA : out std_logic
    );
end not_element;

architecture impl of not_element is
begin

    nA <= not A;

end impl; """

@pytest.fixture()
def simple_not():
    filename = "simple.vhd"
    simple_lines = NOT_ELEMENT_TEXT
    with open(filename, 'w') as simple:
        simple.write(simple_lines)

    yield filename

    import os
    os.remove(filename)

def tests_add_to_empty_file(simple_not):
    out_filename = "out.vhd"
    out_line = 0
    with open(out_filename, 'w') as out_file:
        out_file.write(' ')

    instVHDL.instantiateEntityVHDL(simple_not, out_filename, out_line)

