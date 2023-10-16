from flask import Blueprint, render_template

views = Blueprint('views', __name__)

import os, json
import dotenv

import requests

from flask import request, jsonify, send_file 
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent, AgentType

introspection_query = """
  query IntrospectionQuery {
    __schema {
      queryType { name }
      mutationType { name }
      subscriptionType { name }
      types {
        ...FullType
      }
      directives {
        name
        description
        locations
        args {
          ...InputValue
        }
      }
    }
  }
  fragment FullType on __Type {
    kind
    name
    description
    fields(includeDeprecated: true) {
      name
      description
      args {
        ...InputValue
      }
      type {
        ...TypeRef
      }
      isDeprecated
      deprecationReason
    }
    inputFields {
      ...InputValue
    }
    interfaces {
      ...TypeRef
    }
    enumValues(includeDeprecated: true) {
      name
      description
      isDeprecated
      deprecationReason
    }
    possibleTypes {
      ...TypeRef
    }
  }
  fragment InputValue on __InputValue {
    name
    description
    type { ...TypeRef }
    defaultValue
  }
  fragment TypeRef on __Type {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                }
              }
            }
          }
        }
      }
    }
  }
"""

def get_schema(connection_string: str) -> str:
  request_response = requests.post(url=connection_string, json={"query":introspection_query}).json()
  response = json.dumps(request_response)
  return response

# Code for routing goes here
@views.route("/chatapi", methods=['GET','POST'])
def chat_api():
    if request.method == "POST":
        print(request.headers)
        request_body = request.get_json()
        print("debug marker")

        dotenv.load_dotenv("./.env")
        llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

        tools = load_tools(
            ["graphql"],
            graphql_endpoint=request_body["graph_url"],
        )

        agent = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        )

        prompt =  \
        """You will recieve the schema of a graphQL endpoint and a question from a user for info from that 
        endpoint, respond with the most accurate answer in a polite and helpful way using only information
        you retrieved from the graphQL api."""

        result = agent.run(
            prompt + "\n"
            + get_schema(request_body["graph_url"]) + "\n"
            + request_body["user_request"] 
        )
        result = {"message": result}
    else:
        result = {}
    print(result)
    print(type(jsonify(result)))

    return render_template('base.html', context={'result':jsonify(result)})
"""
Summary:
handles a user request with json body of format:
{
  "user_request": the users message as a string
  "graph_url": the url to the subgraph the user wants to access as a string
}

Returns:
  str: the chat bots response to the users request
"""

@views.route("/<filename>", methods=['GET','POST'])
def doc(filename):
  try:
    return send_file(os.path.join('files/', filename))
  except:
    return "404 not found"