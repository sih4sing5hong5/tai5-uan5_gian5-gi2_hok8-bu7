from os.path import join
from sys import stderr

from django.core.management.base import BaseCommand


from 臺灣言語服務.HTS模型訓練 import HTS模型訓練
from 臺灣言語服務.資料模型路徑 import 資料路徑


class Command(BaseCommand):
    help = '訓練一个語言的HTS模型'

    def add_arguments(self, parser):
        parser.add_argument(
            '語言',
            type=str,
            help='愛訓練的語言'
        )
        parser.add_argument(
            '語者',
            type=str,
            help='發音人'
        )

    def handle(self, *args, **參數):
        try:
            語言 = 參數['語言']
            語者 = 參數['語者']
            語料資料夾 = join(資料路徑, 語言, '{}-HTS語料'.format(語者))
            模型資料夾 = join(資料路徑, 語言, '{}-HTS模型'.format(語者))
            HTS模型訓練.輸出一種語言語料(語料資料夾, 語言, 語者)
            對齊聲韻結果資料夾=HTS模型訓練.對齊聲韻(語料資料夾, 模型資料夾)
            HTS模型訓練.輸出HTS標仔(語料資料夾,對齊聲韻結果資料夾, 模型資料夾)
        except FileNotFoundError:
            raise
            print('資料庫無「{}」的語料！！'.format(參數['語言']), file=stderr)
