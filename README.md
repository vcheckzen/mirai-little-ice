# Mirai Little Ice

基于 [python-mirai](https://github.com/NatriumLab/python-mirai) 和 [小冰](https://www.msxiaobing.com/) 的 QQ 群聊机器人，仅对接聊天接口，可自行扩展其他功能。

## 部署

### 领养小冰

1. 根据官方提示领养 [小冰](https://www.msxiaobing.com/) 并绑定 `新浪微博`
2. 使用 Chrome 浏览器 `无痕模式` 登录 [https://m.weibo.cn](https://m.weibo.cn)，按 `F12` 打开控制台并切换到 `Network` 标签
3. 私信小冰，找到包含 `send` 路径的 Network 请求，复制对应 `Request Headers` 粘贴到项目 `config` 目录的 `ice.header` 文件中，覆盖掉默认配置

### 安装依赖

#### 配置 mirai-console

1. 下载并解压 [miraiOK](https://github.com/LXY1226/miraiOK#%E4%B8%8B%E8%BD%BD%E5%9C%B0%E5%9D%80)
2. 进入解压文件夹，编辑 `config.txt`，在最后一行，填写机器人账号密码，格式如下。填写完毕后，`回车换行` 保存文件，否则无法自动登录

```bash
login qq password
```

3. 运行 `miraiOK_windows_amd64.exe`，跟随提示登录机器人账号，成功后关闭窗口
4. 进入 `plugins` 目录，下载 [mirai-api-http-vxxx.jar](https://github.com/project-mirai/mirai-api-http/releases) 并放入其中。在该目录下新建 `MiraiAPIHTTP` 文件夹并 `进入` 它，在里面新建文件 `setting.yml`
5. 打开 `setting.yml`，写入以下配置

```yml
port: 3333
authKey: 1234567890
enableWebsocket: True
cors:
  - '*'
```

6. 再次运行 `miraiOK_windows_amd64.exe`，登录成功后，将窗口最小化

#### 配置 mirai-little-ice

1. 安装 [Python 3.8](https://www.python.org/) 
2. 下载本项目，进入文件夹后，打开命令行执行命令，安装 python 依赖

```bash
pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

3. 打开项目下的 `config/config.json`，修改 `mirai_http_api - qq` 字段，改为你的 `bot qq`
4. 启动项目

```bash
python index.py
```

5. 将机器人邀进群组，@它聊天。

## 开发

### 项目结构

```bash
.
├── README.md
├── assets
│   └── image
│       └── public  # 临时图片
├── config
│   ├── config.json # 配置文件
│   └── ice.header  # 微博请求头
├── handler
│   ├── command.py  # 命令处理，自行扩展
│   ├── group.py    # 群组处理，可载入不同命令、插件和响应
│   ├── response.py # 响应分发，根据消息类型，分发命令和响应
│   └── task.py     # 定时任务，自行扩展
├── index.py        # 启动文件
├── plugins
│   ├── base.py     # 插件抽象类，所有插件必须实现
│   └── ice.py      # 小冰插件
├── requirements.txt
└── utils
    ├── base.py     # 工具抽象类，单例，所有工具必须实现
    ├── config.py   # 配置读取
    └── image.py    # 图片处理
```

## 致谢

- [python-mirai](https://github.com/NatriumLab/python-mirai) 及其父依赖