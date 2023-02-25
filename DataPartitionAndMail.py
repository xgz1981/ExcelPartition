# encoding: utf8
import datetime
import os

import pandas
import win32com.client as win32


def read_excel(excel_path):
    contact_sheet_datas = dict()
    sheet_datas = pandas.read_excel(excel_path, sheet_name=0)
    for sheet_name, sheet_data in sheet_datas.items():
        sheet_data = pandas.DataFrame(sheet_data)
        grouped_datas = sheet_data.groupby("数据接口人账号")
        for group_name, grouped_data in grouped_datas:
            if group_name in contact_sheet_datas.keys():
                sheet_contact_data = contact_sheet_datas.get(group_name)
            else:
                sheet_contact_data = dict()
                contact_sheet_datas[group_name] = sheet_contact_data
            sheet_contact_data[sheet_name] = grouped_data
    return contact_sheet_datas


def write_excel_by_contact(contact_sheet_datas):
    contact_file = dict()
    path = "C:\\月度数据发放\\" + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + "\\"
    os.makedirs(path)
    for contact, contact_datas in contact_sheet_datas.items():
        excel_path = r'{}数据分发表to—{}.xlsx'.format(path, contact)
        with pandas.ExcelWriter(excel_path) as writer:
            for sheet_name, contact_data in contact_datas.items():
                contact_data.to_excel(writer, sheet_name=sheet_name, index=False)
        contact_file[contact] = excel_path
    print(f"数据已经拆分到 {path}")
    return contact_file


def send_mail(mail_address, excel_file):
    outlook = win32.Dispatch('Outlook.Application')
    mail_item = outlook.CreateItem(0)   # 0: olMailItem
    mail_item.Recipients.Add(mail_address + '@envision-energy.com')
    mail_item.Subject = '月度数据发放'
    mail_item.BodyFormat = 2    # 2: Html format
    mail_item.Attachments.Add(excel_file)
    mail_item.HTMLBody  = '''
        <H2>你好，数据分发邮件，请及时查收.</H2>
        '''
    mail_item.Send()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print("需要传入两个参数：excel文件路径，必选；是否发送邮件，可选")
    #     print("Excel路径，如：c:\\excel\\excel.xslx")
    #     print("是否发送邮件，1:发送，0：不发送")
    #     sys.exit(1)

    # excel_file = sys.argv[1]
    # mail_or_not = sys.argv[2]
    
    excel_file = r'D:\系统数据分发表.xlsx'
    mail_or_not = False
    print(excel_file)
    print(mail_or_not)
    contact_sheet_datas = read_excel(excel_file)
    contact_file = write_excel_by_contact(contact_sheet_datas)
    if (int(mail_or_not)):
        for contact, excel_file in contact_file.items():
            send_mail(contact, excel_file)
        print("邮件已发送")
    print("over")



