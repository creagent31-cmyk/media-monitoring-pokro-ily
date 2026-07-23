
def create(items):


    html="""

<h1>
📰 Cresco Media Monitoring
</h1>

"""


    for i in items:


        html+=f"""

<h3>
{i['title']}
</h3>

<p>
{i['summary']}
</p>

<p>
Sentiment:
{i['sentiment']}
</p>

<hr>

"""


    return html
