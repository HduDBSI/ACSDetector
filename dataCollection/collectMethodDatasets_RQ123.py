import os
import os.path
from tqdm import tqdm
import regex as re
import csv
import Levenshtein
import random
import shutil
from astTools import *
import json
from tqdm import tqdm
from func_timeout import func_set_timeout, FunctionTimedOut

def copyfile(old_file_path,new_folder_path):
    shutil.copy(old_file_path, new_folder_path)

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
def codeNormalize(codepath):
    programfile=open(codepath,encoding='utf-8')
    programtext=programfile.read()
    #print("programtext",programtext)
    #删除代码中的所有注释
    programtext = re.sub(r'((\/[*]([*].+|[\\n]|\\w|\\d|\\s|[^\\x00-\\xff])+[*]\/))', "", programtext)
    #print("programtext",programtext)
    return programtext

def getmethodMetricxDict(methodMetricsfile):
    with open(methodMetricsfile, 'r') as csvfile:
        methodMetricsDict = {}
        spamreader = csv.reader(csvfile)
        line = 0
        for row in spamreader:
            if line>0:
                key = '-'.join(row[:4])
                value = list(map(float, row[4:]))
                methodMetricsDict[key] = value
            line+=1
    #print(len(methodMetricsDict))
    return methodMetricsDict

def getCodeSmellDict(codeSmellsfile):
    with open(codeSmellsfile, 'r') as csvfile:
        codesmelldict = {}
        spamreader = csv.reader(csvfile)
        line = 0
        for row in spamreader:
            if line>0:
                key = '-'.join(row[1:4])+'.java'
                value = str(row[4])
                codesmelldict[key] = value
            line+=1
    return codesmelldict

projectList = ['Ant','jruby','kafka','mockito','storm','tomcat']



# Ant
project = projectList[0]
threshold000 = 12.03
threshold111 = 12.03
less1 = 0 #----------------> 01 #00000
less2 = 1 #----------------> 01 #11111
flag = 1 #----------------> 01
# # jruby
project = projectList[1]
threshold000 = 6.52
threshold111 = 6.52
less1 = 0 #----------------> 01 #00000
less2 = 0 #----------------> 01 #11111
flag = 1 #----------------> 01
# # kafka
project = projectList[2]
threshold000 = 12.85
threshold111 = 12.85
less1 = 0 #----------------> 01 #00000
less2 = 0 #----------------> 01 #11111
flag = 1 #----------------> 01
# # mockito
project = projectList[3]
threshold000 = 93.72
threshold111 = 93.72
less1 = 0 #----------------> 01 #00000
less2 = 0 #----------------> 01 #11111
flag = 1 #----------------> 01
# # storm
project = projectList[4]
threshold000 = 12
threshold111 = 12
less1 = 0 #----------------> 01 #00000
less2 = 0 #----------------> 01 #11111
flag = 1 #----------------> 01
# # tomcat
project = projectList[5]
threshold000 = 6
threshold111 = 6
less1 = 0 #----------------> 01 #00000
less2 = 0 #----------------> 01 #11111
flag = 1 #----------------> 01


aim = 0  #----------------> 123
s10_th = 0 #1
s_000_th = 0 #2
s_111_th = 0 #3

survival_refact_list = []
survival_no_refact_list = []
savePath = 'DataSet/'+project+'/methods/'
if aim==0:
    trainLabelPath = savePath+"/trainlabels.txt"
    testLabelPath = savePath+"/testlabels.txt"
    s10_th = 100000
    s_000_th = 2543
    s_111_th = 100000
elif aim==1:
    trainLabelPath = savePath+"/trainlabels_s10.txt"
    testLabelPath = savePath+"/testlabels_s10.txt"
    s10_th = 100
elif aim==2:
    trainLabelPath = savePath+"/trainlabels_s_000.txt"
    testLabelPath = savePath+"/testlabels_s_000.txt"
    s_000_th = 100
elif aim==3:
    trainLabelPath = savePath+"/trainlabels_s_111.txt"
    testLabelPath = savePath+"/testlabels_s_111.txt"
    s_111_th = 100


#aProjectVersionsPath = '/home/yqx/Downloads/DesigniteJava-master/myData/'+project+'Versions/'
aProjectVersionsLabeledPath = project+'VersionsLabeled/'
methodfilepath = 'DataSet/'+project+"/methods/pureJavaMethod"
jsonfilepath = 'DataSet/'+project+"/methods/rawjson"

versionList = list(traversalDir_FirstDir(aProjectVersionsLabeledPath))
versionList.sort(key=lambda x: tuple(int(v) for v in x.split('-')[-1].split(".")), reverse=False)
print(versionList)


