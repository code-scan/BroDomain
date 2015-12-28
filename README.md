# BroDomain


<img src=./log/logo.png>
## 使用方法
```
python brodomain.py baidu.com
```


## 运行逻辑

    brodomain.py
    |---输入域名
    |    |---查询域名注册邮箱
    |    |---通过域名查询备案号
    |    |---通过备案号查询域名
    |    |---反查注册邮箱
    |    |---反查注册人
    |    |---通过注册人查询到的域名在查询邮箱
    |    |---通过上一步邮箱去查询域名
    |    |---查询以上获取出的域名的子域名
    |    \---结束
    \---生成html和log报告

## 报告demo
  ```
  ./log/ly.com.html
  ./log/ly.com.log
  ```
  <img src=./log/pic.png>
