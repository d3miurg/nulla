import amino

from django.http import JsonResponse

response = {
		'status': 'ok',
		'additional': 'none'
		}

#возможно, стоит поменять имя
def handle_errors(func):
    def exec_func(*args, **kwargs):
        try:
            func(*args, **kwargs)

        except json.decoder.JSONDecodeError:
            response['status'] = 'Сервера упали. Как всегда, блять'

        except requests.exceptions.SSLError:
            response['status'] = 'А де интернет?'
            
        return JsonResponse(response)

    return exec_func

@handle_errors
def login(request):
	global user
	global response
	
	email = request.GET.get('email', '')
	password = request.GET.get('password', '')
	print(email)
	print(password)
	user = amino.Client()
	try:
		if (not email) or (not password):
			raise ValueError
		user.login(email, password)
	
	except ValueError:
		response['status'] = 'fields needed to be filled'
	
	except amino.lib.util.exceptions.InvalidEmail or amino.lib.util.exceptions.AccountDoesntExist:
		response['status'] = 'Can\'t find accaunt'
		
	except amino.lib.util.exceptions.InvalidAccountOrPassword or amino.lib.util.exceptions.InvalidPassword:
	    response['status'] = 'Invalid  password'
	    
	except amino.lib.util.exceptions.ActionNotAllowed:
    	#почините это, кто-нибудь
		response['status'] = 'device was blocked'

@handle_errors
def getCommunities(request):
    global user
    global response
    
    names = []
    ids = []
    communities = user.sub_clients()

    for i in range(0, len(communities.name)):
        names.append([communities.name[i], communities.comId[i]])
        
    response['additional'] = {
     	'communityNames': names,
     	'communityIds': ids
     }
		
#def enterCommunity(request):

#def enterChat(request):	
			
#def readChatHistory(request):
	
def readLastMessage(requst):
	return JsonResponse({"test":"success"})

#def sendMessage(request):