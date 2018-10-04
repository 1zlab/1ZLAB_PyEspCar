# 测试PyESPCar-SDK



在当前目录下运行`ipython/Jupyter`

把下面的内容粘贴进去

`test_pyespcar.py`

```python
import paho.mqtt.client as mqtt
from pyespcar_sdk import PyCarSDK

mqtt_client = mqtt.Client()
# mqtt_client.on_message = on_message
mqtt_client.connect('localhost', 1883, 60)
sdk = PyCarSDK(mqtt_client, is_debug=True)
```



然后你就可以测试`sdk`对象的各种方法了。