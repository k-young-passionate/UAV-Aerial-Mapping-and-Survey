# SIFT(Scale-Invariant Feature Transform)알고리즘

- `Harris코너 검출`과 `Shi-Tomasi코너 검출` 방법 : 이미지가 회전 하더라도 코너를 제대로 검출할 수 있지만 이미지의 크기가 커지면 코너를 제대로 검출하지 못하는 단점을 가지고 있다.

- 이미지 크기에 상관없이 이미지의 특징을 규정할 수 있다.
- 이미지에서 스케일 불변인 키포인트를 추출하고 추출한 `키포인트`들의 `descriptor`을 계산한다.

## Scale-space Extream Detection(스케일-공간 극값 검출)
- 가우시안 필터 후 라플라시안(Laplacian of Gaussian: LoG) 필터를 적용(가우시안 함수를 각 축으로 편미분)하면 이미지에서 다양한 크기의 방울 모양의 이미지를 검출
- LoG는 다소 시간이 소요되기 때문에 SIFT 알고르즘에서는 하나의 이미지에서 서로 다른 필터를 적용한 가우시안 피라미드 이미지의 차(Difference of Gaussian:DoG)를 이용
- DoG를 찾으면 이미지에서 스케일-공간 좌표상 극값을 찾는다. 만약 극값이 있으면 이를 잠재적 키포인트(Potential Keypoint)라고 한다.
## Keypoint localization (키포인트 지역화)
- 이미지에서 잠재적 키포인트들의 위치를 모두 찾았으면 보다 정확한 결과를 위해 잠재적 키포인트들의 정제과정을 거쳐 키포인트들을 추출
정제과정은 테일러 전개를 이용하여 수행
## Orientation assignment(방향 할당하기)
- 최종적으로 추출된 키포인트들에 방향성-불변이 되도록 방향을 할당한다.
- 이미지가 확대되거나 회전되더라도 추출된 키포인트들은 이미지의 특징을 고스란히 보존한다
## Keypoint descriptor(키포인트 디스크립터 계산하기)
- 키포인트를 이용하여 키포인트 디스크립터를 계산한다.
- 키포인트 디스크립터는 이미지 히스토그램을 활용하여 표한한다.
- 이에 조명의 변화나 회전등에도 키포인트들이 특징을 보존하기 위한 몇가지 측정값을 추가
## Keypoint matching(키포인트 매칭)
- 두 개의 이미지에서 키포인트들을 매칭하여 동일한 이미지 추출이나 이미지 검색 등에 활용

## SIFT를 위해 OpenCV에서 제공하는 함수는 다음과 같은것들이 있다.

### cv2.xfeatures2d.SIFT_create() : SIFT의 키포인트, 디스크립터들을 계산하는 함수 제공
- Detect(graying) : grayimg에서 키포인트를 검출하여 리턴
- Compute(keypoints) : keypoints에서 디스크립터를 계산한 후 키포인트와 디스크립터를 리턴
- detectAndCompute(graying) : grayimg에서 키포인트와 디스크립터를 한번에 계산하고 리턴
### cv2.drawKeypoints(graying, keypoints, outimg) : grayimg에 키포인트들을 outimg에 표시


# FLANN 기반 이미지 특성 매칭
- `FLANN(Fast Library for Approximate Nearest Neighbors)` : 큰 이미지에서 특성들을 매칭할 때 성능을 위해 최적화된 라이브러리 모음

```
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
```
- FLANN기반 매칭을 위해 두 개의 사전 자료형의 인자가 필요.(indexParams, searchParams)
- SIFT와 SURF를 활용하는 경우 indexParams는 위처럼 생성하면 된다.
- searchParams는 특성 매칭을 위한 반복 회수
- checks 값이 커지만 보다 정확한 결과값이 나오지만 속도는 느려진다.

```
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1,des2,k=2)
```

- FLANN 기반 매칭 객체를 앞에서 구성한 사전 자료 형태의 인자를 이용해 생성
- 그리고 `KNN(K-Nearest Neighbors)매칭` 수행
- KNN 매칭은 k=2로 설정된 순위만큼 리턴하므로 2번째로 가까운 매칭 결과까지 리턴
- KNN 매칭을 하는 이유는 리턴한 결과를 사용자가 선택하여 다룰 수 있기 때문이다.
- k=2라고 설정하였으므로 matches는 1순위 매칭결과와 2순위 매칭결과가 멤버인 리스트가 된다.

```
good = []
for m,n in matches:
	if m.distance < 0.7*n.distance:
		good.append(m)
```
- matches의 각 멤버에서 1순위 매칭 결과가 2순위 매칭 결과의 factor로 주어진 비율보다 더 가까운 값만을 취한다. 
- factor의 값은 0.7이므로 1순위 매칭 결과가 2순위 매칭 결과의 0.7배보다 더 가까운 값만을 취한다.