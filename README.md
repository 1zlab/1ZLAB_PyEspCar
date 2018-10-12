# PyEspCar - 基于MicroPython-ESP32的WIFI小车

**1Z实验室出品**
**1ZLAB**： **Make Things Easy**



## 项目简介

1ZLab在准备挑选合适的小车来研发计算机视觉的教程时候 , 发现习惯了Python语法的我们, 在市面上找不到合适小车, 后来我们选了ESP32作为小车的控制主板, 可以使用Python对其进行交互式编程, 极大的提升了开发效率.

下图是我们的**PyESPCar V2.1**版本的实物图, 舵机云台上面挂载了手机, 可以通过手机WIFI传图, 然后在PC上用OpenCV做图像处理, 然后PC发送控制指令给PyESPCar WIFI小车. 

![0914_1](./image/0914_1.jpg)



> 小车采用预售的模式, 购买小车联系1Z实验室阿凯  
> QQ： 244561792
> 微信：xingshunkai



## 小车自身特性



* MicroPython编程，小车通过repl交互式编程

* **远程调试**，通过WebREPL，可以远程给小车进行编程，上传/同步代码文件。

* 软件硬件与机械结构全部**开源(Open Source)**。

  不用购买之后再提供，直接放在Github上，后续再配套教程持续制作用户友好的**文档**

* **配套教程**  制作PyEspCar Z1的视频教程（讲micropython-esp32与运动控制），发布在**Bilibili**上面， 内容可以参考下文的 `MicroPython-ESP32教学`与 `自控与运动学控制` 这两部分。

  B站主页： https://space.bilibili.com/40344504/#/

* **代码规范**，逐行注释，容易看懂， 参见代码仓库。

* 自主研发**ESP32 Web IDE**， [IDE地址](http://dev.1zlab.com)

## 开发文档

* [PyESPCar开发环境配置](/doc/PyESPCar开发环境配置_pyespcar-environment-config//doc/PyESPCar开发环境配置_pyespcar-environment-config.md)
## 综合例程

[PyESPCar按键控制模式](https://github.com/1zlab/1ZLAB_PyEspCar/tree/master/examples/01-keyboards_ctl_mode)



![mqtt keyboards](./examples/01-keyboards_ctl_mode/image/MQTT远程控制.png)



[PyESPCar色块追踪](https://github.com/1zlab/1ZLAB_PyEspCar/tree/master/examples/02-color-block-track)

![color track](./examples/02-color-block-track/image/小车色块追踪.png)



## 机械结构与硬件



* **轻量级二自由度云台**

  ![machine](./image/PyEspCar-Z1.png)

  更适合放在小车上面，同时末端可以承受较大负载（例如手机）。

  高品质20KG 数字舵机， 后期可以拓展为机械臂。

  

* **PyESPCar 小车底板** 

  ![0914_2](./image/0914_2.png)

  

  填补了目前ESP32小车底板的空白，主控采用安信可公司的NodeMCU32s，直插在小车底板上。

  板子预留资源如下: 

  *  用户按键 ×1
  *  电机与AB相编码器接口 ×2
   *  传感器接口×2  
   *  UART串口x2  
   *  I2C接口 x1（两个I2C插口）

  

* **全金属双层小车底板**  材质选用铝合金，比亚克力更坚固， 尺寸比一般的两轮差速小车大270mm。

  底板上面也预留了**数莓派**，二自由度云台，电池，超声波，ESP32小车控制板,还有**激光雷达**的孔位。

* **12V电池组，电池容量6000毫安时**， 配套充电器, 调试一天不用充电.



物料成本列表见： [PyESPCar配件清单+物料成本核算-V2](https://github.com/1zlab/1ZLAB_PyEspCar/blob/master/hardware/PyESPCar-Z1-%E9%85%8D%E4%BB%B6%E6%B8%85%E5%8D%95%2B%E7%89%A9%E6%96%99%E6%88%90%E6%9C%AC%E6%A0%B8%E7%AE%97.md)



## 贡献者(Ccontributor)

**特别感谢魏彦峰同学在机械结构设计还有小车控制板设计做出的贡献。**

* [魏彦峰-1Z实验室&中国地质大学（武汉）](https://github.com/rose-w)
* [邢顺凯-1Z实验室&杭州电子科技大学](https://github.com/mushroom-x)
* [吴彬聪-1Z实验室&杭州电子科技大学](https://github.com/littleoniononion)
* [刘新宇-廊坊师范](https://github.com/LiuXinyu12378)
* [杨子豪-平衡小车之家](http://minibalance.com/)




## 加入1Z实验室

出品：1Z实验室 （1ZLAB： Make Things Easy）

1Z实验室 Make Things Easy . 致力于在机器人+计算机视觉+人工智能的重叠区域, 制作小白友好的教程.
![1zlab](https://upload-images.jianshu.io/upload_images/1199728-589a80ff77f380d8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/700)

