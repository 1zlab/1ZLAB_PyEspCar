#!/usr/bin/python3  
# -*- coding: utf-8 -*-  

'''
同步当前的目录下所有的.py文件到ESP32
'''
import glob
import subprocess
import sys

# ESP32 端口设备编号
dev_port_name = '/dev/ttyUSB0'
if len(sys.argv) > 1:
    # 更新设备名称
    dev_port_name = sys.argv[1]

# 白名单正则样式
white_list = ['*.txt', '*.py']
# 黑名单
black_list = ['esp-update.py']

fname_list = []
# 获取原始文件列表
for pattern in white_list:
    fname_list += glob.glob(pattern)

# 根据黑名单进行过滤
for fname in black_list:
    if fname not in fname_list:
        continue
    fname_list.remove(fname)


print('[INFO] 即将要上传的文件列表')
print(fname_list)

print('[INFO] 开始同步文件夹至设备{}'.format(dev_port_name))

for fname in fname_list:
    print('[INFO] 开始上传文件：{}'.format(fname))
    code = subprocess.call(['sudo', 'ampy','--port', dev_port_name, 'put', fname])
    if code == 0:
        print('[INFO] 成功上传文件: {}'.format(fname))
    else:
        print('[ERROR] 文件 {} 上传失败'.format(fname))
        print('程序意外退出')
        exit(0)

print('[END] 完成文件同步至设备{}'.format(dev_port_name))