## Readme

#### 使用方法：

1、windows系统下运行cmd，通过cd 指令，找到manage文件夹目录

2、输入指令：pipenv install （该指令用于创建python虚拟环境，并且安装相关的依赖包，依赖包已存放在Pipfile文件中）

3、输入指令：pipenv shell（用于激活当前环境）

4、输入命令：flask initdb --drop（用于清空原先数据库的数据，并重新创建）
由于为了能在非本地环境运行，此处使用了SQLite而非MariaDB

5、（暂时不用）输入命令： flask forge（用于生成模拟数据：默认为20条，仅包含username和content）
也可以用flask forge --count来指定要生成模拟数据的个数，其中count是个数

6、输入命令：flask run（运行）

### 文件介绍：

.flaskenv : 储存程序运行的环境变量

data.db  SQLite数据库文件

Pipfile : 程序运行所需的相关依赖包（相当于旧版的requirements.txt文件）

manage ： 后端代码包

PIPENV_VENV_IN_PROJECT ： 改程序中已安装好的python环境和包



