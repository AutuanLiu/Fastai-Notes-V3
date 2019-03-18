# How to ?

- [How to ?](#how-to)
  - [常用命令行操作](#%E5%B8%B8%E7%94%A8%E5%91%BD%E4%BB%A4%E8%A1%8C%E6%93%8D%E4%BD%9C)
  - [如何安装常用软件](#%E5%A6%82%E4%BD%95%E5%AE%89%E8%A3%85%E5%B8%B8%E7%94%A8%E8%BD%AF%E4%BB%B6)
  - [Linux 用户管理](#linux-%E7%94%A8%E6%88%B7%E7%AE%A1%E7%90%86)
  - [Linux 其他操作](#linux-%E5%85%B6%E4%BB%96%E6%93%8D%E4%BD%9C)
    - [用户权限](#%E7%94%A8%E6%88%B7%E6%9D%83%E9%99%90)
  - [读写权限](#%E8%AF%BB%E5%86%99%E6%9D%83%E9%99%90)
  - [Jupyter Notebook Server Config](#jupyter-notebook-server-config)
  - [Install Cuda](#install-cuda)
  - [ufw 设置防火墙](#ufw-%E8%AE%BE%E7%BD%AE%E9%98%B2%E7%81%AB%E5%A2%99)
  - [参考文献](#%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE)

## 常用命令行操作

|命令|含义|
|---|---|
|`du -sh *`|文件夹的大小统计|
|`ctrl + a`|光标移到命令的开头|
|`ctrl + e`|光标移到命令的末尾|
|`ctrl + u`|删除光标前面的内容|
|`ctrl + k`|删除光标后面的内容|
|`ctrl + f`|向右移到一个字符|
|`ctrl + b`|向左移到一个字符|
|`esc + f`|向右移到一个单词|
|`esc + b`|向左移到一个单词|

## 如何安装常用软件

- 下载安装conda
	- [下载最新Conda](https://conda.io/en/latest/miniconda.html)
	- 双击安装
	- 更新 `conda update conda`
- 创建独立工作环境
	- `conda create -n fastai python=3`  或者明确一个版本3.5
	- `conda activate fastai` 开启实验环境
	- `conda deactivate` 关闭实验环境
	- `conda remove -n fastai --all` 删除环境
- 下载安装pdbpp 适配python 3.6而非3.7，所以先装更好
	- `conda install pdbpp` is a must
	- not `pip3 install pdbpp`
- 下载安装Jupyter notebook
	- 更新 pip:  `python3 -m pip install --upgrade pip`
	- 下载更新Jupyter: `python3 -m pip install jupyter`
- 下载安装 Pytorch和fastai libraries
	- 一步安装：`conda install -c pytorch -c fastai fastai pytorch`
	- 更新  ` conda update conda -y `  outside env
	- 更新 ` conda update -c fastai fastai ` inside env
	- 检验 `conda list` `pip show`

## Linux 用户管理
|命令|含义|
|---|---|
|`useradd –d /home/username -m username`|为用户创建相应的帐号和用户目录 /home/username|
|`passwd username`|为用户设置密码
|`userdel -r username`|删除用户|
|`su userB`| 切换登录用户|
|`exit`| 退出当前用户回到 root 用户|
|`groups`|添加用户操作也会相应的增加一个同名的组，用户属于同名组；查看当前用户所属的组|
|`usermod -G groupNmame username`|一个用户可以属于多个组，将用户加入到组|
|`usermod -g groupName username`|变更用户所属的根组(将用户加入到新的组，并从原有的组中除去)|
|`more /etc/passwd`|查看**所有用户及权限**, 系统的所有用户及所有组信息分别记录在两个文件中：`/etc/passwd` , `/etc/group` 默认情况下这两个文件对所有用户可读|
|`more /etc/group`|查看**所有的用户组及权限**|
|`usermod -G sudo username`|给 sudo 权限|

## Linux 其他操作

|命令|含义|
|---|---|
|`chown username dirOrFile`|更改文件或目录的拥有者|
|`chown -R weber server/`|使用-R选项递归更改该目下所有文件的拥有者|
|`which command`|查看 command 的路径|
|`whereis command`|查看 command 的搜索路径|
|`find ./ | wc -l`|查看当前目录下文件个数|
|`ls | cat -n`|查看文件并编号|
|`find ./ -name '*.o'`|查找目标文件夹中是否有obj文件|
|`find ./ -name "*.o" -exec rm {} \`|递归当前目录及子目录删除所有.o文件|
|`find ./ -name "core*" | xargs file`|搜寻文件或目录|
|`locate string`|find是实时查找，如果需要更快的查询，使用locate；locate会为文件系统建立索引数据库，如果有文件更新，需要定期执行更新命令来更新索引库 `updatedb`|
|`ls -al | more`|按页显示|
|`head -1 filename`|显示文件第一行|
|`tail -5 filename`|显示文件倒数第五行|
|`diff file1 file2`|查看两个文件间的差别|
|`tail -f crawler.log`|动态显示文本最新信息|
|`:> a.txt`|清空文件内容|
|`sort -nrk 1 data.txt`|排序，-n 按数字进行排序，-d 按字典序进行排序，-r 逆序排序，-k N 指定按第N列排序|
|`uniq`|消除重复行|
|`cut`|按列切分文本|
|`paste`|按列拼接文本|
|`wc -l file`|统计行数, `wc -w file`, 统计单词数,`wc -c file` 统计字符数|
|`sed '/^$/d' file`|移除空白行, sed 用来进行文本替换|
|`tar`|打包解包工具|
|`ps -ef`|查询正在运行的进程信息|
|`ps -ajx`|以完整的格式显示所有的进程|
|`top`|显示进程信息，并实时更新|
|`lsof -i:3306`|查看端口占用的进程状态|
|`lsof -u username`|查看用户username的进程所打开的文件|
|`kill PID`|杀死指定PID的进程 (PID为Process ID)|
|`pmap PID`|输出进程内存的状况，可以用来分析线程堆栈|
|`sar -u`|查看CPU使用率|
|`free -m`|查看内存使用量|
|`netstat -a`|列出所有端口|
|`netstat -at`|列出所有 tcp 端口|
|`route -n`|查看路由状态|
|`ping IP`|发送ping包到地址IP|
|`traceroute IP`|探测前往地址IP的路由路径|
|`host domain`|DNS查询，寻找域名domain对应的IP|
|`host IP`|反向DNS查询|
|`ssh ID@host`|SSH登陆, ssh登陆远程服务器host，ID为用户名|
|`sftp ID@host`|ftp/sftp文件传输|
|`lftp`|同步文件夹(类似rsync工具) `lftp -u user:pass host`|
|`scp localpath ID@host:path`|将本地localpath指向的文件上传到远程主机的path路径|
|`scp -r ID@site:path localpath`|以ssh协议，遍历下载path路径下的整个文件系统，到本地的localpath|
|`uname -a`|查看Linux系统版本|
|`more /etc/release`|查看Unix系统版本：操作系统版本|
|`arch`|显示架构|
|`pagesize`|显示内存page大小（以KByte为单位|
|`cat /proc/meminfo`|查看内存信息|
|`cat /proc/cpuinfo | grep processor | wc -l`|查看CPU的核的个数|
|`cat /proc/cpuinfo`|查询CPU信息|
|`sar -u 5 10`|查看CPU使用情况|
|`date`|显示当前系统时间|







### 用户权限

使用`ls -l`可查看文件的属性字段，文件属性字段总共有10个字母组成，第一个字母表示**文件类型**，如果这个字母是一个减号 `-`, 则说明该文件是一个普通文件。字母 `d` 表示该文件
是一个目录。 后面的9个字母为该文件的权限标识，3个为一组，分别表示**文件所属用户、用户所在组、其它用户的读写和执行权限**； 例如:

```bash
[/home/weber#]ls -l /etc/group
-rwxrw-r-- colin king 725 2013-11-12 15:37 /home/colin/a
```

表示这个文件对文件拥有者 colin 这个用户可读写、可执行；对 colin 所在的组（king）可读可写；对其它用户只可读；

## 读写权限

使用chmod命令更改文件的读写权限，更改读写权限有两种方法，一种是字母方式，一种是数字方式

* 字母方式:

```bash
$chmod userMark(+|-)PermissionsMark
```

  * userMark取值：
    * u：用户
    * g：组
    * o：其它用户
    * a：所有用户
  * PermissionsMark取值：
    * r:读
    * w：写
    * x：执行

例如:
```bash
$chmod a+x main         # 对所有用户给文件main增加可执行权限
$chmod g+w blogs        # 对组用户给文件blogs增加可写权限
```

* 数字方式：

数字方式直接设置所有权限，相比字母方式，更加简洁方便；

使用三位八进制数字的形式来表示权限，第一位指定属主的权限，第二位指定组权限，第三位指定其他用户的权限，每位通过4(读)、2(写)、1(执行)三种数值的和来确定权限。
如6(4+2)代表有读写权，7(4+2+1)有读、写和执行的权限。

例如:

```bash
$chmod 740 main     # 将main的用户权限设置为 rwxr-----
```

## Jupyter Notebook Server Config

1. 安装Jupyter Notebook库

```bash
$ pip install Jupyter
```

2. 生成Jupyter Notebook 配置文件

生成的配置文件，后来用来设置服务器的配置

```bash
$ jupyter notebook --generate-config
```


3. 设置Jupyter Notebook密码

设置密码用于设置服务器配置，以及登录Jupyter。打开 iPython 终端，输入以下：

```bash
In [1]: from IPython.lib import passwd
In [2]: passwd()
Enter password:
Verify password:
Out[2]: '这里是密码'
```

4. 设置服务器配置文件

```bash
$ nano ~/.jupyter/jupyter_notebook_config.py
```

修改以下参数设置

   * c.NotebookApp.ip = '*' # 所有绑定服务器的IP都能访问，若想只在特定ip访问，输入ip地址即可, 也可以使用 0.0.0.0 代表所有IP
   * c.NotebookApp.port = 6666 # 端口设置，默认是8888
   * c.NotebookApp.open_browser = False # 我们并不想在服务器上直接打开 Jupyter Notebook，所以设置成False
   * c.NotebookApp.notebook_dir = '/home/username/jupyter_projects' # 这里是设置Jupyter的根目录
   * c.NotebookApp.allow_root = True # 为了安全，Jupyter默认不允许以 root 权限启动jupyter
   * c.NotebookApp.password = 'sha1:e1c8cc'  # 生成的密码


5. 启动Jupyter 远程服务器

```bash
$ jupyter notebook
```

6. 远程访问

- 方法一: 在本地浏览器上，输入 http://ip_address:port，将会打开远程Jupyter

- 方法二：如果方法一登陆失败，则有可能是服务器防火墙设置的问题，此时最简单的方法是在本地建立一个ssh通道：
  - 在本地终端中输入ssh username@address_of_remote -L127.0.0.1:your_port:127.0.0.1:remote_port
  - 切换到对应的环境，打开 jupyter notebook
  - 在localhost:your_port 就可以直接访问远程的jupyter


## Install Cuda
[cuda install](https://cloud.google.com/compute/docs/gpus/add-gpus)

* Ubuntu16.04 Cuda9

```bash
#!/bin/bash
echo "Checking for CUDA and installing."
# Check for CUDA and try to install.
if ! dpkg-query -W cuda-9-0; then
  # The 16.04 installer works with 16.10.
  curl -O http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.0.176-1_amd64.deb
  dpkg -i ./cuda-repo-ubuntu1604_9.0.176-1_amd64.deb
  apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
  apt-get update
  apt-get install cuda-9-0 -y
fi
# Enable persistence mode
nvidia-smi -pm 1
```

* Ubuntu16.04 Cuda10

```bash
#!/bin/bash
echo "Checking for CUDA and installing."
# Check for CUDA and try to install.
if ! dpkg-query -W cuda-9-0; then
  # The 16.04 installer works with 16.10.
  curl -O http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_10.1.105-1_amd64.deb
  dpkg -i ./cuda-repo-ubuntu1604_10.1.105-1_amd64.deb
  apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
  apt-get update
  apt-get install cuda -y
fi
# Enable persistence mode
nvidia-smi -pm 1
```

## ufw 设置防火墙

|命令|含义|
|---|---|
|sudo apt-get install ufw|安装 ufw|
|ufw status|查看状态|
|sudo ufw default allow outgoing|允许所有传出连接|
|sudo ufw default deny incoming|拒绝所有传入|
|sudo ufw allow ssh|允许ssh|
|sudo ufw allow http|允许http|
|sudo ufw allow https|允许https|
|sudo ufw allow 22|允许22端口|
|sudo ufw deny 111|禁止 111端口|
|sudo ufw allow 80/tcp|允许80 tcp端口|
|sudo ufw allow 1725/udp|允许1725udp端口|
|sudo ufw allow from 123.45.67.89|允许某ip|
|sudo ufw delete allow 80|删除一条规则|


## 参考文献
1. [Linux工具快速教程 — Linux Tools Quick Tutorial](https://linuxtools-rst.readthedocs.io/zh_CN/latest/index.html)
2. [Fast.ai v3 2019课程中文版笔记 - Part 1 (2019) / UTC+8 China / SE Asia - Deep Learning Course Forums](https://forums.fast.ai/t/fast-ai-v3-2019/39325)
