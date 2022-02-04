from onmt.translate.translator import build_translator
import onmt.opts as opts
from onmt.utils.parse import ArgumentParser
import MeCab
from telegram_bot import TelegramBot
import re


class GenerativeSystem:
    def __init__(self):
        # おまじない
        parser = ArgumentParser()
        opts.config_opts(parser)
        opts.translate_opts(parser)
        self.opt = parser.parse_args()
        ArgumentParser.validate_translate_opts(self.opt)
        self.translator = build_translator(self.opt, report_score=True)

        # 単語分割用にMeCabを使用
        self.mecab = MeCab.Tagger("-Owakati")
        self.mecab.parse("")

    def initial_message(self, input):
        return {'utt': 'おいでやす。どないしたん？', 'end': False}

    def reply(self, input):
        # 単語を分割
        src = [self.mecab.parse(input["utt"])[0:-2]]
        # OpenNMTで応答を生成
        scores, predictions = self.translator.translate(
            src=src,
            tgt=None,
            src_dir=self.opt.src_dir,
            batch_size=self.opt.batch_size,
            attn_debug=False
        )
        # OpenNMTの出力も単語に分割されているので，半角スペースを削除
        utt = predictions[0][0].replace(" ", "")
        #utt = re.sub("それな","せやな",utt)
        #utt = re.sub("です。","やで。",utt)
        #utt = re.sub("です！","やで！",utt)
        #utt = re.sub("だよ。","やで。",utt)
        #utt = re.sub("だよ！","やで！",utt)
        #utt = re.sub("だね。","やね。",utt)
        #utt = re.sub("ですか。","やろか。",utt)
        #utt = re.sub("かも。","やろなあ。",utt)
        #utt = re.sub("だった。","やった。",utt)
        #utt = re.sub("じゃん。","やん。",utt)
        #utt = re.sub("見えない。","見えへん。",utt)
        #utt = re.sub("出ない。","でーへん。",utt)
        #utt = re.sub("分からない。","分からへん。",utt)
        #utt = re.sub("見ない。","みーひん。",utt)
        #utt = re.sub("着ない。","きーへん。",utt)
        #utt = re.sub("しないで。","せんとって。",utt)
        #utt = re.sub("お母さん","おかん",utt)
        #utt = re.sub("お父さん","おとん",utt)
        #utt = re.sub("本当","ほんま",utt)
        #utt = re.sub("変わった","けったい",utt)
        #utt = re.sub("だめ","あかん",utt)
        #utt = re.sub("ありがとう。","おおきに。",utt)
        #utt = re.sub("とても","ばり",utt)
        #utt = re.sub("あなた","自分",utt)
        #utt = re.sub("私は","うちは",utt)
        #utt = re.sub("私の","うちの",utt)
        #utt = re.sub("私を","うちを",utt)
        #utt = re.sub("私に","うちに",utt)
        #utt = re.sub("私が","うちが",utt)
        #utt = re.sub("私へ","うちへ",utt)
        #utt = re.sub("私と","うちと",utt)
        #utt = re.sub("ですね","やね",utt)
        #utt = re.sub("いいよ。","かまへん。",utt)
        #utt = re.sub("いいよ","かまへん",utt)
        #utt = re.sub("どういたしまして","かまへんよ",utt)
        #utt = re.sub("わかる","せやな",utt)
        #utt = re.sub("仕方ない","しゃーない",utt)
        #utt = re.sub("いいな","ええな",utt)
        #utt = re.sub("そうなんですよね","そうやな",utt)
        #utt = re.sub("面白い","おもろい",utt)
        #utt = re.sub("違う","ちゃう",utt)
        #utt = re.sub("早く","はよ",utt)
        #utt = re.sub("いくら","なんぼ",utt)
        #utt = re.sub("どのくらい","なんぼ",utt)
        #utt = re.sub("とても","めっちゃ",utt)
        #utt = re.sub("すごく","めっちゃ",utt)
        print(utt)
        return {'utt': utt, "end": False}


if __name__ == '__main__':
    system = GenerativeSystem()
    bot = TelegramBot(system)
    bot.run()
    
