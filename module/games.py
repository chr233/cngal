'''
# @Author       : Chr_
# @Date         : 2020-11-27 23:42:40
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-28 00:58:05
# @Description  : 读取games.txt
'''

from os import getcwd, path


from .log import get_logger

logger = get_logger('Games')

default_path = path.join(getcwd(), 'games.txt')


def get_games(cpath: str = default_path) -> list:
    '''
    读取games.txt

    参数:
        [path]:配置文件路径,默认为games.txt
    返回:
        list:appid 列表
    '''
    logger.info('开始读取游戏列表')
    errors = 0
    applist = []
    try:
        with open(cpath, 'r+', encoding='utf-8') as f:
            for line in f:
                l = line.strip()
                try:
                    num_s, *_ = l.split()
                    num = int(num_s)
                    applist.append(num)
                except ValueError:
                    errors += 1
                    logger.debug(f'读取文件出错 {l}')
    except FileNotFoundError:
        logger.error(f'游戏列表文件[{cpath}]不存在')
        with open(cpath, 'w+', encoding='utf-8') as f:
            f.writelines(['# 脚本只会读取数字，后面的文字仅作注释',
                          '654260	旧手表'])
        logger.error('已生成示例文件,请修改后重新运行程序')

    if applist:
        logger.debug(f'失败计数 {errors}')
    return applist