#!/usr/bin/python
#-------------------------------------------------------------------------------
# Name:        VHDL instantiation script
# Purpose:  Using with VIM
#
# Author:      BooZe
#
# Created:     25.03.2013
# Copyright:   (c) BooZe 2013
# Licence:     BSD
#-------------------------------------------------------------------------------

import re

class port(object):
    def __init__(self,portName,portType):
        self.portName = portName
        self.portType = portType

    def getName(self):
        return self.portName

    def getType(self):
        return self.portType

    def setName(self,portName):
        self.portName = portName


    def setType(self,portType):
        self.portType = portType

    def getStrList(self):
        pass

class genericPort(port):
    def __init__(self,portName,portType,defaultValue):
        port.__init__(self,portName,portType)
        self.defaultValue = defaultValue

    def getDefault(self):
        return self.defaultValue

    def setDefault(self,defaultValue):
        self.defaultValue = defaultValue

    def getStrAligned(self,nameMax):
        pass

class genericPortVHDL(genericPort):
    def __init__(self,portName,portType,defaultValue):
        genericPort.__init__(self,portName,portType,defaultValue)
        self.defaultValue = defaultValue

    def getStrAligned(self,nameMax):
        nameLen = len(self.getName())
        strDefault = self.getDefault()
        if strDefault != "":
            strDefault = " := "+strDefault
        return [self.getName()+" "*(nameMax-nameLen)+" : "+self.getType()+\
                    strDefault+";"]

    def getStrList(self):
        return [self.getName()+" : "+self.getType()+";"]

    def __str__(self):
        strOut = self.getName()+" : "+self.getType()
        if (self.getDefault() != ""):
            strOut += ":= "+self.getDefault()
        return strOut+";\n"

class inoutPort(port):
    def __init__(self,portName,portType,inoutType):
        port.__init__(self,portName,portType)
        self.inoutType = inoutType

    def getInout(self):
        return self.inoutType

    def setInout(self,inoutType):
        self.inoutType = inoutType

    def getStrAligned(self,nameMax,inoutMax):
        pass

class inoutPortVHDL(inoutPort):
    def __init__(self,portName,portType,inoutType):
        inoutPort.__init__(self,portName,portType,inoutType)
        self.inoutType = inoutType

    def getStrAligned(self,nameMax,inoutMax):
        nameLen = len(self.getName())
        inoutLen = len(self.getInout())
        return [self.getName()+" "*(nameMax-nameLen)+" : "+self.getInout()+\
                " "*(inoutMax-inoutLen)+' '+self.getType()+";"]

    def getStrList(self):
        return [self.getName()+" : "+self.getType()+";"]

    def __str__(self):
        return self.getName()+" : "+self.getInout()+' '+self.getType()+";\n"

class component(object):

    def __init__(self,name):
        self.name = name
        self.lib = "None_lib"
        self.genericList = []
        self.inoutList = []
        self.portMaxLen = 0
        self.inoutMaxLen = 0


    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getLib(self):
        return self.lib

    def setLib(self, lib):
        self.lib = lib

    def addGeneric(self,genericPort):
        strLen = len(genericPort.getName())
        if strLen>self.portMaxLen:
            self.portMaxLen = strLen
        self.genericList.append(genericPort)

    def addGeneric(self,genericPort):
        strLen = len(genericPort.getName())
        if strLen>self.portMaxLen:
            self.portMaxLen = strLen
        self.genericList.append(genericPort)

    def addGenericStr(self,portName,portType,defaultValue):
        tmp = genericPort(portName,portType,defaultValue)
        strLen = len(portName)
        if strLen>self.portMaxLen:
            self.portMaxLen = strLen
        self.genericList.append(tmp)


    def setGeneric(self,genericList):
        for inout in genericList:
            strNameLen = len(genericList.getName())
            if strNameLen>self.portMaxLen:
                self.portMaxLen = strNameLen
        self.genericList = genericList

    def getGeneric(self):
        return self.genericList

    def addInout(self,inoutPort):
        strNameLen = len(inoutPort.getName())
        if strNameLen>self.portMaxLen:
            self.portMaxLen = strNameLen
        strInoutLen = len(inoutPort.inoutMaxLen())
        if strInoutLen>self.inoutMaxLen:
            self.inoutMaxLen = strInoutLen
        self.inoutList.append(inoutPort)

    def addInoutStr(self,portName,portType,inoutType):
        strNameLen = len(portName)
        if strNameLen>self.portMaxLen:
            self.portMaxLen = strNameLen
        strInoutLen = len(inoutType)
        if strInoutLen>self.inoutMaxLen:
            self.inoutMaxLen = strInoutLen
        tmp = inoutPortVHDL(portName,portType,inoutType)
        self.inoutList.append(tmp)

    def setInout(self,inoutList):
        for inout in inoutList:
            strNameLen = len(inout.getName())
            if strNameLen>self.portMaxLen:
                self.portMaxLen = strNameLen
            strInoutLen = len(inout.getInout())
            if strInoutLen>self.inoutMaxLen:
                self.portMaxLen = strInoutLen
        self.inoutList = inoutList


    def getStrLib(self):
        pass

    def getStrMap(self):
        pass
    def parseFile(self,fileName):
        pass

