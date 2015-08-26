/*
 * our custom implementation of eq_snom function. this function is called from code behind as client action
 */
openerp.eq_snom = function (instance) {
    instance.web.client_actions.add('eq_snom.action', 'instance.eq_snom.action');
    instance.eq_snom.action = function (parent, action) {
        //console.log("Executed the action", action);
    	//console.log("url", action.url);
    	
    	// get url from paramater action and execute http get
    	var i = document.createElement("img");
		i.src = action.url;		
    };
};