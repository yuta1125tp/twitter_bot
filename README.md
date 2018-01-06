

# twitter_bot
source code for twitter bot  
[kawa1125bot](https://twitter.com/kawa1125bot)  

# TOC
<!-- TOC -->

- [twitter_bot](#twitter_bot)
- [TOC](#toc)
- [dependency](#dependency)
- [how to install mecab](#how-to-install-mecab)
    - [download pre-build MeCab for Windows](#download-pre-build-mecab-for-windows)
    - [install python binding via pip](#install-python-binding-via-pip)
    - [install mecab-ipadic-neologd for windows](#install-mecab-ipadic-neologd-for-windows)

<!-- /TOC -->


# dependency
this repository mainly dependent to following softwares.
- MeCab([origin](http://taku910.github.io/mecab/), [Windows binary](https://qiita.com/yukinoi/items/990b6933d9f21ba0fb43), [Windows dict](http://hired.hateblo.jp/entry/mecab-ipadic-neologd-windows))  
- natural-language-preprocessings([github](https://github.com/Hironsan/natural-language-preprocessings))  

more details are discribed in requirements.txt

# how to install mecab
## download pre-build MeCab for Windows
pre-build MeCab dll for x64 is released at following  url.  
ref: https://qiita.com/yukinoi/items/990b6933d9f21ba0fb43  
## install python binding via pip
you can install MeCab python binding via pip.  
```cmd
pip install mecab-python-windows
```
## install mecab-ipadic-neologd for windows
you can download neologd dict which is better than original dict in case of web texts.  
ref http://hired.hateblo.jp/entry/mecab-ipadic-neologd-windows

1. copy "MeCab" dir into C:/Program Files/ and replace existing MeCab files
2. edit mecabrc file in ```<MeCab Root>/etc/mecabrc```  
remove all " (x86)".  
```diff
;
; Configuration file of MeCab
;
;
dicdir =  $(rcpath)\..\dic\ipadic

-userdic = C:\Program Files (x86)\MeCab\dic\neologd\mecab-user.dic,C:\Program Files (x86)\MeCab\dic\neologd\neologd-adjective-exp.dic,C:\Program Files (x86)\MeCab\dic\neologd\neologd-adjective-std.dic,C:\Program Files (x86)\MeCab\dic\neologd\neologd-adjective-verb.dic,C:\Program Files (x86)\MeCab\dic\neologd\neologd-adverb.dic,C:\Program Files (x86)\MeCab\dic\neologd\neologd-common-noun-ortho-variant.dic,C:\Program Files (x86)\MeCab\dic\neologd\neologd-date-time-infreq.dic,C:\Program Files (x86)\MeCab\dic\neologd\neologd-ill-formed-words.dic,C:\Program Files (x86)\MeCab\dic\neologd\neologd-interjection.dic,C:\Program Files (x86)\MeCab\dic\neologd\neologd-noun-sahen-conn-ortho-variant.dic,C:\Program Files (x86)\MeCab\dic\neologd\neologd-proper-noun-ortho-variant.dic,C:\Program Files (x86)\MeCab\dic\neologd\neologd-quantity-infreq.dic
+userdic = C:\Program Files\MeCab\dic\neologd\mecab-user.dic,C:\Program Files\MeCab\dic\neologd\neologd-adjective-exp.dic,C:\Program Files\MeCab\dic\neologd\neologd-adjective-std.dic,C:\Program Files\MeCab\dic\neologd\neologd-adjective-verb.dic,C:\Program Files\MeCab\dic\neologd\neologd-adverb.dic,C:\Program Files\MeCab\dic\neologd\neologd-common-noun-ortho-variant.dic,C:\Program Files\MeCab\dic\neologd\neologd-date-time-infreq.dic,C:\Program Files\MeCab\dic\neologd\neologd-ill-formed-words.dic,C:\Program Files\MeCab\dic\neologd\neologd-interjection.dic,C:\Program Files\MeCab\dic\neologd\neologd-noun-sahen-conn-ortho-variant.dic,C:\Program Files\MeCab\dic\neologd\neologd-proper-noun-ortho-variant.dic,C:\Program Files\MeCab\dic\neologd\neologd-quantity-infreq.dic

; output-format-type = wakati
; input-buffer-size = 8192

; node-format = %m\n
; bos-format = %S\n
; eos-format = EOS\n
```
3. open cmd as administrator
4. cd into ```<MeCab Root>/dic/ipadic```
5. kick following command for make index
```cmd
"C:\Program Files\MeCab\bin\mecab-dict-index.exe" -f SHIFT-JIS -t UTF-8
```
6. unzip all .zip files at dic/neologd
```cmd
cd ..\neologd
unzip \*.zip
```
7. edit mecab-dict-compile.cmd  
    - remove " (x86)"  
    - change output binary dict encoding format from shift-jis to utf-8

```diff
@echo off

-set MECAB_HOME="C:\Program Files (x86)\MeCab"
+set MECAB_HOME="C:\Program Files\MeCab"

-%MECAB_HOME%\bin\mecab-dict-index.exe -d %MECAB_HOME%\dic\ipadic -u %2 -f shift-jis -t shift-jis %MECAB_HOME%\dic\neologd\%1
+%MECAB_HOME%\bin\mecab-dict-index.exe -d %MECAB_HOME%\dic\ipadic -u %2 -f shift-jis -t utf-8 %MECAB_HOME%\dic\neologd\%1
```

8. kick compile-all.cmd