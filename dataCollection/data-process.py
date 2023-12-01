import os
from astTools import *
import json
from tqdm import tqdm
from func_timeout import func_set_timeout, FunctionTimedOut


edgelabels={'childFather':0,'Nextsib':1,'Nexttoken':2,'Prevtoken':3,'Nextuse':4,'Prevuse':5,'If':6,'Ifelse':7,'While':8,'For':9,'Nextstmt':10,'Prevstmt':11,'Prevsib':12}
edgelabels_new = dict(zip(edgelabels.values(),edgelabels.keys()))
#代码数据预处理

projectname = 'ant-rel-1.10.12'
projectname = 'dubbo-dubbo-3.0.6'
projectname = 'hadoop-release-3.3.2-RC5'
projectname = 'jfreechart-1.5.3'
projectname = 'jmeter-rel-v5.4.3'
projectname = 'jruby-9.3.3.0'
projectname = 'kafka-3.1.0'
projectname = 'mockito-4.4.0'
projectname = 'neo4j-4.4.4'
projectname = 'tomcat-10.0.18'

typeMetricsfile = "/home/yqx/Desktop/TD-data-process/rawDate/"+projectname+"/typeMetrics.csv"
codeSmellsfile = "/home/yqx/Desktop/TD-data-process/rawDate/"+projectname+"/designCodeSmells.csv"
typefilepath = "/home/yqx/Desktop/TD-data-process/rawDate/"+projectname+"/pureJava"
jsonfilepath = os.path.join('outData',projectname,'rawjson') 
if not os.path.exists(jsonfilepath):
    os.makedirs(jsonfilepath)
typelabelpath = os.path.join('outData',projectname) 
typelabelfile = typelabelpath + '/' + 'typelabels.txt'

corpusfile = typelabelpath + '/' + 'corpus.txt'


#得到所有designSmell的type，并保存在dict中，便于逐条查找，确认label
codesmelldict = getCodeSmellDict(codeSmellsfile)




#codepath = "/home/yqx/Desktop/TD-data-process/testData/ant-rel-1.10.12/pureJava/oata-HelloWorld.java"
astparseexceptions = 0

for root, ds, files in os.walk(typefilepath):
    for file in tqdm(files):
        codepath = root + '/' + file
        
        try:
            try:
                pureAST = code2AST(codepath) #得到AST需要的数据，递归各节点遍历出一棵树 tree
            except:
                astparseexceptions+=1
        except FunctionTimedOut as e:
            print('function timeout + msg = ', e.msg)
            break

        codeName = '__'.join([codepath.split('/')[-3],codepath.split('/')[-1].split('-')[0],codepath.split('/')[-1].split('-')[1].split('.')[0]])
        typeMetrics = getTypeMetricxDict(typeMetricsfile)

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

        #添加一条到label文件
        addItem2labelfile(typelabelfile, codeName, codesmelldict)

        #添加一行到corpus.txt
        with open(corpusfile, 'a') as corpus:
            
            newline = ' '.join(list(map(str, nodelist)))+'\n'
            corpus.write(newline.encode('UTF-8', 'ignore').decode('UTF-8'))


        
print("astparseexceptions:", astparseexceptions)

       









