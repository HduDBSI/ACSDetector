# ACSDetector
-----
A dual-stream model for detecting and identifying actionable code smells.
-----
-----About the datasets we collect-----

The DataSet folder contains actionable code smell datasets that we collected from 10 open source projects, of which 6 projects were used in RQ1~3 and 4 projects were used in RQ4.

-----All source code for our approach and the baselines-----

The Experiments folder contains all source code for our approach and the baselines. We place the relevant code for each RQ in a separate subfolder. The execution of all approaches is similar.
1. We provide our experimental environment file "py36.yaml", open the Terminal, and execute the command line to quickly copy our experimental environment: "conda env create -f py36.yaml". Execute "conda activate py36" to activate the environment.
2. Download and unzip the zip file of the dataset and code.
3. Change the code path to your own correct path, and then you can freely run the code of all approaches.
For example: 1) Execute "python train.py" in the astnn_xx folder to run the astnn. 2) Execute "python main.py" in the myNewModel_xx folder to run multiple models (i.e., our dual-stream model, BiLSTM and DNN) in sequence. 3) Execute "python RandomForestClassification.py" in the randomForest_xx folder to run RF.

-----Collect your own datasets based on DesigniteJava-----

If you want to collect your own dataset from scratch based on DesigniteJava, the code in the dataCollection folder will help you.
1. You need to modify the path part in "DesigniteJava-master" to the path where you want to save the java snippets, and then compile it to get "DesigniteJava.jar".
2. Download a series of historical versions of the target project and execute "projectBatchLabel.py" to output the results of using DesigniteJava to detect code smells in each version, as well as code snippets and code metrics.
3. Execute "collectXXXDatasets_XXX.py" to collect actionable code smell data sets.
Tips: All paths need to be modified to your own correct paths.
