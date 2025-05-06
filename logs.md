2025-05-04T22:10:01.524827493Z   File "/opt/render/project/src/app.py", line 21, in get_posts
2025-05-04T22:10:01.524830193Z     posts = await parser.get_posts(channel_list, limit, days_back)
2025-05-04T22:10:01.524832663Z             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:01.524838603Z   File "/opt/render/project/src/telegram_parser/parser.py", line 24, in get_posts
2025-05-04T22:10:01.524841383Z     await client.start(phone=self.phone)
2025-05-04T22:10:01.524843894Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/auth.py", line 186, in _start
2025-05-04T22:10:01.524846324Z     await self.send_code_request(phone, force_sms=force_sms)
2025-05-04T22:10:01.524849094Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/auth.py", line 446, in send_code_request
2025-05-04T22:10:01.524851624Z     result = await self(functions.auth.SendCodeRequest(
2025-05-04T22:10:01.524854104Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:01.524856554Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/users.py", line 30, in __call__
2025-05-04T22:10:01.524862594Z     return await self._call(self._sender, request, ordered=ordered)
2025-05-04T22:10:01.524865224Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:01.524867684Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/users.py", line 92, in _call
2025-05-04T22:10:01.524870404Z     result = await future
2025-05-04T22:10:01.524872884Z              ^^^^^^^^^^^^
2025-05-04T22:10:01.524875424Z telethon.errors.rpcerrorlist.FloodWaitError: A wait of 84280 seconds is required (caused by SendCodeRequest)
2025-05-04T22:10:07.929624484Z INFO:     83.50.76.252:0 - "GET /api/posts?channels=@temno&limit=10 HTTP/1.1" 500 Internal Server Error
2025-05-04T22:10:07.930962319Z ERROR:    Exception in ASGI application
2025-05-04T22:10:07.930976539Z Traceback (most recent call last):
2025-05-04T22:10:07.93097964Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py", line 403, in run_asgi
2025-05-04T22:10:07.93098346Z     result = await app(  # type: ignore[func-returns-value]
2025-05-04T22:10:07.93098687Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:07.93099067Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
2025-05-04T22:10:07.93099387Z     return await self.app(scope, receive, send)
2025-05-04T22:10:07.93099767Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:07.93100111Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 1054, in __call__
2025-05-04T22:10:07.93100465Z     await super().__call__(scope, receive, send)
2025-05-04T22:10:07.93100802Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/applications.py", line 112, in __call__
2025-05-04T22:10:07.93101151Z     await self.middleware_stack(scope, receive, send)
2025-05-04T22:10:07.93101517Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 187, in __call__
2025-05-04T22:10:07.931018361Z     raise exc
2025-05-04T22:10:07.93102177Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 165, in __call__
2025-05-04T22:10:07.931024901Z     await self.app(scope, receive, _send)
2025-05-04T22:10:07.931028621Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 62, in __call__
2025-05-04T22:10:07.931042751Z     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
2025-05-04T22:10:07.931045141Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
2025-05-04T22:10:07.931047271Z     raise exc
2025-05-04T22:10:07.931049541Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
2025-05-04T22:10:07.931051671Z     await app(scope, receive, sender)
2025-05-04T22:10:07.931054391Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 714, in __call__
2025-05-04T22:10:07.931056551Z     await self.middleware_stack(scope, receive, send)
2025-05-04T22:10:07.931058691Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 734, in app
2025-05-04T22:10:07.931060822Z     await route.handle(scope, receive, send)
2025-05-04T22:10:07.931063002Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 288, in handle
2025-05-04T22:10:07.931065112Z     await self.app(scope, receive, send)
2025-05-04T22:10:07.931067232Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 76, in app
2025-05-04T22:10:07.931069382Z     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
2025-05-04T22:10:07.931071472Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
2025-05-04T22:10:07.931073562Z     raise exc
2025-05-04T22:10:07.931075702Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
2025-05-04T22:10:07.931077832Z     await app(scope, receive, sender)
2025-05-04T22:10:07.931079952Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 73, in app
2025-05-04T22:10:07.931082862Z     response = await f(request)
2025-05-04T22:10:07.931084992Z                ^^^^^^^^^^^^^^^^
2025-05-04T22:10:07.931087112Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 301, in app
2025-05-04T22:10:07.931089222Z     raw_response = await run_endpoint_function(
2025-05-04T22:10:07.931091362Z                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:07.931093523Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 212, in run_endpoint_function
2025-05-04T22:10:07.931095632Z     return await dependant.call(**values)
2025-05-04T22:10:07.931097752Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:07.931099823Z   File "/opt/render/project/src/app.py", line 21, in get_posts
2025-05-04T22:10:07.931101993Z     posts = await parser.get_posts(channel_list, limit, days_back)
2025-05-04T22:10:07.931104123Z             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:07.931106813Z   File "/opt/render/project/src/telegram_parser/parser.py", line 24, in get_posts
2025-05-04T22:10:07.931108893Z     await client.start(phone=self.phone)
2025-05-04T22:10:07.931111003Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/auth.py", line 186, in _start
2025-05-04T22:10:07.931113113Z     await self.send_code_request(phone, force_sms=force_sms)
2025-05-04T22:10:07.931115243Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/auth.py", line 446, in send_code_request
2025-05-04T22:10:07.931117343Z     result = await self(functions.auth.SendCodeRequest(
2025-05-04T22:10:07.931119513Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:07.931125363Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/users.py", line 30, in __call__
2025-05-04T22:10:07.931141564Z     return await self._call(self._sender, request, ordered=ordered)
2025-05-04T22:10:07.931145604Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:07.931148984Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/users.py", line 92, in _call
2025-05-04T22:10:07.931152334Z     result = await future
2025-05-04T22:10:07.931155464Z              ^^^^^^^^^^^^
2025-05-04T22:10:07.931158944Z telethon.errors.rpcerrorlist.FloodWaitError: A wait of 84274 seconds is required (caused by SendCodeRequest)
2025-05-04T22:10:21.112836855Z INFO:     83.50.76.252:0 - "GET /api/posts?channels=temno&limit=10 HTTP/1.1" 500 Internal Server Error
2025-05-04T22:10:21.114833858Z ERROR:    Exception in ASGI application
2025-05-04T22:10:21.114855999Z Traceback (most recent call last):
2025-05-04T22:10:21.114862879Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py", line 403, in run_asgi
2025-05-04T22:10:21.114868759Z     result = await app(  # type: ignore[func-returns-value]
2025-05-04T22:10:21.114872639Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:21.114876479Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
2025-05-04T22:10:21.114881279Z     return await self.app(scope, receive, send)
2025-05-04T22:10:21.114885129Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:21.1148894Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 1054, in __call__
2025-05-04T22:10:21.11489338Z     await super().__call__(scope, receive, send)
2025-05-04T22:10:21.11489714Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/applications.py", line 112, in __call__
2025-05-04T22:10:21.11490147Z     await self.middleware_stack(scope, receive, send)
2025-05-04T22:10:21.1149053Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 187, in __call__
2025-05-04T22:10:21.11490911Z     raise exc
2025-05-04T22:10:21.11491355Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 165, in __call__
2025-05-04T22:10:21.11491731Z     await self.app(scope, receive, _send)
2025-05-04T22:10:21.11492119Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 62, in __call__
2025-05-04T22:10:21.114927401Z     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
2025-05-04T22:10:21.114931191Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
2025-05-04T22:10:21.114935541Z     raise exc
2025-05-04T22:10:21.114939501Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
2025-05-04T22:10:21.114943441Z     await app(scope, receive, sender)
2025-05-04T22:10:21.114949381Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 714, in __call__
2025-05-04T22:10:21.114953331Z     await self.middleware_stack(scope, receive, send)
2025-05-04T22:10:21.114957731Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 734, in app
2025-05-04T22:10:21.114961511Z     await route.handle(scope, receive, send)
2025-05-04T22:10:21.114965482Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 288, in handle
2025-05-04T22:10:21.114979742Z     await self.app(scope, receive, send)
2025-05-04T22:10:21.114982632Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 76, in app
2025-05-04T22:10:21.114984902Z     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
2025-05-04T22:10:21.114987312Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
2025-05-04T22:10:21.114989912Z     raise exc
2025-05-04T22:10:21.114992802Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
2025-05-04T22:10:21.114995582Z     await app(scope, receive, sender)
2025-05-04T22:10:21.114997803Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 73, in app
2025-05-04T22:10:21.115002003Z     response = await f(request)
2025-05-04T22:10:21.115007233Z                ^^^^^^^^^^^^^^^^
2025-05-04T22:10:21.115009903Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 301, in app
2025-05-04T22:10:21.115012573Z     raw_response = await run_endpoint_function(
2025-05-04T22:10:21.115015123Z                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:21.115017763Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 212, in run_endpoint_function
2025-05-04T22:10:21.115020343Z     return await dependant.call(**values)
2025-05-04T22:10:21.115023113Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:21.115025723Z   File "/opt/render/project/src/app.py", line 21, in get_posts
2025-05-04T22:10:21.115028123Z     posts = await parser.get_posts(channel_list, limit, days_back)
2025-05-04T22:10:21.115030583Z             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:21.115033763Z   File "/opt/render/project/src/telegram_parser/parser.py", line 24, in get_posts
2025-05-04T22:10:21.115036053Z     await client.start(phone=self.phone)
2025-05-04T22:10:21.115038284Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/auth.py", line 186, in _start
2025-05-04T22:10:21.115040653Z     await self.send_code_request(phone, force_sms=force_sms)
2025-05-04T22:10:21.115042904Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/auth.py", line 446, in send_code_request
2025-05-04T22:10:21.115045434Z     result = await self(functions.auth.SendCodeRequest(
2025-05-04T22:10:21.115048204Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:21.115050924Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/users.py", line 30, in __call__
2025-05-04T22:10:21.115069874Z     return await self._call(self._sender, request, ordered=ordered)
2025-05-04T22:10:21.115073025Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:21.115075445Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/users.py", line 92, in _call
2025-05-04T22:10:21.115077985Z     result = await future
2025-05-04T22:10:21.115080485Z              ^^^^^^^^^^^^
2025-05-04T22:10:21.115083145Z telethon.errors.rpcerrorlist.FloodWaitError: A wait of 84260 seconds is required (caused by SendCodeRequest)
2025-05-04T22:10:28.637437701Z INFO:     83.50.76.252:0 - "GET /api/posts?channels=@durov&limit=10 HTTP/1.1" 500 Internal Server Error
2025-05-04T22:10:28.638735525Z ERROR:    Exception in ASGI application
2025-05-04T22:10:28.638744625Z Traceback (most recent call last):
2025-05-04T22:10:28.638749326Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py", line 403, in run_asgi
2025-05-04T22:10:28.638790847Z     result = await app(  # type: ignore[func-returns-value]
2025-05-04T22:10:28.638795067Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:28.638798527Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
2025-05-04T22:10:28.638801937Z     return await self.app(scope, receive, send)
2025-05-04T22:10:28.638806887Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:28.638810607Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/applications.py", line 1054, in __call__
2025-05-04T22:10:28.638813877Z     await super().__call__(scope, receive, send)
2025-05-04T22:10:28.638816077Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/applications.py", line 112, in __call__
2025-05-04T22:10:28.638818227Z     await self.middleware_stack(scope, receive, send)
2025-05-04T22:10:28.638820567Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 187, in __call__
2025-05-04T22:10:28.638822757Z     raise exc
2025-05-04T22:10:28.638824937Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 165, in __call__
2025-05-04T22:10:28.638827197Z     await self.app(scope, receive, _send)
2025-05-04T22:10:28.638829357Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 62, in __call__
2025-05-04T22:10:28.638832078Z     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
2025-05-04T22:10:28.638834638Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
2025-05-04T22:10:28.638836808Z     raise exc
2025-05-04T22:10:28.638838918Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
2025-05-04T22:10:28.638841038Z     await app(scope, receive, sender)
2025-05-04T22:10:28.638844158Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 714, in __call__
2025-05-04T22:10:28.638846568Z     await self.middleware_stack(scope, receive, send)
2025-05-04T22:10:28.638848768Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 734, in app
2025-05-04T22:10:28.638850938Z     await route.handle(scope, receive, send)
2025-05-04T22:10:28.638853038Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 288, in handle
2025-05-04T22:10:28.638855138Z     await self.app(scope, receive, send)
2025-05-04T22:10:28.638857248Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 76, in app
2025-05-04T22:10:28.638861448Z     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
2025-05-04T22:10:28.638863609Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
2025-05-04T22:10:28.638865718Z     raise exc
2025-05-04T22:10:28.638867829Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
2025-05-04T22:10:28.638870139Z     await app(scope, receive, sender)
2025-05-04T22:10:28.638872249Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 73, in app
2025-05-04T22:10:28.638875019Z     response = await f(request)
2025-05-04T22:10:28.638877109Z                ^^^^^^^^^^^^^^^^
2025-05-04T22:10:28.638879169Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 301, in app
2025-05-04T22:10:28.638885669Z     raw_response = await run_endpoint_function(
2025-05-04T22:10:28.638887819Z                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:28.638889889Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/fastapi/routing.py", line 212, in run_endpoint_function
2025-05-04T22:10:28.638892049Z     return await dependant.call(**values)
2025-05-04T22:10:28.638894169Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:28.638896409Z   File "/opt/render/project/src/app.py", line 21, in get_posts
2025-05-04T22:10:28.638898539Z     posts = await parser.get_posts(channel_list, limit, days_back)
2025-05-04T22:10:28.63890073Z             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:28.638903439Z   File "/opt/render/project/src/telegram_parser/parser.py", line 24, in get_posts
2025-05-04T22:10:28.638905519Z     await client.start(phone=self.phone)
2025-05-04T22:10:28.63890765Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/auth.py", line 186, in _start
2025-05-04T22:10:28.63890972Z     await self.send_code_request(phone, force_sms=force_sms)
2025-05-04T22:10:28.6389118Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/auth.py", line 446, in send_code_request
2025-05-04T22:10:28.63891386Z     result = await self(functions.auth.SendCodeRequest(
2025-05-04T22:10:28.63891594Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:28.6389181Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/users.py", line 30, in __call__
2025-05-04T22:10:28.6389329Z     return await self._call(self._sender, request, ordered=ordered)
2025-05-04T22:10:28.63893701Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-05-04T22:10:28.63894064Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/telethon/client/users.py", line 92, in _call
2025-05-04T22:10:28.63894408Z     result = await future
2025-05-04T22:10:28.638947331Z              ^^^^^^^^^^^^
2025-05-04T22:10:28.638949621Z telethon.errors.rpcerrorlist.FloodWaitError: A wait of 84253 seconds is required (caused by SendCodeRequest)