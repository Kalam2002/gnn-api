from pydantic import BaseModel
from typing import List

class Flow(BaseModel):
    src_ip: str
    src_port: int
    dst_ip: str
    dst_port: int
    proto: str
    service: str
    duration: float
    src_bytes: float
    dst_bytes: float
    conn_state: str
    src_pkts: float
    dst_pkts: float

class FlowRequest(BaseModel):
    flows: List[Flow]