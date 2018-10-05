# PyCor 0.0.7

## Python Module for Korean Language Processing
### NLCP : Natural Language Contextual Parsing
* Corpus기반 사전 학습, Dictionary 없이 한국어 형태소 분석이 가능한 자연어 파서
* 문장들을 처리하는 과정에서 Dictionary를 스스로 만드는 형태소분석기 
* 한정된 문법형태소의 결합 규칙과 문서 혹은 문서 집합 안에서의 체언, 용언의 활용형태 분석
* 문장 단위, Document단위, Document set단위로 컨텍스트 생성, 자연어 파싱
* 제약 조건 : 기본적인 한국어 맞춤법을 지키는 정규화된 한글 문서에 적합(위키, 논문, 뉴스 기사 등)
* 목적 : 체계적인 지식을 기술한 문서의 파싱과 이해


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
