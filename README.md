## vonmgr 

### 1、目的
集群管理的工具的集中，比如之前写的[集群传key工具](https://github.com/vonhng/transfer_pubkey.git)、[服务器电源管理](https://github.com/vonhng/ipmimgr)

### 2、说明
```shell
➜  ~ vonmgr -h
vonmgr 1.0.0

Usage:
    vonmgr [SWITCHES] [SUBCOMMAND [SWITCHES]] args...

Meta-switches:
    -h, --help         Prints this help message and quits
    --help-all         Print help messages of all subcommands and quit
    -v, --version      Prints the program's version and quits

Subcommands:
    cmd                execute cmd in remote node; see 'vonmgr cmd --help' for more info
    count_code         count code rows in path; see 'vonmgr count_code --help' for more info
    power              check/change power status; see 'vonmgr power --help' for more info
    add                transfer key.pub into remote authorized_keys; see 'vonmgr trans_key --help' for more info
```
目前已经集成了四个工具：
- cmd： 交互式在集群的1~all个节点执行命令

```shell
Switches:
    -i, --ip IPS:str            执行命令的节点的ip,string格式，使用 "/"分隔
    --no-log                    if given, no print detail
    -p, --password PWD:str      password
    -u, --user USER:str         user
```
- count_code：查询某个目录下的代码行数，目前统计'yaml', 'py', 'yml', 'go', 'sh'

```shell
Switches:
    --no-log                 if given, print detail
    -p, --path PATH:str      directory path
```
- power：服务器电源管理工具,详细用法在[power工具用法](https://github.com/vonhng/ipmimgr/blob/master/README.md)

```shell
Switches:
    -g                                 if given, get power status
    -i IP:str                          IPMI IP,example: 111(only 10.10.90.111)/10.10.xxx.xxx
    -p PWD:str                         IPMI PASSWORD,default: 123456; requires -u
    -s CMD:{'reset', 'on', 'off'}      set power on|off|reset; requires -i; excludes -g
    -u USER:str                        IPMI USER,default: ADMIN; requires -i, -p
```
- add：上传key，详细用法在[传key工具用法](https://github.com/vonhng/transfer_pubkey/blob/master/README.md)

```Switches:
    -i, --ip IPS:str            remote ips,use '/' to split
    -p, --password PWD:str      password
    -u, --user USER:str         user
```
### 3、使用
- clone repo
- pip install -r requirements.txt
- 更新 `bin/vonmgr`脚本里的path
- cp vonmgr /usr/local/bin

### 4、TODO
- 增加新工具
- 增加.rc集中管理集群变量
- go重写，解决依赖