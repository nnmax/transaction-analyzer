import os
import re
import math
import traceback
import pandas as pd

print(pd.__version__)

# 模拟JavaScript的parseFloat函数行为
def parse_float(s):
    # 使用正则表达式匹配字符串开头的数字部分
    match = re.match(r'^[-+]?\d*\.?\d+', s)
    if match:
        return float(match.group(0))
    return float('nan')  # 如果没有匹配到数字，返回NaN

# 智能打开文件，自动处理编码问题（兼容Windows中文系统）
def open_file_with_encoding(file_path, mode='r'):
    """
    尝试使用多种编码打开文件，解决Windows中文系统下的编码问题
    先尝试UTF-8，如果失败则尝试GBK等中文编码
    """
    encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030']
    
    # 先尝试用二进制模式读取一小部分来测试编码
    for encoding in encodings:
        try:
            # 打开文件并尝试读取第一行来验证编码
            f = open(file_path, mode, encoding=encoding)
            # 读取第一行测试编码是否有效
            first_line = f.readline()
            # 重置文件指针到开头
            f.seek(0)
            return f
        except UnicodeDecodeError:
            # 如果读取失败，关闭文件（如果已打开）并尝试下一个编码
            try:
                f.close()
            except:
                pass
            continue
        except Exception:
            # 其他异常也继续尝试下一个编码
            try:
                f.close()
            except:
                pass
            continue
    
    # 如果所有编码都失败，使用GBK并忽略错误
    return open(file_path, mode, encoding='gbk', errors='ignore')

def main():
    try:
        # 查找当前目录的第一个 .txt 文件
        files = os.listdir('./')
        txt_file = None
        for file in files:
            if file.endswith('.txt'):
                txt_file = file
                break

        if not txt_file:
            print('未找到 .txt 文件')
            return

        count_lines_with_number(txt_file)
        sum_numbers_after_keyword(txt_file)
        count_realtime_tax_from_a(txt_file)
    
    except Exception as e:
        print(f"程序运行出错: {e}")
        print("\n详细错误信息:")
        traceback.print_exc()

"""
统计借方笔数和贷方笔数
"""
def count_lines_with_number(txt_file):
    count1 = 0
    count2 = 0
    
    try:
        with open_file_with_encoding(txt_file, 'r') as file:
            for line in file:
                parts = line.split('|')
                if len(parts) > 8:
                    try:
                        num1 = parse_float(parts[7].strip().replace(',', ''))
                        if not math.isnan(num1):
                            count1 += 1
                    except:
                        pass
                    
                    try:
                        num2 = parse_float(parts[8].strip().replace(',', ''))
                        if not math.isnan(num2):
                            count2 += 1
                    except:
                        pass
        
        print(f"借方笔数: {count1:,}; 贷方笔数: {count2:,}")
    except Exception as e:
        print(f"统计借贷方笔数时出错: {e}")

"""
统计借方合记或贷方合记
"""
def sum_numbers_after_keyword(txt_file):
    total_sum1 = 0
    total_sum2 = 0
    
    try:
        with open_file_with_encoding(txt_file, 'r') as file:
            for line in file:
                type1 = '借方合计'
                type2 = '贷方合计'
                index1 = line.find(type1)
                index2 = line.find(type2)
                
                if index1 != -1:
                    number_part = line[index1 + len(type1):].strip().replace(',', '')
                    try:
                        number = parse_float(number_part)
                        if not math.isnan(number):
                            total_sum1 += number
                    except:
                        pass
                        
                if index2 != -1:
                    number_part = line[index2 + len(type2):].strip().replace(',', '')
                    try:
                        number = parse_float(number_part)
                        if not math.isnan(number):
                            total_sum2 += number
                    except:
                        pass
        
        print(f"借方合记: {total_sum1:,.2f}; 贷方合记: {total_sum2:,.2f}")
    except Exception as e:
        print(f"统计借贷方合计时出错: {e}")

"""
统计交易类型为「实时缴税」的笔数与借方发生额合计
"""
def count_realtime_tax_from_a(txt_file):
    count = 0
    debit_sum = 0

    try:
        with open_file_with_encoding(txt_file, 'r') as file:
            for line in file:
                parts = line.split('|')
                if len(parts) <= 8:
                    continue
                if parts[4].strip() != '实时缴税':
                    continue

                count += 1
                debit = parse_float(parts[7].strip().replace(',', ''))
                if not math.isnan(debit):
                    debit_sum += debit

        print(f"实时缴税笔数: {count:,}; 借方发生额合计: {debit_sum:,.2f}")
    except Exception as e:
        print(f"统计实时缴税数据时出错: {e}")

if __name__ == "__main__":
    main()
    
    # 防止窗口立即关闭
    input("\n按回车键退出程序...")
