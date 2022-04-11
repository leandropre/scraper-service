from prometheus_client import start_http_server, Gauge
import requests
import http.server
import prometheus_client as prom
import simplejson
import json

"""Remove internal metrics from prometheus that we don't need""" 

prom.REGISTRY.unregister(prom.PROCESS_COLLECTOR)
prom.REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
prom.REGISTRY.unregister(prom.GC_COLLECTOR)

"""We also can use Counter instead of Gauge (the value of the Gauge can be increased and decreased)
   Finally, I have used Gauge in order to have the same output than the file you sent me 
   (Counter adds _total and _created suffix in the runtime)"""

REQUEST_COUNT = Gauge('http_get', 'Http Count',['url', 'code'])

class ServerHandler(http.server.BaseHTTPRequestHandler):

  def _set_headers(self):
    """This method send the header configuration"""
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()

  def do_HEAD(self):
    """This method serves the 'HEAD' request type: it sends the headers it would send for the equivalent GET Request"""
    self._set_headers()

  def do_GET(self):
    """This method serves the 'GET' request type"""
    self._set_headers()
    self.wfile.write(json.dumps({'success': True }).encode('utf-8'))

  def do_POST(self):
    """This method serves the 'POST' request type"""
    self._set_headers()

    content_len = int(self.headers.get('content-length', 0))
    content_type = self.headers.get('content-type', 0)

    """Only json request with valid data"""
    if content_type != 'application/json' or content_len <= 0 :
        self.send_response(400)
        self.end_headers()
        return
    
    """With the json data, the url is scraped"""
    post_body = self.rfile.read(content_len)
    
    test_data = simplejson.loads(post_body)

    url=test_data.get('url')

    """Make the get request with the scraped url. We set allow_redirects=False in order to avoid requests to handle redirections"""
    response = requests.get(url,allow_redirects=False)

    """Increment Request_count with the scraped url and the status code of the request made previously"""
    REQUEST_COUNT.labels(url=url,code=response.status_code).inc(1)

    self.wfile.write(json.dumps({'success': True }).encode('utf-8'))
    
  

if __name__ == "__main__":
    """Start server on ports 8080 ,and 9095 for metrics"""

    start_http_server(9095)
    server = http.server.HTTPServer(('', 8080), ServerHandler)
    print("Prometheus metrics available on port http://localhost:9095/metrics")
    print("HTTP server available on port http://localhost:8080")

    try:
      server.serve_forever()
    except KeyboardInterrupt:
      print("Shutting down...")
      server.socket.close()
      