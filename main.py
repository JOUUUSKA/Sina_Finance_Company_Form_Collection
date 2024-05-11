# -*- coding: UTF-8 -*-
'''
@Project ：Python_SPIDER_File 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：JOUUUSKA
@Date    ：2024-05-10 19:26 
'''
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()
import pandas as pd
import os
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
from tqdm import tqdm


class ZCFZB:
    '''
    网址:https://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/600000/ctrl/2019/displaytype/4.phtml
    资产负债表板块
    '''

    def __init__(self, year, Company_number):
        self.year = year
        self.Company_number = Company_number

        self.response = spidertool.get(
            f'https://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/{self.Company_number}/ctrl/{self.year}/displaytype/4.phtml').text

        self.time_list = []
        self.zichan_list = []
        self.fuzhai_list = []
        self.syzqy_list = []

        self.time_headline_list = []
        self.zichan_headline_list = []
        self.fuzhai_headline_list = []
        self.syzqy_headline_list = []

        spidertool.create_infile(name='浦发银行资产负债表')

    def parse(self, xpath_num):
        '''
        :param xpath_num:
        1:报表日期
        2:None
        3:资产:4-24
        25:负债:26-43
        44:所有者权益:45-59
        :return:
        '''
        num_list = [i for i in range(2, 6)]
        need_list = [
            spidertool.xpath(self.response, f'//*[@id="BalanceSheetNewTable0"]/tbody/tr[{xpath_num}]/td[{i}]/text()')
            for i in num_list]
        return need_list

    def get_headline(self):
        '''
        :return: 获取大标题
        '''
        headline = spidertool.xpath(self.response, '//*[@id="BalanceSheetNewTable0"]/thead/tr/th/text()')
        return headline

    def get_titles(self):
        '''
        :return: 获取小标题
        '''
        return spidertool.xpath(self.response, '//*[@id="BalanceSheetNewTable0"]/tbody//strong/text()')

    def get_time(self):
        '''
        :return: 获取报表日期值
        '''
        return self.parse(1)

    def get_zichan(self):
        '''
        :return: 获取资产值的小标题与值
        '''
        for i in range(4, 25):
            headline = spidertool.xpath(self.response, f'//*[@id="BalanceSheetNewTable0"]/tbody/tr[{i}]//a/text()')
            self.zichan_headline_list.append(headline)

        for i in range(4, 25):
            self.zichan_list.append(self.parse(i))
        # print(self.zichan_headline_list)
        return self.zichan_headline_list, self.zichan_list

    def get_fuzhai(self):
        '''
        :return: 获取负债值的小标题与值
        '''
        for i in range(26, 44):
            headline = spidertool.xpath(self.response, f'//*[@id="BalanceSheetNewTable0"]/tbody/tr[{i}]//a/text()')
            self.fuzhai_headline_list.append(headline)

        for i in range(26, 44):
            self.fuzhai_list.append(self.parse(i))
        # print(self.fuzhai_headline_list)
        return self.fuzhai_headline_list, self.fuzhai_list

    def get_syzqy(self):
        '''
        :return: 获取所有者权益的小标题与值
        '''
        for i in range(45, 60):
            headline = spidertool.xpath(self.response, f'//*[@id="BalanceSheetNewTable0"]/tbody/tr[{i}]//a/text()')
            self.syzqy_headline_list.append(headline)

        for i in range(45, 60):
            self.syzqy_list.append(self.parse(i))
        # print(self.syzqy_headline_list)
        return self.syzqy_headline_list, self.syzqy_list

    def export_excel(self, title_lst, value_lst):
        '''
        :param title_lst: 表头列表
        :param value_lst: 值列表
        :return: None
        '''
        # 合并为字典
        data_dict = {}
        for header, value in zip(title_lst, value_lst):
            data_dict[header[0]] = [v[0] for v in value]
        # 创建DataFrame对象
        df = pd.DataFrame(data_dict)
        # 写入Excel文件
        file_path = f'浦发银行资产负债表/浦发银行{self.year}资产负债表.xlsx'
        if not os.path.exists(file_path):
            df.to_excel(file_path, index=False)
        else:
            # 读取已有的Excel文件
            existing_df = pd.read_excel(file_path)
            # 合并新数据与已有数据
            df = pd.concat([existing_df, df], ignore_index=True)
            # 写入Excel文件
            df.to_excel(file_path, index=False)

    def run(self):
        title1, value1 = self.get_zichan()
        title2, value2 = self.get_fuzhai()
        title3, value3 = self.get_syzqy()

        title1.extend(title2)
        title1.extend(title3)

        value1.extend(value2)
        value1.extend(value3)

        return self.export_excel(title1, value1)


