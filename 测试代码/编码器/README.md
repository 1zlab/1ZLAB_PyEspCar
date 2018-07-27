编码器计数

需要用到外部中断 IRQ 
一个编码器(AB相)需要用到两个IRQ中断资源

TODO 翻手册 12 14 17 26 是否具备IRQ资源
TODO 创建一个编码器类
TODO 添加转向属性
TODO 添加转速属性

IRQ :(上升沿+下降沿)
IRQ handler -> 面向对象里的方法 

先用一个



查看STM32版本的是怎么写的。

ESP32 引脚Trigger设置的好像有问题 Trigger = 3 好像不是这个意思


改用定时器论巡？

**问题主要出在噪声上面**

如果 快速转转动， 误差就很小。



## 接线

右侧编码器
pina = Pin(21) # uno底板 pin7
pinb = Pin(19) # uno底板 pin2

左侧编码器
pina = Pin(5) # uno底板 pin8
pinb = Pin(18) # uno底板 pin4
