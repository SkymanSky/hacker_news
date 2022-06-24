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
print(submission_dicts)

titles,hn_links,comments=[],[],[]
for i in range(len(submission_dicts)):
    titles.append(submission_dicts[i]['title'])
    hn_links.append(submission_dicts[i]['hn_link'])
    comments.append(submission_dicts[i]['comments'])


#Veri görselleştirme
data=[{
    'type':'bar',
    'x':titles,
    'y':comments,
}]

my_layout={
        'title':'Most commented topics in Hacker News',
        'xaxis':{'title':'Topic'},
        'yaxis':{'title':'Comments'}
}

fig={'data':data,'layout':my_layout}
offline.plot(fig,filename='hn_topics.html')