class componentVHDL(component):

    def addGenericStr(self,portName,portType,defaultValue):
        tmp = genericPortVHDL(portName,portType,defaultValue)
        strLen = len(portName)
        if strLen>self.portMaxLen:
            self.portMaxLen = strLen
        self.genericList.append(tmp)

    def getStrGeneric(self):
        listOut = []
        if (self.genericList != []) :
            listOut.append("\tgeneric (\n")
            for gen in self.getGeneric():
                for strAl in gen.getStrAligned(self.portMaxLen):
                    listOut.append("\t\t"+strAl+"\n")
            listOut[-1] = listOut[-1][:-2]+"\n"
            listOut.append("\t);\n")
        return listOut

    def getStrEntity(self):
        listOut = ["\tport (\n"]
        for port in self.inoutList:
            for strAl in port.getStrAligned(self.portMaxLen,self.inoutMaxLen):
                listOut.append("\t\t"+strAl+"\n")
        listOut[-1] = listOut[-1][:-2]+"\n"
        listOut.append("\t);\n")
        return listOut

    def getStrUse(self):
        return ["\tFOR ALL : "+self.getName()+" USE ENTITY "+self.getLib()+\
                "."+self.getName()+";\n"]

    def getStrMap(self):
        strOut = ["\t"+self.getName()+"0 : "+self.getName()+"\n"]
        if self.genericList != []:
            strOut += ["\t\tgeneric map (\n"]
            for gen in self.genericList:
                genNameLen = len(gen.getName())
                strOut += ["\t\t\t"+gen.getName()+" "*(self.portMaxLen-genNameLen)+\
                            " => "+gen.getName()+",\n"]
            strOut[-1] = strOut[-1][:-2]+"\n"
            strOut += ["\t\t)\n"]
        strOut += ["\t\tport map(\n"]
        for inout in self.inoutList:
            inoutNameLen = len(inout.getName())
            strOut += ["\t\t\t"+inout.getName()+" "*(self.portMaxLen-inoutNameLen)+\
                        " => "+inout.getName()+",\n"]
        strOut[-1] = strOut[-1][:-2]+"\n"
        strOut += ["\t\t);\n"]
        return strOut

    def getStrLib(self):
        return ["LIBRARY " +self.getLib()+";\n"]

    def getStrComponent(self):
        strOut =["component "+self.getName()+"\n"]
        strOut += self.getStrGeneric()
        strOut += self.getStrEntity()
        strOut += ["end component;\n"]
        for ind in range(len(strOut)):
            strOut[ind] = "\t"+strOut[ind]
        return strOut

    def parseLib(self, fileName):
        libName = re.compile(r"\\[\w]+_lib\\",re.I)
        resLib = libName.search(fileName)
        if resLib != None:
            self.setLib(resLib.group()[1:-1])
        else:
            self.setLib("SomeLib")

    def parseGenerics(self, genericStr):
        openParPlace = genericStr.find("(")
        closeParPlace = genericStr.rfind(")")
        # Checking for empty generics list
        if (openParPlace == -1 or closeParPlace == -1):
            return
        genericContent = genericStr[openParPlace+1:closeParPlace]
        # Generic list creation
        genericList = genericContent.split(";")
        for gen in genericList:
            partLst = gen.split(":")
            # First - parameter name, second - type, last - default value
            if len(partLst) > 1:
                parName = partLst[0].strip(" ")
                parType = partLst[1].strip(" ")
                if len(partLst) == 3:
                    parDefVal = partLst[2]
                    # Removing = sign
                    parDefVal = parDefVal.strip("=")
                    parDefVal = parDefVal.strip(" ")
                else:
                    parDefVal = ""
                self.addGenericStr(parName, parType, parDefVal)

    def parsePorts(self, portString):
        openParPlace = portString.find("(")
        closeParPlace = portString.rfind(")")
        # Checking for empty port list
        if (openParPlace == -1 or closeParPlace == -1):
            return
        genericContent = portString[openParPlace+1:closeParPlace]
        # Generic list creation
        genericList = genericContent.split(";")
        for gen in genericList:
            partLst = gen.split(":")
            # First - port name, second - type with inout type
            if len(partLst) > 1:
                portName = partLst[0].strip()
                typeWords = partLst[1].split()
                portInout = typeWords[0]
                portType = " ".join(typeWords[1:])
                self.addInoutStr(portName, portType, portInout)

    def parseEntity(self, entityFile):
        entityStr = ""
        with open(entityFile, "r") as f:
            # Entity begining searching
            entNameRE = re.compile(r"(?<=entity)[ \t]+[\w]+[ \t]+(?=is)",re.I)
            entName = None
            line = None
            while (entName == None and line != ""):
                line = f.readline()
                entName = entNameRE.search(line)
            if entName == None:
                self.name = "someEnt"
            else:
                self.name = entName.group().strip()
            # Entity end searching
            entEndER = re.compile(r"\bend\b",re.I)
            entEnd = None
            while(entEnd == None and line != ""):
                line = f.readline()
                # Comment removing
                commentBeg = line.find("--")
                lineSearch = line[:commentBeg]
                entEnd = entEndER.search(lineSearch)
                if (entEnd == None):
                    # Adding to entity string
                    entityStr += lineSearch

        portRE = re.compile(r"\bport\b",re.I);
        entSplit = portRE.split(entityStr)
        # Parsing of generic and port list
        if (len(entSplit) == 2):
            self.parseGenerics(entSplit[0])
            self.parsePorts(entSplit[1])
        elif (len(entSplit) == 1):
            self.parsePorts(entSplit[0])




    def parseFile(self, fileName):
        # Getting library
        self.parseLib(fileName)
        # Getting entity content
        self.parseEntity(fileName)

