# Nop_Commerce

# Introduction
Performance tests based on [locust.io](https://docs.locust.io/en/stable/) tool.

## Installation process
1. Install at least Python 3.8
2. Clone project
3. Switch to project root
4. Create virtualenv `virtualenv --python=<path to python> venv`
5. Activate virtualenv `. venv/bin/activate`
6. Install requirements run `pip install -r requirements.txt` from root directory

## Local test with web interface
1. Create a `.env` file inside `NopCommerce` with the desired configuration.
2. Set in the `.env` file system variables:
    - BASE_URL
    - ENV_TYPE
    - WAIT_TIME_MIN
    - WAIT_TIME_MAX
    - NOP_ANTIFORGERY
    - NOP_CUSTOMER
    - CF_CLEARANCE
3. Configure `Run/Debug Configuration` in the IDE.
   - Set `Python interpriter` which located in the `.venv` folder
   - Choose from the dropdown `Run scrimp or module` -> `module` -> write `locust`
   - Set path to the `locustfile.py` - > `-f src/locustfiles/locustfile.py`
   - Set `Working directory`
   - Set path to the `.env`  file location in the project
   - Click `Apply` button
4. To run test click on the `Run` button is in the top right corner. 
5. Open a web browser and enter the following in the URL field `localhost:8089`.
6. In the locust web interface you can enter or change the following fields:
   - Number of users
   - Spawn rate
   - Host
   - Advanced option `Run time` sets the duration of the test execution
   - After test execution, for the download report, move to `Download data` and click on 'Download Report'

###.env_example
```bash
LOCUSTFIELE=src/locustfiles/locustfile.py
BASE_URL=nopcommerce.com
ENV_TYPE=demo
WAIT_TIME_MIN=2
WAIT_TIME_MAX=5
NOP_ANTIFORGERY=str<Get fro web browser dev tool -> Application -> Cookies >
NOP_CUSTOMER=str<Get fro web browser dev tool -> Application -> Cookies >
CF_CLEARANCE=str<Get fro web browser dev tool -> Application -> Cookies >
```