'use strict'

var _HEADER_TYPES = 'Accept,Accept-Charset,Accept-Encoding,Accept-Language,Connection,Cookie,Host,Referer,User-Agent'.split(',');

function _create_xhr() {
    var _xhr = null;
    if(window.XMLHttpRequest) {
        _xhr = new XMLHttpRequest()
    } else {
        _xhr = new ActiveXObject("Microsoft.XMLHTTP")
    }
    return _xhr;
}

function _serialize(params) {
    var _rtn = [];
    for(var key in params) {
        _rtn.push(encodeURIComponent(key) + '=' + encodeURIComponent(params[key])) 
    }
    return _rtn.join("&");
}

function request(url, params, callback, method, async, timeout, headers) {
    params = params || {};
    callback = callback || function(text, xml, xhr, headers){};
    var callback_timeout = function() {};
    timeout = timeout || 60;
	async = async == undefined || !!async;
    method = method || 'POST';
    headers = headers || {};
    
    var _xhr = _create_xhr()
    if('GET' == method.toUpperCase()) {
        var _params = _serialize(params);
        if(_params) {
            url += '?' + _params;
        }
     } else {
        params = null;
    }
    _xhr.onreadystatechange = function(){
        if(4 == _xhr.readyState) {
            if((_xhr.status >= 200 && _xhr.status < 300) || 404 == _xhr.status) {
                callback(_xhr.responseText, _xhr.responseXML, _xhr, _xhr.getAllResponseHeaders());
            }
        }
    };
    _xhr.open(method, url, async);
    if(async) {
	    _xhr.timeout = timeout;
	    _xhr.ontimeout = function() {callback_timeout();}
    }
	for(var key in headers) {
        _xhr.setRequestHeader(key, headers[key]);
    }
    _xhr.send(params)
}


/*
跨域访问:服务器端需要设置reponse header:Access-Control-Allow-Origin:*

IE可用XDomainRequest进行跨域访问
*/

/*
TestCase

index.html
<!DOCTYPE html>
<html>
  <head>
	<meta charset="utf-8"/>
	<title>xhr</title>
    <script type="text/javascript" src="xhr.js"></script>
    <script type="text/javascript">
      request("http://localhost/data.json", {"time":(new Date()).getTime()}, function(){console.log(arguments);}, "get");
    </script>
  </head>
</html>

data.json
{"name":"silence"}
*/
