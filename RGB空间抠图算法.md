## 项目简介

### 任务

针对高分辨率白底图，对白底图中物品进行精细化高分辨率分割，要求如下:

1. 输出分割 Mask 仅为物品，不包含因打光造成的物品阴影、背景灰尘、背景颜色不均等问 题。
2. 输出 Mask 分辨率与原图相同，要求物品边缘清晰干净，不能有锯齿、模糊、残缺等问题。
3. 针对完全透明商品部件(如透明镜片)或非完全透明商品部件(如墨镜镜片)，应视为商品。 
4. 商品不区分具体类别，可能为瓶子、盒子、眼镜、化妆品等各种类别商品置于白底上进行 拍摄，算法应自动区分前景商品和背景白底。



### 数据集

一组高分辨率白底图片，共计18张

<img src="http://xiangkun-img.oss-cn-shenzhen.aliyuncs.com/20210903095753.png" alt="image-20210718173711864" style="zoom: 33%;" />



### 难点

1. 保持分辨率不变，且不丢失原有信息，因此不能在原图上直接加工。
2. 物体在光线下会产生阴影，需要将其与物体本身区分开，不能抠出来阴影
3. 对完全透明物体，需要分辨出透过物体的背景和真实背景



## 算法流程

本算法首先检测图像中存在的阴影和背景，以此生成掩膜，再对掩膜进行一系列图像增强算法来过滤噪点、增强边缘，最后用掩膜覆盖到原图片上，过滤出最终物体。

### 阴影检测与掩膜生成

阴影检测是本算法最核心的部分。我们在实验中发现阴影部分的rgb值几乎都相同，而镜架部分却很少出现相同rgb的像素，因为镜架是自然成像，而阴影是自然光照在物体形成的被动成像。除此之外，白色背景也几乎都符合被动成像的规则。

经过一系列测试，我们判定r、g、b值相等或在+-1范围内浮动时为背景或阴影，并且本数据集中图片的背景和阴影的red与green的值具有高度相关性，即使blue值很大或者很小，r与g依旧相等或接近。

因此阴影检测部分代码如下：

```python
def if_same_rgb(point):
  # 判定rgb值是否相似，true表示检测到的像素为图像阴影或背景
    if point[0] < 110 and point[1] < 110 and point[2] < 110:
        return False
    elif point[0] == point[1]+1 and point[2] == point[1]+2:
        return True
    elif point[0] == point[1] == point[2]:
        return True
    elif point[1] == point[2]-1 or point[1] == point[2]+1 or point[1] == point[2]:
        return True
    return False
  
  def process_shadow(img):
    # 检测阴影，并将其和背景一起置为灰色
    mask = np.zeros_like(img)
    w = img.shape[0]
    h = img.shape[1]
    for i in tqdm(range(w), desc="Processing Shadow:"):
        for j in range(h):
            point = img[i, j, :]
            # 若该点的rgb值相同或近似相同，则判断为阴影
            if if_same_rgb(point):
                # 阴影全部置为灰色
                mask[i, j, :] = 128
    return mask
```

在该算法中我们将阴影像素值全部置为128，是因为方便下面抠图时选择阈值。

### 噪点去除

至此提取到了一个像素值为128的掩膜，但由于是逐像素判断，掩膜中存在大量白色噪点，并消去了很多原有物体信息，因此我们使用图像增强算法去除部分噪点。

实验中我们测试了高斯滤波、中值滤波、均值模糊、非局部平均去噪三种降噪方法，并尝试了不同kennel size的腐蚀膨胀操作，最终选择了kennel size=9或11的中值滤波。

