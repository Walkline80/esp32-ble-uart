<h1 align="center">ESP32 BLE - UART</h1>

<p align="center"><img src="https://img.shields.io/badge/Licence-MIT-green.svg?style=for-the-badge" /></p>

### 项目介绍

[MicroPython for ESP32 开发板低功耗蓝牙（BLE）研究学习项目](https://gitee.com/walkline/esp32-ble)的分支项目，使用`ESP32开发板`通过`UART`与其它设备交换数据

### 如何使用呢？

* 下载并烧录自定义的固件到开发板
* 如果你用的是官方最新固件的话可以参考`不想烧录自定义固件？`部分
* 把项目目录下的`main.py`和`ble`文件夹上传到开发板，并运行`main.py`文件
* 使用安卓手机下载安装 [nRF Connect](https://github.com/NordicSemiconductor/Android-nRF-Connect/releases)
* 在`nRF Connect`中搜索并连接默认名称为`mpy-uart`的设备
* 然后按如下顺序操作：
	1. 按一下开发板上的`BOOT`按键，板载 Led 点亮的同时手机会收到数据`on`，再次按下按键收到`off`
	2. 手机上点`RX Characteristic`右侧的上箭头，在弹出的数据发送窗口中，以`byte`形式发送`0x01`或以`text`形式发送`on`，都可以点亮开发板的板载 Led
	3. ~~手机上点`TX Characteristic`右侧的下箭头，可以读取到开发板上板载 Led 的状态数据，也就是`on`~~ **未验证**

### 下载烧录自定义固件

访问 [自定义固件下载项目](https://gitee.com/walkline/esp32_firmware) 下载最新的自定义固件，并参考 [附录1：如何刷写固件](https://gitee.com/walkline/esp32_firmware#%E9%99%84%E5%BD%951%E5%A6%82%E4%BD%95%E5%88%B7%E5%86%99%E5%9B%BA%E4%BB%B6) 烧录固件到开发板

### 不想烧录自定义固件？

当然没问题，不过要确认你现在的固件是**支持`ble`的**，然后

* 下载 [const.py](https://gitee.com/walkline/micropython-beacon-library/raw/master/ble/const.py)

* 下载 [tools.py](https://gitee.com/walkline/micropython-beacon-library/raw/master/ble/tools.py)

保存到项目目录`ble`文件夹下，一起上传到开发板即可

### 合作交流

* 联系邮箱：<walkline@163.com>
* QQ 交流群：
    * 走线物联：163271910
    * 扇贝物联：31324057

<p align="center"><img src="https://gitee.com/walkline/WeatherStation/raw/docs/images/qrcode_walkline.png" width="300px" alt="走线物联"><img src="https://gitee.com/walkline/WeatherStation/raw/docs/images/qrcode_bigiot.png" width="300px" alt="扇贝物联"></p>
