# CyberDog_Ctrl
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/Karlsx/CyberDog_Ctrl/blob/main/README.en.md)
该demo使用python实现的[gRPC](http://doc.oschina.net/grpc?t=58008) client向cyberdog发送控制指令，通信协议为官方开源[cyberdog_app.proto](https://partner-gitlab.mioffice.cn/cyberdog/athena_cyberdog/-/tree/devel/athena_common/athena_grpc/protos) ，但因无具体协议说明文档，只能靠手机端App使用方式推测具体接口的使用方法。

目前能实现基础的移动控制与基础的动作指令控制。

### 依赖安装

- grpc：`sudo pip install grpcio` （运行需要）

- grpc-tools：`sudo pip install grpcio-tools` （cyberdog_app.proto编译需要）

- keyboard：`sudo pip install keyboard` （运行需要）

  ***因为keyboard模块需要root权限，为防止sudo模式运行python文件找不到模块，统一使用sudo install，其他环境请自行调整***

### 协议编译

下载官方通信协议：[cyberdog_app.proto](https://partner-gitlab.mioffice.cn/cyberdog/athena_cyberdog/-/tree/devel/athena_common/athena_grpc/protos)

放入`make_proto.bash`同级目录下，运行`make_proto.bash`

成功后会生成`cyberdog_app_pb2.py`和`cyberdog_app_pb2_grpc.py`

### gRPC 协议调用

 本demo采用Python编写，但gRPC支持c++，c#， Go，Java，Node，php，ruby，objective-c

官方文档：[中文](https://doc.oschina.net/grpc)——[GitHub](https://github.com/grpc/grpc)

[官方gRPC Python教程](http://doc.oschina.net/grpc?t=60138)

### Demo使用

使用官方CyberdogApp正确连接铁蛋，进入遥控界面后左上角会显示铁蛋的IP地址

将PC连接到铁蛋相同的网络环境下

运行：`sudo python3 cyberdog_ctrl.py`

按提示输入模式选择与IP地址

- RunOrderCMD：

  将执行以下动作：

  - 站起来
  - 握手动作
  - 趴下去

- RunMoveCMD：

  将执行以下动作：

  - 站起来
  - 切换为小跑步态
  - 按指令进行移动
  - 趴下去