class LRB:
    '''
    利润表网址:https://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/600000/ctrl/2016/displaytype/4.phtml
    利润表板块
    '''

    def __init__(self):
        spidertool.create_infile(name='浦发银行利润表')

    def get_data(self):

        # 近10年的利润表
        years = 10
        for i in range(years):
            # 发送HTTP请求获取网页内容
            url = "https://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/600000/ctrl/{}/displaytype/4.phtml".format(
                2014 + i)
            response = spidertool.get(url)
            html_content = response.text

            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(html_content, "html.parser")

            # 找到表格元素
            table = soup.find("table", {"id": "ProfitStatementNewTable0"})

            # 提取表格数据
            data = []
            for row in table.find_all("tr"):
                row_data = []
                for cell in row.find_all("td"):
                    row_data.append(cell.text.strip())
                # 过滤掉空行与不完整的数据行
                if len(row_data) > 1:
                    data.append(row_data)
                print(data)

            # 将JSON数据保存到文件
            with open("浦发银行利润表\data-{}.json".format(2014 + i), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

    def get_transform_data(self):

        # 循环读取JSON文件
        years = 10
        for i in range(years):
            with open('浦发银行利润表\data-{}.json'.format(2014 + i), 'r', encoding="utf-8") as f:
                first_data = json.load(f)

            result = {}
            for item in first_data:
                # 转换：将每一个元素的第一个值作为属性名，剩余元素作为值
                result.update([(item[0], item[1:])])

                # 将数据保存为JSON格式
                json_data = json.dumps(result)

                # 将JSON数据保存到文件
                with open("浦发银行利润表\data-transform-{}.json".format(2014 + i), "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False)

    def get_merge_data(self):

        # 循环读取合并JSON文件
        years = 10
        merged_data = {}
        transformed = {}
        for i in range(years):
            with open('浦发银行利润表\data-transform-{}.json'.format(2014 + i), 'r', encoding="utf-8") as f:
                first_data = json.load(f)
                transformed[2014 + i] = first_data
                merged_data = {**merged_data, **transformed}

        # 将合并后的JSON文件写入磁盘
        with open('浦发银行利润表\data-merged.json', 'w', encoding="utf-8") as f:
            json.dump(merged_data, f, indent=4, ensure_ascii=False)

    def export_excel(self):
        with open('浦发银行利润表\data-merged.json', 'r', encoding='utf8') as f:
            data = eval(f.read())
            df = pd.json_normalize(data, sep='_')

            excel_file_path = '浦发银行利润表\浦发银行历年利润表.xlsx'
            df.to_excel(excel_file_path, index=False, )

    def paint(self):

        with open('浦发银行利润表\data-merged.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        x_data = []
        y1_data = []
        y2_data = []
        for key, value in data.items():
            # print(key)
            print()
            print(float(data[key]["一、营业收入"][0].replace(',', '')))
            print()
            print(float(data[key]['二、营业支出'][0].replace(',', '')))

            x_data.append(key)
            y1_data.append(float(data[key]['一、营业收入'][0].replace(',', '')))
            y2_data.append(float(data[key]['二、营业支出'][0].replace(',', '')))

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        plt.bar(x_data, y1_data, label='营业收入')
        plt.plot(x_data, y2_data, label='营业支出', color='cyan', linestyle='--')
        plt.title('浦发银行近10年营业收入与营业成本')
        plt.xlabel('年份')
        plt.ylabel('营业收入与营业支出/万元')

        # 关闭纵轴的科学计数法
        axis_y = plt.gca()
        axis_y.ticklabel_format(axis='y', style='plain')

        # 图例
        plt.legend()

        # 显示图表
        plt.show()

    def run(self):
        self.get_data()
        self.get_transform_data()
        self.get_merge_data()
        self.export_excel()
        self.paint()


class XJLLB:
    '''
    现金流量表网址:https://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/600000/ctrl/2016/displaytype/4.phtml
    现金流量表板块
    '''

    def __init__(self, year, Company_number):
        self.year = year
        self.Company_number = Company_number

        self.response = spidertool.get(
            f'https://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/{self.Company_number}/ctrl/{self.year}/displaytype/4.phtml').text

        self.time_list = []
        self.zichan_list = []
        self.fuzhai_list = []
        self.syzqy_list = []

        self.time_headline_list = []
        self.zichan_headline_list = []
        self.fuzhai_headline_list = []
        self.syzqy_headline_list = []

        spidertool.create_infile(name='浦发银行现金流量表')

    def parse(self, xpath_num):
        '''
        :param xpath_num:
        1:报表日期
        2:None
        3:经营活动产生的现金流量:4-17
        18:投资活动产生的现金流量:19-29
        30:筹资活动产生的现金流量:31-43
        44:汇率变动对现金及现金等价物的影响
        45-46:现金及现金等价物净增加额
        47:期末现金及现金等价物余额
        48:附注:49-96
        :return:
        '''
        num_list = [i for i in range(2, 6)]
        need_list = [
            spidertool.xpath(self.response, f'//*[@id="ProfitStatementNewTable0"]/tbody/tr[{xpath_num}]/td[{i}]/text()')
            for i in num_list]
        return need_list

    def get_time(self):
        '''
        :return: 报表时间
        '''
        return self.parse(1)

    def get_jyhd(self):
        '''
        :return: 经营活动产生的现金流量的小标题与值
        '''
        for i in range(4, 18):
            headline = spidertool.xpath(self.response, f'//*[@id="ProfitStatementNewTable0"]/tbody/tr[{i}]//a/text()')
            self.zichan_headline_list.append(headline)

        for i in range(4, 18):
            self.zichan_list.append(self.parse(i))
        # print(self.zichan_headline_list)
        return self.zichan_headline_list, self.zichan_list

    def get_tzhd(self):
        '''
        :return: 投资活动产生的现金流量的小标题与值
        '''
        for i in range(19, 30):
            headline = spidertool.xpath(self.response, f'//*[@id="ProfitStatementNewTable0"]/tbody/tr[{i}]//a/text()')
            self.zichan_headline_list.append(headline)

        for i in range(19, 30):
            self.zichan_list.append(self.parse(i))
        # print(self.zichan_headline_list)
        return self.zichan_headline_list, self.zichan_list

    def get_czhd(self):
        '''
        :return: 筹资活动产生的现金流量的小标题与值
        '''
        for i in range(31, 44):
            headline = spidertool.xpath(self.response, f'//*[@id="ProfitStatementNewTable0"]/tbody/tr[{i}]//a/text()')
            self.zichan_headline_list.append(headline)

        for i in range(31, 44):
            self.zichan_list.append(self.parse(i))
        # print(self.zichan_headline_list)
        return self.zichan_headline_list, self.zichan_list

    def get_hlbd(self):
        '''
        :return: 汇率变动对现金及现金等价物的影响的小标题与值
        '''
        for i in range(44, 45):
            headline = spidertool.xpath(self.response, f'//*[@id="ProfitStatementNewTable0"]/tbody/tr[{i}]//a/text()')
            self.zichan_headline_list.append(headline)

        for i in range(44, 45):
            self.zichan_list.append(self.parse(i))
        # print(self.zichan_headline_list)
        return self.zichan_headline_list, self.zichan_list

    def get_xjdjw(self):
        '''
        :return: 现金及现金等价物净增加额的小标题与值
        '''
        for i in range(45, 47):
            headline = spidertool.xpath(self.response, f'//*[@id="ProfitStatementNewTable0"]/tbody/tr[{i}]//a/text()')
            self.zichan_headline_list.append(headline)

        for i in range(45, 47):
            self.zichan_list.append(self.parse(i))
        # print(self.zichan_headline_list)
        return self.zichan_headline_list, self.zichan_list

    def get_qmxj(self):
        '''
        :return: 期末现金及现金等价物余额的小标题与值
        '''
        for i in range(47, 48):
            headline = spidertool.xpath(self.response, f'//*[@id="ProfitStatementNewTable0"]/tbody/tr[{i}]//a/text()')
            self.zichan_headline_list.append(headline)

        for i in range(47, 48):
            self.zichan_list.append(self.parse(i))
        # print(self.zichan_headline_list)
        return self.zichan_headline_list, self.zichan_list

    def get_fuzhu(self):
        '''
        :return: 附注的小标题与值
        '''
        for i in range(49, 97):
            headline = spidertool.xpath(self.response, f'//*[@id="ProfitStatementNewTable0"]/tbody/tr[{i}]//a/text()')
            self.zichan_headline_list.append(headline)

        for i in range(49, 97):
            self.zichan_list.append(self.parse(i))
        # print(self.zichan_headline_list)
        return self.zichan_headline_list, self.zichan_list

    def export_excel(self, title_lst, value_lst):
        '''
        :param title_lst: 表头列表
        :param value_lst: 值列表
        :return: None
        '''
        # 合并为字典
        data_dict = {}
        for header, value in zip(title_lst, value_lst):
            data_dict[header[0]] = [v[0] for v in value]
        # 创建DataFrame对象
        df = pd.DataFrame(data_dict)
        # 写入Excel文件
        file_path = f'浦发银行现金流量表/浦发银行{self.year}现金流量表.xlsx'
        if not os.path.exists(file_path):
            df.to_excel(file_path, index=False)
        else:
            # 读取已有的Excel文件
            existing_df = pd.read_excel(file_path)
            # 合并新数据与已有数据
            df = pd.concat([existing_df, df], ignore_index=True)
            # 写入Excel文件
            df.to_excel(file_path, index=False)

    def run(self):
        '''
        启动函数
        '''
        title1, value1 = self.get_jyhd()
        title2, value2 = self.get_tzhd()
        title3, value3 = self.get_czhd()
        title4, value4 = self.get_hlbd()
        title5, value5 = self.get_xjdjw()
        title6, value6 = self.get_qmxj()
        title7, value7 = self.get_fuzhu()

        title1.extend(title2)
        title1.extend(title3)
        title1.extend(title4)
        title1.extend(title5)
        title1.extend(title6)
        title1.extend(title7)

        value1.extend(value2)
        value1.extend(value3)
        value1.extend(value4)
        value1.extend(value5)
        value1.extend(value6)
        value1.extend(value7)

        return self.export_excel(title1, value1)


def main():
    lrb = LRB()
    lrb.run()
    for i in tqdm(range(2014, 2024), desc='完成进度'):
        zcfzb = ZCFZB(i, 600000)
        zcfzb.run()
        xjllb = XJLLB(i, 600000)
        xjllb.run()


if __name__ == '__main__':
    main()
