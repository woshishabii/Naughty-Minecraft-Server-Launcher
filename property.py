# http://blog.sina.com.cn/s/blog_6a24f10901018lhn.html

class Property:
    fileName = ''
    def __init__(self, fileName):
        self.fileName = fileName

    def getProperties(self):
        try:
            pro_file = open(self.fileName, 'r')
            properties = {}
            for line in pro_file:
                if line.fing('=') > 0:
                    strs = line.replace('\n', '').split('=')
                    properties[strs[0]] = str[1]
        except Exception, e:
            raise e
        else:
            pro_file.close()
            return properties

