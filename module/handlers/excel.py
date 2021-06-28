# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-07-06 18:22:37
# @LastEditors  : Chr_
# @LastEditTime : 2021-06-27 15:43:04
# @Description  : 输出Xlsx文件
'''

from xlsxwriter import Workbook

from ..log import get_logger
from ..utils import is_lowest_str, get_output_path

logger = get_logger('Excel')


def handler(wishdict: dict, index: list, symbol: str):
    '''
    这个函数将会被crawer调用

    参数:
        wishdict: 愿望单字典
    '''
    p = get_output_path('swh-excel.xlsx')
    try:
        wb = Workbook(p)
        formater(wishdict, index, symbol, wb)
        wb.close()
    except Exception as e:
        logger.error(f'遇到意外错误 {e}')

    logger.info(f'写入文件到 {p}')


def formater(wishdict: dict, index: list, symbol: str, wb: Workbook):
    '''
    这个函数用于从愿望单字典中提取数据

    参数:
        wishdict: 愿望单字典
    '''

    fmt = wb.add_format({'font_name': '微软雅黑', 'align': 'center'})

    ws = wb.add_worksheet(name='Steam Wishlist Helper')

    ws.set_column('A:A', 10, fmt)
    ws.set_column('B:B', 20, fmt)
    ws.set_column('C:C', 60, fmt)
    ws.set_column('D:D', 8, fmt)
    ws.set_column('E:E', 8, fmt)
    ws.set_column('F:F', 8, fmt)
    ws.set_column('G:G', 8, fmt)
    ws.set_column('H:H', 8, fmt)
    ws.set_column('I:I', 8, fmt)
    ws.set_column('J:J', 15, fmt)
    ws.set_column('K:K', 15, fmt)
    ws.set_column('L:L', 20, fmt)
    ws.set_column('M:M', 100, fmt)
    
    ws.write(0, 0, '商店链接')
    ws.write(0, 1, 'Appid')
    ws.write(0, 2, '游戏名')
    ws.write(0, 3, '卡牌')
    ws.write(0, 4, f'现价({symbol})')
    ws.write(0, 5, f'原价({symbol})')
    ws.write(0, 6, '折扣')
    ws.write(0, 7, f'史低({symbol})')
    ws.write(0, 8, '史低')
    ws.write(0, 9, '开发商')
    ws.write(0, 10, '发行商')
    ws.write(0, 11, '发售日期')
    ws.write(0, 12, '游戏简介')
    if wishdict:
        for col, (appid, detail) in enumerate(wishdict.items(), 1):
            link = f'https://store.steampowered.com/app/{appid}'
            name = detail.get('name', '')
            card = '有' if detail.get('card', False) else ''
            dev = ','.join(detail.get('developer',''))
            pub = ','.join(detail.get('publisher',''))
            release = detail.get('release','')
            desc = detail.get('description','')
            if 'price' in detail:
                price = detail['price']
                p_now = price.get('current')
                p_old = price.get('origin')
                p_cut = price.get('current_cut')
                p_low = price.get('lowest')
                shidi = is_lowest_str(price.get('is_lowest',0))
                discount = f'-{p_cut}%'
            else:
                shidi = '-'
                discount = '-'
                p_now = '-'
                p_low = '-'
                p_old = '-'
            if detail['free']:
                p_now = '免费'
                shidi = '免费'
                p_low = '免费'
                p_old = '免费'
            if p_now == -1:
                p_now = '-'
                p_old = '-'
                p_low = '-'

            ws.write(col, 0, link)
            ws.write(col, 1, appid)
            ws.write(col, 2, name)
            ws.write(col, 3, card)
            ws.write(col, 4, p_now)
            ws.write(col, 5, p_old)
            ws.write(col, 6, discount)
            ws.write(col, 7, p_low)
            ws.write(col, 8, shidi)
            ws.write(col, 9, dev)
            ws.write(col, 10, pub)
            ws.write(col, 11, release)
            ws.write(col, 12, desc)
    else:
        ws.write(1, 1, '游戏列表空,请检查过滤器设置以及是否将愿望单公开')
