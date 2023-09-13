from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import math
import textwrap
import pickle
import datetime

def make_pdf(title_text,subtitle_text,date_affiliation,midashi_list,honbun_list):#,im_1_file_list,im_2_file_list):
    # 画像変形関数
    def image_mag(im_x_f, im_y_f, canvas_x, canvas_y):
        canvas_ratio = canvas_y / canvas_x  
        im_ratio = im_y_f / im_x_f
        if im_ratio > canvas_ratio:
            mag = canvas_y / im_y_f 
        else:
            mag = canvas_x / im_x_f 
        return mag

    # オブジェクトの生成、用紙設定
    c = canvas.Canvas('static/slides/presentation.pdf')  # pdfファイルの生成 
    w, h = 1462, 1033
    c.setPageSize((w,h))  # 1462 x 1033ピクセル(125dpi)設定
    font_name = 'HeiseiKakuGo-W5'  # フォント名
    pdfmetrics.registerFont(UnicodeCIDFont(font_name))  # フォントを登録
    margin = 40  # ページ余白

    # ロゴ用画像のサイズ調整
    logo_area_x, logo_area_y = 100, 100
    logo = Image.open('test.png')  
    logo_x,logo_y = logo.size
    logo_mag = image_mag(logo_x, logo_y, logo_area_x, logo_area_y)
    logo_r = logo.resize((int(logo_x*logo_mag),int(logo_y*logo_mag)))
    logo_r_x,logo_r_y = logo_r.size

    # タイトルページの設定
    title_font_size = 72  # タイトルの文字サイズ
    subtitle_font_size = 48  # サブタイトルの文字サイズ
    affiliation_font_size = 32  # 所属情報の文字サイズ
    # title_text = 'プレゼン資料を自動で生成'
    # subtitle_text ='パワポにペタペタするのは面倒ですよね？'
    # date_affiliation = '2020/3/8 Pythonでいろいろやってみる'

    # タイトルページの描画
    c.setFont(font_name, title_font_size)
    c.drawCentredString(w/2, h/2, title_text)  # タイトルをページ中心に表示
    c.setFont(font_name, subtitle_font_size)
    c.drawCentredString(w/2, h/2-title_font_size-20, subtitle_text)  # サブタイトルタイトルの下に表示
    c.setFont(font_name, affiliation_font_size)
    c.drawRightString(w-margin,margin,date_affiliation)  # 所属情報を右下に表示
    c.drawInlineImage(logo_r,w-logo_r_x-margin,h-logo_r_y-margin)  # ロゴを右上に表示
    
    # # 本文ページの内容()
    # midashi_list = ['プレゼン資料作りは時間がかかる割に・・・',
    #             '資料を自動生成させれば労力は大幅に減ります']
    # honbun_list = ['プレゼン用資料作りは時間がかかって大変です。特に画像の大きさ調整とか文字の表示位置のずれを直すとかむなしいですね。自動化できればありがたいです。',
    #             '内容をテキストで書いておき画像をファイル名で指定することで自動で体裁が整ったプレゼン用pdfファイルが生成されます']
    im_1_file_list = ['test.png',
                'test.png']
    im_2_file_list = ['test.png',
                'test.png']

    # 本文ページの設定
    pages = len(midashi_list)  # 本文のページ数
    midashi_font_size = 60  # 見出しの文字サイズ
    text_font_size = 30  # 本文の文字サイズ
    gyokan = 15  # 本文の行間隔\
    honbun_y_pos = 240  # 本文の表示位置(y)
    im_1_area_x, im_1_area_y = 650, 450  # 画像1表示エリアのサイズ
    im_2_area_x, im_2_area_y = 650, 450  # 画像2表示エリアのサイズ


    for midashi, honbun_dict, im_1_file, im_2_file in zip(midashi_list, honbun_list, im_1_file_list, im_2_file_list): 
        
        c.showPage()  # 改ページ
        
        # イメージ1のサイズ調整
        im_1 = Image.open(im_1_file)  # ロゴ用画像の読み出し
        im_1_x,im_1_y = im_1.size
        im_1_mag = image_mag(im_1_x, im_1_y, im_1_area_x, im_1_area_y)
        im_1_r = im_1.resize((int(im_1_x*im_1_mag),int(im_1_y*im_1_mag)))

        # イメージ2のサイズ調整
        im_2 = Image.open(im_2_file)  # ロゴ用画像の読み出し
        im_2_x,im_2_y = im_2.size
        im_2_mag = image_mag(im_2_x, im_2_y, im_2_area_x, im_2_area_y)
        im_2_r = im_2.resize((int(im_2_x*im_2_mag),int(im_2_y*im_2_mag)))

        honbun = f"""
        課題:{honbun_dict['problem']}

        手法:{honbun_dict['method']}

        結果:{honbun_dict['result']}
        """
        
        text_area_w = w-2*margin 

        c.drawInlineImage(logo_r,w-logo_r_x-margin,h-logo_r_y-margin)

        # 見出しのテキスト折り返し
        midashi_len = len(midashi)
        midashi_chr_w = text_area_w // (midashi_font_size/2)  # 見出しの1行の文字数
        midashi_rows = math.ceil(midashi_len/midashi_chr_w)  # 見出しの行数
        midashi_rows_list = textwrap.wrap(midashi, midashi_chr_w)  # 見出しの折り返し

        c.setFont(font_name, midashi_font_size)

        count_row = 0
        for i in midashi_rows_list:
            c.drawString(margin, h-90-count_row*(midashi_font_size+gyokan), i)
            count_row += 1

        # 本文のテキスト折り返し
        honbun_len = len(honbun)
        text_chr_w = text_area_w // text_font_size  # 本文の1行の文字数
        honbun_rows = math.ceil(honbun_len/text_chr_w)  # 本文の行数
        honbun_rows_list = textwrap.wrap(honbun, text_chr_w) 

        c.setFont(font_name, text_font_size)
        
        count_row = 0
        for i in honbun_rows_list:
            c.drawString(margin, h-honbun_y_pos-count_row*(text_font_size+gyokan), i)
            count_row += 1

        # 図の表示
        # c.drawInlineImage(im_1_r,margin,margin)
        # c.drawInlineImage(im_2_r,w/2+margin,margin)

    c.save()  # ファイル保存

if __name__ == '__main__':
    # load pickle
    with open('info_dict.pickle', 'rb') as f:
        return_list = pickle.load(f)
    today = datetime.date.today()
    today_str = today.strftime('%Y%m%d')

    title_list = [ item['title'] for item in return_list ]
    # body_list = [ "\n".join(item['gpt_summaries'].values()) for item in return_list ]
    body_list = [ item['gpt_summaries'] for item in return_list ]

    make_pdf(title_text='動画編集サーベイ',
                subtitle_text='サーベイ実験',
                date_affiliation=today_str,
                midashi_list=title_list,
                honbun_list=body_list)