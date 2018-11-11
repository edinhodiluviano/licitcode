from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render

from web3 import Web3, HTTPProvider

from django.views.decorators.csrf import csrf_exempt

abi = """[
        {
                "constant": false,
                "inputs": [],
                "name": "count",
                "outputs": [
                        {
                                "name": "",
                                "type": "uint256"
                        }
                ],
                "payable": false,
                "stateMutability": "nonpayable",
                "type": "function"
        },
        {
                "constant": false,
                "inputs": [
                        {
                                "name": "id",
                                "type": "uint256"
                        },
                        {
                                "name": "text",
                                "type": "string"
                        }
                ],
                "name": "new_contract",
                "outputs": [
                        {
                                "name": "",
                                "type": "int256"
                        }
                ],
                "payable": false,
                "stateMutability": "nonpayable",
                "type": "function"
        },
        {
                "constant": false,
                "inputs": [
                        {
                                "name": "id",
                                "type": "uint256"
                        }
                ],
                "name": "read",
                "outputs": [
                        {
                                "name": "",
                                "type": "string"
                        }
                ],
                "payable": false,
                "stateMutability": "nonpayable",
                "type": "function"
        },
        {
                "constant": true,
                "inputs": [
                        {
                                "name": "",
                                "type": "uint256"
                        }
                ],
                "name": "contracts",
                "outputs": [
                        {
                                "name": "id",
                                "type": "uint256"
                        },
                        {
                                "name": "text",
                                "type": "string"
                        }
                ],
                "payable": false,
                "stateMutability": "view",
                "type": "function"
        }
]"""



def index(request):
    template = loader.get_template("template1.html")
    c = {}
    return render(request, "template1.html", c)
#    return HttpResponse(template.render())


@csrf_exempt
def register(request):
    web3 = Web3(HTTPProvider('https://rinkeby.infura.io'))
    uri = '0xc7B3609B4B33Ad29BBDb1f6FbAf1da3834761B6f'
    c = web3.eth.contract(uri, abi=abi)
    l = c.functions.count().call() + 1
    s = c.functions.new_contract(l, request.POST['text']).call()
    try:
#        s = c.functions.new_contract(l, request.POST['text']).call()
        if 'csrfmiddlewaretoken' in request.POST:
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("{'contract_number':" + str(l) + "}")
    except:
        if 'csrfmiddlewaretoken' in request.POST:
            return HttpResponseRedirect('/')
        else:
            return HttpResponse(-1)
