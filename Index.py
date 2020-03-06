import requests
from json import dump
from json import loads

def run_query(json, headers): # A simple function to use requests.post to make the API call.

    request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}. {}"
                        .format(request.status_code, json['query'],
                                json['variables']))

query = """
query example{
  search(query:"stars:>100", type:REPOSITORY, first:100{AFTER}){
    pageInfo{
        hasNextPage
        endCursor
    }
    nodes{
      ... on Repository{
        nameWithOwner
        diskUsage
      }
    }
  }
}
"""

finalQuery = query.replace("{AFTER}", "")

json = {
    "query":finalQuery, "variables":{}
}

token = '66df1b1e877468580db25ae2b95f4198da961205' #insert your token
headers = {"Authorization": "Bearer " + token}

total_pages = 1

result = run_query(json, headers)

nodes = result['data']['search']['nodes']
next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]

#paginating
while (next_page and total_pages < 10):
    total_pages += 1
    cursor = result["data"]["search"]["pageInfo"]["endCursor"]
    next_query = query.replace("{AFTER}", ", after: \"%s\"" % cursor)
    json["query"] = next_query
    result = run_query(json, headers)
    nodes += result['data']['search']['nodes']
    next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]

#saving data
for node in nodes:
    with open("C:/Users/PICHAU/PycharmProjects/Laboratorio6/dadosgit.csv", 'a') as the_file:
        the_file.write("Nome do Repositorio: " + node['nameWithOwner'] + "\n" + "diskUsage: " + str(node['diskUsage']) + "\n")