methodVersionDict = {}
smellVersionDict = {}
methodMetricVersionDict = {}
methodList = []
for version in tqdm(versionList):
    methodPath = aProjectVersionsLabeledPath+version+'/pureJavaMethod/'
    implementationCodeSmells = aProjectVersionsLabeledPath+version+'/implementationCodeSmells.csv'
    methodMetricsfile = aProjectVersionsLabeledPath+version+'/methodMetrics.csv'
    for root,dirs,files in os.walk(methodPath):
        methodVersionDict[version] = files
        methodList+=files
    smellVersionDict[version] = getCodeSmellDict(implementationCodeSmells)
    methodMetricVersionDict[version] = getmethodMetricxDict(methodMetricsfile)


projectVersionSmell = {}
for javaFile in tqdm(set(methodList)):
    row = []
    for i,version in enumerate(versionList):
        #首先判断是不是smell,否则是不是0，再不然是不是不存在（-1）
        if javaFile in smellVersionDict[version]:
            row.append(1)
        elif javaFile in methodVersionDict[version]:
            row.append(0)
        else:
            row.append(-1)
    projectVersionSmell[javaFile] = row

#print(projectVersionSmell)

posPaths = []
negPaths = []

s10 = 0
s1_ = 0
s0_ = 0
s_000 = 0
s_111 = 0
for code in projectVersionSmell:
    create_version = 0
    refact_version = 0
    survival_versions = 0
    for i,v in enumerate(projectVersionSmell[code]):
        if i>0 and projectVersionSmell[code][i-1] != 1 and v==1 or i==0 and v==1:
            create_version = i
        if i<len(versionList)-1 and v==1 and projectVersionSmell[code][i+1] == 0 and s10<s10_th:
            posPath = aProjectVersionsLabeledPath+versionList[i]+'/pureJavaMethod/'+code
            negPath = aProjectVersionsLabeledPath+versionList[i+1]+'/pureJavaMethod/'+code
            posPaths.append(posPath)
            negPaths.append(negPath)
            s10+=1
            refact_version = i
            survival_versions = refact_version - create_version + 1
            #print('survival_versions: ', survival_versions, posPath)
            survival_refact_list.append(survival_versions)
            create_version = 0
            refact_version = 0

    
    for i in range(len(versionList)):
        #构造[-1,-1,0,0,0,0,0,0,0]
        aa = []
        for j in range(i):
            aa.append(-1)
        for k in range(len(versionList)-i):
            aa.append(0)
        #print(aa)
        survival_versions = aa.count(0)
        if aa == projectVersionSmell[code] and survival_versions>threshold000 and s_000<s_000_th:
            # 取中间版本
            negPath = aProjectVersionsLabeledPath+versionList[aa.count(-1)+aa.count(0)//2]+'/pureJavaMethod/'+code
            negPaths.append(negPath)
            s_000+=1

            # 此类样本不够，则多次采样，如采集首尾数据
            if less1==1:
                negPath = aProjectVersionsLabeledPath+versionList[aa.count(-1)]+'/pureJavaMethod/'+code
                negPaths.append(negPath)
                s_000+=1
                negPath = aProjectVersionsLabeledPath+versionList[len(aa)-1]+'/pureJavaMethod/'+code
                negPaths.append(negPath)
                s_000+=1


        #构造[-1,-1,1,1,1,1,1,1,1]
        bb = []
        for j in range(i):
            bb.append(-1)
        for k in range(len(versionList)-i):
            bb.append(1)
        survival_versions = bb.count(1)
        if bb == projectVersionSmell[code] and survival_versions>threshold111 and s_111<s_111_th:
            # 取中间样本
            negPath = aProjectVersionsLabeledPath+versionList[bb.count(-1)+bb.count(1)//2]+'/pureJavaMethod/'+code
            negPaths.append(negPath)
            s_111+=1
            survival_no_refact_list.append(survival_versions)
            # 此类样本不够，则多次采样，如采集首尾数据
            if less2==1:
                negPath = aProjectVersionsLabeledPath+versionList[bb.count(-1)]+'/pureJavaMethod/'+code
                negPaths.append(negPath)
                s_111+=1
                negPath = aProjectVersionsLabeledPath+versionList[len(bb)-1]+'/pureJavaMethod/'+code
                negPaths.append(negPath)
                s_111+=1

                negPath = aProjectVersionsLabeledPath+versionList[bb.count(-1)+2]+'/pureJavaMethod/'+code
                negPaths.append(negPath)
                s_111+=1
                negPath = aProjectVersionsLabeledPath+versionList[len(bb)-1-2]+'/pureJavaMethod/'+code
                negPaths.append(negPath)
                s_111+=1
                
               
                
            
print(len(posPaths))
print(len(negPaths))

print('survival_refact_list',survival_refact_list)
print('survival_no_refact_list',survival_no_refact_list)

print(len(posPaths)+len(negPaths))
print(len(posPaths+negPaths))

print('s10',s10)
print('s_000',s_000)
print('s_111',s_111)

print('posPaths',len(posPaths))
print('negPaths',len(negPaths))

if flag==0:
    exit()
mkdir(savePath+'pureJavaMethod')

#乱序
random.shuffle(posPaths)
random.shuffle(negPaths)

# 划分 训练集：测试集 = 6:4
trainSamples = []
testSamples = []

for i,v in enumerate(negPaths):
    #print('negPath',v)
    #/home/yqx/Downloads/DesigniteJava-master/myData/AntVersionsLabeled/ant-rel-1.9.5/pureJavaMethod/org.apache.tools.ant.taskdefs.optional.pvcs-PvcsProject.java
    #/home/yqx/Downloads/DesigniteJava-master/myData/AntVersionsLabeled/ant-rel-1.8.4/pureJavaMethod/org.apache.tools.ant.taskdefs.optional-Rpm-guessRpmBuildCommand.java
    newname = savePath+'pureJavaMethod/'+'-'.join([v.split('/')[-3],v.split('/')[-1]])
    copyfile(v,newname)
    v = '-'.join([v.split('/')[-3],v.split('/')[-1]])
    if i < len(negPaths) * 0.6:
        trainSamples.append(v+'    0\n')
    else:
        testSamples.append(v+'    0\n')

for i,v in enumerate(posPaths):
    newname = savePath+'pureJavaMethod/'+'-'.join([v.split('/')[-3],v.split('/')[-1]])
    copyfile(v,newname)
    v = '-'.join([v.split('/')[-3],v.split('/')[-1]])
    if i < len(posPaths) * 0.6:
        trainSamples.append(v+'    1\n')
    else:
        testSamples.append(v+'    1\n')

#乱序写入train test文件
random.shuffle(trainSamples)
random.shuffle(testSamples)
'''
trainLabelPath = savePath+"/trainlabels.txt"
testLabelPath = savePath+"/testlabels.txt"
'''
trainLabelFile = open(trainLabelPath, 'w')
testLabelPath = open(testLabelPath, 'w')

trainLabelFile.writelines(trainSamples)
testLabelPath.writelines(testSamples)

trainLabelFile.close()
testLabelPath.close()



edgelabels={'childFather':0,'Nextsib':1,'Nexttoken':2,'Prevtoken':3,'Nextuse':4,'Prevuse':5,'If':6,'Ifelse':7,'While':8,'For':9,'Nextstmt':10,'Prevstmt':11,'Prevsib':12}
edgelabels_new = dict(zip(edgelabels.values(),edgelabels.keys()))



mkdir(jsonfilepath)
#解析抽象语法树
astparseexceptions = 0
for root, ds, files in os.walk(methodfilepath):
    for file in tqdm(files):
        codepath = root + '/' + file
        #/home/yqx/Downloads/DesigniteJava-master/myData/Ant/pureJavaMethod/ant-rel-1.1-com.oreilly.servlet-MailMessage.java
        #/home/yqx/Downloads/DesigniteJava-master/myData/Ant/methods/pureJavaMethod/ant-rel-1.7.0-org.apache.tools.ant.taskdefs-AllHandler-handle.java
        #print(codepath)
        
        try:
            pureAST = code2AST(codepath) #得到AST需要的数据，递归各节点遍历出一棵树 tree
            codeName = codepath.split('/')[-1][:-5]
            #print('codeName',codeName)
            version = '-'.join(codepath.split('/')[-1].split('-')[:-3])
            #print('version',version)
            methodMetrics = methodMetricVersionDict[version]

            #利用深度优先递归出结点列表（用于收集词库corpus和存储一个nodelist.json便于使用ELMO提取动态词向量）
            newtree, nodelist = getNodeList(pureAST)
            #print("nodelist",nodelist)

            #统计各种语句数量
            ifcount,whilecount,forcount,blockcount,docount,switchcount,alltokens,vocabdict = astStaticCollection(pureAST)

            # 遍历出树中所有的结点\边\边类型
            x,vocabdict,edge_index,edge_attr = getFA_AST(newtree, vocabdict)

            #准备封装数据：proj_pkg_cls.json = {"nodelist":{},"node":{},"edge":{},"metrics":[]}
            #准备封装label：labeled.txt  ：   proj_pkg_cls  0 / 1
            #得到node{}：（利用x和vocabdict）、得到edge{}：{利用edge_index和edge_attr}、得到metrics和label：读取CSV文件

            #保存raw json文件
            getJsonFile(nodelist,x,vocabdict,edge_index,edge_attr,edgelabels,edgelabels_new,methodMetrics,jsonfilepath,codeName)
        except:
            astparseexceptions+=1
print("astparseexceptions:", astparseexceptions)