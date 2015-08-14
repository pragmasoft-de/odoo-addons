import werkzeug.urls

import openerp
import openerp.addons.web.controllers.main as webmain

class eq_snom_controller(openerp.http.Controller):
    _name = 'eq.snom.controller'
    
    @openerp.http.route('/snom/call', type='http', auth="none")
    def start_javascript_call(self, url):
        out = """<html><head><script>
                function LoadURL(){
                    var i = document.createElement("img");
                    i.src = \"""" + url + """\";
                }
                </script></head><body onload="LoadURL();" /></html>"""                  
        return out