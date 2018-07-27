

## 关于ADC的问题

- Invalid Pin for ADC
TODO 查阅文档 需要修改固件 (成本比较高, 而且浪费资源)
IO2 -> ADC2 Channel 2
TODO 改固件 从而可以支持ADC2
临时方案 底板Uno(A0) - 接Uno(A2) = ESP32 GPIO35
BUG 电压取值adc采样 不稳 一直在浮动 

多次采样然后平均
与标准电压比对 (5v 3v) * 系数

## [已解决] IRQ外部中断

MicroPython-ESP32中, irq 只有上升沿或下降沿 (二选1)

>TODO 修改固件, 添加Change模式. 

**而且这里需要的应该是-非阻塞(no-blocking)模式**


**查看ESP-IDF是否有这个API**
是否有必要使用外部中断, 可以使用定时器, 定时查看IO电平是否变化
https://github.com/BramRausch/encoderLib


ESP32 是否有硬件计数?


## [TODO]增量式编码器使用
编码器噪声问题 不是完全按照 0132的顺序来的。

两个引脚都是中断。

TODO 寻找项目参考
添加滤波器

1. 比对 可以大于等于两个？
2. 二者相等的情景？ 
3. 添加状态机 State (之前一直在正转 马上反转的可能性不大。)
4. 是否引入变量： 触发中断的管脚

**增量式编码器**
https://blog.csdn.net/cuhkljt/article/details/25845217
https://item.taobao.com/item.htm?spm=a230r.1.14.27.63de2886VbW8iL&id=45347924687&ns=1&abbucket=6#detail

## 刷固件

刷固件， 需要把ESP32开发板从底板下取下。

## 声明引脚输入输出是个好习惯

Pin.IN
Pin.OUT

## [Done]电机引脚问题

Problem 左侧电机一动，reboot -> 更换引脚已解决 （因为用了D2接口）

## [Done]电机只能反转不能正转？
电机驱动模块插反
