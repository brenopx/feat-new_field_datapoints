'''
This module executes the Backend
of the configuration tool.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* fastapi
'''

# Import system libs
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import custom libs
from . import database
from .env import Enviroment as Env
from .crud import Tuser
from .database import SessionManager, engine
from .user_auth import schemas as auth_schemas
from .user_auth import routes as auth_routes
from .plc_datasource import schemas as ds_schemas
from .plc_datasource import routes as ds_routes
from .plc_datapoint import schemas as dp_schemas
from .plc_datapoint import routes as dp_routes


#######################################

database.Base.metadata.create_all(bind=engine)

app = FastAPI(root_path=f"{Env.API_NAME}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check for users and create a default one if it is empty
with SessionManager() as db:
    if (len(Tuser.get_all(db))==0):
        admin_usr = auth_schemas.UserCreate(name='admin', password='admin')
        Tuser.create(db,admin_usr)

# Application Routes 

### Authentication
app.add_api_route("/login",
    methods=["POST"], response_model=auth_schemas.LoginSucess,
    endpoint=auth_routes.authentication)

### Defaults
app.add_api_route("/protocol_defaults",
    methods=["GET"], response_model=ds_schemas.comboBox,
    endpoint=ds_routes.get_protocol_defaults)

app.add_api_route("/datasource_defaults/{prot_name}",
    methods=["GET"], response_model=ds_schemas.dataSourceInfo,
    endpoint=ds_routes.get_datasource_defaults)

### DataSources
app.add_api_route("/datasource",
    methods=["POST"], response_model=ds_schemas.dataSource,
    endpoint=ds_routes.create_datasource)

app.add_api_route("/datasource/{ds_name}",
    methods=["GET"], response_model=ds_schemas.dataSource,
    endpoint=ds_routes.get_datasource_by_name)

app.add_api_route("/datasources",
    methods=["GET"], response_model=List[ds_schemas.dataSource],
    endpoint=ds_routes.get_datasources)

app.add_api_route("/datasources/range/{ini}-{end}",
    methods=["GET"], response_model=List[ds_schemas.dataSource],
    endpoint=ds_routes.get_datasources_by_range)