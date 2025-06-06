# opcua-srtm
OpcUa client to access SRTM monitoring data
- This python script can be used to access OpcUa data from the ATLAS SRTM
- Currently, the code connects to the SRTM OpcUa socket and then launches a window to display various data values
- The socket connection currently seems very flaky, and the code tests for socket connectivity before accessing any data

## Installation
pip install opcua

## Running
python client-srtm.py
