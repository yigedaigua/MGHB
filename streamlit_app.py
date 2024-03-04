
import streamlit as st
import pandas as pd
from dataprocessing import dataprocessing,datatimeSubdatatime,max_min_avg_stand
import matplotlib.pyplot as plt
st.title('HB数据分析')
# st.header('HB数据分析')
st.subheader('请上传HB模温机原始CSV文件')
accepted_file_types = ["csv"]
# 显示上传文件控件
uploaded_files = st.file_uploader(
    label="请选择一个CSV文件",
    accept_multiple_files=False,
    type=accepted_file_types
)
if uploaded_files is not None:
    optionslist = []
    options = st.multiselect(
        '请选择需要查看的数据',
        ['Set temperature(current)', 'Return line', 'Flow rate', 'System pressure', 'Main line', 'Regulation ratio',
         'Set value system pressure', 'Pump pressure differential'],
        ['Set temperature(current)'])
    selectvalues = st.slider(
        '请选择需要显示的时间范围',
        0.0, 24.0, (0.0, 24.0))
    for count in range(len(options)):
        optionslist.append(options[count])
    if st.button('查看数据图表'):
        if len(options) != 0:
            #开始处理CSV文件并显示
            # 读取CSV文件
            my_bar = st.progress(0)
            my_bar.progress(10, text="开始读取CSV文件")
            data = pd.read_csv(uploaded_files, encoding='utf16', skiprows=13)
            # 获取行数
            lines = data.values.shape
            print(lines)
            # 提取第一行数据并去除分号
            infolist = []
            my_bar.progress(12, text="开始分析CSV文件")
            for i in range(lines[0]):
              newinfolist = []
              cleaned_data = str(data.values[i][0]).split(';')
              # print(cleaned_data)
              # 打印清洗后的数据
              # HB时间
              HBdata = f"{cleaned_data[0]}:{cleaned_data[1]}"
              # 设定温度（电流）
              temperature = dataprocessing(cleaned_data[2])
              # 正线
              Mainline = dataprocessing(cleaned_data[3])
              # 回流管
              Returnline = dataprocessing(cleaned_data[4])
              # 流量
              Flowrate = dataprocessing(cleaned_data[11])
              # 系统压力
              Systempressure = dataprocessing(cleaned_data[14])
              # 调节比率
              Regulationratio = dataprocessing(cleaned_data[9])
              # 设定值系统压力
              Setvaluesystempressure = dataprocessing(cleaned_data[13])
              # 泵压差
              Pumppressuredifferential = dataprocessing(cleaned_data[16])
              newinfolist.append(HBdata)
              newinfolist.append(temperature)
              newinfolist.append(Returnline)
              newinfolist.append(Flowrate)
              newinfolist.append(Systempressure)
              newinfolist.append(Mainline)
              newinfolist.append(Regulationratio)
              newinfolist.append(Setvaluesystempressure)
              newinfolist.append(Pumppressuredifferential)
              infolist.append(newinfolist)

            # ['2023-07-06:21:52:03', 40.0,39.3, 10.0,   0.7,   38.6,   0.7,        0,       0.1],
            #   HB时间                 温度   回流管 流量  系统压力  主线   调节比率  设定值系统压力   泵压差
            # 计算zeit-h
            my_bar.progress(50, text="CSV文件分析完成，开始处理CSV文件")
            zeitlist = []
            for info in range(len(infolist)):
              zeith = datatimeSubdatatime(infolist[0][0], infolist[info][0])
              zeitlist.append(zeith)
            my_bar.progress(55, text="开始处理时间")
            # 将zeti与处理信息合并
            for z in range(len(infolist)):
              infolist[z].insert(2, zeitlist[z])

            valueslist = []
            for info in infolist:
                if info[2] >= selectvalues[0] and info[2] <= selectvalues[1]:
                    valueslist.append(info)
            infolist = valueslist
            # for i in infolist:
            #   print(i)

            # x轴---时间差zeti-h
            xlist = []
            for x in range(len(infolist)):
              xlist.append(infolist[x][2])
            my_bar.progress(60, text="开始处理Set temperature(current)")

            #  y1轴数据 -温度 Set temperature(current)
            ylist = []
            for y in range(len(infolist)):
              ylist.append(infolist[y][1])

            my_bar.progress(65, text="开始处理Return line ")
            # Return line  :回流管 :y1
            Returnlinelist = []
            for R in range(len(infolist)):
              Returnlinelist.append(infolist[R][3])
            my_bar.progress(70, text="开始处理Flow rate ")
            #Flow rate：流量：y1
            Flowratelist = []
            for F in range(len(infolist)):
              Flowratelist.append(infolist[F][4])
            my_bar.progress(75, text="开始处理System pressure")
            # System pressure:系统压力:y2
            Systempressurelist = []
            for S in range(len(infolist)):
              Systempressurelist.append(infolist[S][5])

            my_bar.progress(80, text="开始处理Main line")
            # Main line：正线::y1
            Mainlinelist = []
            for L in range(len(infolist)):
              Mainlinelist.append(infolist[L][6])

            my_bar.progress(85, text="开始处理Regulation ratio")
            # Regulation ratio：调节比率:y2
            Regulationratiolist = []
            for R in range(len(infolist)):
              Regulationratiolist.append(infolist[R][7])

            my_bar.progress(90, text="开始处理Set value system pressure")
            # Set value system pressure：设定值系统压力:y2
            Setvaluesystempressurelist = []
            for R in range(len(infolist)):
              Setvaluesystempressurelist.append(infolist[R][8])

            my_bar.progress(95, text="开始处理Pump pressure differential")

            # y2轴数据：Pump pressure differential
            Pumppressuredifferentiallist = []
            for y in range(len(infolist)):
              Pumppressuredifferentiallist.append(infolist[y][-1])
            my_bar.progress(98, text="数据处理完成，正在处理图表")
            # 创建折线图
            fig, ax = plt.subplots(figsize=(10, 6))
            # 绘制第一个数据集

            # 'Set temperature(current)', 'Return line', 'Flow rate', 'System pressure', 'Main line', 'Regulation ratio',
            #      'Set value system pressure', 'Pump pressure differential'

            # 绘制Set temperature(current)
            if "Set temperature(current)" in optionslist:
                ax.plot(xlist, ylist, color='#000000', label='Set temperature(current)')  # '#000000'表示黑色实线

            if "Return line" in optionslist:
                ax.plot(xlist, Returnlinelist, color='#0000FF', label='Return line')

            if "Flow rate" in optionslist:
                ax.plot(xlist, Flowratelist, color='#A020F0', label='Flow rate')
            if "Main line" in optionslist:
                ax.plot(xlist, Mainlinelist, color='#FF0000', label='Main line')
            plt.xlabel('Zeit  h')
            # plt.ylim(-30, 170)  # 调整y轴的显示范围
            plt.xlim(9.0, 24.0)  # 调整x轴的显示范围
            plt.xticks([9.0, 11.0, 13.0, 15.0, 17.0, 19.0, 21.0, 23.0],
                       ["9.0", "11.0", "13.0", "15.0", "17.0", "19.0", "21.0", "23.0"])  # 设置x轴刻度及对应标签
            # plt.yticks([-20.0, 0.0, 20.0, 40.0, 60.0, 80.0, 100.0, 120.0, 140.0, 160.0],
            #            ["-20.0", "0.0", "20.0", "40.0", "60.0", "80.0", "100.0", "120.0", "140.0",
            #             "160.0"])  # 设置y轴刻度及对应标签
            # 设置第一个y轴的标签和刻度
            ax.set_ylabel('Temperatur  °C;  Stellgrad  %', color='blue')
            ax.tick_params(axis='y', labelcolor='blue')  # 设置y轴刻度标签颜色
            # 创建第二个y轴
            ax2 = ax.twinx()

            # y2轴数据;Pump pressure differential
            if "Pump pressure differential" in optionslist:
                ax2.plot(xlist, Pumppressuredifferentiallist, color='#FF69B4', label='Pump pressure differential')

            if "System pressure" in optionslist:
                ax2.plot(xlist, Systempressurelist, color='#458B00', label='System pressure')

            # Regulation ratio：调节比率:y2
            if "Regulation ratio" in optionslist:
                ax2.plot(xlist, Regulationratiolist, color='#008B00', label='Regulation ratio')

            # Set value system pressure：设定值系统压力:y2
            if "Set value system pressure" in optionslist:
                ax2.plot(xlist, Setvaluesystempressurelist, color='#8B5A2B', label='Set value system pressure')

            ax2.set_ylim(-10, 40)
            ax2.set_ylabel('Durchfluss  L/min;  Druck  bar', color='red')  # 设置第二个y轴的标签
            ax2.tick_params(axis='y', labelcolor='red')  # 设置第二个y轴刻度标签颜色
            # ax2.set_yticks([-10.0, -5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0])  # 设置第二个y轴刻度
            # ax2.set_yticklabels(
            #     ["-10.0", "-5.0", "0.0", "5.0", "10.0", "15.0", "20.0", "25.0", "30.0", "35.0", "40.0"])  # 设置第二个y轴刻度标签
            lines, labels = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines + lines2, labels + labels2, loc='lower center', bbox_to_anchor=(1.2, 1))
            # if "Set temperature(current)" in options:
            #   print(1234567)

            # 开始计算最大值，最小值，平均值，标准差
            # Set temperature(current)：设定温度（电流)
            Settempervalue = max_min_avg_stand(1,infolist)

            #Return line：回流管
            Returnlinevalue = max_min_avg_stand(3,infolist)

            # Flow rate：流量
            Flowratevalue = max_min_avg_stand(4,infolist)

            # System pressure：系统压力
            Systempressurevalue = max_min_avg_stand(5,infolist)

            # Main line：正线
            Mainlinevalue = max_min_avg_stand(6,infolist)

            # Regulation ratio：调节比率
            Regulationratiovalue = max_min_avg_stand(7,infolist)

            # Set value system pressure：设定值系统压力
            Setvaluesystempressurevalue = max_min_avg_stand(8,infolist)

            # Pump pressure differential：泵压差
            Pumppressuredifferentialvalue = max_min_avg_stand(9,infolist)

            data = {
                'Column1': Settempervalue,
                'Column2': Returnlinevalue,
                'Column3': Flowratevalue,
                'Column4': Systempressurevalue,
                'Column5': Mainlinevalue,
                'Column6': Regulationratiovalue,
                'Column7': Setvaluesystempressurevalue,
                'Column8': Pumppressuredifferentialvalue
            }
            df = pd.DataFrame(data)
            df.index = ['Max', 'Min', 'Mittelwert', 'Standardabw.']  # 设置行名
            df.columns = ['Set temperature(current)', 'Return line', 'Flow rate', 'System pressure', 'Main line', 'Regulation ratio', 'Set value system pressure', 'Pump pressure differential']  # 设置列名
            # 显示表格
            st.table(df)
            st.pyplot(fig)
            my_bar.progress(100, text="图表显示完成！")
        else:
            st.write("请选择要分析的数据")

    else:
        st.write("☝️点击查看数据表")
else:
    st.info('☝️ 上传HB模温机原始CSV文件')



