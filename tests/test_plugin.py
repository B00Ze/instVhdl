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


import os
def create_subdirs(full_filename):
    dirs = os.path.split(full_filename)
    if dirs[-1].endswith('.vhd'):
        dirs = dirs[:-1]
    directory_path = os.path.join(*dirs)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


@pytest.fixture()
def testsample_directory():
    TEST_SAMPLES_DIR = os.path.join(os.getcwd(), "test_samples")
    create_subdirs(TEST_SAMPLES_DIR)
    return TEST_SAMPLES_DIR

@pytest.fixture()
def file_writer(testsample_directory):
    files = []

    def create(filename="tmp.vhd", text=''):
        full_path = os.path.join(testsample_directory, filename)
        create_subdirs(full_path)
        with open(full_path, 'w') as rw_file:
            rw_file.write(text)
        files.append(full_path)
        return full_path
    yield create

#    for filename in files:
#        os.remove(filename)

@pytest.fixture()
def file_reader(testsample_directory):
    def read_file(filename="tmp.vhd"):
        full_path = os.path.join(testsample_directory, filename)
        create_subdirs(full_path)
        with open(full_path, 'r') as read_file:
            data = read_file.read()
        return data
    yield read_file

@pytest.fixture()
def simple_not(file_writer):
    filename = "simple.vhd"
    simple_lines = NOT_ELEMENT_TEXT
    yield file_writer(filename, simple_lines)



def tests_add_to_empty_file(file_writer, file_reader, simple_not):
    out_filename = "out.vhd"
    out_line = 0
    full_out_path = file_writer(out_filename, ' ')

    instVHDL.instantiateEntity(simple_not, full_out_path, out_line)

    instantiated = file_reader(out_filename)

    assert "not_element" in instantiated
    assert "port map" in instantiated
    assert instantiated.count('=>') == 2

def tests_add_to_not(file_reader, file_writer, simple_not):
    out_filename  = "not_out.vhd"
    full_out_path = file_writer(out_filename, NOT_ELEMENT_TEXT)
    out_line = 12

    instVHDL.instantiateEntity(simple_not, full_out_path, out_line)

    instantiated = file_reader(out_filename)

    assert "not_element" in instantiated
    assert "port map" in instantiated
    assert instantiated.count('=>') == 2
    assert "component" in instantiated
    assert "end component" in instantiated
    assert "FOR ALL" in instantiated
    assert "USE ENTITY" in instantiated


def tests_add_library(file_reader, file_writer):
    input_libname = "inp_lib"
    input_filename  = os.path.join(input_libname, "not_lib_in.vhd")
    full_input_path = file_writer(input_filename, NOT_ELEMENT_TEXT)

    output_libname = "output_lib"
    output_libtext = "LIBRARY "+output_libname+";\n"+NOT_ELEMENT_TEXT
    out_filename  = "not_lib_out.vhd"
    full_out_path = file_writer(out_filename, output_libtext)

    out_line = 12

    instVHDL.instantiateEntity(full_input_path, full_out_path, out_line)

    instantiated = file_reader(out_filename)

    assert "not_element" in instantiated
    assert "port map" in instantiated
    assert instantiated.count('=>') == 2
    assert "component" in instantiated
    assert "end component" in instantiated
    assert "FOR ALL" in instantiated
    assert "USE ENTITY" in instantiated
    assert output_libname in instantiated
    assert input_libname in instantiated


def tests_add_to_not(file_reader, file_writer, simple_not):
    out_filename  = "not_double_out.vhd"
    full_out_path = file_writer(out_filename, NOT_ELEMENT_TEXT)
    out_line = 12

    instVHDL.instantiateEntity(simple_not, full_out_path, out_line)
    out_line = 25
    instVHDL.instantiateEntity(simple_not, full_out_path, out_line)

    instantiated = file_reader(out_filename)

    assert "not_element" in instantiated
    assert instantiated.count("port map") == 2
    assert instantiated.count('=>') == 4

NOT_VECTOR_GENERIC_TEXT =  """
entity not_element is
    generic (
        CLK_FREQ     : natural := 24840000; -- Clock frequency in Hz
        DATA_BIT_LEN : natural := 8         -- Vector bit length
      );
    port (
        A : in std_logic(DATA_BIT_LEN-1 downto 0);
        nA : out std_logic(DATA_BIT_LEN-1 downto 0)
    );
end not_element;

architecture impl of not_element is
begin

    nA <= not A;

end impl; """

def tests_add_generic_to_not(file_reader, file_writer):
    input_filename  = "not_generic_in.vhd"
    full_input_path = file_writer(input_filename, NOT_VECTOR_GENERIC_TEXT)

    out_filename  = "not_generic_out.vhd"
    full_out_path = file_writer(out_filename, NOT_ELEMENT_TEXT)
    out_line = 12

    instVHDL.instantiateEntity(full_input_path, full_out_path, out_line)

    instantiated = file_reader(out_filename)

    assert "not_element" in instantiated
    assert "port map" in instantiated
    assert instantiated.count('=>') == 4
    assert "component" in instantiated
    assert "end component" in instantiated
    assert "FOR ALL" in instantiated
    assert "USE ENTITY" in instantiated


