# encoding="utf-8"
# Version: Python 3.9.0
# Date of creation: 12/23/2020
# My page : https://github.com/idontwantagirlfriend/
# Required modules: 
# copy
# jieba
# nltk.tokenize.word_tokenize
# random.randint
# os.path


from nltk.tokenize import word_tokenize as nltk_tokenize
from random import randint as rand
from copy import deepcopy
from jieba import lcut as jieba_tokenize
from os.path import realpath as path

class nameshuffler:
    """
    A name shuffler can generate from a text pool (str format) a random name of a given length.
    The default corpus is from a book about syntax, while you can load a custom corpus.
    Currently only supports Chinese and languages in latin alphabets. You may however give a few more attempts on other languages.
    """
              
    def __init__(self, corpus="README.txt",lang="alpha", sep="word",mode="plain"):
        """Good luck on finding yourself a good name!
        Parameters:
            corpus: The path of the text from which the name is generated. Attention: not the text itself. 
            lang:
                alpha: for alphabetic languages. Uses nltk for tokenization.
                zh: for Chinese language especially. Uses jieba for tokenization. Compatible with alphabetic languages like English, French, etc.
            sep:
                word: The name is shuffled out from words.
                char: The name is shuffled out from characters. The shuffling can be slow as all the characters within the given text are iterated.
            mode:
                plain: Ignore the distribution of words/characters.
                dist: Consider the distribution of words/characters. The most frequent token is the most likely to be shuffled in.
                easy: Bypass the corpus and shuffle directly from a token list. Currenly only support latin alphabetic languages. 
        """
        if mode=="easy":
            temp_lst=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        elif mode=="plain" or mode=="dist":
            temp_lst=[]
            if lang=="alpha" or lang=="zh":            
                _scrap=("'", '7', '\uf8fb', '\uf8f4', 'ϵ', ',', '⇝', '@', '⊂', '‘', '$', '（', '⟨', '!', '8', '\uf8fd', '–', '∀', '|', ')', '\uf8f3', '&', '⟩', '0', '\n', '<', '3', '！', '—', '）', '5', '6', '#', '；', '′', '\uf8fe', '≤', '’', '⇔', '‚', '"', '《', '-', '9', '(', '∨', '＼', '？', '⪰', '*', '[', '∈', '{', '∃', '+', '1', '◦', '…', '\uf8f1', '\uf8ef', '∗', '}', ' ', '„', '\uf8f0', '•', '?', ':', '>', '%', ';', '”', ']', '\uf8ee', '↑', '\uf8fa', '》', '→', '⁇', '=', '，', '\\', '−', '∅', '\uf8f9', 'd', '⊕', '4', '⇒', '∧', '。', '、', '“', '/', '\uf8fc', '⃝', '：', '.', '2', '↔', '↓', '\uf8f2')
            else:
                raise ValueError("Invalid language parameter. Must be between \"zh\" and \"latin\"")
            #标点符号列表，你不会考虑带有标点符号的名字吧？

            with open(path(corpus), encoding="utf-8") as text:
                for line in text:
                    if lang=="alpha":
                        temp_lst.extend(nltk_tokenize(line))
                    elif lang=="zh":
                        if sep=="word":
                            temp_lst.extend(jieba_tokenize(line))
                        elif sep=="char":
                            temp_lst.extend(line)
                        else:
                            raise ValueError("Invalid sep parameter. Must be \"word\" or \"char\".")
                    
            if mode=="plain":
                temp_pool=set(temp_lst)
                temp_lst=deepcopy(list(temp_pool))
            else: #mode=="dist"
                temp_pool=deepcopy(temp_lst)
            #如果对temp_pool（一个set）的遍历正在进行，但set的长度改变，这个遍历会无法继续：
            #RuntimeError: Set changed size during iteration
            #所以设定了temp_pool提供遍历来源，masked作为工事对象，在masked被改变时，不会影响temp_pool
            #的长度，遍历可以继续。
            #对于mode=distribution的情况，masked层去除后遍历仍然可以正常进行。可以优化，也可以保留。
            
            for i in temp_pool:
                if isinstance(i,str):
                    if i.startswith("_"):
                        temp_lst.remove(i)
                    else:
                        for j in _scrap:
                            if j in i:
                                temp_lst.remove(i)
                                break
            #当temp_pool中的词汇i因为包含_scrap中的字符已经被移除，而对_scrap的穷举“for j in _scrap”仍然没有
            #结束时，如果i在之后对_scrap的遍历中再次被判定为要移除，则会发出temp_pool.remove(i)，对
            #temp_pool移除一个本来就不存在于其中的元素，所以报错：
            #    KeyError: [i]
            #这里通过remove后立刻break中断遍历，解决了这个问题。当然也可以：
            #Optiion 1: 通过在内部for加入
            #    if i in temp_pool:
            #        <remove operation>
            #    else:
            #        break
            #Option 2: 在内部for加入
            #    if j in i:
            #         try: temp_pool.remove(i)
            #         except KeyError:
            #             pass
            #temp_lst, temp_pool : 刚分好词的pool
            #temp_lst : list
            #temp_pool : set or list
            
            if lang=="alpha":
                if sep=="word":
                    pass
                elif sep=="char":
                    temp_pool=set()
                    if mode=="plain":
                        for i in temp_lst:
                            g=set(i)
                            temp_pool=temp_pool.union(g)
                    else:
                        temp_pool=list(temp_pool)
                        for i in temp_lst:
                            temp_pool.extend(i)
                    temp_lst=list(temp_pool)
        else:
            raise ValueError("Invalid mode parameter. Must be \"plain\", \"distribution\" or \"easy\".")
        
        self.corpus=corpus
        self.pool=temp_lst
        self.lang=lang
        self.mode=mode
        self.sep=sep
        #成为class内部的全局变量，这样就可以在接下来继续使用参数

    def __getitem__(self,num):
        return self.pool.__getitem__(num)

    def shuffle_parsed(self,lengt):
        """Returns the name as a list of lemma."""
        #从已经建立的pool中抽取元素。允许重复。
        size=len(self.pool)
        counter1=0
        shufflename=[]
        
        while counter1<lengt:
            key=self.pool[rand(0,size-1)]
            if self.mode=="easy":
                pass
            else:
                if isinstance(key,str):
                    if self.lang=="alpha" and self.sep=="word":
                        key=key.lower()
                        key=key.capitalize()
                    else:
                        pass
            shufflename.append(key)
            counter1+=1

        return shufflename

    def shuffle(self, leng):
        """From the corpus, shuffles out a name at given length.
        Returns the name as a string."""    
        shuffle_parsed=self.shuffle_parsed(lengt=leng)
        if self.mode=="easy":
            pass
        else: 
            if self.lang=="alpha" and self.sep=="word":
                    return " ".join(shuffle_parsed)
        return "".join(shuffle_parsed)

    def __call__(self,lengt=2):
        """Shuffles out a name at given length, actually the same function as the shuffle method."""
        return self.shuffle(leng=lengt)

    def special(self, a, lengt):
        """Keeps shuffling until the given pattern is present in the final name.
        Returns the name as a string."""
        #根据特定的字符，定制名字。
        #直到名字被产生之前，shuffle将会一直进行下去。
        b=self.shuffle(leng=lengt)
        while (a in b)==False:
            b=self.shuffle(leng=lengt)
        return b

    def client(self):
        """Starts a user interface. Return NoneType."""
        print("Hello! How long do you want the generated name to be?", end=" ")
        self.speak()
        print("See you next time! ")

    def speak(self):
        """\"Speak\" function itself. """ 
        lengt=input("Enter an integer as length.\n")
        if lengt=="quit":
            pass
        else:      
            if isinstance(lengt,int):
                print("The name I have chosen for you is: \n\"\n    {}\n\".".format(self.shuffle(lengt)))
            else:
                try: lengt=int(lengt)
                except ValueError:
                    print("Invalid input parameter. Integer only, please! ")
                    return self.speak()
                print("The name I have chosen for you is: \n\"\n    {}\n\".".format(self.shuffle(lengt)))
            print("If you want to try again...",end=" ")
            return self.speak()
