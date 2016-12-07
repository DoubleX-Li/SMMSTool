import requests


class ImageUrl():
    """
    存放图片的路径和删除路径
    """
    def __init__(self, name, url, delete):
        self.name = name
        self.url = url
        self.delete = delete


class SMMSTool():
    """
    sm.ms工具
    api：https://sm.ms/doc/
    """
    uploadUrl = 'https://sm.ms/api/upload'
    historyUrl = 'https://sm.ms/api/list'
    clearUrl = 'https://sm.ms/api/clear'
    urlList = []

    def __init__(self):
        self.cookies = dict(PHPSESSID='')

    def upload(self, filepath):
        """
        上传图片
        :param filepath: 待上传图片路径
        :return: [int, string] 状态码，状态
        """
        print("开始上传图片")
        files = {
            'smfile':open(filepath, 'rb')
        }
        params = {
            'ssl':True
        }
        r = requests.post(self.uploadUrl, params=params, files=files)
        commit_data = r.json()
        self.cookies['PHPSESSID'] = r.cookies['PHPSESSID']

        # 获取上传文件状态
        code = commit_data['code']
        if code == "success":       # 成功则构造ImageUrl加入urlList
            filename = commit_data['data']['filename']
            url = commit_data['data']['url']
            delete = commit_data['data']['delete']
            self.urlList.append(ImageUrl(filename, url, delete))
            self.outputInfo()
            return [0, "上传成功"]
        elif code == "error":       # 返回"error"则返回错误msg
            msg = commit_data['msg']
            return [-1, msg]
        else:
            return [-2, "未知异常"]

    def delete(self, imageUrl):
        """
        删除图片
        :param imageUrl: 待上传图片的ImageUrl对象
        :return: [int, string] 状态码，状态
        """
        print("开始删除图片")
        deleteUrl = imageUrl.delete
        r = requests.get(deleteUrl)
        if r.status_code == 200:
            return [0, "删除成功"]
        else:
            return [-1, "未知异常"]

    def history(self):
        """
        查询上传历史
        重要！！！：若要关闭程序后仍能查询到历史记录，应在upload中保存cookies，待施工
        :return: [int, string] 状态码，状态
        """
        print("开始查询历史记录")
        r = requests.get(self.historyUrl, cookies=self.cookies)
        commit_data = r.json()
        code = commit_data['code']
        if code == 'success':
            if len(commit_data['data']) == 0:
                return [-1, "没有已上传的文件"]
            else:
                return [0, commit_data['data']]
        elif code == 'error':
            return [-2, "没有已上传的文件"]

    def clear(self):
        """
        清空历史记录
        重要！！！：若要关闭程序后仍能清除历史记录，应在upload中保存cookies，待施工
        :return: [str, str] 状态码，状态
        """
        print("开始清除历史记录")
        r = requests.get(self.clearUrl, cookies = self.cookies)
        commit_data = r.json()
        code = commit_data['code']
        msg = commit_data['msg']
        return [code, msg]

    def outputInfo(self):
        print("内置输出")
        for url in self.urlList:
            print("url:" + url.url + "\n" + "delete:" + url.delete + "\n\n")

# if __name__ == "__main__":
#     tool = SMMSTool()
#
#     clearCode, clearMsg = tool.clear()
#     print(clearMsg)
#
#     filepath1 = r"D:\test.jpg"
#     uploadStatus, uploadMsg = tool.upload(filepath1)
#     print(uploadMsg)
#
#     for url in tool.urlList:
#         print("url:" + url.url + "\n" + "delete:" + url.delete + "\n\n")
#
#     filepath2 = r"D:\test2.jpg"
#     uploadStatus, uploadMsg = tool.upload(filepath2)
#     print(uploadMsg)
#
#     for url in tool.urlList:
#         print("url:" + url.url + "\n" + "delete:" + url.delete + "\n\n")
#
#     historyStatus, historyData = tool.history()
#     if historyStatus == -1 or -2:
#         print(historyData)
#     elif historyStatus == 0:
#         for data in historyData:
#             print("url:" + data['url'] + "\n" + "delete:" + data['delete'] + "\n\n")





