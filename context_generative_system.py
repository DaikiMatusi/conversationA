from onmt.translate.translator import build_translator
import onmt.opts as opts
from onmt.utils.parse import ArgumentParser
import MeCab
import re
from telegram_bot import TelegramBot


class ContextGenerativeSystem:
    def __init__(self):
        # コマンドラインで指定したオプションをもとにモデルを読み込む
        parser = ArgumentParser()
        opts.config_opts(parser)
        opts.translate_opts(parser)
        self.opt = parser.parse_args()
        ArgumentParser.validate_translate_opts(self.opt)
        self.translator = build_translator(self.opt, report_score=True)
        
        # 分かち書きのためにMeCabを使用
        self.mecab = MeCab.Tagger("-Owakati")
        self.mecab.parse("")
        
        # 前回の応答を保存しておく辞書
        self.prev_uttr_dict = {}


    def initial_message(self, input):
        message = 'おいでやす。どないしたん？'
        self.prev_uttr_dict[input["sessionId"]] = message
        return {'utt': message, 'end':False}
        

    def reply(self, input):
        # 前回の応答と入力文をSEPを挟んで連結する
        context = self.prev_uttr_dict[input["sessionId"]] + " SEP " + input['utt']
        # 分かち書きにする
        src = [self.mecab.parse(context)[0:-2]]
        # ニューラルネットワークに分かち書きされた文脈を入力し，生成結果を得る
        _, predictions = self.translator.translate(
            src=src,
            tgt=None,
            src_dir=self.opt.src_dir,
            batch_size=self.opt.batch_size,
            attn_debug=False
        )
        # 生成結果も分かち書きされているので空白を削除
        utt = predictions[0][0].replace(" ", "")
        utt = re.sub("それな","せやな",utt)
        utt = re.sub("です。","やで。",utt)
        utt = re.sub("です！","やで！",utt)
        utt = re.sub("だよ。","やで。",utt)
        utt = re.sub("だよ！","やで！",utt)
        utt = re.sub("だね。","やね。",utt)
        utt = re.sub("ですか。","やろか。",utt)
        utt = re.sub("かも。","やろなあ。",utt)
        utt = re.sub("だった。","やった。",utt)
        utt = re.sub("じゃん。","やん。",utt)
        utt = re.sub("見えない。","見えへん。",utt)
        utt = re.sub("出ない。","でーへん。",utt)
        utt = re.sub("分からない。","分からへん。",utt)
        utt = re.sub("見ない。","みーひん。",utt)
        utt = re.sub("着ない。","きーへん。",utt)
        utt = re.sub("しないで。","せんとって。",utt)
        utt = re.sub("お母さん","おかん",utt)
        utt = re.sub("お父さん","おとん",utt)
        utt = re.sub("本当","ほんま",utt)
        utt = re.sub("変わった","けったい",utt)
        utt = re.sub("だめ","あかん",utt)
        utt = re.sub("ありがとう。","おおきに。",utt)
        utt = re.sub("とても","ばり",utt)
        utt = re.sub("あなた","自分",utt)
        utt = re.sub("私は","うちは",utt)
        utt = re.sub("私の","うちの",utt)
        utt = re.sub("私を","うちを",utt)
        utt = re.sub("私に","うちに",utt)
        utt = re.sub("私が","うちが",utt)
        utt = re.sub("私へ","うちへ",utt)
        utt = re.sub("私と","うちと",utt)
        utt = re.sub("ですね","やね",utt)
        utt = re.sub("いいよ。","かまへん。",utt)
        utt = re.sub("いいよ","かまへん",utt)
        utt = re.sub("どういたしまして","かまへんよ",utt)
        utt = re.sub("わかる","せやな",utt)
        utt = re.sub("仕方ない","しゃーない",utt)
        utt = re.sub("いいな","ええな",utt)
        utt = re.sub("そうなんですよね","そうやな",utt)
        utt = re.sub("面白い","おもろい",utt)
        utt = re.sub("違う","ちゃう",utt)
        utt = re.sub("早く","はよ",utt)
        utt = re.sub("いくら","なんぼ",utt)
        utt = re.sub("どのくらい","なんぼ",utt)
        utt = re.sub("とても","めっちゃ",utt)
        utt = re.sub("がんばれ","応援しとるで",utt)
        generated_reply = re.sub("すごく","めっちゃ",utt)
        print(input['utt'])
        print(generated_reply)
        # 次回の応答生成のために今回の応答を保存
        self.prev_uttr_dict[input["sessionId"]] = generated_reply
        return {"utt": generated_reply,  "end": False}


if __name__ == '__main__':
    system = ContextGenerativeSystem()
    bot = TelegramBot(system)
    bot.run()
    
