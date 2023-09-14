from flask import Flask, render_template, send_file, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
import os
import arxiv
import openai
from dotenv import load_dotenv
from create_pdf import make_pdf
import datetime
import pickle 

# MagicProp: Diffusion-based Video Editing via Motion-aware Appearance Propagation

#OpenAIのapiキー
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = """与えられた論文の要点をまとめ、以下の項目で日本語で出力せよ。それぞれの項目は最大でも180文字以内に要約せよ。
```
課題:この論文が解決する課題
手法:この論文が提案する手法
結果:提案手法によって得られた結果
```"""

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Create a Flask-WTF form for user input
class PdfGenerationForm(FlaskForm):
    keywords = StringField('Keywords', render_kw={"placeholder":'Video Prediction, Music Generation, Mixture of Experts, etc...'})
    paper_titles = TextAreaField('Paper Titles (comma sperated)', render_kw={"placeholder":' Distilling the Knowledge in a Neural Network, \n Hierarchical Text-Conditional Image Generation with CLIP Latents,'})
    submit = SubmitField('Generate PDF')

@app.route('/', methods=['GET', 'POST'])
def input_page():
    form = PdfGenerationForm()
    if form.validate_on_submit():
        # Handle form submission here
        keywords = form.keywords.data
        paper_titles = form.paper_titles.data
        # print(keywords, paper_titles)
        if keywords:
            print("keywords", keywords)
            result_list = get_papers_from_keyword(keywords, 5, 2019)
            print("result_list", result_list)
        elif paper_titles:
            print("paper_titles", paper_titles)
            paper_titles = paper_titles.split(',')
            result_list = get_papers_from_list(paper_titles)
            print("result_list", result_list)
        else:
            result_list = []
            print("error")

        if len(result_list) > 0:
            return_list = generate_summaries(result_list)
            # print("info_dict", return_list)

        # save as pickle
        with open('info_dict.pickle', 'wb') as f:
            pickle.dump(return_list, f)

        today = datetime.date.today()
        today_str = today.strftime('%Y/%m/%d')

        title_list = [ item['title'] for item in return_list ]
        # body_list = [ "\n".join(item['gpt_summaries'].values()) for item in return_list ]
        body_list = [ item['gpt_summaries'] for item in return_list ]
        urls = [ item['pdf_url'] for item in return_list ]
        years = [ item['published'].year for item in return_list ]
        authors = [ item['authors'] for item in return_list ]

        print(len(title_list), len(body_list))
        make_pdf(title_text=keywords or '論文サーベイ',
                 subtitle_text='サーベイ',
                 date_affiliation=today_str,
                 midashi_list=title_list,
                 honbun_list=body_list,
                 url_list=urls,
                 year_list=years,
                 author_list=authors,)
        
        return render_template('download_pdf.html', form=form)
        
        

    return render_template('input_page.html', form=form)

@app.route('/download_pdf_page')
def download_pdf_page():
    return render_template('download_pdf.html')

@app.route('/static/slides/<path:filename>')
def static_file(filename):
    return send_from_directory('static/slides', filename)


@app.route('/static/slides/download_pdf')
def download_pdf():
    pdf_file = 'presentation.pdf'  # Replace with the path to your PDF file
    return send_file(pdf_file, as_attachment=True)


def get_papers_from_list(paper_title_list):
    result_list = []
    for paper_title in paper_title_list:
        search = arxiv.Search(
            query=f"all:%22 {paper_title} %22",
            max_results=1
        )
        for result in search.results():
            result_list.append(result)
            # print(result, result.published.year, result.title)
            # if result.published.year >= from_year:
            #     result_list.append(result)
    return result_list

def get_papers_from_keyword(query, max_results,from_year):
    result_list = []
    query = f'all:%22 {query} %22'
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )
    for result in search.results():
        print(result.title,result.published.year)
        if result.published.year >= from_year:
            result_list.append(result)
    return result_list

def generate_summaries(result_list):
    return_list = []
    
    for result in result_list:
        pdf_info = {}
        pdf_info["title"] = result.title
        pdf_info["abstract"] = result.summary
        pdf_info["pdf_url"] = result.pdf_url
        pdf_info["published"] = result.published
        pdf_info["doi"] = result.doi
        pdf_info["primary_category"] = result.primary_category
        pdf_info["authors"] = result.authors
        text = f"title: {result.title}\nbody: {result.summary}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # model='gpt-4',
            messages=[
                {'role': 'system', 'content': prompt},
                {'role': 'user', 'content': text}
            ],
            temperature=0.25,
        )

        summary = response['choices'][0]['message']['content']
        # print("#### GPT", summary)
        gpt_dict = {}    
        for b in summary.split('\n'):
            # print("****", b)
            if b.startswith("課題"):
                gpt_dict['problem'] = b[3:].lstrip()
            if b.startswith("手法"):
                gpt_dict['method'] = b[3:].lstrip()
            if b.startswith("結果"):
                gpt_dict['result'] = b[3:].lstrip()
        # print("Dict by ChatGPT", dict)

        pdf_info["gpt_summaries"] = gpt_dict
        return_list.append(pdf_info)
    return return_list

def create_pdf_from_info_dict(info_dict):
    pass

if __name__ == '__main__':
    app.run(debug=True)
