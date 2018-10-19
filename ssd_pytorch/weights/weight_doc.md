## Training SSD

```
mkdir weights
cd weights
wget https://s3.amazonaws.com/amdegroot-models/vgg16_reducedfc.pth
```

## pre-trained SSD network for detection
- SSD300 trained on VOC0712 (newest PyTorch weights)
```
wget https://s3.amazonaws.com/amdegroot-models/ssd300_mAP_77.43_v2.pth
```
- SSD300 trained on VOC0712 (original Caffe weights)
```
wget https://s3.amazonaws.com/amdegroot-models/ssd_300_VOC0712.pth
```
