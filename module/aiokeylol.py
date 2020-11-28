# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-06-30 05:08:57
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-28 02:32:05
# @Description  : 对接Keylol的API【异步】
'''

import asyncio
from httpx import AsyncClient

from .log import get_logger
from .static import URLs
from .aionet import adv_http_get_keylol


logger = get_logger('Keylol')


async def get_games_tags(appids: list) -> dict:
    '''
    异步读取Steam愿望单

    参数:
        appids: appid列表
    返回：
        dict: 游戏信息字典
    '''
    gameinfo = {}
    cut = 10
    if appids:
        subs = [appids[i:i+cut] for i in range(0, len(appids), cut)]
        for i, sub in enumerate(subs, 1):
            async with AsyncClient() as client:
                tasks = {
                    asyncio.create_task(_get_game_tags(client=client, appid=i)) for i in sub
                }
                await asyncio.wait(tasks)
            for task in tasks:
                gameinfo.update(task.result())
            if i < len(subs):
                logger.info(f'当前进度{i}/{len(subs)},暂停10秒')
                await asyncio.sleep(10)
                if i % 3 == 0:
                    logger.info('歇一会,暂停20秒')
                    await asyncio.sleep(20)
            else:
                logger.info(f'当前进度{i}/{len(subs)},已完成')
    return (gameinfo)


async def _get_game_tags(client: AsyncClient, appid: int) -> dict:
    '''
    其乐API,读取steam游戏信息

    参数:
        appid: appid
    返回:
        dict: 包含游戏附加信息的dict
    '''
    url = URLs.Keylol_Get_Game_Info % appid
    jd = await adv_http_get_keylol(client=client,
                                   url=url,
                                   retrys=5)
    result = {}
    if jd:
        if jd.get('name') == '无法显示游戏信息':
            logger.warning(f'无法读取{appid}的信息,请检查输入是否有误')
        else:
            result[appid] = {
                'name': jd.get('name', '【读取出错】'),
                'link': URLs.Steam_Store_App % appid,
                'picture':  URLs.Steam_Game_Pic_SM % appid,
                'description': jd.get('description', '【读取出错】'),
                'tags': jd.get('tags', []),
                'developer': jd.get('developer', []),
                'publisher': jd.get('publisher', []),
                'release': jd.get('release'),
                'card': len(jd.get('card', [])) > 0,
                'free': '免费游玩' in jd.get('genre', [])
            }
    return (result)
