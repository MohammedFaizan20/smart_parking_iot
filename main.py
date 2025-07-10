import uvicorn
from fastapi import Request,FastAPI
from api.user.app import public_router as public_app
from api.auth_app.app import router as auth_app

from fastapi_auth_middleware import AuthMiddleware
import logging,time,os,datetime,json
from fastapi.middleware.cors import CORSMiddleware
from db.config import settings



# exclusive url which one not check aouthentication by middleware
excluded_urls_list = ["/parking/auth/api/docs", "/parking/auth/openapi.json"]
#
# # private (auth) router mapping
# isauthenticate = FastAPI(docs_url="/api/docs" if settings.allow_swagger_url == True else None)
# isauthenticate.include_router(authenticate_app, prefix="", tags=["Internal 1"])
# isauthenticate.add_middleware(AuthMiddleware, verify_header=verify_authorization_header, auth_error_handler=handle_auth_error, excluded_urls = excluded_urls_list)
#
# # middleware log configurations for private router
# LOG_DIR = settings.log_path
# if not os.path.exists(LOG_DIR):
#     os.mkdir(LOG_DIR)
#
# # auth router log and response body encryption base on .env condition
# @isauthenticate.middleware("http")
# async def log_requests(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     if (settings.auth_response_encode == True and request.url.path not in excluded_urls_list):
#         res_body = b''
#         encryption_base_key = request.headers.get("authorization").split(" ")[1]
#         async for chunk in response.body_iterator:
#             res_body += chunk
#         req_body = response_encryption(res_body,key=encryption_base_key[-32:])
#         result = {"success":True,"data":req_body.decode()}
#     process_time = (time.time() - start_time) * 1000
#     formatted_process_time = '{0:.2f}'.format(process_time)
#     logging.basicConfig(handlers=[logging.FileHandler(filename="{}/{}.log".format(LOG_DIR, datetime.datetime.utcnow().strftime("%Y-%b-%d")),
#                                                         encoding='utf-8', mode='a+')],
#                                                         format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%F %A %T",
#                                                         level=logging.INFO)
#     logging.info(f"start request path={request.url} completed_in={formatted_process_time}ms status_code={response.status_code}")
#     if (settings.auth_response_encode == True and request.url.path not in excluded_urls_list):
#         return Response(content=json.dumps(result).encode('utf-8'), status_code=response.status_code, media_type="application/json")
#     else:
#         return response
#

# public router mapping
ispublic = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")
ispublic.include_router(public_app, prefix="", tags=["Internal"])
ispublic.include_router(auth_app, prefix="", tags=["Internal"])

# ispublic.include_router(router)

# public router log and response body encryption base on .env condition
@ispublic.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    return response

# fast-api app creation
app = FastAPI(openapi_url="/openapi.json")
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)

# All router mount with fast-api
# app.mount(path="/ai/auth", app=isauthenticate)  # auth router expects an authorization header.
app.mount(path="/parking/public", app=ispublic)  # public router

# health check Api's
@app.get("/health")
async def heath_check():
    return {"success":True}

# name-space for local run in pycharm
if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=9000)


