# Python 工具库 #

+ 2015-08-08 [crontab](https://github.com/imsilence/packages/blob/master/python/crontab.py)

    定时执行控制程序, 同unix中crontab

    crontab.py监控并读取crontab_scripts目录及其子孙目录中的crontab文件，根据crontab中配置定时执行外部脚本

    配置文件参考：[配置](https://github.com/imsilence/packages/blob/master/python/crontab_scripts/crontab)

    注：crontab配置文件中指定的程序需要与其在相同目录

    后台启动: `python crontab.py`

+ 2015-08-07 [runserver](https://github.com/imsilence/packages/blob/master/python/runserver.py)

    后台运行程序

    用法：
    ```
        import threading

        from runserver import Callback, run_as_server

        def callback1():
            print '1'
            
        def callback2():
            print '2'
            pass
            
        def stop():
            time.sleep(1000)
            stop_server()
            
        threading.Thread(target=stop).start()
        run_as_server([Callback(callback=callback1),Callback(callback=callback2)])
    ```

+ 2015-08-06 [fmonitor](https://github.com/imsilence/packages/blob/master/python/fmonitor.py)

    文件&文件夹监控, 当监控文件&文件夹发生变化后调用回调函数

    函数说明:

        file_monitor(path, callback, sleeptime=10, content=True, *args, **kwargs)
        参数:
            path: 监控文件
            callback: 回调函数
            sleeptime: 监控周期
            content: True/False, True表示监测文件内容, False表示监测修改时间
            其余参数为callback回调函数的输入参数

        folder_monitor(path, callback, sleeptime=20, content=True, filter=None, *args, **kwargs)
        参数:
            path: 监控文件夹
            callback: 回调函数
            sleeptime: 监控周期
            content: True/False, True表示监测文件内容, False表示监测文件修改时间
            filter: 用于对文件夹中文件进行过滤，为lambda函数或None, lambda函数回调参数为监控文件夹下的文件绝对路径
            其余参数为callback回调函数的输入参数


    用法：
    ```
        import time

        from fmonitor import file_monitor, folder_monitor
        
        def callback(*args, **kwargs):
            print args[0]

        file_monitor("d:/file.txt", callback, 10, False, 'file changed')
        folder_monitor("d:/folder", callback, 20, False, lambda path:path.endswith('.monitor'), 'folder changed')
        while 1:
            time.sleep(5)
    ```

+ 2015-08-05 [consistent_hash](https://github.com/imsilence/packages/blob/master/python/consistent_hash.py)

    一致性hash算法

    用法：
    ```
        import consistent_hash from ConsistentHash

        _util = ConsistentHash()
        for i in xrange(0, 3):
            _util.add_target('target-%s' % i)
        print _util.lookup_list('a', 2)
        print _util.remove_target('target-0').lookup('a')
    ```

   
+ 2015-05-28 [webserver](https://github.com/imsilence/packages/blob/master/python/webserver)

    python wsgi webserver

    后台启动: `python wsgiserver.py test:test`

    浏览器访问: `http://localhost:43001`

+ 2015-05-28 [log](https://github.com/imsilence/packages/blob/master/python/log)

    python logging模块watcher,监控logging.cfg变化并对logging环境进行重新配置 

    用法：
    ```
        from logwatcher import LogWatcher

        LogWatcher('logging.cfg').start()
    ```
    [logging.cfg配置](https://github.com/imsilence/blogs/blob/master/python/python_logging.md)

+ 2015-05-27 [muuid](https://github.com/imsilence/packages/blob/master/python/muuid.py)

    唯一id创建库,线程安全

    用法:
    ```
        import muuid

        print(muuid.getuuid())
    ```
