本工具用于自动分离/剪掉明日方舟视频中的暂停
实现原理为检测右上角暂停以及中央PAUSE像素点识别是否为暂停
检测右上角靠左识别是否加速（用于懒人版自动2倍速）
检测左侧靠中间的灰色带识别是否为有效暂停
给定编队界面的秒数（可使用小数比如2.12）可以自行识别边框大小，不过裁剪功能仅对边框像素为>=0时才能正常使用（边框像素<0不影响剪暂停只影响裁剪）
因为国服版本的字体与外服不同，外服有失效情况（不过据IronCobra佬说一直能用）
录制到快捷键/光标同样会影响使用，请攻略者录制时注意隐藏

以下写给有兴趣一起完善代码的大佬：
cut_tool.py是唯一手写代码部分
（什么！你真要读这shi山代码吗？创这个repo的最初目的一是确实维护一下代码，二是改正下自己懒惰的习惯吧，代码一直写这么shi也不是个事
python版本为3.6.8
开发运行报错的时候应该会说缺了哪些dependency吧，记不清当时下了哪些包了
3/17/2025
按照代码规范修改了大部分的代码
包括新建可重用function
常量定义，变量名按实际用途定义
删除冗余代码
修复了懒人模式下部分有效暂停被截断的bug

打包时先运行下面命令
pyinstaller -D .\cut_tool.py
再将git目录下的cv2，numpy，pydub，bin（这个文件超过100M是unzip_me开头那个）覆盖进去，创建一个空working_folder再一起zip打包即可


TODO:
![TODO](pics/todo.png "TODO")