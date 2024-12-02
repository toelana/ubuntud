# -*- coding: utf-8 -*-
# @Time     :2023/12/26 17:00
# @Author   :ym
# @File     :main.py
# @Software :PyCharm
import asyncio
import random
import ssl
import json
import time
import uuid
from loguru import logger
from websockets_proxy import Proxy, proxy_connect


async def connect_to_wss(socks5_proxy, user_id):
    device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, socks5_proxy))
    logger.info(device_id)
    while True:
        try:
            await asyncio.sleep(random.randint(1, 10) / 10)
            custom_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            uri = "wss://proxy.wynd.network:4650/"
            server_hostname = "proxy.wynd.network"
            proxy = Proxy.from_url(socks5_proxy)
            async with proxy_connect(uri, proxy=proxy, ssl=ssl_context, server_hostname=server_hostname,
                                     extra_headers=custom_headers) as websocket:
                async def send_ping():
                    while True:
                        send_message = json.dumps(
                            {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                        logger.debug(send_message)
                        await websocket.send(send_message)
                        await asyncio.sleep(20)

                # asyncio.create_task(send_http_request_every_10_seconds(socks5_proxy, device_id))
                await asyncio.sleep(1)
                asyncio.create_task(send_ping())

                while True:
                    response = await websocket.recv()
                    message = json.loads(response)
                    logger.info(message)
                    if message.get("action") == "AUTH":
                        auth_response = {
                            "id": message["id"],
                            "origin_action": "AUTH",
                            "result": {
                                "browser_id": device_id,
                                "user_id": user_id,
                                "user_agent": custom_headers['User-Agent'],
                                "timestamp": int(time.time()),
                                "device_type": "extension",
                                "version": "2.5.0"
                            }
                        }
                        logger.debug(auth_response)
                        await websocket.send(json.dumps(auth_response))

                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        logger.debug(pong_response)
                        await websocket.send(json.dumps(pong_response))
        except Exception as e:
            logger.error(e)
            logger.error(socks5_proxy)


async def main():
    # TODO 修改user_id
    _user_id = '2oRC5IKxfweW3db497nQyvNAOZz'
    # TODO 修改代理列表
    socks5_proxy_list = [
        'socks5://miell1-zone-custom-region-US-session-79107555-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-73883439-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-14918103-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-87669502-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-24365825-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-12988173-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-50792872-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-43360115-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-29367105-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-12284259-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-39840941-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-52080588-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-76762677-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-75548364-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-73057024-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-66539438-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-97311802-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-90600602-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-97838641-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-20481353-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-11537655-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-63926214-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-49814966-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-31385733-sessTime-179:miell1@as.711proxy.com:10000,socks5://miell1-zone-custom-region-US-session-24539132-sessTime-179:miell1@as.711proxy.com:10000',
    ]
    tasks = [asyncio.ensure_future(connect_to_wss(i, _user_id)) for i in socks5_proxy_list]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    # # 运行主函数
    asyncio.run(main())
