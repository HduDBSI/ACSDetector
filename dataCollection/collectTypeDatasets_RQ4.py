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

def getTypeMetricxDict(typeMetricsfile):
    with open(typeMetricsfile, 'r') as csvfile:
        typeMetricsDict = {}
        spamreader = csv.reader(csvfile)
        line = 0
        for row in spamreader:
            if line>0:
                key = '-'.join(row[:3])
                value = list(map(float, row[3:]))
                typeMetricsDict[key] = value
            line+=1
    #print(len(typeMetricsDict))
    return typeMetricsDict

def getCodeSmellDict(codeSmellsfile):
    with open(codeSmellsfile, 'r') as csvfile:
        codesmelldict = {}
        spamreader = csv.reader(csvfile)
        line = 0
        for row in spamreader:
            if line>0:
                key = '-'.join(row[1:3])+'.java'
                value = str(row[3])
                codesmelldict[key] = value
            line+=1
    return codesmelldict

jarPath = '/home/yqx/Downloads/comment_data/comment-data/DesigniteJava-master/myData/DesigniteJava.jar'
rootPath = '/home/yqx/Downloads/comment_data/comment-data/DesigniteJava-master/myData/'



#projectList = ['Ant','flink','gradle','hadoop','hbase','jruby','kafka','mockito','storm','tomcat']
projectList = ['Ant','jruby','kafka','mockito','storm','tomcat']

projectList = ['hadoop','hbase','gradle','flink']
project = projectList[3]

savePath = '/home/yqx/Downloads/comment_data/comment-data/DesigniteJava-master/myData/'+project+'_new'+'/types/'

typeSmellList = ['Imperative Abstraction','Multifaceted Abstraction','Unnecessary Abstraction','Unutilized Abstraction',
'Deﬁcient Encapsulation','Unexploited Encapsulation','Broken Modularization','Cyclic-Dependent Modularization',
'Insufﬁcient Modularization','Hub-like Modularization','Broken Hierarchy','Cyclic Hierarchy','Deep Hierarchy',
'Missing Hierarchy','Multipath Hierarchy','Rebellious Hierarchy','Wide Hierarchy']

#current_smell = typeSmellList[0]

