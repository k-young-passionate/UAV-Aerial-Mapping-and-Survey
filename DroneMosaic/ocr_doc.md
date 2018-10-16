# ocr python code comparison
## extract text from image

### ocr.py
- result : string 
```
text 40'25'32“ 2
86°54‘3 5" M

S§_eK
```
> 결과값이 잘 나오는데 이제 이 string에서 위도 경도를 어떻게 뽑아내는냐가 관건. 다른 필요없는 값들도 많이 나온다.

### ocr1.py
- result : string
```
Enter the file path : 1.jpeg
Do you want to pre-process the image ?
Threshold : 1
Grey : 2
None : 0
Enter your choice : 1

Do you want to pre-process the image ?
Threshold : 1
Grey : 2
None : 0
Enter your choice : 2

Do you want to pre-process the image ?
Threshold : 1
Grey : 2
None : 0
Enter your choice : 0

```
> 아예 결과를 못 뽑아냄

### ocr2.py
- result : pic, string
```
> python ocr2.py -i 1.jpeg


```
> 그레이 스케일된 이미지는 뽑지만 텍스트 추출이 불가.
## ocr3.py
- result : string
```


40'25'32" 2
86°54‘35" M

SEEK

```
> 제일 정확하게 값을 뽑는 것 같다. 이것도 ocr.py와 마찬가지로 위도 경도 뽑는 것이 문제일 듯
## ocr4.py
- result : 5 image, string
```

```
> 각 다른 필터를 씌운 5개의 이미지를 저장하는데 어떤 이미지로 값을 뽑느냐에 따라 결과값이 다른 것 같다. 잘 다듬으면 제일 정확하게 뽑힐 것 같기도 하다.