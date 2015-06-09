# Python 工具库 #

+ 2015-05-28 [webserver](https://github.com/imsilence/packages/blob/master/python/webserver)

   python wsgi webserver

   后台启动: `python wsgiserver.py test:test`

   浏览器访问: `http://localhost:43001`

+ 2015-05-28 [log](https://github.com/imsilence/packages/blob/master/python/log)

   python logging模块watcher,监控logging.cfg变化并对logging环境进行重新配置 
   
   用法：

   `from logwatcher import LogWatcher;LogWatcher('logging.cfg').start()`

   [logging.cfg配置](https://github.com/imsilence/blogs/blob/master/python/python_logging.md)

+ 2015-05-27 [muuid](https://github.com/imsilence/packages/blob/master/python/muuid.py)
      
    唯一id创建库,线程安全
      
    用法:

    `import muuid;print(muuid.getuuid());`
