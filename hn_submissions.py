from operator import itemgetter
import requests
from plotly.graph_objs import Bar
from plotly import offline

#API çağrısı yap.
url='https://hacker-news.firebaseio.com/v0/topstories.json'
r=requests.get(url)
print(f"Status code: {r.status_code}")

#Her bir gönderi ile ilgili olan veriyi işle.
submission_ids=r.json()
submission_dicts=[]

for submission_id in submission_ids[:10]:
    #Her bir id için ayrı API çağrısı yap
    url=f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r=requests.get(url)
    print(f"id: {submission_id}\tStatus: {r.status_code}")
    response_dict=r.json()
    #Her bir makale için sözlük oluştur.
    #print(response_dict)
    submission_dict={
            'title':response_dict['title'],
            'hn_link':f"http://news.ycombinator.com/item?id={submission_id}",
            'comments':response_dict['descendants'],
    }
    submission_dicts.append(submission_dict)
submission_dicts=sorted(submission_dicts,key=itemgetter('comments'),reverse=True)


titles,hn_links,comments=[],[],[]
for i in range(len(submission_dicts)):
    title=submission_dicts[i]['title']
    link=submission_dicts[i]['hn_link']
    link_with_title=f"<a href='{link}'>{title}</a>"
    titles.append(submission_dicts[i]['title'])
    hn_links.append(link_with_title)
    comments.append(submission_dicts[i]['comments'])


#Veri görselleştirme
data=[{
    'type':'bar',
    'x':hn_links,
    'y':comments,
    'marker':{
        'color':'rgb(60,100,150)',
        'line':{'width':1.5,'color':'rgb(25,25,25)'
        }
    },
    'opacity':0.6,
}]

my_layout={
        'title':'Most commented topics in Hacker News',
        'titlefont':{'size':28},
        'xaxis':{
            'title':'Topics',
            'titlefont':{'size':24},
            'tickfont':{'size':14},
            },
        'yaxis':{
            'title':'Comments',
            'titlefont':{'size':24},
            'tickfont':{'size':14},
            }
}

fig={'data':data,'layout':my_layout}
offline.plot(fig,filename='hn_topics.html')