for current_smell in typeSmellList:

    print(current_smell)
    threshold = 0.9
    less1 = 0 #----------------> 01 #00000
    less2 = 0 #----------------> 01 #11111


    flag = 1 #----------------> 01



    aim = 1  #----------------> 12345

    s10_th = 0 #1
    s1__th = 0 #2
    s0__th = 0 #3  ###
    s_000_th = 0 #4
    s_111_th = 0 #5

    if aim==0:
        trainLabelPath = savePath+"/trainlabels.txt"
        testLabelPath = savePath+"/testlabels.txt"
        s10_th = 2000
        s1__th = s10_th
        s0__th = 0
        s_000_th = 2000
        s_111_th = s_000_th
    elif aim==1:
        trainLabelPath = savePath+"/trainlabels_s10.txt"
        testLabelPath = savePath+"/testlabels_s10_"+current_smell+".txt"
        s10_th = 1000000
    elif aim==2:
        trainLabelPath = savePath+"/trainlabels_s1_.txt"
        testLabelPath = savePath+"/testlabels_s1_.txt"
        s1__th = 1000000
    elif aim==3:
        trainLabelPath = savePath+"/trainlabels_s0_.txt"
        testLabelPath = savePath+"/testlabels_s0_.txt"
        s0__th = 1000000
    elif aim==4:
        trainLabelPath = savePath+"/trainlabels_s_000.txt"
        testLabelPath = savePath+"/testlabels_s_000.txt"
        s_000_th = 1000000
    elif aim==5:
        trainLabelPath = savePath+"/trainlabels_s_111.txt"
        testLabelPath = savePath+"/testlabels_s_111.txt"
        s_111_th = 1000000

    #aProjectVersionsPath = '/home/yqx/Downloads/comment_data/comment-data/DesigniteJava-master/myData/'+project+'Versions/'
    aProjectVersionsLabeledPath = '/home/yqx/Downloads/comment_data/comment-data/DesigniteJava-master/myData/'+project+'VersionsLabeled/'
    typefilepath = savePath+'pureJava'
    jsonfilepath = savePath+'rawjson'
    #print(typefilepath)
    versionList = list(traversalDir_FirstDir(aProjectVersionsLabeledPath))
    versionList.sort(key=lambda x: tuple(int(v) for v in x.split('-')[-1].split(".")), reverse=False)
    print(versionList)


    typeVersionDict = {}
    smellVersionDict = {}
    typeMetricVersionDict = {}
    typeList = []
    for version in tqdm(versionList):
        typePath = aProjectVersionsLabeledPath+version+'/pureJava/'
        designCodeSmells = aProjectVersionsLabeledPath+version+'/designCodeSmells.csv'
        typeMetricsfile = aProjectVersionsLabeledPath+version+'/typeMetrics.csv'
        for root,dirs,files in os.walk(typePath):
            typeVersionDict[version] = files
            typeList+=files
        smellVersionDict[version] = getCodeSmellDict(designCodeSmells)
        typeMetricVersionDict[version] = getTypeMetricxDict(typeMetricsfile)

    #print("smellVersionDict: ",smellVersionDict)
    projectVersionSmell = {}
    for javaFile in tqdm(set(typeList)):
        row = []                                                                                                                                                    
        for i,version in enumerate(versionList):
            #首先判断是不是smell,否则是不是0，再不然是不是不存在（-1）
            if javaFile in smellVersionDict[version] and smellVersionDict[version][javaFile] == current_smell:
                #print(current_smell)
                row.append(1)
            elif javaFile in typeVersionDict[version] and javaFile not in smellVersionDict[version]:
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
        for i,v in enumerate(projectVersionSmell[code]):
            if i<len(versionList)-1 and v==1 and projectVersionSmell[code][i+1] == 0 and s10<s10_th:
                posPath = aProjectVersionsLabeledPath+versionList[i]+'/pureJava/'+code
                negPath = aProjectVersionsLabeledPath+versionList[i+1]+'/pureJava/'+code
                posPaths.append(posPath)
                negPaths.append(negPath)
                s10+=1
            elif i<len(versionList)-1 and v==1 and projectVersionSmell[code][i+1] == -1 and s1_<s1__th:
                posPath = aProjectVersionsLabeledPath+versionList[i]+'/pureJava/'+code
                posPaths.append(posPath)
                s1_+=1
            #'''
            elif i<len(versionList)-1 and v==0 and projectVersionSmell[code][i+1] == -1 and s0_<s0__th:
                posPath = aProjectVersionsLabeledPath+versionList[i]+'/pureJava/'+code
                posPaths.append(posPath)
                s0_+=1
            #'''
        #构造[-1,-1,0,0,0,0,0,0,0]
        
        for i in range(len(versionList)):
            if (len(versionList)-i)/len(versionList)>threshold:
                aa = []
                for j in range(i):
                    aa.append(-1)
                for k in range(len(versionList)-i):
                    aa.append(0)
                #print(aa)
                if aa == projectVersionSmell[code] and s_000<s_000_th:
                    negPath = aProjectVersionsLabeledPath+versionList[(len(versionList)+i)//2]+'/pureJava/'+code
                    negPaths.append(negPath)
                    s_000+=1
                    if less1==1:
                        negPath = aProjectVersionsLabeledPath+versionList[i+1]+'/pureJava/'+code
                        negPaths.append(negPath)
                        s_000+=1
                        negPath = aProjectVersionsLabeledPath+versionList[len(versionList)-2]+'/pureJava/'+code
                        negPaths.append(negPath)
                        s_000+=1
                        '''
                        negPath = aProjectVersionsLabeledPath+versionList[len(versionList)-5]+'/pureJava/'+code
                        negPaths.append(negPath)
                        s_000+=1
                        negPath = aProjectVersionsLabeledPath+versionList[len(versionList)-7]+'/pureJava/'+code
                        negPaths.append(negPath)
                        s_000+=1
                        
                        negPath = aProjectVersionsLabeledPath+versionList[i+5]+'/pureJava/'+code
                        negPaths.append(negPath)
                        s_000+=1
                        
                        negPath = aProjectVersionsLabeledPath+versionList[i+10]+'/pureJava/'+code
                        negPaths.append(negPath)
                        s_000+=1
                        '''
            if (len(versionList)-i)/len(versionList)>threshold and s_111<s_111_th:# and False
                bb = []
                for j in range(i):
                    bb.append(-1)
                for k in range(len(versionList)-i):
                    bb.append(1)
                if bb == projectVersionSmell[code]:
                    negPath = aProjectVersionsLabeledPath+versionList[(len(versionList)+i)//2]+'/pureJava/'+code
                    negPaths.append(negPath)
                    s_111+=1
                    if less2==1:
                        negPath = aProjectVersionsLabeledPath+versionList[i+1]+'/pureJava/'+code
                        negPaths.append(negPath)
                        s_111+=1
                        negPath = aProjectVersionsLabeledPath+versionList[len(versionList)-2]+'/pureJava/'+code
                        negPaths.append(negPath)
                        s_111+=1

                        #'''
                        negPath = aProjectVersionsLabeledPath+versionList[i+5]+'/pureJava/'+code
                        negPaths.append(negPath)
                        s_111+=1
                        #negPath = aProjectVersionsLabeledPath+versionList[len(versionList)-6]+'/pureJava/'+code
                        #negPaths.append(negPath)
                        #s_111+=1
                        #negPath = aProjectVersionsLabeledPath+versionList[len(versionList)-12]+'/pureJava/'+code
                        #negPaths.append(negPath)
                        #s_111+=1
                        #'''
                
    print(len(posPaths))
    print(len(negPaths))

    print('len(posPaths)+len(negPaths):',len(posPaths)+len(negPaths))
    print('len(posPaths+negPaths):',len(posPaths+negPaths))

    print('s10',s10)
    print('s1_',s1_)
    print('s0_',s0_)
    print('s_000',s_000)
    print('s_111',s_111)
    if flag==0:
        exit()
    mkdir(savePath+'pureJava')

    #乱序
    random.shuffle(posPaths)
    random.shuffle(negPaths)

    # 划分 训练集：测试集 = 6:4
    trainSamples = []
    testSamples = []

    for i,v in enumerate(negPaths):
        #/home/yqx/Downloads/comment_data/comment-data/DesigniteJava-master/myData/AntVersionsLabeled/ant-rel-1.9.5/pureJava/org.apache.tools.ant.taskdefs.optional.pvcs-PvcsProject.java
        newname = savePath+'pureJava/'+'-'.join([v.split('/')[-3],v.split('/')[-1]])
        try:
            copyfile(v,newname)
        except:
            continue
        v = '-'.join([v.split('/')[-3],v.split('/')[-1]])

        testSamples.append(v+'    0\n')
        '''
        if i < len(negPaths) * 0.6:
            trainSamples.append(v+'    0\n')
        else:
            testSamples.append(v+'    0\n')
        '''

    for i,v in enumerate(posPaths):
        newname = savePath+'pureJava/'+'-'.join([v.split('/')[-3],v.split('/')[-1]])
        try:
            copyfile(v,newname)
        except:
            continue
        v = '-'.join([v.split('/')[-3],v.split('/')[-1]])

        testSamples.append(v+'    1\n')

        '''
        if i < len(posPaths) * 0.6:
            trainSamples.append(v+'    1\n')
        else:
            testSamples.append(v+'    1\n')
        '''
    #乱序写入train test文件
    #random.shuffle(trainSamples)
    random.shuffle(testSamples)



    #trainLabelFile = open(trainLabelPath, 'w')
    testLabelPath = open(testLabelPath, 'w')

    #trainLabelFile.writelines(trainSamples)
    testLabelPath.writelines(testSamples)

    #trainLabelFile.close()
    testLabelPath.close()



    edgelabels={'childFather':0,'Nextsib':1,'Nexttoken':2,'Prevtoken':3,'Nextuse':4,'Prevuse':5,'If':6,'Ifelse':7,'While':8,'For':9,'Nextstmt':10,'Prevstmt':11,'Prevsib':12}
    edgelabels_new = dict(zip(edgelabels.values(),edgelabels.keys()))



    mkdir(jsonfilepath)
    #解析抽象语法树
    astparseexceptions = 0
    for root, ds, files in os.walk(typefilepath):
        for file in tqdm(files):
            codepath = root + '/' + file
            #/home/yqx/Downloads/comment_data/comment-data/DesigniteJava-master/myData/Ant/pureJava/ant-rel-1.1-com.oreilly.servlet-MailMessage.java
            #print(codepath)
            #try:
            try:
                pureAST = code2AST(codepath) #得到AST需要的数据，递归各节点遍历出一棵树 tree
            
                #except FunctionTimedOut as e:
                #    print('function timeout + msg = ', e.msg)
                #    break

                codeName = codepath.split('/')[-1][:-5]
                #print(codeName)
                version = '-'.join(codepath.split('/')[-1].split('-')[:-2])
                #print(version)
                typeMetrics = typeMetricVersionDict[version]

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
                getJsonFile(nodelist,x,vocabdict,edge_index,edge_attr,edgelabels,edgelabels_new,typeMetrics,jsonfilepath,codeName)
            except:
                astparseexceptions+=1

    print("astparseexceptions:", astparseexceptions)