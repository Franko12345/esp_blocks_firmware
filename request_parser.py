def parse_request(request):
    request = list(filter(lambda x: x, request.decode().replace("\r", "").replace("\n\n", "\n").split("\n")))
    
    request_mode, url, _ = request[0].replace("https://", "").replace("http://", "").split(" ")
    print(request[0])
    
    args = {}
    if "?" in url:
        args = {x.split("=")[0]:x.split("=")[1] for x in url.split("?")[1].split("&")}
    
    url = url.split("?")[0]
    
    body = ""
    if not ":" in request[-1]:
        body = request[-1]
        
    request = request[1:-1]
    
    print(request)
    #parsed_request = {x.split(":")[0]:x.split(":")[1] for x in request}
    
    return {"method": request_mode, "url":url, "args":args, "headers": request, "body":body}