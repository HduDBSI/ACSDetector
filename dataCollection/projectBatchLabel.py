import os
import os.path
from tqdm import tqdm

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        print(path + ' 目录已存在')
        return False
def traversalDir_FirstDir(path):
    list = []
    if (os.path.exists(path)):
        files = os.listdir(path)
        for file in files:
            m = os.path.join(path,file)
            if (os.path.isdir(m)):
                h = os.path.split(m)
                #print(h[1])
                list.append(h[1])
        return list
    

jarPath = '/home/yqx/Downloads/DesigniteJava-master/myData/DesigniteJava.jar'
rootPath = '/home/yqx/Downloads/DesigniteJava-master/myData/'

#projectList = ['Ant','gradle','tomcat','kafka','jruby','neo4j','mockito','storm','hadoop','jmeter']

projectList = ['Ant','flink','gradle','hadoop','hbase','jruby','kafka','mockito','storm','tomcat']

project = projectList[9]

aProjectVersionsPath = '/home/yqx/Downloads/DesigniteJava-master/myData/'+project+'Versions/'
aProjectVersionsLabeledPath = '/home/yqx/Downloads/DesigniteJava-master/myData/'+project+'VersionsLabeled/'


projectList = traversalDir_FirstDir(aProjectVersionsPath)
print(projectList)
#遍历所有项目，为每个项目生成输入和输出路径
#i.e., java -jar DesigniteJava.jar -i /home/yqx/Downloads/DesigniteJava-master/myData/sourceProject5/sql12 -o /home/yqx/Downloads/DesigniteJava-master/myData/projrctLabled5/sql12
for project in tqdm(projectList):
    projectPath = aProjectVersionsPath+project
    outPath = aProjectVersionsLabeledPath+project
    #创建 pureJava 和 pureJavaMethod 文件夹
    mkdir('/home/yqx/Downloads/DesigniteJava-master/myData/pureJava/')
    mkdir('/home/yqx/Downloads/DesigniteJava-master/myData/pureJavaMethod/')
    #执行 DesigniteJava 的命令行
    os.system('java -jar ' + jarPath + ' -i ' + projectPath + ' -o ' + outPath)
    #将 pureJava 和 pureJavaMethod 文件夹移动到输出路径中
    os.system('mv '+rootPath+'pureJava/ ' + outPath)
    os.system('mv '+rootPath+'pureJavaMethod/ ' + outPath)



