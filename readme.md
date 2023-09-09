# 多用户Shadowsocks项目

这个项目经历了6年的开发、使用，从2018年圣何塞的Crescent Village到现在新加坡的Jurong East。
如今我已经没有更多的精力维护这个项目，但一直都缺少说明文件，所以这应该是最后一次更新了。

## 项目介绍

这个项目是一个多用户的Shadowsocks后端项目，使用Django框架开发，使用MySQL数据库存储用户信息。
前端项目WorldOutlook请参考[这里](https://github.com/Jyonn/WorldOutlook)。

此项目基于Shadowsocks[官方](https://github.com/shadowsocks/shadowsocks)项目。

## 依赖

我没有尝试过更多的Python/Django版本，下方列出的是我使用的版本。

- Python 3.6.9
- Django 3.0.6
- SmartDjango 3.6.8
- QitianSDK 0.1.1

## 齐天SDK

齐天SDK是我开发的一个单点登录SDK，用于实现多个项目之间共用用户系统。
你可以成为齐天的开发者，添加自定义应用。更多的说明请见[这里](https://qt.6-79.cn/)

## 部署

### SSServer 部署

```bash
sudo ssserver --manager-address /var/run/shadowsocks-manager.sock -c server-multi-passwd.json
```

每次运行需要保证`/var/run/shadowsocks-manager.sock`文件不存在，否则会报错。

以下是`server-multi-passwd.json`的内容。`port_password`不能为空。

```json
{
        "server": "0.0.0.0",
        "port_password": {
                "rootuser": "rootpassword"
        },
        "method": "aes-256-cfb",
        "timeout": 600
}
```

项目部署说明已经没有更多精力完成，抱歉。

## 致谢

2018年的自己。