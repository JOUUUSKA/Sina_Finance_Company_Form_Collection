# 一、项目告示：
#### 为优化程序的运行，带给良好的互动体验，此次作业中使用到了一些依赖库<br><br>如：<br>1、tqdm对进度条进行优化，避免面对控制台陷入无尽的等待;<br>2、matplotlib对数据进行可视化操作;<br>3、spider_toolsbox对爬虫工作进行简化
### 复制下面代码到控制台安装依赖，即可运行程序。

```python  
pip install  -r requirements.txt  
```
### spider_toolsbox库可进行pip安装，<br>但是更建议从github进行拉取。

# 二、spider_toolsbox在github的地址：
### https://github.com/JOUUUSKA/spider_toolsbox.git
觉得项目不错，记得给作者点个star~

```python  
pip install spider_toolsbox  
```
```python  
git clone https://github.com/JOUUUSKA/spider_toolsbox.git
```

# 三、使用指南
只需要更换公司的股票代码，即可获取不同公司的表格数据。<br><br>
如下代码所示:<br>600000代表 **上海浦发银行** 公司的股票代码，range(2014, 2024)代表 **2014年到2023年** 时间可根据实际情况自行更改<br>如需更换其他公司，只需要在 **新浪财经网** 找到对应的公司股票代码更换即可
```python  
def main():
    lrb = LRB()
    lrb.run()
    for i in tqdm(range(2014, 2024), desc='完成进度'):
        zcfzb = ZCFZB(i, 600000)
        zcfzb.run()
        xjllb = XJLLB(i, 600000)
        xjllb.run()
```
