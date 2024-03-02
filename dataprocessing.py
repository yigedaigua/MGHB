from datetime import datetime
import numpy as np
def dataprocessing(data:str):
    if "#" in data:
        return 0
    else:
        if "" == data:
            return 0
        else:
            return float(data)
def datatimeSubdatatime(time_str1,time_str2):
    # 将时间字符串转换为datetime对象
    time1 = datetime.strptime(time_str1, '%Y-%m-%d:%H:%M:%S')
    time2 = datetime.strptime(time_str2, '%Y-%m-%d:%H:%M:%S')
    # 计算时间差并将其转换为秒数
    time_difference = (time2 - time1).total_seconds()
    # 将秒数转换为浮点数表示
    float_hours = round(time_difference / 3600, 1)
    return (float_hours)

def max_min_avg_stand(index:int,infolist):
    # 计算每个子列表中第二个元素的最大值
    max_values = max(sublist[index] for sublist in infolist)
    # 计算每个子列表中第二个元素的最小值
    min_values = min(sublist[index] for sublist in infolist)
    # 计算平均值
    average_value = sum(sublist[index] for sublist in infolist) / len(infolist)
    # 提取第二个元素到一个列表中
    second_elements = [sublist[index] for sublist in infolist]
    # 计算标准差
    standard_deviation = np.std(second_elements)
    # 输出结果
    return [max_values, min_values, average_value,standard_deviation]

if __name__ == "__main__":
    print(dataprocessing("-4E-01"))