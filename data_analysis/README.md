# 数据分析及指标计算

### 配置环境
```
cd ./data_analysis
python -m venv data_analysis
.\data_analysis\Scripts\activate
pip install -r requirements.txt
```
### 测试代码
使用test_data下的测试文件进行计算。改动文件路径并运行CushionDataAnalysis.py

### 计算
在data_analysis文件夹下新建data文件夹，将数据迁入，需要确保有任务时间csv。

运行对应程序计算不同数据源指标，如：
```
python ScanerDataAnalysis.py
```
