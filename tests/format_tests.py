import unittest

from lib.utils.wiki import read_template, clean_text


class MyTestCase(unittest.TestCase):
    def test_read_template(self):
        text = """
        {{声优信息
        |名字={{PAGENAME}}
        |image=Hanae Natsuki0.png
        |姓名={{ruby|花江|はなえ|ja}} {{ruby|夏樹|なつき|ja}}<br />（Hanae Natsuki）
        |其它艺名={{黑幕|松田春树}}
        |昵称={{黑幕|爆破鬼才}}、{{黑幕|AV男优}}、<del>花光課金</del><ref>課金與夏树在日語諧音</ref>
        |生日=1991年6月26日
        |血型=B型
        |星座= {{Astrology|6|26}}
        |年龄= {{Age|1991|6|26}}
        |身高=173
        |三围=
        |出身地区=日本神奈川县
        |所属公司=Across Entertainment
        |出道角色=生存游戏社员A《[[便·当]]》
        |代表角色=[[维也纳(前田敦博)]]《[[TARI TARI]]》<br />[[先岛光]]《[[来自风平浪静的明天]]》<br />[[金木研]]《[[东京食尸鬼]]》<br />[[界冢伊奈帆]]《[[ALDNOAH.ZERO]]》<br />[[有马公生]]《[[四月是你的谎言]]》<br />鸟束零太《[[齐木楠雄的灾难]]》<br />[[真壁政宗]]《[[政宗君的复仇]]》<br /> [[寄叶九号S型]]《[[尼尔:机械纪元]]》<br />[[齐格]]《[[Fate/Apocrypha]]》<br />[[灶门炭治郎]]《[[鬼灭之刃]]》<br />[[成神阳太]]《[[成神之日]]》
        |相关人士=
        }}
        """
        result = read_template(text, '声优信息', ['生日', '血型'])
        self.assertEqual(result['生日'], '1991年6月26日')

    def test_clean(self):
        text = "[[森川智之|森川 智之]]"
        text = clean_text(text)
        print(text)

if __name__ == '__main__':
    unittest.main()
