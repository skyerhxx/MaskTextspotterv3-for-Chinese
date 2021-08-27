# MaskTextspotterv3-for-chinese
MaskTextspotterv3应用于中文数据集



原作者github: https://github.com/MhLiao/MaskTextSpotterV3



### 1. 配置环境

cuda runtime 10.0

**安装anaconda环境(步骤与MaskTextspotterv3原版本相同)**

```shell
  conda create --name masktextspotter -y python=3.7
  conda activate masktextspotter

  # this installs the right pip and dependencies for the fresh python
  conda install ipython pip

  # python dependencies
  pip install ninja yacs cython matplotlib tqdm opencv-python shapely scipy tensorboardX pyclipper Polygon3 editdistance rapidfuzz

  # install PyTorch
  conda install pytorch torchvision cudatoolkit=10.0 -c pytorch

  export INSTALL_DIR=$PWD

  # install pycocotools
  cd $INSTALL_DIR
  git clone https://github.com/cocodataset/cocoapi.git
  cd cocoapi/PythonAPI
  python setup.py build_ext install

  # install apex
  cd $INSTALL_DIR
  git clone https://github.com/NVIDIA/apex.git
  cd apex
  python setup.py install --cuda_ext --cpp_ext

  # clone repo
  cd $INSTALL_DIR
  git clone https://github.com/skyerhxx/MaskTextspotterv3-for-chinese.git
  cd MaskTextspotterv3_for_chinese

  # build
  python setup.py build develop


  unset INSTALL_DIR
```

若运行中因为库的版本报错可参考pip_list.txt中相关库版本



### 2. train

```shell
bash train.sh
```

训练数据集: datasets/chinese/train_images, train_gts

训练结果：生成的train_output目录



### 3. test

```shell
bash test.sh
```

* 测试数据集: datasets/chinese/test_images

* 测试结果: 生成的test_output/inference/chinese_test目录

  * test_output目录说明: 目录中包含*results, *seg_results, *seg_visu, *visu 四个目录和一些pth文件(可忽略)

  ​           *results: 测试结果

  ​		   *seg_results: 分割结果

  ​		   *seg_visu: 分割可视化图

  ​           *visu: 测试结果可视化图



* 将测试结果和测试结果可视化图结合

```jieguo 
python visualize_result.py
```

结果见新生成的test_output_visu目录

<img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20210812154817362.png" alt="image-20210812154817362" style="zoom:50%;" />

<img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20210812154844626.png" alt="image-20210812154844626" style="zoom:50%;" />



### 4. evaluation

```shell
python evaluate.py
```

<img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20210812154155667.png" alt="image-20210812154155667" style="zoom:67%;" />







## 5. 改动步骤

**①在datasets目录下创建chinese数据集目录，类型格式参照ic13/15**

* train_gts
* train_images
* test_images

​		gt格式: 13, 338, 258, 320, 264, 408, 19, 426,耻辱不亚于,19, 388, 68, 387, 68, 422, 19, 425,耻,70, 336, 121, 335, 121, 379, 70, 381,辱,123, 330, 167, 328, 168, 363, 123, 364,不,170, 338, 215, 337, 216, 369, 170, 370,亚,222, 371, 262, 369, 262, 409, 222, 410,于

**②修改configs目录下的yaml文件**

* ROI_MASK_HEAD下的PREDICTOR修改为“SeqMaskRCNNC4Predictor”
* ROI_MASK_HEAD下的CHAR_NUM_CLASSES修改为加入汉字后的字典元素总个数(我的是3625)
* DATASETS中加入chinese_train
* SOLVER中的BASE_LR设为0.002
* SEQUENCE中的NUM_CHAR修改为加入汉字后的字典元素总个数(我的是3625)

**③修改maskrcnn_benchmark/config/paths_catalog.py**

* 在class DatasetCatalog 中的DATASETS中仿照ic13加入chinese dataset的目录设置         

     <img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20210701103929119.png" alt="image-20210701103929119" style="zoom:50%;" />

  

* 在下面的get函数中仿照ic13加入

  <img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20210701104047129.png" alt="image-20210701104047129" style="zoom:50%;" />



**④修改maskrcnn_benchmark/data/datasets**

* 参考icdar.py建立chinese.py

**⑤改动MaskTextSpotterV3/maskrcnn_benchmark/utils/chars.py**

* 修改num2char, char2num



## 6. 相关说明

* 因为训练集和测试集是自己制作的，现在还没有条件公开，只能提供少量例子作为参考

* 训练使用10w数据集，最好的acc能达到0.526，再训就要过拟合了。初步分析原因是当feature在送入识别网络之前，会先经过ROI Align，转化为[b,256,32,32]固定大小的feature map, 这样就会导致在大文本，长文本，竖直文本的情况下，势必会将原有汉字的方块形状扭曲。

  

