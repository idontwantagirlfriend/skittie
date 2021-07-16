# coding="utf-8"
# Required modules:
# jieba
# wordcloud
# os.path.realpath

from os.path import realpath as path

def wcgen(text, location, stpwd={"的","有","和","了","与","为","在","上","等","而","以","如","之","只",\
                                 "是","都","即","后","中","同","从","及","也","对","到"}, w=2160, h=1440, mode="zh", font="Deng.ttf"):
    '''Generate word cloud from a given string to a designated location. Default with Chinese text. \nRequires jieba and wordcloud to be installed first.'''
    font=path(font)
    if mode=="zh":
        from jieba import cut
        t2_seg=" ".join(cut(text)) #segmentation of raw text
        import wordcloud
        w2=wordcloud.WordCloud(font_path=font, width=w, \
                               height=h, margin=5, max_words=100, min_font_size=12,\
                              stopwords=stpwd,\
                             random_state=255, background_color='#FFFFFF', max_font_size=200, \
                             font_step=20, mode='RGB', relative_scaling='auto', regexp=None, \
                             collocations=False, colormap=None, normalize_plurals=True, \
                             contour_width=1, contour_color='black', repeat=False, \
                             include_numbers=False, min_word_length=0, collocation_threshold=30)

    elif mode=="en":
        import wordcloud
        w2=wordcloud.WordCloud(font_path=font, width=w, \
                               height=h, margin=5, max_words=500, min_font_size=12,\
                              stopwords=None,\
                             random_state=255, background_color='#FFFFFF', max_font_size=200, \
                             font_step=1, mode='RGB', relative_scaling='auto', regexp=None, \
                             collocations=False, colormap=None, normalize_plurals=True, \
                             contour_width=1, contour_color='black', repeat=False, \
                             include_numbers=False, min_word_length=0, collocation_threshold=30)

    w2.generate(t2_seg)

    #convert escape characters to raw strings, from https://blog.csdn.net/wangchao701123/article/details/56281006
    #without this step, the "invalid argument" error might be prompted when the parameter "location" is called 
    escape_dict={'\a':r'\a',
                            '\b':r'\b',
                            '\c':r'\c',
                            '\f':r'\f',
                            '\n':r'\n',
                            '\r':r'\r',
                            '\t':r'\t',
                            '\v':r'\v',
                            '\'':r'\'',
                            '\"':r'\"',
                            '\0':r'\0',
                            '\1':r'\1',
                            '\2':r'\2',
                            '\3':r'\3',
                            '\4':r'\4',
                            '\5':r'\5',
                            '\6':r'\6',
                            '\7':r'\7',
                            '\8':r'\8',
                            '\9':r'\9'}

    def raw(text):  
        new_string=""
        for char in text:
            try:
               new_string+=escape_dict[char]
            except KeyError:
               new_string+=char
        return new_string

    w2.to_file(raw(location)) #generate and export word cloud