def instantiateEntity(entityFileName,bufferFileName,currLine):
    if entityFileName[-4:]=='.vhd':
        instantiateEntityVHDL(entityFileName,bufferFileName,currLine)

def instantiateEntityVHDL(entityFileName,bufferFileName,currLine):
    newInst = componentVHDL("")
    newInst.parseFile(entityFileName)
    buffFile = open(bufferFileName,"r+")
    currBuffer = buffFile.readlines()
    buffFile.close()
    libRe = re.compile(r"(?<=library)[\w \t]+",re.I)
    entRe = re.compile(r"entity",re.I)
    compRe = re.compile(r"end[\t ]+component",re.I)
    useRe = re.compile(r"USE[ \t]+ENTITY",re.I)
    archRe = re.compile(r"begin",re.I)
    libLine = -1
    libExist = False
    archLine = -1
    compLine = -1
    useLine = -1
    libLower = newInst.getLib().lower()
    for i in range(len(currBuffer)):
        line = currBuffer[i]
        resLib = libRe.search(line)
        if resLib != None:
            libLine = i
            lib = resLib.group()
            lib = lib.strip()
            if lib.lower() == libLower:
                libExist = True
        resComp = compRe.search(line)
        if resComp != None:
            compLine = i
        useComp = useRe.search(line)
        if useComp != None:
            useLine = i
        resArch = archRe.match(line)
        if resArch != None:
            archLine = i
            break
    newFileBuff = []
    strPtr = 0
    #Library declaration
    if (libLine >= 0) and not(libExist):
        newFileBuff += currBuffer[:libLine+1]
        newFileBuff += newInst.getStrLib()
        strPtr = libLine+1
    #Component declaration
    if compLine>=0:
        newFileBuff += currBuffer[strPtr:compLine+1]
        newFileBuff += newInst.getStrComponent()
        strPtr = compLine+1
    elif archLine>= 0:
        newFileBuff += currBuffer[strPtr:archLine]
        newFileBuff += newInst.getStrComponent()
        strPtr = archLine
    #Component mapping before architecture
    if useLine>=0:
        newFileBuff += currBuffer[strPtr:useLine+1]
        newFileBuff += newInst.getStrUse()
        strPtr = useLine+1
    elif archLine>= 0:
        newFileBuff += currBuffer[strPtr:archLine]
        newFileBuff += newInst.getStrUse()
        strPtr = archLine
    #Block instance writing
    if currLine>=0:
        newFileBuff += currBuffer[strPtr:currLine-1]
        newFileBuff += newInst.getStrMap()
        strPtr = currLine-1
    newFileBuff += currBuffer[strPtr:]

    strOut = ""
    for b in newFileBuff:
        strOut += b

    with open(bufferFileName,"rb+") as file:
        file.write(bytearray(strOut.encode('UTF-8')))


import sys
if __name__ == "__main__":
    strUsing = "Using of script:\n\tpython instantiateEntityVHDL.py input_file output_file str_num"

    if len(sys.argv)!=4:
        print(strUsing)
        sys.exit(2)
    instantiateEntity(sys.argv[1],sys.argv[2],int(sys.argv[3]))


