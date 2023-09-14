'''
This module contaims the schemas
expected in HTTP responses.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* pydantic
'''

# Import system libs
from pydantic import BaseModel

#######################################

class comboBox(BaseModel):
    defaultValue: str
    menuItems: list

class protocolInfo(BaseModel):
    name: str
    data: dict

class dataSourceInfo(BaseModel):
    name: str
    plc_ip: str
    plc_port: int
    cycletime: int
    timeout: int
    collector_id: int
    protocol: protocolInfo

class protocol(protocolInfo):
    id: int

class dataSource(dataSourceInfo):
    active: bool
    pending: bool
    protocol: protocol