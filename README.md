# 项目环境安装

项目环境的依赖包在 ``` requirement.txt``` 中，在项目所在目录中运行 ``` pip install -r requirement.txt``` 即可安装依赖

# 项目说明

## ./collection.txt 说明

本项目根据用户提供的 ``` ./collection.txt``` 生成指定的单词本，其中 ``` ./collection.txt``` 的格式要求如下：

```latex
word_1, word_2, word_3, ... , word_n

word_1, word_2, ... , word_m

word_1, word_2, ... , word_k
...
```

即每行有若干个单词（可以只有一个单词），单词间以 ```', '``` 隔开，每行的单词称为一个词组，词组间以一个空行隔开。

## 单词本说明

生成的单词本保存在 ``` ./wordbooks/``` 中，名称为 ``` untranslated_wordbook_{index}``` 和 ``` translated_wordbook_{index}``` ，单词本格式分别为：

``` untranslated_wordbook_{index}:```

```
Word Group 1:
word_1
word_2
...
word_n
Word Group 2:
word_1
word_2
...
word_m
Word Group 3:
...
```

``` translated_wordbook_{index}:```

```
Word Group 1:
word_1: word_1_translated or Fail to translate.
word_2: word_2_translated or Fail to translate.
...
word_n: word_n_translated or Fail to translate.
Word Group 2:
word_1: word_1_translated or Fail to translate.
word_2: word_2_translated or Fail to translate.
...
word_m: word_m_translated or Fail to translate.
Word Group 3:
...
```

新生成的单词本不会覆盖已有的单词本

## 使用说明

在项目所在目录下运行

```
python selector.py [-n/--num <integer>] [-r/--random] [-s/--start <integer>] [-l/--length <integer>] [-t/--toal <integer>]
```

来生成单词本，其中各参数意义如下：

```
-n/-num <integer> 生成的单词本中的词组数量，默认为 40
-r/--random 单词本中的词组是否随机打乱，输入 -r 表示随机打乱
-s/--start <integer> 选取的词组在 ./collection 中的起始位置，默认为 0
-l/--length <integer> 选取的词组在 ./collection 中的范围，默认为 1
-t/--total <integer> 单次生成的单词本数，默认为 1
```

注：

在 ``` selector.py``` 中，需要修改 ``` generate_wordbook``` 函数中 的

```
translator = Translate(proxies = {'https': 'socks5://localhost:4781'})
```

语句内，``` localhost:``` 后的端口改为用户所使用的代理的 ```socks``` 端口。