![image-20210904142632043](http://xiangkun-img.oss-cn-shenzhen.aliyuncs.com/20210904142639.png)

![image-20210904143324977](http://xiangkun-img.oss-cn-shenzhen.aliyuncs.com/20210904143325.png)

上图为前后降噪效果，可以看到很多判别错误的像素点被去除。之所以只对mask图降噪是为了最大幅度减少原图损失。

### 抠出图片

首先将掩膜转化为灰度图，由于背景像素均为128，故我们选择127作为阈值，大于127的置为255，小于127的置为0。最后根据掩膜删除背景区域。

```python
def process_mask(img, mask):
    img1 = img.copy()
    # 首先获取原始图像
    img_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    ret, mask = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)  # 设置阈值，大于175的置为255，小于175的置为0
    mask_inv = cv2.bitwise_not(mask)  # 非运算，mask取反
    img_fg = cv2.bitwise_and(img1, img1, mask=mask_inv)  # 删除了背景区域
    return img_fg
```

### 修改背景

根据要求需修改背景为灰色，故再次遍历了所有像素。此步骤可省略。

```python
def process_bg(input_img):
    # 修改背景颜色为灰色
    img = input_img.copy()
    w = img.shape[0]
    h = img.shape[1]
    for i in tqdm(range(w), desc="Processing Background:"):
        for j in range(h):
            point = img[i, j, :]
            if point[0] == point[1] == point[2] == 0:
                img[i, j, :] = 128
    return img
```



## 结果

这里给出了一些实验结果（左图为原图，右图为抠出图）：

### 普通眼镜

![image-20210904231407712](http://xiangkun-img.oss-cn-shenzhen.aliyuncs.com/20210904231407.png)

![image-20210904231517621](http://xiangkun-img.oss-cn-shenzhen.aliyuncs.com/20210904231517.png)

### 墨镜

![image-20210904231714266](http://xiangkun-img.oss-cn-shenzhen.aliyuncs.com/20210904231714.png)

![image-20210904231623786](http://xiangkun-img.oss-cn-shenzhen.aliyuncs.com/20210904231623.png)

### 护目镜

![image-20210904231804345](http://xiangkun-img.oss-cn-shenzhen.aliyuncs.com/20210904231804.png)



## 对比实验

### Floodfill算法

泛洪算法图形处理中的一个填充算法，基本原理是从一个像素点出发，以此向周边的像素点扩充着色，直到图形的边界。我们在实验中从图像的四周选择出发点向内填充，以达到消除背景的效果。

![image-20210904145308230](http://xiangkun-img.oss-cn-shenzhen.aliyuncs.com/20210904145308.png)

左图为泛洪算法的填充结果，右边是本算法的结果。

可以看出泛洪算法会对接近于背景颜色的物体部位一起填充，而由于光线亮度差异，最终下方较暗的背景也没有被消去，并且该算法无法识别物体内部的阴影（镜片内），因为这些像素在物体轮廓内。

flood fill约用时15s，相对来说速度较快。



### 最优阈值法

对于空白背景的简单图片，我们可以使用opencv里自带的最优阈值法来对灰度图进行二值化处理，从而生成遮罩层。

1. OTSU阈值

   在使用全局阈值时，只能通过不停的尝试来确定一个效果比较好的阈值。如果是一副双峰图像（简单来说双峰图像是指图像直方图中存在两个峰）呢？OTSU就是对一副双峰图像自动根据其直方图计算出最合适阈值的方法。

   ```python
   def OTSU(img):
     # Otsu 二值化之前先对图像进行高斯滤波处理，平滑图像，去除噪声
     #（5,5）为高斯核大小，0为标准差
     blur = cv2.GaussianBlur(img, (5, 5), 0)
     re3, th_img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
     return th_img
   ```

   ![image-20210904222914833](http://xiangkun-img.oss-cn-shenzhen.aliyuncs.com/20210904222914.png)

   OTSU法使用最小二乘法处理像素点,在计算双峰图像时效果好，但实际上物体轮廓、物体阴影、背景形成的直方图可能具有多个峰，计算出的最优阈值可能只能分辨其中最明显的两个峰而忽略其他，导致生成的掩膜有很多镜框部分缺失，且有部分阴影无法被分割。

   

   2. TRIANGLE阈值

   OTSU基于类内最小方差实现阈值寻找, 而cv2.THRESH_TRIANGLE使用三角算法处理像素点。有时候图像的直方图只有一个波峰时使用TRIANGLE方法寻找阈值是比较好的一个选择。

   ```python
   def Triangle(img):
     # Otsu 二值化之前先对图像进行高斯滤波处理，平滑图像，去除噪声
     #（5,5）为高斯核大小，0为标准差
     blur = cv2.GaussianBlur(img, (5, 5), 0)
     re3, th_img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
     return th_img
   ```

   ![image-20210904224225642](http://xiangkun-img.oss-cn-shenzhen.aliyuncs.com/20210904224225.png)

   可以看到左图使用triangle算法后镜框细节保留的比OTSU更多了，但与此同时也有了更多的阴影未被去除。

### LAB空间淡化阴影法

Lab是由一个亮度通道（channel）和两个颜色通道组成的。在Lab颜色空间中，每个颜色用L、a、b三个数字表示，各个分量的含义是这样的： 
\- L代表亮度
\- a代表从绿色到红色的分量 
\- b代表从蓝色到黄色的分量

本方法参考了https://github.com/sbbug/Researching-Image-Shadow-Removal，该作者认为阴影部分图像的LAB三个分量可能与物体的不同，设计了一套对LAB值的选择策略。

我们改进后方法的步骤如下：

1. 首先计算LAB三个通道像素的标准差与均值
2. 在本数据集中A、B的变化不大，而L变化范围较大，我们选择一个阈值为$$thr=avg(L)-sd(L)/3$$
3. 遍历像素，若整个图像的A与B的均值小于256，说明颜色接近于黑色，此时如果亮度L也小于阈值thr，则该像素可能是阴影。
4. 若a+b的均值大于256，说明颜色接近于白色，此时若185<L<240且126<B<129则判定为较淡的阴影或者白色背景。
5. 使用上面得到的像素坐标将图像背景和阴影消去

![image-20210904215025378](http://xiangkun-img.oss-cn-shenzhen.aliyuncs.com/20210904215025.png)

左图为LAB空间阴影淡化法得出的结果，而右图是我们最终使用的RGB空间抠图法。可以看到在LAB中保留眼镜的细节较多，经过滤波处理后边缘依旧很粗糙，且有一部分阴影和背景没有被完全识别。

### Remove.bg

remove.bg是近年来非常火的背景消除ai，号称无需点击就可以在5s内消除背景，并能保留原有图片的信息。我们使用如下代码调用removebg的api：

```python
from removebg import  RemoveBg

def remove_bg(img_path, api_key)
  #输入在官网注册的api密钥
  rmbg=RemoveBg(api_key,"error.log")
  #替换成需要替换的照片
  rmbg.remove_background_from_img_file('=img_path)
```

![image-20210904224906491](http://xiangkun-img.oss-cn-shenzhen.aliyuncs.com/20210904224906.png)

实验过程非常快，大约用了5-10秒就出来了结果，眼镜轮廓划分的非常清楚，而背景也没有剩下噪点。但该ai依旧保留了一部分背景（位于物体周围的少量背景），且对于透明镜片无法分辨，透明镜片内的阴影和背景都没有被去除。相比之下我们的算法（右边）去掉的信息更多，但也造成了一些像素损失，如透明的鼻梁架和部分镜框消失了，但去阴影的效果更好。



## 缺陷

本算法虽然在大部分图片中取得了较好的抠图效果，甚至在有些图片中超过了ai算法，但依旧存在一些缺陷。

1. **计算时间过长**，removebg只需要10s，洪泛算法需要约20s，最优阈值法甚至只需要3-5秒，但由于需遍历每个像素点，本文的方法需要60s以上的计算时间；
2. **信息丢失**，在一些图片中会造成部分物体信息丢失，就像在LAB空间中一样，RGB空间也有一定的局限性，有些物体特征的像素值无法与背景区分；
3. **丢失透明物体信息**，在对护目镜（透明部分较多）抠图时会把镜片部分几乎全部抹除了，这无法达到我们的要求。
