# PyCor 0.0.4

## Python Module for Korean Language Processing

* 사전(Dictionary)을 미리 등록하지 않고 사용할 수 있는 형태소분석기
* 문장들을 처리하는 과정에서 Dictionary를 스스로 만드는 형태소분석기 
* WordCount를 이용한 키워드 추출 

### Install
```
> pip install pycor
```

### Usage
```
> python3
import pycor

pycor.train('training-text-dir')
pycor.savemodel('model-dir')

# 체언 혹은 용언의 어근들을 추출하여 2차원 배열로 제공
word2dArray = pycor.trim(text) 
pycor.trimfile('text-file-path') 

# 키워드 추출
keywordArray = pycor.abstract(text) 

```
