# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-11-01 00:00:47
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-28 00:57:43
# @Description  : 启动入口
'''

import asyncio

from module.games import get_games
from module.config import get_config
from module.crawer import Crawer
from module.log import get_logger
from module.version import check_update

logger = get_logger('Main')


async def main():
    cfg = get_config()
    games = get_games()
    if  not cfg and not games:
        logger.info('读取配置文件失败')
        input('运行结束,按回车键退出……')
        return

    c = Crawer(cfg, games)

    tasks = [
        asyncio.create_task(check_update(cfg)),  # 异步检查更新
        asyncio.create_task(c.start())
    ]
    await asyncio.wait(tasks)

    try:
        if (cfg['other']['wait_screen']):
            input('运行结束,按回车键退出……')
        else:
            print('运行结束,程序退出')
    except KeyboardInterrupt:
        pass
        

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
