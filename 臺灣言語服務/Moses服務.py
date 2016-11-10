# -*- coding: utf-8 -*-
from Pyro4 import expose


from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.斷詞.拄好長度辭典揣詞 import 拄好長度辭典揣詞
from 臺灣言語工具.斷詞.語言模型揀集內組 import 語言模型揀集內組
from 臺灣言語服務.Moses載入 import Moses載入


class Moses服務:

    def __init__(self, 全部翻譯母語模型={}):
        if len(全部翻譯母語模型) == 0:
            self.全部翻譯母語模型 = Moses載入.摩西模型()
        else:
            self.全部翻譯母語模型 = 全部翻譯母語模型

    @expose
    def 支援腔口(self):
        return sorted(self.全部翻譯母語模型.keys())

    @expose
    def 正規化翻譯實作(self, 查詢腔口, 查詢語句):
        母語模型 = self.全部翻譯母語模型[查詢腔口]
        整理後語句 = 文章粗胚.數字英文中央全加分字符號(
            文章粗胚.建立物件語句前處理減號(母語模型['解析拼音'], 查詢語句)
        )

        母語章物件 = (
            拆文分析器.建立章物件(整理後語句)
            .轉音(母語模型['解析拼音'])
            .揣詞(拄好長度辭典揣詞, 母語模型['辭典'])
            .揀(語言模型揀集內組, 母語模型['語言模型'])
            .翻譯(母語模型['摩西用戶端'])
        )
        翻譯結果 = {
            '分詞': 母語章物件.看分詞(),
            '翻譯正規化結果': 母語章物件.看分詞(),
        }
        try:
            翻譯結果['綜合標音'] = 母語章物件.綜合標音(母語模型['字綜合標音'])
        except:
            pass
        return 翻譯結果

    @expose
    def 標漢字音標實作(self, 查詢腔口, 查詢語句):
        母語模型 = self.全部翻譯母語模型[查詢腔口]
        整理後語句 = 文章粗胚.數字英文中央全加分字符號(
            文章粗胚.建立物件語句前處理減號(母語模型['解析拼音'], 查詢語句)
        )
        母語章物件 = (
            拆文分析器.建立章物件(整理後語句)
            .轉音(母語模型['解析拼音'])
            .揣詞(拄好長度辭典揣詞, 母語模型['辭典'])
            .揀(語言模型揀集內組, 母語模型['語言模型'])
        )
        翻譯結果 = {
            '分詞': 母語章物件.看分詞(),
            '翻譯正規化結果': 母語章物件.看分詞(),
        }
        try:
            翻譯結果['綜合標音'] = 母語章物件.綜合標音(母語模型['字綜合標音'])
        except:
            pass
        return 翻譯結果

    def 停(self):
        for 翻譯母語模型 in self.全部翻譯母語模型.values():
            翻譯母語模型['摩西服務'].停()
