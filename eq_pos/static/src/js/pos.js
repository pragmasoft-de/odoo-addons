openerp.eq_pos = function (instance) {
    var _t = instance.web._t;
    var QWeb = instance.web.qweb;
    
    var round_di = instance.web.round_decimals;
    var round_pr = instance.web.round_precision;
    
    
    
    
    
    
    
    // EQUITANIA: Extension of default functionality of module.posDB from db.js
    //-------------------- START - Extension of search function eq_internal_number --------------------------------------//
    instance.point_of_sale.PosDB = instance.web.Class.extend({
        name: 'openerp_pos_db', //the prefix of the localstorage data
        limit: 100,  // the maximum number of results returned by a search
        init: function(options){
            options = options || {};
            this.name = options.name || this.name;
            this.limit = options.limit || this.limit;

            //cache the data in memory to avoid roundtrips to the localstorage
            this.cache = {};

            this.product_by_id = {};
            this.product_by_ean13 = {};
            this.product_by_category_id = {};
            this.product_by_reference = {};

            this.partner_sorted = [];
            this.partner_by_id = {};
            this.partner_by_ean13 = {};
            this.partner_search_string = "";
            this.partner_write_date = null;

            this.category_by_id = {};
            this.root_category_id  = 0;
            this.category_products = {};
            this.category_ancestors = {};
            this.category_childs = {};
            this.category_parent    = {};
            this.category_search_string = {};
            this.packagings_by_id = {};
            this.packagings_by_product_tmpl_id = {};
            this.packagings_by_ean13 = {};
        },
        /* returns the category object from its id. If you pass a list of id as parameters, you get
         * a list of category objects. 
         */  
        get_category_by_id: function(categ_id){
            if(categ_id instanceof Array){
                var list = [];
                for(var i = 0, len = categ_id.length; i < len; i++){
                    var cat = this.category_by_id[categ_id[i]];
                    if(cat){
                        list.push(cat);
                    }else{
                        console.error("get_category_by_id: no category has id:",categ_id[i]);
                    }
                }
                return list;
            }else{
                return this.category_by_id[categ_id];
            }
        },
        /* returns a list of the category's child categories ids, or an empty list 
         * if a category has no childs */
        get_category_childs_ids: function(categ_id){
            return this.category_childs[categ_id] || [];
        },
        /* returns a list of all ancestors (parent, grand-parent, etc) categories ids
         * starting from the root category to the direct parent */
        get_category_ancestors_ids: function(categ_id){
            return this.category_ancestors[categ_id] || [];
        },
        /* returns the parent category's id of a category, or the root_category_id if no parent.
         * the root category is parent of itself. */
        get_category_parent_id: function(categ_id){
            return this.category_parent[categ_id] || this.root_category_id;
        },
        /* adds categories definitions to the database. categories is a list of categories objects as
         * returned by the openerp server. Categories must be inserted before the products or the 
         * product/ categories association may (will) not work properly */
        add_categories: function(categories){
            var self = this;
            if(!this.category_by_id[this.root_category_id]){
                this.category_by_id[this.root_category_id] = {
                    id : this.root_category_id,
                    name : 'Root',
                };
            }
            for(var i=0, len = categories.length; i < len; i++){
                this.category_by_id[categories[i].id] = categories[i];
            }
            for(var i=0, len = categories.length; i < len; i++){
                var cat = categories[i];
                var parent_id = cat.parent_id[0] || this.root_category_id;
                this.category_parent[cat.id] = cat.parent_id[0];
                if(!this.category_childs[parent_id]){
                    this.category_childs[parent_id] = [];
                }
                this.category_childs[parent_id].push(cat.id);
            }
            function make_ancestors(cat_id, ancestors){
                self.category_ancestors[cat_id] = ancestors;

                ancestors = ancestors.slice(0);
                ancestors.push(cat_id);

                var childs = self.category_childs[cat_id] || [];
                for(var i=0, len = childs.length; i < len; i++){
                    make_ancestors(childs[i], ancestors);
                }
            }
            make_ancestors(this.root_category_id, []);
        },
        /* loads a record store from the database. returns default if nothing is found */
        load: function(store,deft){
            if(this.cache[store] !== undefined){
                return this.cache[store];
            }
            var data = localStorage[this.name + '_' + store];
            if(data !== undefined && data !== ""){
                data = JSON.parse(data);
                this.cache[store] = data;
                return data;
            }else{
                return deft;
            }
        },
        /* saves a record store to the database */
        save: function(store,data){
            var str_data = JSON.stringify(data);
            localStorage[this.name + '_' + store] = JSON.stringify(data);
            this.cache[store] = data;
        },
        
        _product_search_string: function(product){
        	var str = product.display_name;
            if (product.ean13) {
                str += '|' + product.ean13;
            }
            if (product.default_code) {
                str += '|' + product.default_code;
            }
            if (product.description) {
                str += '|' + product.description;
            }
            if (product.description_sale) {
                str += '|' + product.description_sale;
            }
            // EQUITANIA: Erweiterung der Suchfunktion um unser Feld eq_internal_number
            if (product.eq_internal_number) {
                str += '|' + product.eq_internal_number;
            }
            
            var packagings = this.packagings_by_product_tmpl_id[product.product_tmpl_id] || [];
            for (var i = 0; i < packagings.length; i++) {
                str += '|' + packagings[i].ean;
            }
            str  = product.id + ':' + str.replace(/:/g,'') + '\n';
            return str;
        },
        add_products: function(products){
            var stored_categories = this.product_by_category_id;

            if(!products instanceof Array){
                products = [products];
            }
            for(var i = 0, len = products.length; i < len; i++){
                var product = products[i];
                var search_string = this._product_search_string(product);
                var categ_id = product.pos_categ_id ? product.pos_categ_id[0] : this.root_category_id;
                product.product_tmpl_id = product.product_tmpl_id[0];
                if(!stored_categories[categ_id]){
                    stored_categories[categ_id] = [];
                }
                stored_categories[categ_id].push(product.id);

                if(this.category_search_string[categ_id] === undefined){
                    this.category_search_string[categ_id] = '';
                }
                this.category_search_string[categ_id] += search_string;

                var ancestors = this.get_category_ancestors_ids(categ_id) || [];

                for(var j = 0, jlen = ancestors.length; j < jlen; j++){
                    var ancestor = ancestors[j];
                    if(! stored_categories[ancestor]){
                        stored_categories[ancestor] = [];
                    }
                    stored_categories[ancestor].push(product.id);

                    if( this.category_search_string[ancestor] === undefined){
                        this.category_search_string[ancestor] = '';
                    }
                    this.category_search_string[ancestor] += search_string; 
                }
                this.product_by_id[product.id] = product;
                if(product.ean13){
                    this.product_by_ean13[product.ean13] = product;
                }
                if(product.default_code){
                    this.product_by_reference[product.default_code] = product;
                }
            }
        },
        add_packagings: function(packagings){
            for(var i = 0, len = packagings.length; i < len; i++){
                var pack = packagings[i];
                this.packagings_by_id[pack.id] = pack;
                if(!this.packagings_by_product_tmpl_id[pack.product_tmpl_id[0]]){
                    this.packagings_by_product_tmpl_id[pack.product_tmpl_id[0]] = [];
                }
                this.packagings_by_product_tmpl_id[pack.product_tmpl_id[0]].push(pack);
                if(pack.ean){
                    this.packagings_by_ean13[pack.ean] = pack;
                }
            }
        },
        _partner_search_string: function(partner){
            var str =  partner.name;
            if(partner.ean13){
                str += '|' + partner.ean13;
            }
            if(partner.address){
                str += '|' + partner.address;
            }
            if(partner.phone){
                str += '|' + partner.phone.split(' ').join('');
            }
            if(partner.mobile){
                str += '|' + partner.mobile.split(' ').join('');
            }
            if(partner.email){
                str += '|' + partner.email;
            }
            str = '' + partner.id + ':' + str.replace(':','') + '\n';
            return str;
        },
        add_partners: function(partners){
            var updated_count = 0;
            var new_write_date = '';
            for(var i = 0, len = partners.length; i < len; i++){
                var partner = partners[i];

                if (    this.partner_write_date && 
                        this.partner_by_id[partner.id] &&
                        new Date(this.partner_write_date).getTime() + 1000 >=
                        new Date(partner.write_date).getTime() ) {
                    // FIXME: The write_date is stored with milisec precision in the database
                    // but the dates we get back are only precise to the second. This means when
                    // you read partners modified strictly after time X, you get back partners that were
                    // modified X - 1 sec ago. 
                    continue;
                } else if ( new_write_date < partner.write_date ) { 
                    new_write_date  = partner.write_date;
                }
                if (!this.partner_by_id[partner.id]) {
                    this.partner_sorted.push(partner.id);
                }
                this.partner_by_id[partner.id] = partner;

                updated_count += 1;
            }

            this.partner_write_date = new_write_date || this.partner_write_date;

            if (updated_count) {
                // If there were updates, we need to completely 
                // rebuild the search string and the ean13 indexing

                this.partner_search_string = "";
                this.partner_by_ean13 = {};

                for (var id in this.partner_by_id) {
                    var partner = this.partner_by_id[id];

                    if(partner.ean13){
                        this.partner_by_ean13[partner.ean13] = partner;
                    }
                    partner.address = (partner.street || '') +', '+ 
                                      (partner.zip || '')    +' '+
                                      (partner.city || '')   +', '+ 
                                      (partner.country_id[1] || '');
                    this.partner_search_string += this._partner_search_string(partner);
                }
            }
            return updated_count;
        },
        get_partner_write_date: function(){
            return this.partner_write_date;
        },
        get_partner_by_id: function(id){
            return this.partner_by_id[id];
        },
        get_partner_by_ean13: function(ean13){
            return this.partner_by_ean13[ean13];
        },
        get_partners_sorted: function(max_count){
            max_count = max_count ? Math.min(this.partner_sorted.length, max_count) : this.partner_sorted.length;
            var partners = [];
            for (var i = 0; i < max_count; i++) {
                partners.push(this.partner_by_id[this.partner_sorted[i]]);
            }
            return partners;
        },
        search_partner: function(query){
            try {
                query = query.replace(/[\[\]\(\)\+\*\?\.\-\!\&\^\$\|\~\_\{\}\:\,\\\/]/g,'.');
                query = query.replace(' ','.+');
                var re = RegExp("([0-9]+):.*?"+query,"gi");
            }catch(e){
                return [];
            }
            var results = [];
            for(var i = 0; i < this.limit; i++){
                r = re.exec(this.partner_search_string);
                if(r){
                    var id = Number(r[1]);
                    results.push(this.get_partner_by_id(id));
                }else{
                    break;
                }
            }
            return results;
        },
        /* removes all the data from the database. TODO : being able to selectively remove data */
        clear: function(stores){
            for(var i = 0, len = arguments.length; i < len; i++){
                localStorage.removeItem(this.name + '_' + arguments[i]);
            }
        },
        /* this internal methods returns the count of properties in an object. */
        _count_props : function(obj){
            var count = 0;
            for(var prop in obj){
                if(obj.hasOwnProperty(prop)){
                    count++;
                }
            }
            return count;
        },
        get_product_by_id: function(id){
            return this.product_by_id[id];
        },
        get_product_by_ean13: function(ean13){
            if(this.product_by_ean13[ean13]){
                return this.product_by_ean13[ean13];
            }
            var pack = this.packagings_by_ean13[ean13];
            if(pack){
                return this.product_by_id[pack.product_tmpl_id[0]];
            }
            return undefined;
        },
        get_product_by_reference: function(ref){
            return this.product_by_reference[ref];
        },
        get_product_by_category: function(category_id){
            var product_ids  = this.product_by_category_id[category_id];
            var list = [];
            if (product_ids) {
                for (var i = 0, len = Math.min(product_ids.length, this.limit); i < len; i++) {
                    list.push(this.product_by_id[product_ids[i]]);
                }
            }
            return list;
        },
        /* returns a list of products with :
         * - a category that is or is a child of category_id,
         * - a name, package or ean13 containing the query (case insensitive) 
         */
        search_product_in_category: function(category_id, query){        	
            try {
                query = query.replace(/[\[\]\(\)\+\*\?\.\-\!\&\^\$\|\~\_\{\}\:\,\\\/]/g,'.');
                query = query.replace(/ /g,'.+');
                var re = RegExp("([0-9]+):.*?"+query,"gi");
            }catch(e){
                return [];
            }
            var results = [];
            for(var i = 0; i < this.limit; i++){
                r = re.exec(this.category_search_string[category_id]);
                if(r){
                    var id = Number(r[1]);
                    results.push(this.get_product_by_id(id));
                }else{
                    break;
                }
            }
            return results;
        },
        add_order: function(order){
            var order_id = order.uid;
            var orders  = this.load('orders',[]);

            // if the order was already stored, we overwrite its data
            for(var i = 0, len = orders.length; i < len; i++){
                if(orders[i].id === order_id){
                    orders[i].data = order;
                    this.save('orders',orders);
                    return order_id;
                }
            }

            orders.push({id: order_id, data: order});
            this.save('orders',orders);
            return order_id;
        },
        remove_order: function(order_id){
            var orders = this.load('orders',[]);
            orders = _.filter(orders, function(order){
                return order.id !== order_id;
            });
            this.save('orders',orders);
        },
        remove_all_orders: function(){
            this.save('orders',[]);
        },
        get_orders: function(){
            return this.load('orders',[]);
        },
        get_order: function(order_id){
            var orders = this.get_orders();
            for(var i = 0, len = orders.length; i < len; i++){
                if(orders[i].id === order_id){
                    return orders[i];
                }
            }
            return undefined;
        },
    });
    //-------------------- END - Extension of search function eq_internal_number --------------------------------------//    
    
    
    
    
    
    
    
    
    
   
    instance.point_of_sale.ProductScreenWidget = instance.point_of_sale.ProductScreenWidget.extend({
        init: function() {
            this._super.apply(this, arguments);
        },
        start:function(){
            var self = this;

            self.product_list_widget = new instance.point_of_sale.ProductListWidget(this,{
                click_product_action: function(product){
                    if(product.to_weight && self.pos.config.iface_electronic_scale){
                        self.pos_widget.screen_selector.set_current_screen('scale',{product: product});
                    }else{
                        self.pos.get('selectedOrder').addProduct(product);
                    }
                },
                product_list: this.pos.db.get_product_by_category(0)
            });
            self.product_list_widget.replace(this.$('.placeholder-ProductListWidget'));

            this.product_categories_widget = new instance.point_of_sale.ProductCategoriesWidget(this,{
                product_list_widget: this.product_list_widget,
            });
            this.product_categories_widget.replace(this.$('.placeholder-ProductCategoriesWidget'));
            pos = self.pos;
            selectedOrder = self.pos.get('selectedOrder');
            $('#return_order_ref').html('');
            pos = pos;
            
            // Return Order
            
            $("span#return_order").click(function() {
//                var self = this;
                selectedOrder = pos.get('selectedOrder');
                $("span#return_order").css('background', 'blue');
                $("span#sale_mode").css('background', '');
                $("span#missing_return_order").css('background', '');
                $('div.order').css('background', '#fde1fc');
                dialog = new instance.web.Dialog(this, {
                    title: _t("Return Order"),
                    size: 'medium',
                    buttons: [
                        {text: _t("Validate"), click: function() {
                            var ret_o_ref = dialog.$el.find("input#return_order_number").val();
                            var bonus_return_check = dialog.$el.find("input#bonus_return").is(':checked');
                            if (ret_o_ref.indexOf('Verkauf') == -1) {
                                ret_o_ref = 'Verkauf ' + ret_o_ref.toString();
                            }
                            if (ret_o_ref.length > 0) {
                                var close_dialog = false;
                                new instance.web.Model("pos.order").get_func("search_read")
                                            ([['pos_reference', '=', ret_o_ref],['parent_return_order', 'ilike', '']], 
                                            ['id', 'pos_reference', 'partner_id']).pipe(
                                    function(result) {
                                        if (result && result.length == 1) {
                                            new instance.web.Model("pos.order.line").get_func("search_read")
                                                    ([['order_id', '=', result[0].id],['return_qty', '>', 0]], []).pipe(
                                            function(res) {
                                                if (res) {
                                                    products = [];
                                                    _.each(res,function(r) {
                                                        product = pos.db.get_product_by_id(r.product_id[0]);
                                                        products.push(product)
                                                    });
                                                    self.product_list_widget.set_product_list(products);
                                                }
                                            });
                                            selectedOrder.set_ret_o_id(result[0].id);
                                            selectedOrder.set_ret_o_ref(result[0].pos_reference);
                                            selectedOrder.set_bonus_return_check(bonus_return_check);
                                            $('#return_order_ref').html(result[0].pos_reference);
                                            if (result[0].partner_id) {
                                                var partner = pos.db.get_partner_by_id(result[0].partner_id[0]);
                                                selectedOrder.set_client(partner);
                                            }
                                        } else {
                                            var error_str = _t('Please enter correct reference number !');
                                            var error_dialog = new instance.web.Dialog(this, { 
                                                size: 'medium',
                                                buttons: [{text: _t("Close"), click: function() { this.parents('.modal').modal('hide'); }}],
                                            }).open();
                                            error_dialog.$el.append(
                                                '<span id="error_str" style="font-size:16px;">' + error_str + '</span>');
                                        }
                                    }
                                );
                                if (!dialog.$el.find("input[id=return_checked]").is(':checked')) {
                                    alert(_t('Convert to bonus or not ?'));
                                    close_dialog = false;
                                    return;
                                } else {
                                    close_dialog = true;
                                    if (close_dialog) {
                                        this.parents('.modal').modal('hide');
                                    }
                                }
                            } else {
                                var error_str =_t('Please enter correct reference number !');
                                var error_dialog = new instance.web.Dialog(this, { 
                                    size: 'medium',
                                    buttons: [{text: _t("Close"), click: function() { this.parents('.modal').modal('hide'); }}],
                                }).open();
                                error_dialog.$el.append(
                                    '<span id="error_str" style="font-size:18px;">' + error_str + '</span>');
                            }
                        }},
                        {text: _t("Cancel"), click: function() { 
                            $("span#return_order").css('background', '');
                            $("span#sale_mode").css('background', 'blue');
                            $("span#missing_return_order").css('background', '');
                            $('div.order').css('background', '');
                            this.parents('.modal').modal('hide'); 
                        }}
                    ]
                }).open();
                dialog.$el.html(QWeb.render("pos-return-order", self));
                dialog.$el.find("input#return_order_number").focus();
                dialog.$el.find("button.bonus_return_required").click(function(ev) {
                    if ($(ev.target).attr('id') == 'yes_return_bonus') {
                        dialog.$el.find('#yes_return_bonus').attr('style', 'background: #00704a; !important;color: #FFF;');
                        dialog.$el.find('#no_return_bonus').attr('style', 'background: #e3e3e3; !important;color: #4c4c4c;');
                        dialog.$el.find("input[id=bonus_return]").prop('checked', true);
                        dialog.$el.find("input[id=return_checked]").prop('checked', true);
                    } else {
                        dialog.$el.find('#no_return_bonus').attr('style', 'background: #00704a; !important;color: #FFF;');
                        dialog.$el.find('#yes_return_bonus').attr('style', 'background: #e3e3e3; !important;color: #4c4c4c;');
                        dialog.$el.find("input[id=bonus_return]").prop('checked', false);
                        dialog.$el.find("input[id=return_checked]").prop('checked', true);
                    }
                });
            });
            
            $("span#sale_mode").click(function(event) {
                var selectedOrder = pos.get('selectedOrder');
                if (selectedOrder.get_order_id()) {
                    alert (_t('Please click on Clear Order button to continue !'));
                    return;
                }
                var id = $(event.target).data("category-id");
                selectedOrder.set_ret_o_id('');
                var category = pos.db.get_category_by_id(id);
                self.product_categories_widget.set_category(category);
                self.product_categories_widget.renderElement();
                
                currentOrderLines = selectedOrder.get('orderLines');
                for (i=0; i <= currentOrderLines.length + 1; i++) {
                    (currentOrderLines).each(_.bind( function(item) {
                        selectedOrder.removeOrderline(item);
                    }, this));
                }
                
                $("span#sale_mode").css('background', 'blue');
                $("span#return_order").css('background', '');
                $("span#missing_return_order").css('background', '');
                $('div.order').css('background', '');
                selectedOrder.set_ret_o_ref('');
                $('#return_order_ref').html('');
            });
            
            $("span#missing_return_order").click(function(event) {
                var selectedOrder = pos.get('selectedOrder');
                if (selectedOrder.get_order_id()) {
                    alert (_t('Please click on Clear Order button to continue !'));
                    return;
                }
                var id = $(event.target).data("category-id");
                selectedOrder.set_ret_o_id(_t('Missing Receipt'));
                var category = pos.db.get_category_by_id(id);
                self.product_categories_widget.set_category(category);
                self.product_categories_widget.renderElement();
                
                $("span#sale_mode").css('background', '');
                $("span#return_order").css('background', '');
                $("span#missing_return_order").css('background', 'blue');
                selectedOrder.set_ret_o_ref(_t('Missing Receipt'));
                $('#return_order_ref').html(_t('Missing Receipt'));
                $('div.order').css('background', '#fde1fc');
            });
            
            var fetch = function(model, fields, domain, ctx){
                this._load_progress = (this._load_progress || 0) + 0.05; 
                self.pos_widget.loading_message(_t('Loading')+' '+model,this._load_progress);
                return new instance.web.Model(model).query(fields).filter(domain).context(ctx).all()
            }
            
            $("#create_coupon").click(function() {
                selectedOrder = pos.get('selectedOrder');
                if (!selectedOrder.get_coupon_id() && !selectedOrder.get_recharge_coupon_id()) {
                    new instance.web.Model("pos.coupon").get_func("create")
                        ({
                            'name': _t('Coupon'),

                        }).done(function(result) {
                            if (result) {
                                $('#coupon_name').html(_t('Coupon Created'));
                                selectedOrder.set_coupon(coupon_name);
                                selectedOrder.set_coupon_id(result);
                                var products1 = fetch(
                                    'product.product', 
                                    ['id', 'name', 'list_price','price','pos_categ_id','product_brand_id','product_season_id', 'categ_id', 'taxes_id', 'ean13', 'default_code', 
                                    'qty_available', 'disc_price', 'description_sale', 'uom_id', 'uos_id', 'uos_coeff', 'mes_type', 'description', 'variants', 'is_coupon', 'is_card'],
                                    [['is_coupon','=',true],['available_in_pos','=',true]],
                                    {pricelist: pos.pricelist.id} // context for price
                                ).then(function(products1){
                                    products = [];
                                    _.each(products1,function(r) {
                                        product = pos.db.get_product_by_id(r.id);
                                        products.push(product)
                                    });
                                    self.product_list_widget.set_product_list(products);
                                });
                            }
                        });
                    } else {
                        alert (_t('Coupon is already created !'));
                    }
                }
            );
            
            $("#show_bonus_coupons").click(function() {
                var connection = false;
                new instance.web.Model("pos.order").get_func("check_connection")().done(function(result) {
                    if (result) {
                        selectedOrder = pos.get('selectedOrder');
                        var self = this;
                        var today = new Date();
                        var dd = (today.getDate()).toString();
                        var mm = (today.getMonth()+1).toString();
                        var yyyy = today.getFullYear().toString();
                        
                        new instance.web.Model("bonus.return").get_func("search_read")
                            ([['bonus_remaining_amt', '>', 0.0]]).pipe(
                            function(result) {
                                initial_ids = _.map(result, function(x) {return x['id']});
                                var pop = new instance.web.form.SelectCreatePopup(this);
                                pop.select_element(
                                    'bonus.return',
                                    {
                                        title: 'Bonus Coupon', 
                                        initial_ids: initial_ids, 
                                        initial_view: 'search',
                                        disable_multiple_selection: true,
                                        no_create: true
                                    }, [], new instance.web.CompoundContext({}));
                            }
                        );
                    }
                }).fail(function(result, ev) {
                    ev.preventDefault();
                    connection = false;
                    return
                });
            });

            $("#show_coupons").click(function() {
                var connection = false;
                new instance.web.Model("pos.order").get_func("check_connection")().done(function(result) {
                    if (result) {
                        selectedOrder = pos.get('selectedOrder');
                        var self = this;
                        var today = new Date();
                        var dd = (today.getDate()).toString();
                        var mm = (today.getMonth()+1).toString();
                        var yyyy = today.getFullYear().toString();
                        
                        new instance.web.Model("pos.coupon.line").get_func("search_read")
                            ([['remaining_amt', '>', 0.0], ['date_expiry_line', '>', yyyy + '-' + mm + '-' + dd]]).pipe(
                            function(result) {
                                initial_ids = _.map(result, function(x) {return x['id']});
                                var pop = new instance.web.form.SelectCreatePopup(this);
                                pop.select_element(
                                    'pos.coupon.line',
                                    {
                                        title: _t('Coupon History'), 

                                        initial_ids: initial_ids, 
                                        initial_view: 'search',
                                        disable_multiple_selection: true,
                                        no_create: true
                                    }, [], new instance.web.CompoundContext({}));
                            }
                        );
                    }
                }).fail(function(result, ev) {
                    ev.preventDefault();
                    connection = false;
                    return
                });
            });
            
            $("#recharge_coupon").click(function() {
                var connection = false;
                selectedOrder = pos.get('selectedOrder');
                if (!selectedOrder.get_coupon_id()) {
                    new instance.web.Model("pos.order").get_func("check_connection")().done(function(result) {
                        if (result) {
                            selectedOrder = pos.get('selectedOrder');
//                            var today = new Date();
//                            var dd = (today.getDate()).toString();
//                            var mm = (today.getMonth()+1).toString();
//                            var yyyy = today.getFullYear().toString();
                            
                            new instance.web.Model("pos.coupon.line").get_func("search_read")
                                ([]).pipe(
                                function(result) {
                                    initial_ids = _.map(result, function(x) {return x['id']});
                                    var pop = new instance.web.form.SelectCreatePopup(this);
                                    pop.select_element(
                                        'pos.coupon.line',
                                        {
                                            title: _t('Select coupon to recharge'), 

                                            initial_ids: initial_ids, 
                                            initial_view: 'search',
                                            disable_multiple_selection: true,
                                            no_create: true
                                        }, [], new instance.web.CompoundContext({}));
                                pop.on("elements_selected", self, function(element_ids) {
                                    var dataset = new instance.web.DataSetStatic(self, 'pos.coupon.line', {});
                                    dataset.name_get(element_ids).done(function(data) {
                                        if (data[0][0]) {
                                            selectedOrder.set_recharge_coupon_line_id(data[0][0]);
                                            selectedOrder.set_recharge_coupon_serial(data[0][1]);
                                            new instance.web.Model("pos.coupon.line").get_func("search_read")
                                                ([['id', '=', data[0][0]]]).pipe(
                                                function(res) {
                                                    if (res && res[0]) {
                                                        $('#coupon_name').html(data[0][1] + _t(' Coupon selected'));
                                                        selectedOrder.set_recharge_coupon_id(res[0].coupon_id[0]);
                                                        selectedOrder.set_remaining_coupon_amt(res[0].remaining_amt);
                                                        var products1 = fetch(
                                                            'product.product', 
                                                            ['id', 'name', 'list_price','price','pos_categ_id','product_brand_id','product_season_id', 'categ_id', 'taxes_id', 'ean13', 'default_code', 
                                                            'qty_available', 'disc_price', 'description_sale', 'uom_id', 'uos_id', 'uos_coeff', 'mes_type', 'description', 'variants', 'is_coupon', 'is_card'],
                                                            [['is_coupon','=',true],['id', '=', res[0].product_id[0]],['available_in_pos','=',true]],
                                                            {pricelist: pos.pricelist.id} // context for price
                                                        ).then(function(products1){
                                                            products = [];
                                                            _.each(products1,function(r) {
                                                                product = pos.db.get_product_by_id(r.id);
                                                                products.push(product)
                                                            });
                                                            self.product_list_widget.set_product_list(products);
                                                        });
                                                    }
                                                }
                                            );
                                        }
                                    });
                                });
                            });
                        }
                    }).fail(function(result, ev) {
                        ev.preventDefault();
                        connection = false;
                        return
                    });
                } else {
                    alert (_t('Coupon is already created !'));
                }
            });
        },
    });

    instance.point_of_sale.ReceiptScreenWidget.include({
    	wait: function( callback, seconds){
            return window.setTimeout( callback, seconds * 1000 );
        },
        show: function(){
            this._super();
            var self = this;
            var barcode_val = this.pos.get('selectedOrder').getName();
            if (barcode_val.indexOf('Verkauf') != -1) {
                var vals = barcode_val.split('Verkauf ');
                if (vals) {
                    barcode = vals[1];
                    $("tr#barcode1").html($("<td style='padding:2px 2px 2px 0px; text-align:center;'><div style='margin: 0 -10px;' class='" + barcode + "' width='150' height='50'/></td>"));
                    $("tr#barcode1_number").html($("<td style='padding:2px 2px 2px 0px; text-align:center;'>" + _t("Barcode:") + barcode + "</td>"));
                    $("." + barcode.toString()).barcode(barcode.toString(), "code128");
                }
            }
        },
        print: function() {
        	if (!this.pos.get('selectedOrder')._printed) {
        		this.wait( function(){ 
        			this.pos.get('selectedOrder')._printed = true;
        			window.print(); 
        		}, 2);
        	} else {
                this.pos.get('selectedOrder')._printed = true;
                window.print();
        	}
        },
        finishOrder: function() {
            this.pos.get('selectedOrder').set_ret_o_id('')
            this.pos.get('selectedOrder').destroy();
            $("span#sale_mode").css('background', 'blue');
            $("span#return_order").css('background', '');
            $("span#missing_return_order").css('background', '');
            $('#return_order_ref').html('');
            $('#return_order_number').val('');
            $('#coupon_name').html('');
        }
    });
    
    instance.point_of_sale.UsernameWidget = instance.point_of_sale.UsernameWidget.extend({
    	refresh: function(){
            this.renderElement();
            $('.username').click(function() {
            	var search_view = new instance.web.SearchView();
            	
                new instance.web.Model("res.users").get_func("search_read")([], ['id']).pipe(
                    function(result) {
                        initial_ids = _.map(result, function(x) {return x['id']});
                        var pop = new instance.web.form.SelectCreatePopup(this);
                        pop.select_element(
                            'res.users',
                            {
                                title: _t('Salesman'), 

                                initial_ids: initial_ids, 
                                initial_view: 'search',
                                disable_multiple_selection: true,
                                no_create: true
                            }, [], new instance.web.CompoundContext({}));
                        pop.on("elements_selected", self, function(element_ids) {
                            var dataset = new instance.web.DataSetStatic(self, 'res.users', {});
                            dataset.name_get(element_ids).done(function(data) {
                                if (data && data[0]) {
                                	dialog = new instance.web.Dialog(this, {
					                    title: _t(data[0][1]),
					                    size: 'medium',
					                    buttons: [
					                        {text: _t("Validate"), click: function() {
					                            var user_password = dialog.$el.find("input#user_password").val();
					                            if (user_password.length > 0) {
                                                    new instance.web.Model("pos.order").get_func("check_pwd")(data[0][0], user_password).pipe(
                                                        function(res) {
                                                        	if (res) {
                                                        		if (!self.pos.cashier) {
                                                        			self.pos.cashier = {};
                                                        			self.pos.cashier['id'] = data[0][0];
                                                        			self.pos.cashier['name'] = data[0][1];
                                                        			$('span.username').html(data[0][1]);
                                                        		} else {
                                                                    self.pos.cashier['id'] = data[0][0];
                                                                    self.pos.cashier['name'] = data[0][1];
                                                                    $('span.username').html(data[0][1]);
                                                        		}
                                                        		dialog.$el.modal('hide');
                                                        	} else {
                                                        		alert (_t('Invalid Password !'));

                                                        	}
                                                        });
					                            } else {
					                                var error_str =_t('Please enter correct password !');
					                                var error_dialog = new instance.web.Dialog(this, { 
					                                    width: 'medium',
					                                    buttons: [{text: _t("Close"), click: function() { this.parents('.modal').modal('hide'); }}],
					                                }).open();
					                                error_dialog.$el.append(
					                                    '<span id="error_str" style="font-size:18px;">' + error_str + '</span>');
					                            }
					                        }},
					                        {text: _t("Cancel"), click: function() { 
					                            this.parents('.modal').modal('hide'); 
					                        }}
					                    ]
					                }).open();
					                dialog.$el.html(QWeb.render("salesman-password", self));
					                dialog.$el.find("input#user_password").focus();
                                }
                            });
                        });
                    }
                );
            });
        },
    });
    
    var orderline_id = 1;
    
    instance.point_of_sale.Orderline = instance.point_of_sale.Orderline.extend({
        initialize: function(attr,options){
            this.pos = options.pos;
            this.order = options.order;
            this.product = options.product;
            this.price   = options.product.price;
            this.quantity = 1;
            this.quantityStr = '1';
            this.discount = 0;
            this.discountStr = '0';
            this.type = 'unit';
            this.selected = false;
            this.id       = orderline_id++;
            this.oid = null;
            this.history_id = null;
            
            this.coupon_serial = null;
        },
        
        set_coupon_serial: function(coupon_serial) {
            this.set('coupon_serial', coupon_serial)
        },
        get_coupon_serial: function() {
            return this.get('coupon_serial');
        },
        
        set_coupon_history_id: function(history_id){
        	this.set('history_id', history_id);
        },
        get_coupon_history_id: function() {
        	return this.get('history_id');
        },
        
        set_quantity: function(quantity){
            if(quantity === 'remove'){
                this.set_oid('');
                this.pos.get('selectedOrder').removeOrderline(this);
                return;
            }else{
                var quant = parseFloat(quantity) || 0;
                var unit = this.get_unit();
                if(unit){
                    this.quantity    = round_pr(quant, unit.rounding);
                    this.quantityStr = this.quantity.toFixed(Math.ceil(Math.log(1.0 / unit.rounding) / Math.log(10)));
                }else{
                    this.quantity    = quant;
                    this.quantityStr = '' + this.quantity;
                }
            }
            this.trigger('change',this);
        },
        export_as_JSON: function() {
            var self = this;
            var oid = this.get_oid();
            var qty = this.get_quantity();
            var return_process = false;
            if (oid) {
                return_process = true;
            } else {
                var return_qty = this.get_quantity();
            }
            var order_ref = this.pos.get('selectedOrder').get_ret_o_id();
            if (order_ref) {
                qty = this.get_quantity() * -1;
            }
            return {
                qty: qty,
                return_process: return_process,
                return_qty: parseInt(return_qty),
                price_unit: this.get_unit_price(),
                discount: this.get_discount(),
                product_id: this.get_product().id,
            };
        },
      //used to create a json of the ticket, to be sent to the printer
        export_for_printing: function(){
            return {
                quantity:           this.get_quantity(),
                unit_name:          this.get_unit().name,
                price:              this.get_unit_price(),
                discount:           this.get_discount(),
                product_name:       this.get_product().display_name,
                price_display :     this.get_display_price(),
                price_with_tax :    this.get_price_with_tax(),
                price_without_tax:  this.get_price_without_tax(),
                tax:                this.get_tax(),
                product_description:      this.get_product().description,
                product_description_sale: this.get_product().description_sale,
                coupon_serial: this.get_coupon_serial(),
            };
        },
        set_oid: function(oid) {
            this.set('oid', oid)
        },
        get_oid: function() {
            return this.get('oid');
        },
    });

    // EQ: our custom coupon class holding all important data
    var eq_coupon_data = {
    		serial_number: 0,
    		name: "",
    		price: 0.0,
    		currency: "",
    		quantity: 0
    };
    
    instance.point_of_sale.Order = instance.point_of_sale.Order.extend({
        initialize: function(attributes){
            Backbone.Model.prototype.initialize.apply(this, arguments);
            this.pos = attributes.pos; 
            this.sequence_number = this.pos.pos_session.sequence_number++;
            this.uid =     this.generateUniqueId_barcode();     //this.generateUniqueId();
            this.set({
                creationDate:   new Date(),
                orderLines:     new instance.point_of_sale.OrderlineCollection(),
                paymentLines:   new instance.point_of_sale.PaymentlineCollection(),
                name:           _t("Order ") + this.uid, 
                client:         null,
                ret_o_id:       null,
                ret_o_ref:      null,
                
                coupon:                 null,
                coupon_id:              null,
                coupon_amount:          0.0,
                recharge_coupon_serial: null,
                recharge_coupon_line_id:null,
                recharge_coupon_id:     null,
                remaining_coupon_amt:   0.0,
                remaining_validity_days:0,
                
                bonus_return_amount:    0.0,
                bonus_return:           null,
                bonus_name:				null,                
            });
            this.selected_orderline   = undefined;
            this.selected_paymentline = undefined;
            this.screen_data = {};  // see ScreenSelector
            this.receipt_type = 'receipt';  // 'receipt' || 'invoice'
            this.temporary = attributes.temporary || false;
            this.gift_coupon = [];
            this.bonus_coupon = [];
            this.gift_coupon_price = [];            
            this.eq_gift_coupon = [];								// Gutschein
            this.eq_bonus_coupon = [];								// Rückgabegutschein
            
            return this;
        },
        
        generateUniqueId_barcode: function() {
        	// return last 10 digits
        	var code = new Date().getTime().toString();
        	var digit = code.length - 10;
        	var res = code.substring(code.length+1, digit);
            return res;
        },
        set_coupon_amount: function(coupon_amount) {
            this.set('coupon_amount', coupon_amount)
        },
        get_coupon_amount: function() {
            return this.get('coupon_amount');
        },
        set_coupon_id: function(coupon_id) {
            this.set('coupon_id', coupon_id)
        },
        get_coupon_id: function(){
            return this.get('coupon_id');
        },
        set_recharge_coupon_id: function(recharge_coupon_id) {
            this.set('recharge_coupon_id', recharge_coupon_id)
        },
        get_recharge_coupon_id: function() {
            return this.get('recharge_coupon_id')
        },
        set_recharge_coupon_line_id: function(recharge_coupon_line_id) {
            this.set('recharge_coupon_line_id', recharge_coupon_line_id);
        },
        get_recharge_coupon_line_id: function() {
            return this.get('recharge_coupon_line_id');
        },
        set_recharge_coupon_serial: function(recharge_coupon_serial) {
            this.set('recharge_coupon_serial', recharge_coupon_serial);
        },
        get_recharge_coupon_serial: function() {
            return this.get('recharge_coupon_serial');
        },
        set_remaining_coupon_amt: function(remaining_coupon_amt) {
        	this.set('remaining_coupon_amt', remaining_coupon_amt);
        },
        get_remaining_coupon_amt: function() {
            return this.get('remaining_coupon_amt');
        },
        set_remaining_validity_days: function(remaining_validity_days) {
        	this.set('remaining_validity_days', remaining_validity_days);
        },
        get_remaining_validity_days: function() {
        	return this.get('remaining_validity_days');
        },
        set_coupon: function(coupon) {
            this.set('coupon', coupon)
        },
        get_coupon: function(){
            var coupon = this.get('coupon');
            return coupon ? coupon : "";
        },
        setCpnAmt: function(cpn_amt) {
            this.set('cpn_amt', cpn_amt)
        },
        getCpnAmt: function() {
            return this.get('cpn_amt');
        },
        set_add_gift_coupon: function(gift_coupon) {        
        	this.gift_coupon.push(gift_coupon);        	        
        },
        get_add_gift_coupon: function() {
        	return this.gift_coupon;
        },
        
        // EQUIATNIA - Gutschein
        eq_set_add_gift_coupon: function(gift_coupon, price) {        
        	var eq_data = Object.create(eq_coupon_data);
        	eq_data.serial_number = gift_coupon;
        	eq_data.price = price;
        	
        	this.eq_gift_coupon.push(eq_data);
        },
        eq_get_add_gift_coupon: function() {
        	return this.eq_gift_coupon;
        },
               
        set_add_bonus_coupon: function(bonus_coupon) {
        	this.bonus_coupon.push(bonus_coupon);
        },
        get_add_bonus_coupon: function() {
        	return this.bonus_coupon;
        },
        
        // EQUITANIA - Rückgabegutschein
        eq_set_add_bonus_coupon: function(bonus_coupon, price) {
        	var eq_data = Object.create(eq_coupon_data);
        	eq_data.serial_number = bonus_coupon;
        	eq_data.price = price;
        	
        	this.eq_bonus_coupon.push(eq_data);
        },
        eq_get_add_bonus_coupon: function() {
        	return this.eq_bonus_coupon;
        },
        
        
        
        
        getChange: function() {
            if (this.getCpnAmt() > 0.0) {
                change = this.getPaidTotal() - this.getTotalTaxIncluded();
                return parseFloat(this.getCpnAmt()) + parseFloat(change.toFixed(2));
            } else {
                return this.getPaidTotal() - this.getTotalTaxIncluded();
            }
        },
        
        // Return Order
        
        set_ret_o_id: function(ret_o_id) {
            this.set('ret_o_id', ret_o_id)
        },
        get_ret_o_id: function(){
            return this.get('ret_o_id');
        },
        get_order_id: function(){
            return this.get('order_id');
        },
        set_ret_o_ref: function(ret_o_ref) {
            this.set('ret_o_ref', ret_o_ref)
        },
        get_ret_o_ref: function(){
            return this.get('ret_o_ref');
        },
        set_bonus_return_check: function(bonus_return) {
            this.set('bonus_return', bonus_return);
        },
        get_bonus_return_check: function() {
            return this.get('bonus_return');
        },
        set_bonus_return_amount: function(bonus_return_amount) {
            this.set('bonus_return_amount', bonus_return_amount)
        },
        get_bonus_return_amount: function() {
            return this.get('bonus_return_amount');
        },
        set_bonus_name: function(bonus_name) {
            this.set('bonus_name', bonus_name)
        },
        get_bonus_name: function() {
            return this.get('bonus_name');
        },
        getName: function() {
        	// one time only but only 10 digit
            return this.get('name');
        },
        addProduct: function(product, options){
            options = options || {};
            var attr = JSON.parse(JSON.stringify(product));
            attr.pos = this.pos;
            attr.order = this;
            
            if (attr.is_coupon && $('#coupon_name').html().length == 0) {
                alert (_t('Please click on Create Coupon Button !'));
                return;
            }
            
            if (this.pos.get('selectedOrder').get_recharge_coupon_line_id()) {
            	currentOrderLines = this.pos.get('selectedOrder').get('orderLines');
                orderLines = [];
                (currentOrderLines).each(_.bind( function(item) {
                    return orderLines.push(item.export_as_JSON());
                }, this));
                if (orderLines.length >= 1) {
                    return alert (_t('Please select only one product coupon !'));
                }
            }
            
            var retoid = this.pos.get('selectedOrder').get_ret_o_id();
            if (retoid && retoid.toString() != _t('Missing Receipt')) {
                var pids = [];
                new instance.web.Model("pos.order.line").get_func("search_read")
                                    ([['order_id', '=', retoid],['product_id', '=', attr.id],['return_qty', '>', 0]], 
                                    ['return_qty', 'id', 'price_unit', 'discount']).pipe(
                    function(result) {
                        if (result && result.length > 0) {
                            if (result[0].return_qty > 0) {
                                add_prod = true;
                                (attr.order.get('orderLines')).each(_.bind( function(item) {
                                    if (attr.id == item.get_product().id && 
                                        result[0].return_qty <= item.quantity) {
                                        var error_str = _t('Can not return more products !');
                                        var error_dialog = new instance.web.Dialog(this, { 
                                            size: 'medium',
                                            buttons: [{text: _t("Close"), click: function() { this.parents('.modal').modal('hide'); }}],
                                        }).open();
                                        error_dialog.$el.append(
                                            '<span id="error_str" style="font-size:18px;">' + error_str + '</span>');
                                        add_prod = false;
                                    }
                                }, self));
                                
                                if (add_prod) {
                                    var line = new instance.point_of_sale.Orderline({}, {pos: attr.pos, order: this, product: product});
                                    line.set_oid(retoid);
                                    
                                    if (result[0].discount) {
                                        line.set_discount(result[0].discount);
                                    }
                                    
                                    if(options.quantity !== undefined){
                                        line.set_quantity(options.quantity);
                                    }
                                    if(options.price !== undefined){
                                        line.set_unit_price(result[0].price_unit);
                                    }
                                    line.set_unit_price(result[0].price_unit);
                                    var last_orderline = attr.order.getLastOrderline();
                                    if( last_orderline && last_orderline.can_be_merged_with(line) && options.merge !== false){
                                        last_orderline.merge(line);
                                    }else{
                                        attr.order.get('orderLines').add(line);
                                    }
                                    attr.order.selectLine(attr.order.getLastOrderline());
                                }
                            } else {
                                var error_str = _t('Please check quantity of selected product & sold product !');
                                var error_dialog = new instance.web.Dialog(this, { 
                                    size: 'medium',
                                    buttons: [{text: _t("Close"), click: function() { this.parents('.modal').modal('hide'); }}],
                                }).open();
                                error_dialog.$el.append(
                                    '<span id="error_str" style="font-size:18px;">' + error_str + '</span>');
                                return;
                            }
                    } else {
                        var error_str = _t('Product is not in order list !');
                        var error_dialog = new instance.web.Dialog(this, { 
                            size: 'medium',
                            buttons: [{text: _t("Close"), click: function() { this.parents('.modal').modal('hide'); }}],
                        }).open();
                        error_dialog.$el.append(
                            '<span id="error_str" style="font-size:18px;">' + error_str + '</span>');
                    }
                });
            } else {
                var line = new instance.point_of_sale.Orderline({}, {pos: attr.pos, order: self, product: product});
                if (retoid && retoid.toString() != _t('Missing Receipt')) {
                    line.set_oid(retoid);
                }
                if(options.quantity !== undefined){
                    line.set_quantity(options.quantity);
                }
                if(options.price !== undefined){
                    line.set_unit_price(options.price);
                }
                if(options.discount !== undefined){
                    line.set_discount(options.discount);
                }
                var last_orderline = this.getLastOrderline();
                if( last_orderline && last_orderline.can_be_merged_with(line) && options.merge !== false){
                    last_orderline.merge(line);
                }else{
                    this.get('orderLines').add(line);
                }
                this.selectLine(this.getLastOrderline());
            }
        },
        // exports a JSON for receipt printing
        export_for_printing: function(){
            var orderlines = [];
            this.get('orderLines').each(function(orderline){
                orderlines.push(orderline.export_for_printing());
            });            
            var paymentlines = [];
            this.get('paymentLines').each(function(paymentline){            	            	
            	payment_record = paymentline.export_for_printing();
            	payment_record.symbol = paymentline.pos.currency.symbol;
            	paymentlines.push(payment_record);
            	
                //paymentlines.push(paymentline.export_for_printing());		// DEFAULT
            });
            var client  = this.get('client');
            var cashier = this.pos.cashier || this.pos.user;
            var company = this.pos.company;
            var shop    = this.pos.shop;
            var date = new Date();
            
            var barcode_val = this.pos.get('selectedOrder').getName();
            var barcode = '';
            var barcode_src = '';
            
            if (barcode_val.indexOf('Verkauf') != -1) {
                var vals = barcode_val.split('Verkauf ');
                if (vals) {
                    barcode = vals[1];
                }
            }
            return {
                orderlines: orderlines,
                paymentlines: paymentlines,
                subtotal: this.getSubtotal(),
                total_with_tax: this.getTotalTaxIncluded(),
                total_without_tax: this.getTotalTaxExcluded(),
                total_tax: this.getTax(),
                total_paid: this.getPaidTotal(),
                total_discount: this.getDiscountTotal(),
                tax_details: this.getTaxDetails(),
                change: this.getChange(),
                name : this.getName(),
                client: client ? client.name : null ,
                invoice_id: null,   //TODO
                cashier: cashier ? cashier.name : null,
                header: this.pos.config.receipt_header || '',
                footer: this.pos.config.receipt_footer || '',
                precision: {
                    price: 2,
                    money: 2,
                    quantity: 3,
                },
                date: { 
                    year: date.getFullYear(), 
                    month: date.getMonth(), 
                    date: date.getDate(),       // day of the month 
                    day: date.getDay(),         // day of the week 
                    hour: date.getHours(), 
                    minute: date.getMinutes() ,
                    isostring: date.toISOString(),
                    localestring: date.toLocaleString(),
                }, 
                company:{
                    email: company.email,
                    website: company.website,
                    company_registry: company.company_registry,
                    contact_address: company.partner_id[1], 
                    vat: company.vat,
                    name: company.name,
                    phone: company.phone,
                    logo:  this.pos.company_logo_base64,
                },
                shop:{
                    name: shop.name,
                },
                currency: this.pos.currency,
                order_barcode: barcode.toString(),
                ret_o_id: this.get_ret_o_id(),
                bonus_name: this.get_bonus_name(),
                add_gift_coupon: this.get_add_gift_coupon(),
                eq_add_gift_coupon: this.eq_get_add_gift_coupon(),
                add_bonus_coupon: this.get_add_bonus_coupon(),
                eq_add_bonus_coupon: this.eq_get_add_bonus_coupon(),
//                barcode_src: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAANwAAAAoCAIAAAAaOwPZAAAPwklEQVR4nO2ceVRTxxrAJyEbhMgWwiJYMO7SnIBSCWIZ3BCqcopIBEVASg9S7YJLo1Dbaim21dpWaa09dTuiiAdbpNpqj3otIEKFIi6ACycJGEQBiSQsIWTeH3N6330h+qwVmvfO/f115/tm+3K/3PnuzJ0B6K9z6NAhCGFeXh5CaMeOHRDCM2fOIIQyMzMhhNXV1Wb5o6OjIYQQwrCwMFLY2toKIUxKSiIllZWV8E+2bt1Kyg8ePAghPHLkCELo888/h/9JTU0NQig1NRUOYtasWQghrVYLIZTL5QihO3fuQAhXrVpl0a6CggII4d69ey1qFQoFhPDKlSsIoZSUFAihRqNBCEVFRUEIDQaDwWCAEEZFRSGENBqNWWcUCgVZVXFxMYTw66+/Rgjt3bsXQlhQUGDW3Pr16yGEV69eJSVyuRxCqNVqqdk6OjoghEuXLiUlNTU1EMINGzaQkqKiIgjh7t27zZrYunUrhJAgCIv2xsbGQgi7uroQQmFhYfPmzSNVarXazLrMzEyE0JkzZyCEO3bsQAjl5eVBCA8dOmSx8ifDAn8dlUpFEER4eDgA4NatWwRBrFixAgBw7do1giA6OzvN8peXl7e0tAAAmEwmKezr6yMIYvLkyaTk4cOHBEHga19fX7PmIiMjAQA3b94k82Bwc1VVVdXV1WbtstlsAIDRaCQIwsfHBwCg1+sJgujv77doV3NzM0EQL7/8skVtbW0tQRBarRYAcPny5StXrvT09AAAysrK2traTCYTAIAgCKFQCADo6ekx66ednR15rdFoCIKYMmUKAECpVBIEsXDhwic0h6moqFAqlUajkZrNYDAQBDFmzBjqD0IQhEAgMGsuMDDQrImGhgaCINra2izaW15e3tTUhJu7cOGCra0tqRpsnYODAwDg3r17BEFMmjQJAKBWqwmCmDNnjsXKnwzzv2ehoRleaKeksTpop6SxOminpLE6aKeksTpop6SxOminpLE6aKeksTpop6SxOminpLE6aKeksTpop6SxOminpLE6aKeksTpop6SxOminpLE6aKeksTpop6SxOp5lO8TjWLRo0cSJE0eNGmUmX7VqVVdXFwCAwWCQQoFAoFAoRCIRKfH19VUoFPgabxXABAcHKxSKadOmAQDCw8MdHR2plXt7ewMAkpKS5s6da9Yu3n3B4/EUCgUu5erqqlAoXnjhBYv9DwwMVCgUM2bMsKhdvHixRCLBza1YsaKlpcWsJ1QcHR1JWzDjx48nr6VSKdnQjBkzFArF4L0KsbGxUqnUy8uLlKSlpXV2dvJ4PGo2Pp+vUChcXFxIibe3t0KhmDBhAinx9/dXKBSDt3lERka6ublRO0YlPT1dq9Xi5t599128twTj7OxsZh3eAvHceIZ9PdnZ2QCAnJwchFB6ejoA4ODBg89Qz/8HeFNOb29vb28vAEAoFP7TPfrHOHjwIPZmhFBOTg4AIDs7+xnqoYdvGquDdkoaq8NCTNnd3Z2VlfXpp5+yWM8z4rRIaWlpRUXFmjVrSElXV9fRo0cbGhrs7e0jIiJeeuklUqXT6Q4fPnzz5s1Ro0bFx8fjcZNU5efn19fXe3p6xsXFeXh4kCq9Xp+fn19XV+fh4bFkyZKRI0dSO3Dx4sVffvmlv78/JCQkMjKSGvUOMw0NDceOHXv06FFQUNCrr76Ke3L16tVr164NzhwXF3f9+vXa2trBKrlcjoPp69evHz9+vKurKyAgICYmhno3q6urT5w40dfXFxwcPH/+fNLqzs7On3/+mVqbWCym3oJhwmw4HxgYkMvlAICenp7HDfnPK6a8f/++m5ubt7c3Kbl9+7aXl5enp2dCQkJoaCgA4MMPP8QqtVrt6+vr5OS0dOlSmUzm5OR06dIlrNJoNKNHjx45cmRiYqJEIhEIBKWlpVjV2to6ZswYDw+PxMREqVRqb29/4cIFsrkNGzYwmcxXXnklOjqaxWIlJCQ8gxXPJaY8ffo0l8udMWNGXFwcn89fvHgxlr/33nuDbxmTyUQIbd68ebCKwWD09/cjhA4fPsxisWQyWXx8vEAgCAoK6u7uxnXu2LGDwWDMnTtXLpfb2dlFRUUNDAxgVVFRkVmFKSkpT2/F84op/8MpHzx4EBERgXszDE65cOFCDodDdcr58+dPmDDh0aNHOPnRRx8xmczbt28jhBYtWuTi4qJSqbAqLS3Nx8cH34DU1FSRSPTgwQOE0MDAwMyZMwMCAnC29PR0oVDY2tqKEDKZTOHh4X5+flhVWloKAMjPz8fJffv2AQDKysr+qhV/3yn7+vo8PDzIw0LKysoYDEZhYSFCqL+/v4fCr7/+ymAw8NkkZqpz584xGIw9e/YghIxGo1AoxIeCIIRqa2uZTObOnTsRQhqNhsPhZGVlYVV5eTkA4NixYzj5wQcfjBw5klqtwWB4ekOe/4vOjRs3xGKxUql86623nvm5+/R89913tbW1ycnJVKFKpVq+fDl5ukNCQoLJZKqsrDQajT/99NPrr79OzjetX79eqVSePXsWABAQEJCZmYmdg8lkhoaG3rhxA2eTSqUbNmzAE08MBiM0NLSurg6rdu/ePX36dDwsAACWLl26bds2d3f3Ibd8EBcuXGhpaXn77bdxMjg4OCgo6PDhwwAAFovF+xOj0ZicnBwXFxcfH2+mMplMycnJ0dHRqampAICOjo62tjbydIoXX3zR29sb/yZdXV3Lli3DjxIAQFBQEI/HI3+umpqaqVOn8ihQZ4KGjX/HGSaTKScnJzU1df/+/UPd6q1bt9asWXPixIlTp05R5WZBUkNDAwDA3d1dp9P19fXho1cw2M+uXLkSHh6elpZGyvV6fVFRUXBwME7im4Tp7u7+4YcfZDIZTl68eHH58uU6ne7kyZNarTY0NJQa2g4n1dXVbDbbz8+PlPj7+5vFdgCAzMxMrVb7xRdfDK5h06ZN7e3tu3btwkmhUOjj43Ps2LHExEQWi1VWVqZWq3FoOG7cuO+//54sWFhY2NvbS/5cf/zxh1wuz83NvX79uo+PT1JSEnUiedj495PSz88vPT19GP4ZRqMxISHhtddegxA+IZtOp8vIyJBIJBBCBwcHZ2fnyspKUltRUQEAaG9vJyUdHR1yuVwsFvf09Bw4cIBalVarXbJkiVgs1mq1eXl5WKhWq7Va7fjx49etW7dp06ZJkybhEWf4aW1tFQqFNjY2pEQkErW2tlLzqNXqb775ZuPGja6urmbF7969u3PnzvXr15OPeQaDUVxcrFQqR48eHRISEhYWlpWVlZiYSC114MCBsLCw2NjYrVu3zp49GwDQ0dGhUqm2b99+5MiR5ubm7OzsiRMnVlVVDYnNT+QfmBLasmVLV1fXxx9//IQ83d3dCxYs0Gg0x48fZzAYDAZj5cqV+/bt27ZtW1NTU0lJyRtvvMHn8/GxUmQRiUQSExOjVCrXrl1LVen1ej8/v5iYmKampnfeecdkMvX19RmNxq+++ionJ0etVms0moyMjI0bN2JfH2b6+/vNngUsFsvsFK4vv/ySzWaTwy6VnTt3MpnM1atXkxKE0Geffdbc3BwbGxsVFeXv779//36zUYjFYs2ZMycwMDAnJ+f8+fMAgI6Ojnnz5hUUFJSWlp44caK+vl4gEJjFV8PE4DBzz549YMhedC5evGhra3v58mWcXLduHfVFB6NSqSZPnuzu7l5fX08KDQZDeno6ntcQCoUFBQWenp5btmwZ3MSPP/4IABh8uB5C6OTJkwCAvLy8gYEBBoMxc+ZMav0CgWDt2rVPaQjJ33/RWbt2rUgkokqysrJGjBhBJvv7+11cXNLS0gaXNRqNIpHI7B25sLAQAHD69GkyT0hIiEQisVhcJpONHj3aYsc++eQTAEBTU9NTGvK/uqJz5MiR3t5emUzG4XA4HM727dubm5vxBc5QVVU1depUJpNZX19PXZZls9m5ubnt7e0NDQ0ajSYiIuLevXv4CDyEEPX8QfxSf+nSpcGqyMhIPp9/6dIlJpMpEonwQjZZv6enZ0dHx9DabwkvL6/29va+vj5ScvfuXWrfzp8/397eTr6TUSkpKbl//35sbCxVWF5e7uLiQn4MYGNjs2TJktraWvwFwp07d8icNjY20dHRjY2N+EBAg8FArQcHlPjEw+FkuJ1yxYoVR48ezfuT+fPnOzs74wsAQH19/axZs6ZMmVJdXY2PPCTJzs7evXv3iBEjxo0bx2az8YxaWFgYAMDR0fH9998nc7a0tBgMBvyDCoXCjRs3kqr79+/39PTgsEwmk1EDJp1Op1Kpxo4dO7T2W0Imkw0MDOApKkxJScn06dPJ5NmzZ3k8HlVCVXE4HDynS+Lk5KTT6fR6PSlpa2vjcrlcLjc3N3fs2LEajYZUqVQqHo83YsSIXbt2cbnc5uZmUlVZWeng4EB9vxwmBj88h3T4NoM6fJtMJolE4uLiUlxcfJoCHj7efPNNV1fXxsZGhFBdXZ2Xl1dycjIuuHr1altb2/LycvxcjIiIEAgEuFRGRgaPxyspKUEIabXaBQsW8Pl8pVKJEMKB1ObNmwcGBgwGQ0pKip2d3dMPVSR/f/g2mUz+/v5BQUGdnZ3oz8ntqqoqMsPs2bODg4Mtlo2IiAgMDDQTNjY28ni8ZcuW6fV6hFBFRYWzszP+uVpaWuzt7RcvXozv76lTp2xtbfGA29jYyOVyo6OjcamTJ09yudxNmzY9vSFDMnmO+aecEk/kDubbb79FCD18+DA4OJjFYo0aNYrJZM6bNw+ffIwQ0uv10dHRDAbDy8uLy+X6+vpiL0QI9fb24lEPq3x8fKinKe/bt08gEDg7Ozs4ODg5ORUXFz+DCc9lRef27dtjxoyxs7Nzc3PjcDi5ublU7dixY5cvX26x4KRJk+Li4gbLT5065ebmZmdnh5dVFy1aRP5cZ86cEYlE9vb27u7uNjY2KSkpvb29WFVUVOTq6srn8z08PJhM5sqVK/HyxFPyvJzSwup2fHx8ZGQkl8t9vo9ki2RmZmZkZOBrqVRKHTtI8GeLjo6OZWVlNTU1Go1GLBZTw007O7vCwsI7d+40NDS4uroGBASQ0ytcLjc/Pz8nJ6eurk4oFE6ZMoU685KUlBQTE4NnmqZNm8bn84fM0P+CWCy+ceNGZWUlXqo2mx387bffzD6jJDl37pzFOxUREaFWq3///fdHjx5NnDiROgTPmTNHpVJVVlb29PRIJBLqdwILFy68e/duRUWFTqeTSCSenp7Px7y/iAWn5PP5w3Z7HBwcyNiRx+OZfS0xGKlUKpVKLarEYrFYLLao8vX1pR6iTsXe3n7mzJlP292hhM1mW4waAQBPWGdyc3N7nIrD4TyuQh6P97ij3dlsdkhIyBN7OuTQn67RWB20U9JYHf8CkkoA/YVCHisAAAAASUVORK5CYII="
            };
            
        },
        
        export_as_JSON: function() {
            var orderLines, paymentLines;
            
            parent_return_order = '';
            var ret_o_id = this.get_ret_o_id();
            var ret_o_ref = this.get_ret_o_ref();
            var return_seq = 0;
            
            orderLines = [];
            (this.get('orderLines')).each(_.bind( function(item) {
                return orderLines.push([0, 0, item.export_as_JSON()]);
            }, this));
            paymentLines = [];
            (this.get('paymentLines')).each(_.bind( function(item) {
                return paymentLines.push([0, 0, item.export_as_JSON()]);
            }, this));
            
            if (ret_o_id) {
                parent_return_order = this.get_ret_o_id();
            }
            
            return {
                name: this.getName(),
                amount_paid: this.getPaidTotal(),
                amount_total: this.getTotalTaxIncluded(),
                amount_tax: this.getTax(),
                amount_return: this.getChange(),
                lines: orderLines,
                statement_ids: paymentLines,
                pos_session_id: this.pos.pos_session.id,
                partner_id: this.get_client() ? this.get_client().id : false,
                user_id: this.pos.cashier ? this.pos.cashier.id : this.pos.user.id,
                uid: this.uid,
                sequence_number: this.sequence_number,
                parent_return_order: parent_return_order, // Required to create paid return order
                return_seq: return_seq || 0,
                back_order: this.get_ret_o_ref()
            };
        },
    });
    
    instance.point_of_sale.PaymentScreenWidget = instance.point_of_sale.PaymentScreenWidget.extend({
        validate_order: function(options) {
            var self = this;
            options = options || {};

            var currentOrder = this.pos.get('selectedOrder');
            var coupon_amt = currentOrder.get_coupon_amount();
            var ret_coupon_amt = currentOrder.get_bonus_return_amount();

            if(currentOrder.get('orderLines').models.length === 0){
                this.pos_widget.screen_selector.show_popup('error',{
                    'message': _t('Empty Order'),
                    'comment': _t('There must be at least one product in your order before it can be validated'),
                });
                return;
            }

            var plines = currentOrder.get('paymentLines').models;
            for (var i = 0; i < plines.length; i++) {
                if (plines && plines[i].cashregister.journal.type === 'bank' && plines[i].get_amount() < 0) {
                    this.pos_widget.screen_selector.show_popup('error',{
                        'message': _t('Negative Bank Payment'),
                        'comment': _t('You cannot have a negative amount in a Bank payment. Use a cash payment method to return money to the customer.'),
                    });
                    return;
                }
            }

            if(!this.is_paid()){
                return;
            }

            // The exact amount must be paid if there is no cash payment method defined.
            if (Math.abs(currentOrder.getTotalTaxIncluded() - currentOrder.getPaidTotal()) > 0.00001) {
                var cash = false;
                for (var i = 0; i < this.pos.cashregisters.length; i++) {
                    cash = cash || (this.pos.cashregisters[i].journal.type === 'cash');
                }
                if (!cash) {
                    this.pos_widget.screen_selector.show_popup('error',{
                        message: _t('Cannot return change without a cash payment method'),
                        comment: _t('There is no cash payment method available in this point of sale to handle the change.\n\n Please pay the exact amount or add a cash payment method in the point of sale configuration'),
                    });
                    return;
                }
            }

            if (this.pos.config.iface_cashdrawer) {
                    this.pos.proxy.open_cashbox();
            }

            if(options.invoice){
                // deactivate the validation button while we try to send the order
                this.pos_widget.action_bar.set_button_disabled('validation',true);
                this.pos_widget.action_bar.set_button_disabled('invoice',true);

                var invoiced = this.pos.push_and_invoice_order(currentOrder);

                invoiced.fail(function(error){
                    if(error === 'error-no-client'){
                        self.pos_widget.screen_selector.show_popup('error',{
                            message: _t('An anonymous order cannot be invoiced'),
                            comment: _t('Please select a client for this order. This can be done by clicking the order tab'),
                        });
                    }else{
                        self.pos_widget.screen_selector.show_popup('error',{
                            message: _t('The order could not be sent'),
                            comment: _t('Check your internet connection and try again.'),
                        });
                    }
                    self.pos_widget.action_bar.set_button_disabled('validation',false);
                    self.pos_widget.action_bar.set_button_disabled('invoice',false);
                });

                invoiced.done(function(){
                    self.pos_widget.action_bar.set_button_disabled('validation',false);
                    self.pos_widget.action_bar.set_button_disabled('invoice',false);
                    self.pos.get('selectedOrder').destroy();
                });
            } else {
            	var coupon_id = currentOrder.get_coupon_id();
                var recharge_coupon_id = currentOrder.get_recharge_coupon_id();
                var connection = false;
                var context = {};
                new instance.web.Model("pos.order").get_func("check_connection")().done(function(result) {
                    if (result) {
                        if (coupon_id) {
                            new instance.web.Model("pos.coupon").get_func("search_read")
                                                  ([['id', '=', coupon_id]], ['date_create']).pipe(
                                function(result) {
                                    if (result && result[0]) {
                                        if (currentOrder.get('orderLines').length > 0) {
                                            var tr1 = [];
                                            (currentOrder.get('orderLines')).each(_.bind( function(item) {
                                                if (item.get_product().is_coupon) {
                                                    var coupon_serial = currentOrder.generateUniqueId_barcode();
                                                    if (item.quantity > 1) {
                                                        for (i=0; i < item.quantity; i++) {
                                                            var coupon_serial = currentOrder.generateUniqueId_barcode();
                                                            item.set_coupon_serial(coupon_serial);
                                                            new instance.web.Model("pos.coupon.line").get_func("create")
                                                                ({
                                                                    'name': coupon_serial,
                                                                    'amount': item.price,
                                                                    'remaining_amt': item.price,
                                                                    'product_id': item.get_product().id,
                                                                    'validity':item.get_product().validity_days, 
                                                                    'coupon_id': coupon_id
                                                                });
                                                            tr1.push($("<tr id='prod_info'><td style='text-align:center;'>-- " + _t("Coupon Information") + " --</td></tr>" +
                                                            "<tr id='prod_info'><td style='padding:2px;'>" + item.get_product().display_name + " [ " + _t("Qty") + ": " + item.quantity + ", " + _t("Price") + ": " + self.format_currency(item.price) +" ]</td></tr>"));
                                                            tr1.push($("<tr id='" + coupon_serial + "'><td style='padding: 0px;'><div style='text-align:center;' class='" + coupon_serial + "' width='150' height='50'/></td></tr>"))
                                                            tr1.push($("<tr id='barcode_number'><td style='padding: 2px;text-align:center;font-size:25px;'>" + coupon_serial + "</td></tr>"));
//                                                            $('#' + coupon_serial_line.toString()).barcode(coupon_serial_line.toString(), "code128")
                                                        }
                                                    } else {
                                                    	item.set_coupon_serial(coupon_serial);
                                                        new instance.web.Model("pos.coupon.line").get_func("create")
                                                        ({
                                                            'name': coupon_serial,
                                                            'amount': item.price,
                                                            'remaining_amt': item.price,
                                                            'product_id': item.get_product().id,
                                                            'validity':item.get_product().validity_days, 
                                                            'coupon_id': coupon_id
                                                        });
                                                    tr1.push($("<tr id='prod_info'><td style='text-align:center;'>-- " + _t("Coupon Information") + " --</td></tr>" +
                                                    "<tr id='prod_info'><td style='padding:2px;'>" + item.get_product().display_name + " [" + _t("Qty") + ": " + item.quantity + ", " + _t("Price") + ": " + self.format_currency(item.price) +"]</td></tr>"));
                                                    tr1.push($("<tr id='" + coupon_serial + "'><td style='padding: 0px;'><div style='text-align:center;' class='" + coupon_serial + "' height='50'/></td></tr>"))
                                                    tr1.push($("<tr id='barcode_number'><td style='padding: 2px;text-align:center;font-size:25px;'>" + coupon_serial + "</td></tr>"));
//                                                    $('#' + coupon_serial_line.toString()).barcode(coupon_serial_line.toString(), "code128")
                                                }
                                            }
                                        }));
                                        _.each(tr1, function(tr) {
                                            var tr_id = tr.attr('id').toString();
                                            $('table#barcode_table tbody').append(tr);
                                            if (tr_id.length <= 10) {
                                                $('.' + tr_id).barcode(tr_id, "code128")
                                            }
                                        });

//                                            self.pos_widget.screen_selector.set_current_screen(self.next_screen);
                                        }
                                    }
//                                    self.pos.push_order(currentOrder) 
//                                    if(! self.pos.config.iface_print_via_proxy){
//                                    	self.pos_widget.screen_selector.set_current_screen(self.next_screen);
//                                    }
                            });
                        } else if (recharge_coupon_id) {
                            new instance.web.Model("pos.coupon").get_func("search_read")
                                                  ([['id', '=', recharge_coupon_id]], ['date_create']).pipe(
                                function(result) {
                                    if (result && result[0]) {
                                        if (currentOrder.get('orderLines').length > 0) {
                                            var tr1 = [];
                                            (currentOrder.get('orderLines')).each(_.bind( function(item) {
                                                if (item.get_product().is_coupon) {
                                                    var coupon_serial = currentOrder.get_recharge_coupon_serial();
                                                    item.set_coupon_serial(coupon_serial);
                                                    if (item.quantity == 1) {
                                                    	new instance.web.Model("pos.coupon.line").get_func("recharge_coupon")
                                                        (currentOrder.get_recharge_coupon_line_id(), item.get_product().id, 
                                                            item.get_product().validity_days, item.get_product().list_price).pipe(
                                                                function(history_res) {
                                                                	item.set_coupon_history_id(history_res);
                                                                }
                                                            );
                                                            
                                                        tr1.push($("<tr id='prod_info'><td style='text-align:center;'>-- " + _t("Coupon Information") + " --</td></tr>" +
                                                        "<tr id='prod_info'><td style='padding:2px;'>" + item.get_product().display_name + " [ " + _t("Qty") + ": " + item.quantity + ", " + _t("Price") + ": " + self.format_currency(item.price) +" ]</td></tr>"));
                                                        tr1.push($("<tr id='" + coupon_serial + "'><td style='padding: 2px;'><div class='" + coupon_serial + "' width='150' height='50'/></td></tr>"))
                                                        tr1.push($("<tr id='barcode_number'><td style='padding: 2px;text-align:center;font-size:25px;'>" + coupon_serial + "</td></tr>"));
//                                                        $('#' + coupon_serial.toString()).barcode(coupon_serial.toString(), "code128")
                                                    } else {
                                                        alert (_t('Please select coupon product to recharge !'));
                                                    }
                                                }
                                            }));
                                            _.each(tr1, function(tr) {
                                                var tr_id = tr.attr('id').toString();
                                                $('table#barcode_table tbody').append(tr);
                                                if (tr_id.length <= 10) {
                                                    $('.' + tr_id).barcode(tr_id, "code128")
                                                }
                                            });

//                                            self.pos_widget.screen_selector.set_current_screen(self.next_screen);
                                        }
                                    }
//                                    self.pos.push_order(currentOrder) 
//                                    if(! self.pos.config.iface_print_via_proxy){
//                                    	self.pos_widget.screen_selector.set_current_screen(self.next_screen);
//                                    }
                            });
                        }
//                        else {
//                        	console.log("else called")
//                        	self.pos.push_order(currentOrder) 
//                            if(! self.pos.config.iface_print_via_proxy){
//                            	self.pos_widget.screen_selector.set_current_screen(self.next_screen);
//                            }
//                        }
                    }
                });
//                this.pos.push_order(currentOrder) 
//                if(this.pos.config.iface_print_via_proxy){
//                    var receipt = currentOrder.export_for_printing();
//                    var proxy_receipt = QWeb.render('XmlReceipt',{
//                        receipt: receipt, widget: self,
//                    })
////                     proxy on popup
//                    var dialog = new instance.web.Dialog(this, { 
//                        size: 'medium',
//                        buttons: [{text: _t("Close"), click: function() { this.parents('.modal').modal('hide'); }}],
//                    }).open();
//                    dialog.$el.html(proxy_receipt);
//                    
//                    this.pos.proxy.print_receipt(proxy_receipt);
//                    
//                    this.pos.get('selectedOrder').destroy();    //finish order and go back to scan screen
//                    this.pos.get('selectedOrder').set_ret_o_id('')
//                    $("span#sale_mode").css('background', 'blue');
//                    $("span#return_order").css('background', '');
//                    $("span#missing_return_order").css('background', '');
//                    $('#return_order_ref').html('');
//                    $('#return_order_number').val('');
//                }else{
//                    this.pos_widget.screen_selector.set_current_screen(this.next_screen);
//                }
                self.pos.push_order(currentOrder) 
                if(! self.pos.config.iface_print_via_proxy){
                	self.pos_widget.screen_selector.set_current_screen(self.next_screen);
                }
            }

            // hide onscreen (iOS) keyboard 
            setTimeout(function(){
                document.activeElement.blur();
                $("input").blur();
            },250);
        },
        wait: function( callback, seconds){
           return window.setTimeout( callback, seconds * 1000 );
        },
        show: function(){
            this._super();
            var self = this;
            
            var currentOrder = pos.get('selectedOrder');
            var due_total = currentOrder.getTotalTaxIncluded();
            pos = self.pos;
            pos_widget = self.pos_widget;
            
            // gift coupon remove            
            $('table').delegate('img[id=remove_serial]', 'click', function() {            	
                var $this = $(this);
                var tr_id = $this.closest('tr').attr('id');
                id = tr_id.split('_');
                id = id[2];
                var coupon_amt = parseFloat($('#gift_coupon_input_coupon_amount_' + id.toString()).html());
                if (coupon_amt) {
                    currentOrder.set_coupon_amount(parseFloat(currentOrder.get_coupon_amount()) - coupon_amt);
                }
                $this.closest('tr').remove();
                //self.update_payment_summary();   
                self.eq_update_payment_summary(coupon_amt);                
            });
            
            // Bonus Return remove
                
            $('table').delegate('img[id=bonus_coupon_remove_serial]', 'click', function() {
                var $this = $(this);
                var tr_id = $this.closest('tr').attr('id');
                id = tr_id.split('_');
                id = id[2];
                var ret_coupon_amt = parseFloat($('#bonus_coupon_input_coupon_amount_' + id.toString()).html());
                if (ret_coupon_amt) {
                    currentOrder.set_bonus_return_amount(parseFloat(currentOrder.get_bonus_return_amount()) - ret_coupon_amt);
                }
                $this.closest('tr').remove();
                //self.update_payment_summary();
                self.eq_update_payment_summary(ret_coupon_amt);
            });
            
            // Gift Coupon Updated
                
            var gift_click_count = 0;
            $('#add_gift_coupon').click(function() {
                var connection = false;
                new instance.web.Model("pos.order").get_func("check_connection")().done(function(result) {
                    if (result) {
                        dialog = new instance.web.Dialog(this, {
                            title: _t("Enter gift coupon information"),
                            size: 'medium',
                            buttons: [
                                {text: _t("Ok"), click: function() {
                                    var gift_coupon_serial = dialog.$el.find("input#gift_coupon_barcode_pay").val();
                                    if (gift_coupon_serial) {
                                        var today = new Date();
                                        var dd = (today.getDate()).toString();
                                        var mm = (today.getMonth()+1).toString();
                                        var yyyy = today.getFullYear().toString();
                                        new instance.web.Model("pos.coupon.line").get_func("search_read")([['name', '=', gift_coupon_serial], 
                                                                                    ['date_expiry_line', '>', yyyy + '-' + mm + '-' + dd]], 
                                                                                    ['id','amount','remaining_amt']).pipe(
                                            function(result) {
                                                if (result && result[0]) {
                                                    if (result[0].remaining_amt > 0) {
                                                        if (due_total >= result[0].remaining_amt) {
                                                            gift_click_count = gift_click_count + 1;
                                                            var table = $('#pay_by_coupon_table');
                                                            table.append("<tr id='gift_rettr_" + gift_click_count.toString() + "'><td style='text-align:right;padding-right:15px;width:80%;'>" +
                                                            "<span id='gift_coupon_" + gift_click_count.toString() + "' class='gift_coupon_serial_input' style='font-weight:bold;width:30px;padding:0 5px;'/></td>" +
                                                            "<td style='text-align:right;padding-right:15px;width:20%;'>" +
                                                            "<span id='gift_coupon_input_coupon_amount_" + gift_click_count.toString() + "' class='gift_coupon_amount_input' " +
                                                            "style='width:30px;padding:0 5px;font-weight:bold;'/></td><td style='padding:5px;'>" +
                                                            "<a href='javascript:void(0)' class='delete-payment-line'>" +
                                                            "<img src='/point_of_sale/static/src/img/search_reset.gif' id='remove_serial'></a>" +
                                                            "</td></tr>");
                                                            
                                                            $('span#gift_coupon_' + gift_click_count.toString()).html(gift_coupon_serial);                                                            
                                                            //$('span#gift_coupon_input_coupon_amount_' + gift_click_count.toString()).html(parseFloat((result[0].remaining_amt).toFixed(2)));		// DEFAULT

                                                            // EQ: Format coupon price
                                                            var formated_cpn_value = parseFloat((result[0].remaining_amt).toFixed(2))
                                                            formated_cpn_value = round_di(formated_cpn_value, 2).toFixed(2);
                                                            formated_cpn_value = openerp.web.format_value(round_di(formated_cpn_value, 2), { type: 'float', digits: [69, 2]});                                                			
                                                            $('span#gift_coupon_input_coupon_amount_' + gift_click_count.toString()).html(formated_cpn_value);										// Changed version - number is formatted
                                                            
                                                            currentOrder.set_coupon_amount(parseFloat(currentOrder.get_coupon_amount()) + parseFloat(result[0].remaining_amt));
                                                        } else if (due_total < result[0].remaining_amt) {
                                                            gift_click_count = gift_click_count + 1;
                                                            var table = $('#pay_by_coupon_table');
                                                            table.append("<tr id='gift_rettr_" + gift_click_count.toString() + "'><td style='text-align:right;padding-right:15px;width:80%;'>" +
                                                            "<span id='gift_coupon_" + gift_click_count.toString() + "' class='gift_coupon_serial_input' style='font-weight:bold;width:30px;padding:0 5px;'/></td>" +
                                                            "<td style='text-align:right;padding-right:15px;width:20%;'>" +
                                                            "<span id='gift_coupon_input_coupon_amount_" + gift_click_count.toString() + "' class='gift_coupon_amount_input' " +
                                                            "style='width:30px;padding:0 5px;font-weight:bold;'/></td><td style='padding:5px;'>" +
                                                            "<a href='javascript:void(0)' class='delete-payment-line'>" +
                                                            "<img src='/point_of_sale/static/src/img/search_reset.gif' id='remove_serial'></a>" +
                                                            "</td></tr>");
                                                            
                                                            $('span#gift_coupon_' + gift_click_count.toString()).html(gift_coupon_serial);                                                            
                                                            //$('span#gift_coupon_input_coupon_amount_' + gift_click_count.toString()).html(parseFloat(due_total.toFixed(2)));					// DEFAULT
                                                            
                                                            // EQ: Format coupon price
                                                            var formated_cpn_value = parseFloat(due_total.toFixed(2))
                                                            formated_cpn_value = round_di(formated_cpn_value, 2).toFixed(2);
                                                            formated_cpn_value = openerp.web.format_value(round_di(formated_cpn_value, 2), { type: 'float', digits: [69, 2]});
                                                            $('span#gift_coupon_input_coupon_amount_' + gift_click_count.toString()).html(formated_cpn_value);									// Changed version - number is formatted
                                                            
                                                            currentOrder.set_coupon_amount(parseFloat(currentOrder.get_coupon_amount()) + parseFloat(due_total));
                                                        }
                                                    } else {
                                                        dialog.$el.find("input#gift_coupon_barcode_pay").val('');
                                                        alert (_t('Amount should be greater than zero !'));
                                                    }
                                                } else {
                                                    dialog.$el.find("input#gift_coupon_barcode_pay").val('');
                                                    dialog.$el.find("input#gift_coupon_barcode_amt").val('');
                                                    alert (_t('Either date is expired or invalid barcode.'))
                                                }
                                                self.update_payment_summary();
                                            }
                                        );
                                    }
                                    this.parents('.modal').modal('hide');
                                    $('.modal').modal('hide');						// EQ: hide modal dialog and all parts of it
                                    $('.modal-dialog').hide();						// EQ: hide modal dialog and all parts of it
                                }},
                                {text: _t("Cancel"), click: function() { 
                                    this.parents('.modal').modal('hide');
                                }}
                            ]
                        }).open();
                        dialog.$el.html(QWeb.render("pay_gift_coupon_info", this));
                        this.enter_barcode_handler = function(e){
                            if(e.which >= 10){
                                var today = new Date();
                                var dd = (today.getDate()).toString();
                                var mm = (today.getMonth()+1).toString();
                                var yyyy = today.getFullYear().toString();
                                new instance.web.Model("pos.coupon.line").get_func("search_read")([['name', '=', dialog.$el.find("input#gift_coupon_barcode_pay").val()], 
                                                                        ['date_expiry_line', '>', yyyy + '-' + mm + '-' + dd]], 
                                                                        ['remaining_amt']).pipe(
                                        function(result) {
                                            if (result && result[0]) {
                                                $('#remain_gift_coupon_bal').html(result[0].remaining_amt);
                                            }
                                        }
                                );
                            }
                        };
                        dialog.$el.on('keypress', this.enter_barcode_handler);
                        dialog.$el.find("input#gift_coupon_barcode_pay").focus();
                        dialog.$el.find("input#gift_coupon_barcode_pay").focusout(function() {
                            var today = new Date();
                            var dd = (today.getDate()).toString();
                            var mm = (today.getMonth()+1).toString();
                            var yyyy = today.getFullYear().toString();
                            new instance.web.Model("pos.coupon.line").get_func("search_read")([['name', '=', dialog.$el.find("input#gift_coupon_barcode_pay").val()], 
                                                                    ['date_expiry_line', '>', yyyy + '-' + mm + '-' + dd]], 
                                                                    ['remaining_amt']).pipe(
                                    function(result) {
                                        if (result && result[0]) {
                                            $('#remain_gift_coupon_bal').html(result[0].remaining_amt);
                                        }
                                    }
                            );
                        });
                    }
                }).fail(function(result, ev) {
                    ev.preventDefault();
                    connection = false;
                    return
                });
            });
            
            // Bonus Return Updated

            var bonus_click_count = 0;
            $('#add_bonus_coupon').click(function() {
                var connection = false;
                new instance.web.Model("pos.order").get_func("check_connection")().done(function(result) {
                    if (result) {
                        dialog = new instance.web.Dialog(this, {
                            title: _t("Enter bonus coupon information"),
                            size: 'medium',
                            buttons: [
                                {text: _t("Ok"), click: function() {
                                    var bonus_coupon_serial = dialog.$el.find("input#bonus_coupon_barcode_pay").val();
                                    var bonus_barcode_amt = dialog.$el.find("input#bonus_coupon_barcode_amt").val();
                                    if (bonus_coupon_serial && bonus_barcode_amt) {
                                        new instance.web.Model("bonus.return").get_func("search_read")([['name', '=', bonus_coupon_serial]], ['bonus_remaining_amt']).pipe(
                                            function(result) {
                                                if (result && result[0]) {
                                                    if (result[0].bonus_remaining_amt > 0) {
                                                        if (bonus_barcode_amt <= result[0].bonus_remaining_amt) {
                                                            bonus_click_count = bonus_click_count + 1;
                                                            var table = $('#pay_by_bonus_coupon_table');
                                                            table.append("<tr id='bonus_rettr_" + bonus_click_count.toString() + "'><td style='text-align:right;padding-right:15px;width:80%;'>" +
                                                            "<span id='bonus_coupon_" + bonus_click_count.toString() + "' class='bonus_coupon_serial_input' style='font-weight:bold;width:30px;padding:0 5px;'/></td>" +
                                                            "<td style='text-align:right;padding-right:15px;width:20%;'>" +
                                                            "<span id='bonus_coupon_input_coupon_amount_" + bonus_click_count.toString() + "' class='bonus_coupon_amount_input' " +
                                                            "style='width:30px;padding:0 5px;font-weight:bold;'/></td><td style='padding:5px;'>" +
                                                            "<a href='javascript:void(0)' class='delete-payment-line'>" +
                                                            "<img src='/point_of_sale/static/src/img/search_reset.gif' id='bonus_coupon_remove_serial'></a>" +
                                                            "</td></tr>");
                                                            
                                                            $('span#bonus_coupon_' + bonus_click_count.toString()).html(bonus_coupon_serial);
                                                            $('span#bonus_coupon_input_coupon_amount_' + bonus_click_count.toString()).html(bonus_barcode_amt);
                                                            currentOrder.set_bonus_return_amount(parseFloat(currentOrder.get_bonus_return_amount()) + parseFloat(bonus_barcode_amt));
                                                        } else {
                                                            dialog.$el.find("input#bonus_coupon_barcode_amt").val('');
                                                            alert (_t('Remaining amount in coupon: ' + (result[0].bonus_remaining_amt).toString() + ' !'))
                                                        }
                                                    } else {
                                                        dialog.$el.find("input#bonus_coupon_barcode_pay").val('');
                                                        alert (_t('Amount should be greater than zero !'))
                                                    }
                                                } else {
                                                    dialog.$el.find("input#bonus_coupon_barcode_pay").val('');
                                                    dialog.$el.find("input#bonus_coupon_barcode_amt").val('');
                                                    alert (_t('Invalid barcode !'))
                                                }self.update_payment_summary();
                                            }
                                        );
                                    }
                                    this.parents('.modal').modal('hide');
                                    $('.modal').modal('hide');						// EQ: hide modal dialog and all parts of it
                                    $('.modal-dialog').hide();						// EQ: hide modal dialog and all parts of it
                                }},
                                {text: _t("Cancel"), click: function() { 
                                    this.parents('.modal').modal('hide');
                                }}
                            ]
                        }).open();
                        dialog.$el.html(QWeb.render("pay_bonus_coupon_info", this));
                        dialog.$el.find("input#bonus_coupon_barcode_pay").focusout(function() {
                            new instance.web.Model("bonus.return").get_func("search_read")([['name', '=', dialog.$el.find("input#bonus_coupon_barcode_pay").val()]], 
                                                                    ['bonus_remaining_amt']).pipe(
                                    function(result) {
                                        if (result && result[0]) {
                                            if (currentOrder.getTotalTaxIncluded() > result[0].bonus_remaining_amt) {
                                                $('input#bonus_coupon_barcode_amt').val(result[0].bonus_remaining_amt.toFixed(2));
                                            } else {
                                                $('input#bonus_coupon_barcode_amt').val(currentOrder.getTotalTaxIncluded().toFixed(2));
                                            }
                                        }
                                    }
                            );
                        });
                    }
                }).fail(function(result, ev) {
                    ev.preventDefault();
                    connection = false;
                    return
                });
            });
        },
        eq_update_payment_summary: function(removedBonusValue){
        	// EQUITANIA: our own version of this function that it's triggered after delete of coupon - it's simple solution for wrong calculation of prices after delete of bonus position together with credit cards
        	if (!isNaN(removedBonusValue)){        		        	
	        	var currentOrder = this.pos.get('selectedOrder');	        	
	        	var paidTotal = currentOrder.getPaidTotal();	        	
	            var dueTotal = currentOrder.getTotalTaxIncluded();
	            
	            // round_di(paidTotal, 2).toFixed(2);
	            paidTotal_formated = round_di(paidTotal, 2).toFixed(2);
	            dueTotal_formated = round_di(dueTotal, 2).toFixed(2);
	            if (paidTotal_formated == dueTotal_formated){
	            	paidTotal = currentOrder.getPaidTotal() - removedBonusValue;
	            }
	            	
	            
	            var remaining = dueTotal > paidTotal ? dueTotal - paidTotal : 0;
	            var change = paidTotal > dueTotal ? paidTotal - dueTotal : 0;
	            
	            var cpn_amt = parseFloat(0.0);
	
	            this.$('.payment-due-total').html(this.format_currency(dueTotal));
	            this.$('.payment-paid-total').html(this.format_currency(paidTotal));
	            this.$('.payment-remaining').html(this.format_currency(remaining));
	            this.$('.payment-change').html(this.format_currency(change));
	            
	            _.each($('.gift_coupon_amount_input'), function(amt) {
	            	amt_value = $(amt).html();								// EQ: To be able to deal with formatted numbers, let's get value
	            	amt_value = amt_value.replace(",", ".");				// replace "," by "." und use default functionality
	            	if (parseFloat(amt_value) == '') {
	                    val = 0.0
	                } else {
	                    val = parseFloat(amt_value);
	                }            	
	            	/*
	            	 * DEFAULT
	                if (parseFloat($(amt).html()) == '') {
	                    val = 0.0
	                } else {
	                    val = parseFloat($(amt).html());
	                }
	                */
	                cpn_amt += parseFloat(val);
	            });
	            
	            _.each($('.bonus_coupon_amount_input'), function(amt) {
	                if (parseFloat($(amt).html()) == '') {
	                    val = 0.0
	                } else {
	                    val = parseFloat($(amt).html());
	                }
	                cpn_amt += parseFloat(val);
	            });
	            
	            cpn_amt = parseFloat(cpn_amt);
	            currentOrder.setCpnAmt(cpn_amt);
	            if (cpn_amt > 0 ) {
	            	var use_default_ui_setter = true;
	                var paid_total_cpn = 0.0;
	                if(paidTotal) {
	                	paidTotal_rounded = round_di(paidTotal, 2).toFixed(2);
	                	dueTotal_rounded = round_di(dueTotal, 2).toFixed(2);
	                	if (paidTotal_rounded == dueTotal_rounded){
	                		$('.payment-due-total').html(this.format_currency(dueTotal));				// top result
	                		use_default_ui_setter = false;
	                		sum_without_cpn = paidTotal - cpn_amt;
	                		paid_total_cpn = sum_without_cpn;
	                		
	                		// EQ: fixed an error in logic of calculation of totam price
	                		if (paid_total_cpn => 0){
	                			if (typeof sum_without_cpn === 'number') {
	                    			sum_without_cpn = round_di(sum_without_cpn, 2).toFixed(2);
	                    			sum_without_cpn = openerp.instances[this.session.name].web.format_value(round_di(sum_without_cpn, 2), { type: 'float', digits: [69, 2]});
	                            }
	                    		$('.paymentline-input').val(sum_without_cpn);	
	                		} 
	                	}
	                	else{
	                		paid_total_cpn = paidTotal + cpn_amt;
	                        remaining = dueTotal > paid_total_cpn ? dueTotal - paid_total_cpn : 0;
	                        change = paid_total_cpn > dueTotal ? paid_total_cpn - dueTotal : 0;	
	                	}                    
	                } else {
	                    remaining = dueTotal > cpn_amt ? dueTotal - cpn_amt : 0;
	                    change = cpn_amt > dueTotal ? cpn_amt - dueTotal : 0;
	                    paid_total_cpn = cpn_amt;
	                }
	            }

	            if (use_default_ui_setter){
		            $('.payment-due-total').html(this.format_currency(dueTotal));				// top result
		            $('.payment-paid-total').html(this.format_currency(paid_total_cpn));		// Bezahlt
		            $('.payment-remaining').html(this.format_currency(remaining));				// Restbetrag
		            $('.payment-change').html(this.format_currency(change));					// Wechselgeld
	            }
	            
	            if(currentOrder.selected_orderline === undefined){
	                remaining = 1;  // What is this ? 
	            }
	                
	            if(this.pos_widget.action_bar){
	            	this.pos_widget.action_bar.set_button_disabled('validation', true);
	            	this.pos_widget.action_bar.set_button_disabled('invoice', true);
	                //this.pos_widget.action_bar.set_button_disabled('validation', !this.is_paid());
	                //this.pos_widget.action_bar.set_button_disabled('invoice', !this.is_paid());
	            }
        	}
        },
        update_payment_summary: function() {
            var currentOrder = this.pos.get('selectedOrder');
            var paidTotal = currentOrder.getPaidTotal();
            var dueTotal = currentOrder.getTotalTaxIncluded();
            var remaining = dueTotal > paidTotal ? dueTotal - paidTotal : 0;
            var change = paidTotal > dueTotal ? paidTotal - dueTotal : 0;
            
            var cpn_amt = parseFloat(0.0);

            this.$('.payment-due-total').html(this.format_currency(dueTotal));
            this.$('.payment-paid-total').html(this.format_currency(paidTotal));
            this.$('.payment-remaining').html(this.format_currency(remaining));
            this.$('.payment-change').html(this.format_currency(change));
            
            _.each($('.gift_coupon_amount_input'), function(amt) {
            	amt_value = $(amt).html();								// EQ: To be able to deal with formatted numbers, let's get value
            	amt_value = amt_value.replace(",", ".");				// replace "," by "." und use default functionality
            	if (parseFloat(amt_value) == '') {
                    val = 0.0
                } else {
                    val = parseFloat(amt_value);
                }            	
            	/*
            	 * DEFAULT
                if (parseFloat($(amt).html()) == '') {
                    val = 0.0
                } else {
                    val = parseFloat($(amt).html());
                }
                */
                cpn_amt += parseFloat(val);
            });
            
            _.each($('.bonus_coupon_amount_input'), function(amt) {
                if (parseFloat($(amt).html()) == '') {
                    val = 0.0
                } else {
                    val = parseFloat($(amt).html());
                }
                cpn_amt += parseFloat(val);
            });
            
            cpn_amt = parseFloat(cpn_amt);
            currentOrder.setCpnAmt(cpn_amt);
            if (cpn_amt > 0 ) {
            	var use_default_ui_setter = true;
                var paid_total_cpn = 0.0;
                if(paidTotal) {
                	paidTotal_rounded = round_di(paidTotal, 2).toFixed(2);
                	dueTotal_rounded = round_di(dueTotal, 2).toFixed(2);
                	if (paidTotal_rounded == dueTotal_rounded){
                		$('.payment-due-total').html(this.format_currency(dueTotal));				// top result
                		use_default_ui_setter = false;
                		sum_without_cpn = paidTotal - cpn_amt;
                		paid_total_cpn = sum_without_cpn;
                		
                		// EQ: fixed an error in logic of calculation of totam price
                		if (paid_total_cpn => 0){
                			if (typeof sum_without_cpn === 'number') {
                    			sum_without_cpn = round_di(sum_without_cpn, 2).toFixed(2);
                    			sum_without_cpn = openerp.instances[this.session.name].web.format_value(round_di(sum_without_cpn, 2), { type: 'float', digits: [69, 2]});
                            }
                    		$('.paymentline-input').val(sum_without_cpn);	
                		} 
                		                	                            
                		/*
                		paid_total_cpn = paidTotal - cpn_amt;
                        remaining = dueTotal > paid_total_cpn ? dueTotal - paid_total_cpn : 0;
                        change = paid_total_cpn > dueTotal ? paid_total_cpn - dueTotal : 0;
                        */
                	}
                	else{
                		paid_total_cpn = paidTotal + cpn_amt;
                        remaining = dueTotal > paid_total_cpn ? dueTotal - paid_total_cpn : 0;
                        change = paid_total_cpn > dueTotal ? paid_total_cpn - dueTotal : 0;	
                	}                    
                } else {
                    remaining = dueTotal > cpn_amt ? dueTotal - cpn_amt : 0;
                    change = cpn_amt > dueTotal ? cpn_amt - dueTotal : 0;
                    paid_total_cpn = cpn_amt;
                }
            }
            
            if (use_default_ui_setter){
	            $('.payment-due-total').html(this.format_currency(dueTotal));				// top result
	            $('.payment-paid-total').html(this.format_currency(paid_total_cpn));		// Bezahlt
	            $('.payment-remaining').html(this.format_currency(remaining));				// Restbetrag
	            $('.payment-change').html(this.format_currency(change));					// Wechselgeld
            }
            
            if(currentOrder.selected_orderline === undefined){
                remaining = 1;  // What is this ? 
            }
                
            if(this.pos_widget.action_bar){
                this.pos_widget.action_bar.set_button_disabled('validation', !this.is_paid());
                this.pos_widget.action_bar.set_button_disabled('invoice', !this.is_paid());
            }
        },
        is_paid: function(){
            var currentOrder = this.pos.get('selectedOrder');
            return (currentOrder.getTotalTaxIncluded() < 0.000001 
                   || currentOrder.getPaidTotal() + 0.000001 + currentOrder.getCpnAmt() >= currentOrder.getTotalTaxIncluded());

        },
    });
    
    instance.point_of_sale.OrderWidget.include({
        set_value: function(val) {
            var order = this.pos.get('selectedOrder');
            this.numpad_state = this.pos_widget.numpad.state;
            var mode = this.numpad_state.get('mode');
            if (order.getSelectedLine()) {
                var prod_id = order.getSelectedLine().get_product().id;
                if (order.get('orderLines').length !== 0) {
                    if( mode === 'quantity'){
                        var ret_o_id = order.get_ret_o_id();
                        if (ret_o_id && ret_o_id.toString() != _t('Missing Receipt')) {
                            var self = this;
                            var pids = [];
                            new instance.web.Model("pos.order.line").get_func("search_read")
                                                ([['order_id', '=', ret_o_id],['product_id', '=', prod_id],['return_qty', '>', 0]], 
                                                ['return_qty', 'id']).pipe(
                                function(result) {
                                    if (result && result.length > 0) {
                                        if (result[0].return_qty > 0) {
                                            add_prod = true;
                                            (order.get('orderLines')).each(_.bind( function(item) {
                                                if (prod_id == item.get_product().id && 
                                                    result[0].return_qty < parseInt(val)) {
                                                    var error_str = _t('Can not return more products !');
                                                    var error_dialog = new instance.web.Dialog(this, { 
                                                        size: 'medium',
                                                        buttons: [{text: _t("Close"), click: function() { this.parents('.modal').modal('hide'); }}],
                                                    }).open();
                                                    error_dialog.$el.append(
                                                        '<span id="error_str" style="font-size:18px;">' + error_str + '</span>');
                                                    add_prod = false;
                                                }
                                            }));
                                        }
                                        if (add_prod) {
                                            order.getSelectedLine().set_quantity(val);
                                        }
                                    }
                                }
                            );
                        } else {
                            order.getSelectedLine().set_quantity(val);
                        }
                    }else if( mode === 'discount'){
                        order.getSelectedLine().set_discount(val);
                    }else if( mode === 'price'){
                        order.getSelectedLine().set_unit_price(val);
                    }
                } else {
                    this.pos.get('selectedOrder').destroy();
                }
            }
        },
    });
    
    instance.point_of_sale.PosModel.prototype.models.push({
    	// EQUITANIA: Neues Feld eq_internal_number, damit man danach suchen kann. Dafür wurde auch die Klasse module.PosDB erweitert
        model:  'product.product',
        fields: ['display_name', 'list_price','price','pos_categ_id', 'taxes_id', 'ean13', 'default_code', 'validity_days',
                 'to_weight', 'uom_id', 'uos_id', 'uos_coeff', 'mes_type', 'description_sale', 'description', 'is_coupon',
                 'product_tmpl_id', 'eq_internal_number'],
        domain: [['sale_ok','=',true],['available_in_pos','=',true]],
        context: function(self){ return { pricelist: self.pricelist.id, display_default_code: false }; },
        loaded: function(self, products){
            self.db.add_products(products);
        },
    });
    
    instance.point_of_sale.PosModel = instance.point_of_sale.PosModel.extend({
    	_reformat_coupon_price: function(orderlines){
    		// small helper that reformats couponprice to number with 2 digits
    		for (var i=0; i < orderlines.length; i++){
    			line = orderlines[i];
    			if (line.coupon_serial != undefined){
    				// reformat price
    				line.price = line.price.toFixed(2);    			
    			}    			
    		}    		
    		return orderlines;
    	},
        _save_to_server: function (orders, options) {
            if (!orders || !orders.length) {
                var result = $.Deferred();
                result.resolve([]);
                return result;
            }
                
            options = options || {};

            var self = this;
            var timeout = typeof options.timeout === 'number' ? options.timeout : 7500 * orders.length;

            // we try to send the order. shadow prevents a spinner if it takes too long. (unless we are sending an invoice,
            // then we want to notify the user that we are waiting on something )
            var posOrderModel = new instance.web.Model('pos.order');
            
            var currentOrder = this.get('selectedOrder');
            var coupon_amt = currentOrder.get_coupon_amount();
            var ret_coupon_amt = currentOrder.get_bonus_return_amount();
            var context = {'gift_amount': coupon_amt, 'bonus_amt': ret_coupon_amt};
            
            return posOrderModel.call('create_from_ui',
                [_.map(orders, function (order) {
                    order.to_invoice = options.to_invoice || false;
                    return order;
                }), context],
                undefined,
                {
                    shadow: !options.to_invoice,
                    timeout: timeout
                }
            ).then(function (server_ids) {
            	if (server_ids) {
            		new instance.web.Model("pos.order").get_func("check_connection")().done(function(result) {
                        if (result) {
                        	if (currentOrder.get_recharge_coupon_id()) {
                        		currentOrderLines = currentOrder.get('orderLines');
                                orderLines = [];
                                (currentOrderLines).each(_.bind( function(item) {
                                    new instance.web.Model("pos.coupon.history").get_func("write")(item.get_coupon_history_id(), {'pos_order': orders[0].id.toString()});
                                }, this));
                        	}
                        	if (coupon_amt) {
			            		var coupons = {};
			                    var tr2 = [];
			                    _.each($('span.gift_coupon_serial_input'), function(e) {
			                        if (e['id']) {
			                            serial_id = e['id'].split('_');
			                            id = serial_id[2];
			                            serial = $('#' + e['id']).html();
			                            amount = $('#gift_coupon_input_coupon_amount_' + id).html();
			                            amount = amount.replace(",", ".");
			                            
			                            currentOrder.set_add_gift_coupon(serial);						// DEFAULT
			                            currentOrder.eq_set_add_gift_coupon(serial, amount);			// EQUITANIA			                            
			                            
			                            if (serial && amount) {
			                                coupons[serial] = amount;
			                                tr2.push($("<tr id='prod_info'><td style='text-align:center;'>-- "+ _t("Coupon Information") + " --</td></tr>" +
			                                "<tr id='prod_info'><td style='padding:2px;'>" + _t("Serial No") + ": " + serial + "</td></tr>"));
			                                tr2.push($("<tr id='" + serial + "'><td style='padding: 2px; text-align:center;'><div class='" + serial + "' width='150' height='50'/></td></tr>"));
			                                tr2.push($("<tr id='barcode_number'><td style='padding: 2px;text-align:center;font-size:25px;'>" + serial + "</td></tr>"));
			                            }
			                        }
			                    });
			                    _.each(tr2, function(tr) {
			                        var tr_id = tr.attr('id').toString();
			                        $('table#barcode_table tbody').append(tr);
			                        if (tr_id.length <= 10) {
			                            $('.' + tr_id).barcode(tr_id, "code128")
			                        }
			                    });
			                    $.each(coupons, function(key, value) {
			                        new instance.web.Model("pos.coupon.line").get_func("search_read")([['name', '=', key]], ['id', 'remaining_amt', 'coupon_id']).pipe(
			                            function(result) {
			                                if (result && result[0]) {
			                                    var new_rem_amt = result[0].remaining_amt - value;
			                                    new instance.web.Model("pos.coupon.line").get_func("write")(result[0].id, {'remaining_amt': new_rem_amt});
			                                    new instance.web.Model("pos.coupon.history").get_func("create")({'used_amount':value, 
			                                                                                                    'coupon_id':result[0].coupon_id[0],
			                                                                                                    'name':key,
			                                                                                                    'pos_order': orders[0].id.toString()
			                                                                                                    });
			                                }
			                            }
			                        );
			                    });
			                }
			                if (ret_coupon_amt) {
                                $("span#bonus_coupon_amount").html(ret_coupon_amt);
                                var ret_coupons = {};
                                var tr3 = [];
                                _.each($('span.bonus_coupon_serial_input'), function(e) {
                                    if (e['id']) {
                                        serial_id = e['id'].split('_');
                                        id = serial_id[2];
                                        serial = $('#' + e['id']).html();
                                        amount = $('#bonus_coupon_input_coupon_amount_' + id).html();
                                        if (serial && amount) {
                                        	currentOrder.set_add_bonus_coupon(serial);				// DEFAULT
                                        	currentOrder.eq_set_add_bonus_coupon(serial, amount);				// EQUITANIA
                                        	
                                            ret_coupons[serial] = amount;
                                            tr3.push($("<tr id='prod_info'><td style='text-align:center;'>-- "+ _t("Coupon Information") + " --</td></tr>" +
                                            "<tr id='prod_info'><td style='padding:2px;'>" + _t("Serial No") + ": " + serial + "</td></tr>"));
                                            tr3.push($("<tr id='" + serial + "'><td style='padding: 2px; text-align:center;'><div class='" + serial + "' width='150' height='50'/></td></tr>"));
                                            $('#' + serial.toString()).barcode(serial.toString(), "code128");
                                        }
                                    }
                                });
                                _.each(tr3, function(tr) {
                                    var tr_id = tr.attr('id').toString();
                                    $('table#barcode_table tbody').append(tr);
                                    if (tr_id.length >= 10) {
                                        $('.' + tr_id).barcode(tr_id, "code128")
                                    }
                                });
                                $.each(ret_coupons, function(key, value) {
                                    new instance.web.Model("bonus.return").get_func("search_read")([['name', '=', key]], ['id', 'bonus_remaining_amt']).pipe(
                                        function(result) {
                                            if (result && result[0]) {
                                                var new_rem_amt = result[0].bonus_remaining_amt - value;
                                                new instance.web.Model("bonus.return").get_func("write")(result[0].id, {'bonus_remaining_amt': new_rem_amt});
                                                $('table#remaining_bonus_table').html($("<tr><td style='padding: 2px 0 0 0; font-weight:bold;'>"+ key + " - " + new_rem_amt + "</td></tr>"));
                                                new instance.web.Model("pos.bonus.history").get_func("create")({'used_amount':value, 
                                                                                                                'name':key,
                                                                                                                'bonus_return_id': result[0].id,
                                                                                                                'pos_order': orders[0].id.toString()});
                                            }
                                        });
                                });
			                } else {
			                	if (currentOrder.get_bonus_return_check()) {
	                                var tr4 = [];
	                                var order = currentOrder.export_as_JSON();
	                                var bonus_name = currentOrder.generateUniqueId_barcode();
	                                currentOrder.set_bonus_name(bonus_name);
	                                new instance.web.Model("bonus.return").get_func("create")({'bonus_amount': order.amount_total, 
	                                                                                    'bonus_remaining_amt': order.amount_total,
	                                                                                    'name':bonus_name});
	                                $('#bonus_return_number_span').html(bonus_name);
	                                tr4.push($("<tr id='prod_info'><td style='text-align:center;'>-- "+ _t("Bonus Coupon Information") + " --</td></tr>" +
	                                "<tr id='prod_info'><td style='padding:2px;'>" + _t("Serial No") + ": " + bonus_name + "</td></tr>"));
	                                tr4.push($("<tr id='" + bonus_name + "'><td style='padding: 2px; text-align:center;'><div class='" + bonus_name + "' width='150' height='50'/></td></tr>"));
	                                $('#' + bonus_name.toString()).barcode(bonus_name.toString(), "code128");
	                            }
	                            _.each(tr4, function(tr) {
	                                var tr_id = tr.attr('id').toString();
	                                $('table#barcode_table tbody').append(tr);
	                                if (tr_id.length <= 10) {
	                                    $('.' + tr_id).barcode(tr_id, "code128")
	                                }
	                            });
			                }
			                if(self.config.iface_print_via_proxy){
                                var receipt = currentOrder.export_for_printing();                                
                                
                                // EQ: Added on 07.10.2016 - to be able to reformat price of coupons
                                self._reformat_coupon_price(receipt.orderlines)                                
                                var proxy_receipt = QWeb.render('XmlReceipt',{
                                    receipt: receipt, widget: self,
                                })                                
                                
//                              EQ: Testdialog for Check of print - START, NOTE: !DEACTIVATE BEFORE CHECKIN !
/*                                
                                var dialog = new instance.web.Dialog(self, { 
                                    size: 'medium',
                                    buttons: [{text: _t("Close"), click: function() { self.parents('.modal').modal('hide'); }}],
                                }).open();
                                dialog.$el.html(proxy_receipt);
*/                                
//								EQ: Testdialog for Check of print - END
                                
                                                                         
                                
                                self.proxy.print_receipt(proxy_receipt);
                                
                                self.get('selectedOrder').destroy();    //finish order and go back to scan screen
                                self.get('selectedOrder').set_ret_o_id('')
                                $("span#sale_mode").css('background', 'blue');
                                $("span#return_order").css('background', '');
                                $("span#missing_return_order").css('background', '');
                                $('#return_order_ref').html('');
                                $('#return_order_number').val('');
                            }
                        }
            		});
            	}
                _.each(orders, function (order) {
                    self.db.remove_order(order.id);
                });
                return server_ids;
            }).fail(function (error, event){
                if(error.code === 200 ){    // Business Logic Error, not a connection problem
                    self.pos_widget.screen_selector.show_popup('error-traceback',{
                        message: error.data.message,
                        comment: error.data.debug
                    });
                }
                // prevent an error popup creation by the rpc failure
                // we want the failure to be silent as we send the orders in the background
                event.preventDefault();
                console.error('Failed to send orders:', orders);
            });
        },
    });
}






function openerp_pos_models(instance, module){ //module is instance.point_of_sale
    var QWeb = instance.web.qweb;
	var _t = instance.web._t;

    var round_di = instance.web.round_decimals;
    var round_pr = instance.web.round_precision
    
    // The PosModel contains the Point Of Sale's representation of the backend.
    // Since the PoS must work in standalone ( Without connection to the server ) 
    // it must contains a representation of the server's PoS backend. 
    // (taxes, product list, configuration options, etc.)  this representation
    // is fetched and stored by the PosModel at the initialisation. 
    // this is done asynchronously, a ready deferred alows the GUI to wait interactively 
    // for the loading to be completed 
    // There is a single instance of the PosModel for each Front-End instance, it is usually called
    // 'pos' and is available to all widgets extending PosWidget.

    module.PosModel = Backbone.Model.extend({
        initialize: function(session, attributes) {
            Backbone.Model.prototype.initialize.call(this, attributes);
            var  self = this;
            this.session = session;                 
            this.flush_mutex = new $.Mutex();                   // used to make sure the orders are sent to the server once at time
            this.pos_widget = attributes.pos_widget;

            this.proxy = new module.ProxyDevice(this);              // used to communicate to the hardware devices via a local proxy
            this.barcode_reader = new module.BarcodeReader({'pos': this, proxy:this.proxy, patterns: {}});  // used to read barcodes
            this.proxy_queue = new module.JobQueue();           // used to prevent parallels communications to the proxy
            this.db = new module.PosDB();                       // a local database used to search trough products and categories & store pending orders
            this.debug = jQuery.deparam(jQuery.param.querystring()).debug !== undefined;    //debug mode 
            
            // Business data; loaded from the server at launch
            this.accounting_precision = 2; //TODO
            this.company_logo = null;
            this.company_logo_base64 = '';
            this.currency = null;
            this.shop = null;
            this.company = null;
            this.user = null;
            this.users = [];
            this.partners = [];
            this.cashier = null;
            this.cashregisters = [];
            this.bankstatements = [];
            this.taxes = [];
            this.pos_session = null;
            this.config = null;
            this.units = [];
            this.units_by_id = {};
            this.pricelist = null;
            this.order_sequence = 1;
            window.posmodel = this;

            // these dynamic attributes can be watched for change by other models or widgets
            this.set({
                'synch':            { state:'connected', pending:0 }, 
                'orders':           new module.OrderCollection(),
                'selectedOrder':    null,
            });

            this.bind('change:synch',function(pos,synch){
                clearTimeout(self.synch_timeout);
                self.synch_timeout = setTimeout(function(){
                    if(synch.state !== 'disconnected' && synch.pending > 0){
                        self.set('synch',{state:'disconnected', pending:synch.pending});
                    }
                },3000);
            });

            this.get('orders').bind('remove', function(order,_unused_,options){ 
                self.on_removed_order(order,options.index,options.reason); 
            });
            
            // We fetch the backend data on the server asynchronously. this is done only when the pos user interface is launched,
            // Any change on this data made on the server is thus not reflected on the point of sale until it is relaunched. 
            // when all the data has loaded, we compute some stuff, and declare the Pos ready to be used. 
            this.ready = this.load_server_data()
                .then(function(){
                    if(self.config.use_proxy){
                        return self.connect_to_proxy();
                    }
                });
            
        },

        // releases ressources holds by the model at the end of life of the posmodel
        destroy: function(){
            // FIXME, should wait for flushing, return a deferred to indicate successfull destruction
            // this.flush();
            this.proxy.close();
            this.barcode_reader.disconnect();
            this.barcode_reader.disconnect_from_proxy();
        },
        connect_to_proxy: function(){
            var self = this;
            var  done = new $.Deferred();
            this.barcode_reader.disconnect_from_proxy();
            this.pos_widget.loading_message(_t('Connecting to the PosBox'),0);
            this.pos_widget.loading_skip(function(){
                    self.proxy.stop_searching();
                });
            this.proxy.autoconnect({
                    force_ip: self.config.proxy_ip || undefined,
                    progress: function(prog){ 
                        self.pos_widget.loading_progress(prog);
                    },
                }).then(function(){
                    if(self.config.iface_scan_via_proxy){
                        self.barcode_reader.connect_to_proxy();
                    }
                }).always(function(){
                    done.resolve();
                });
            return done;
        },

        // helper function to load data from the server. Obsolete use the models loader below.
        fetch: function(model, fields, domain, ctx){
            this._load_progress = (this._load_progress || 0) + 0.05; 
            this.pos_widget.loading_message(_t('Loading')+' '+model,this._load_progress);
            return new instance.web.Model(model).query(fields).filter(domain).context(ctx).all()
        },

        // Server side model loaders. This is the list of the models that need to be loaded from
        // the server. The models are loaded one by one by this list's order. The 'loaded' callback
        // is used to store the data in the appropriate place once it has been loaded. This callback
        // can return a deferred that will pause the loading of the next module. 
        // a shared temporary dictionary is available for loaders to communicate private variables
        // used during loading such as object ids, etc. 
        models: [
        {
            model:  'res.users',
            fields: ['name','company_id'],
            ids:    function(self){ return [self.session.uid]; },
            loaded: function(self,users){ self.user = users[0]; },
        },{ 
            model:  'res.company',
            fields: [ 'currency_id', 'email', 'website', 'company_registry', 'vat', 'name', 'phone', 'partner_id' , 'country_id', 'tax_calculation_rounding_method', 'logo'],
            ids:    function(self){ return [self.user.company_id[0]] },
            loaded: function(self,companies){ self.company = companies[0]; },
        },{
            model:  'decimal.precision',
            fields: ['name','digits'],
            loaded: function(self,dps){
                self.dp  = {};
                for (var i = 0; i < dps.length; i++) {
                    self.dp[dps[i].name] = dps[i].digits;
                }
            },
        },{ 
            model:  'product.uom',
            fields: [],
            domain: null,
            context: function(self){ return { active_test: false }; },
            loaded: function(self,units){
                self.units = units;
                var units_by_id = {};
                for(var i = 0, len = units.length; i < len; i++){
                    units_by_id[units[i].id] = units[i];
                    units[i].groupable = ( units[i].category_id[0] === 1 );
                    units[i].is_unit   = ( units[i].id === 1 );
                }
                self.units_by_id = units_by_id;
            }
        },{
            model:  'res.users',
            fields: ['name','ean13'],
            domain: null,
            loaded: function(self,users){ self.users = users; },
        },{
            model:  'res.partner',
            fields: ['name','street','city','state_id','country_id','vat','phone','zip','mobile','email','ean13','write_date'],
            domain: [['customer','=',true]],
            loaded: function(self,partners){
                self.partners = partners;
                self.db.add_partners(partners);
            },
        },{
            model:  'res.country',
            fields: ['name'],
            loaded: function(self,countries){
                self.countries = countries;
                self.company.country = null;
                for (var i = 0; i < countries.length; i++) {
                    if (countries[i].id === self.company.country_id[0]){
                        self.company.country = countries[i];
                    }
                }
            },
        },{
            model:  'account.tax',
            fields: ['name','amount', 'price_include', 'include_base_amount', 'type', 'child_ids', 'child_depend', 'include_base_amount'],
            domain: null,
            loaded: function(self, taxes){
                self.taxes = taxes;
                self.taxes_by_id = {};
                _.each(taxes, function(tax){
                    self.taxes_by_id[tax.id] = tax;
                });
                _.each(self.taxes_by_id, function(tax) {
                    tax.child_taxes = {};
                    _.each(tax.child_ids, function(child_tax_id) {
                        tax.child_taxes[child_tax_id] = self.taxes_by_id[child_tax_id];
                    });
                });
            },
        },{
            model:  'pos.session',
            fields: ['id', 'journal_ids','name','user_id','config_id','start_at','stop_at','sequence_number','login_number'],
            domain: function(self){ return [['state','=','opened'],['user_id','=',self.session.uid]]; },
            loaded: function(self,pos_sessions){
                self.pos_session = pos_sessions[0]; 

                var orders = self.db.get_orders();
                for (var i = 0; i < orders.length; i++) {
                    self.pos_session.sequence_number = Math.max(self.pos_session.sequence_number, orders[i].data.sequence_number+1);
                }
            },
        },{
            model: 'pos.config',
            fields: [],
            domain: function(self){ return [['id','=', self.pos_session.config_id[0]]]; },
            loaded: function(self,configs){
                self.config = configs[0];
                self.config.use_proxy = self.config.iface_payment_terminal || 
                                        self.config.iface_electronic_scale ||
                                        self.config.iface_print_via_proxy  ||
                                        self.config.iface_scan_via_proxy   ||
                                        self.config.iface_cashdrawer;
                
                self.barcode_reader.add_barcode_patterns({
                    'product':  self.config.barcode_product,
                    'cashier':  self.config.barcode_cashier,
                    'client':   self.config.barcode_customer,
                    'weight':   self.config.barcode_weight,
                    'discount': self.config.barcode_discount,
                    'price':    self.config.barcode_price,
                });

                if (self.config.company_id[0] !== self.user.company_id[0]) {
                    throw new Error(_t("Error: The Point of Sale User must belong to the same company as the Point of Sale. You are probably trying to load the point of sale as an administrator in a multi-company setup, with the administrator account set to the wrong company."));
                }
            },
        },{
            model: 'stock.location',
            fields: [],
            ids:    function(self){ return [self.config.stock_location_id[0]]; },
            loaded: function(self, locations){ self.shop = locations[0]; },
        },{
            model:  'product.pricelist',
            fields: ['currency_id'],
            ids:    function(self){ return [self.config.pricelist_id[0]]; },
            loaded: function(self, pricelists){ self.pricelist = pricelists[0]; },
        },{
            model: 'res.currency',
            fields: ['name','symbol','position','rounding','accuracy'],
            ids:    function(self){ return [self.pricelist.currency_id[0]]; },
            loaded: function(self, currencies){
                self.currency = currencies[0];
                if (self.currency.rounding > 0) {
                    self.currency.decimals = Math.ceil(Math.log(1.0 / self.currency.rounding) / Math.log(10));
                } else {
                    self.currency.decimals = 0;
                }

            },
        },{
            model: 'product.packaging',
            fields: ['ean','product_tmpl_id'],
            domain: null,
            loaded: function(self, packagings){ 
                self.db.add_packagings(packagings);
            },
        },{
            model:  'pos.category',
            fields: ['id','name','parent_id','child_id','image'],
            domain: null,
            loaded: function(self, categories){
                self.db.add_categories(categories);
            },
        },{
            model:  'product.product',
            fields: ['display_name', 'list_price','price','pos_categ_id', 'taxes_id', 'ean13', 'default_code', 
                     'to_weight', 'uom_id', 'uos_id', 'uos_coeff', 'mes_type', 'description_sale', 'description',
                     'product_tmpl_id'],
            domain: [['sale_ok','=',true],['available_in_pos','=',true]],
            context: function(self){ return { pricelist: self.pricelist.id, display_default_code: false }; },
            loaded: function(self, products){
                self.db.add_products(products);
            },
        },{
            model:  'account.bank.statement',
            fields: ['account_id','currency','journal_id','state','name','user_id','pos_session_id'],
            domain: function(self){ return [['state', '=', 'open'],['pos_session_id', '=', self.pos_session.id]]; },
            loaded: function(self, bankstatements, tmp){
                self.bankstatements = bankstatements;

                tmp.journals = [];
                _.each(bankstatements,function(statement){
                    tmp.journals.push(statement.journal_id[0]);
                });
            },
        },{
            model:  'account.journal',
            fields: [],
            domain: function(self,tmp){ return [['id','in',tmp.journals]]; },
            loaded: function(self, journals){
                self.journals = journals;

                // associate the bank statements with their journals. 
                var bankstatements = self.bankstatements;
                for(var i = 0, ilen = bankstatements.length; i < ilen; i++){
                    for(var j = 0, jlen = journals.length; j < jlen; j++){
                        if(bankstatements[i].journal_id[0] === journals[j].id){
                            bankstatements[i].journal = journals[j];
                        }
                    }
                }
                self.cashregisters = bankstatements;
            },
        },{
            label: 'fonts',
            loaded: function(self){
                var fonts_loaded = new $.Deferred();

                // Waiting for fonts to be loaded to prevent receipt printing
                // from printing empty receipt while loading Inconsolata
                // ( The font used for the receipt ) 
                waitForWebfonts(['Lato','Inconsolata'], function(){
                    fonts_loaded.resolve();
                });

                // The JS used to detect font loading is not 100% robust, so
                // do not wait more than 5sec
                setTimeout(function(){
                    fonts_loaded.resolve();
                },5000);

                return fonts_loaded;
            },
        },{
            label: 'pictures',
            loaded: function(self){
                self.company_logo = new Image();
                var  logo_loaded = new $.Deferred();
                self.company_logo.onload = function(){
                    var img = self.company_logo;
                    var ratio = 1;
                    var targetwidth = 300;
                    var maxheight = 150;
                    if( img.width !== targetwidth ){
                        ratio = targetwidth / img.width;
                    }
                    if( img.height * ratio > maxheight ){
                        ratio = maxheight / img.height;
                    }
                    var width  = Math.floor(img.width * ratio);
                    var height = Math.floor(img.height * ratio);
                    var c = document.createElement('canvas');
                        c.width  = width;
                        c.height = height
                    var ctx = c.getContext('2d');
                        ctx.drawImage(self.company_logo,0,0, width, height);

                    self.company_logo_base64 = c.toDataURL();
                    logo_loaded.resolve();
                };
                self.company_logo.onerror = function(){
                    logo_loaded.reject();
                };
                    self.company_logo.crossOrigin = "anonymous";
                self.company_logo.src = '/web/binary/company_logo' +'?dbname=' + self.session.db + '&_'+Math.random();

                return logo_loaded;
            },
        },
        ],

        // loads all the needed data on the sever. returns a deferred indicating when all the data has loaded. 
        load_server_data: function(){
            var self = this;
            var loaded = new $.Deferred();
            var progress = 0;
            var progress_step = 1.0 / self.models.length;
            var tmp = {}; // this is used to share a temporary state between models loaders

            function load_model(index){
                if(index >= self.models.length){
                    loaded.resolve();
                }else{
                    var model = self.models[index];
                    self.pos_widget.loading_message(_t('Loading')+' '+(model.label || model.model || ''), progress);
                    var fields =  typeof model.fields === 'function'  ? model.fields(self,tmp)  : model.fields;
                    var domain =  typeof model.domain === 'function'  ? model.domain(self,tmp)  : model.domain;
                    var context = typeof model.context === 'function' ? model.context(self,tmp) : model.context; 
                    var ids     = typeof model.ids === 'function'     ? model.ids(self,tmp) : model.ids;
                    progress += progress_step;
                    

                    if( model.model ){
                        if (model.ids) {
                            var records = new instance.web.Model(model.model).call('read',[ids,fields],context);
                        } else {
                            var records = new instance.web.Model(model.model).query(fields).filter(domain).context(context).all()
                        }
                        records.then(function(result){
                                try{    // catching exceptions in model.loaded(...)
                                    $.when(model.loaded(self,result,tmp))
                                        .then(function(){ load_model(index + 1); },
                                              function(err){ loaded.reject(err); });
                                }catch(err){
                                    loaded.reject(err);
                                }
                            },function(err){
                                loaded.reject(err);
                            });
                    }else if( model.loaded ){
                        try{    // catching exceptions in model.loaded(...)
                            $.when(model.loaded(self,tmp))
                                .then(  function(){ load_model(index +1); },
                                        function(err){ loaded.reject(err); });
                        }catch(err){
                            loaded.reject(err);
                        }
                    }else{
                        load_model(index + 1);
                    }
                }
            }

            try{
                load_model(0);
            }catch(err){
                loaded.reject(err);
            }

            return loaded;
        },

        // reload the list of partner, returns as a deferred that resolves if there were
        // updated partners, and fails if not
        load_new_partners: function(){
            var self = this;
            var def  = new $.Deferred();
            var fields = _.find(this.models,function(model){ return model.model === 'res.partner'; }).fields;
            new instance.web.Model('res.partner')
                .query(fields)
                .filter([['write_date','>',this.db.get_partner_write_date()]])
                .all({'timeout':3000, 'shadow': true})
                .then(function(partners){
                    if (self.db.add_partners(partners)) {   // check if the partners we got were real updates
                        def.resolve();
                    } else {
                        def.reject();
                    }
                }, function(err,event){ event.preventDefault(); def.reject(); });    
            return def;
        },

        // this is called when an order is removed from the order collection. It ensures that there is always an existing
        // order and a valid selected order
        on_removed_order: function(removed_order,index,reason){
            if( (reason === 'abandon' || removed_order.temporary) && this.get('orders').size() > 0){
                // when we intentionally remove an unfinished order, and there is another existing one
                this.set({'selectedOrder' : this.get('orders').at(index) || this.get('orders').last()});
            }else{
                // when the order was automatically removed after completion, 
                // or when we intentionally delete the only concurrent order
                this.add_new_order();
            }
        },

        //creates a new empty order and sets it as the current order
        add_new_order: function(){
            var order = new module.Order({pos:this});
            this.get('orders').add(order);
            this.set('selectedOrder', order);
        },

        get_order: function(){
            return this.get('selectedOrder');
        },

        //removes the current order
        delete_current_order: function(){
            this.get('selectedOrder').destroy({'reason':'abandon'});
        },

        // saves the order locally and try to send it to the backend. 
        // it returns a deferred that succeeds after having tried to send the order and all the other pending orders.
        push_order: function(order) {
            var self = this;

            if(order){
                this.proxy.log('push_order',order.export_as_JSON());
                this.db.add_order(order.export_as_JSON());
            }
            
            var pushed = new $.Deferred();

            this.flush_mutex.exec(function(){
                var flushed = self._flush_orders(self.db.get_orders());

                flushed.always(function(ids){
                    pushed.resolve();
                });
            });
            return pushed;
        },

        // saves the order locally and try to send it to the backend and make an invoice
        // returns a deferred that succeeds when the order has been posted and successfully generated
        // an invoice. This method can fail in various ways:
        // error-no-client: the order must have an associated partner_id. You can retry to make an invoice once
        //     this error is solved
        // error-transfer: there was a connection error during the transfer. You can retry to make the invoice once
        //     the network connection is up 

        push_and_invoice_order: function(order){
            var self = this;
            var invoiced = new $.Deferred(); 

            if(!order.get_client()){
                invoiced.reject('error-no-client');
                return invoiced;
            }

            var order_id = this.db.add_order(order.export_as_JSON());

            this.flush_mutex.exec(function(){
                var done = new $.Deferred(); // holds the mutex

                // send the order to the server
                // we have a 30 seconds timeout on this push.
                // FIXME: if the server takes more than 30 seconds to accept the order,
                // the client will believe it wasn't successfully sent, and very bad
                // things will happen as a duplicate will be sent next time
                // so we must make sure the server detects and ignores duplicated orders

                var transfer = self._flush_orders([self.db.get_order(order_id)], {timeout:30000, to_invoice:true});
                
                transfer.fail(function(){
                    invoiced.reject('error-transfer');
                    done.reject();
                });

                // on success, get the order id generated by the server
                transfer.pipe(function(order_server_id){    

                    // generate the pdf and download it
                    self.pos_widget.do_action('point_of_sale.pos_invoice_report',{additional_context:{ 
                        active_ids:order_server_id,
                    }});

                    invoiced.resolve();
                    done.resolve();
                });

                return done;

            });

            return invoiced;
        },

        // wrapper around the _save_to_server that updates the synch status widget
        _flush_orders: function(orders, options) {
            var self = this;

            this.set('synch',{ state: 'connecting', pending: orders.length});

            return self._save_to_server(orders, options).done(function (server_ids) {
                var pending = self.db.get_orders().length;

                self.set('synch', {
                    state: pending ? 'connecting' : 'connected',
                    pending: pending
                });

                return server_ids;
            });
        },

        // send an array of orders to the server
        // available options:
        // - timeout: timeout for the rpc call in ms
        // returns a deferred that resolves with the list of
        // server generated ids for the sent orders
        _save_to_server: function (orders, options) {
            if (!orders || !orders.length) {
                var result = $.Deferred();
                result.resolve([]);
                return result;
            }
                
            options = options || {};

            var self = this;
            var timeout = typeof options.timeout === 'number' ? options.timeout : 7500 * orders.length;

            // we try to send the order. shadow prevents a spinner if it takes too long. (unless we are sending an invoice,
            // then we want to notify the user that we are waiting on something )
            var posOrderModel = new instance.web.Model('pos.order');
            return posOrderModel.call('create_from_ui',
                [_.map(orders, function (order) {
                    order.to_invoice = options.to_invoice || false;
                    return order;
                })],
                undefined,
                {
                    shadow: !options.to_invoice,
                    timeout: timeout
                }
            ).then(function (server_ids) {
                _.each(orders, function (order) {
                    self.db.remove_order(order.id);
                });
                return server_ids;
            }).fail(function (error, event){
                if(error.code === 200 ){    // Business Logic Error, not a connection problem
                    self.pos_widget.screen_selector.show_popup('error-traceback',{
                        message: error.data.message,
                        comment: error.data.debug
                    });
                }
                // prevent an error popup creation by the rpc failure
                // we want the failure to be silent as we send the orders in the background
                event.preventDefault();
                console.error('Failed to send orders:', orders);
            });
        },

        scan_product: function(parsed_code){
            var self = this;
            var selectedOrder = this.get('selectedOrder');
            if(parsed_code.encoding === 'ean13'){
                var product = this.db.get_product_by_ean13(parsed_code.base_code);
            }else if(parsed_code.encoding === 'reference'){
                var product = this.db.get_product_by_reference(parsed_code.code);
            }

            if(!product){
                return false;
            }

            if(parsed_code.type === 'price'){
                selectedOrder.addProduct(product, {price:parsed_code.value});
            }else if(parsed_code.type === 'weight'){
                selectedOrder.addProduct(product, {quantity:parsed_code.value, merge:false});
            }else if(parsed_code.type === 'discount'){
                selectedOrder.addProduct(product, {discount:parsed_code.value, merge:false});
            }else{
                selectedOrder.addProduct(product);
            }
            return true;
        },
    });

    var orderline_id = 1;

    // An orderline represent one element of the content of a client's shopping cart.
    // An orderline contains a product, its quantity, its price, discount. etc. 
    // An Order contains zero or more Orderlines.
    module.Orderline = Backbone.Model.extend({
        initialize: function(attr,options){
            this.pos = options.pos;
            this.order = options.order;
            this.product = options.product;
            this.price   = options.product.price;
            this.set_quantity(1);
            this.discount = 0;
            this.discountStr = '0';
            this.type = 'unit';
            this.selected = false;
            this.id       = orderline_id++; 
        },
        clone: function(){
            var orderline = new module.Orderline({},{
                pos: this.pos,
                order: null,
                product: this.product,
                price: this.price,
            });
            orderline.quantity = this.quantity;
            orderline.quantityStr = this.quantityStr;
            orderline.discount = this.discount;
            orderline.type = this.type;
            orderline.selected = false;
            return orderline;
        },
        // sets a discount [0,100]%
        set_discount: function(discount){
            var disc = Math.min(Math.max(parseFloat(discount) || 0, 0),100);
            this.discount = disc;
            this.discountStr = '' + disc;
            this.trigger('change',this);
        },
        // returns the discount [0,100]%
        get_discount: function(){
            return this.discount;
        },
        get_discount_str: function(){
            return this.discountStr;
        },
        get_product_type: function(){
            return this.type;
        },
        // sets the quantity of the product. The quantity will be rounded according to the 
        // product's unity of measure properties. Quantities greater than zero will not get 
        // rounded to zero
        set_quantity: function(quantity){
            if(quantity === 'remove'){
                this.order.removeOrderline(this);
                return;
            }else{
                var quant = parseFloat(quantity) || 0;
                var unit = this.get_unit();
                if(unit){
                    if (unit.rounding) {
                        this.quantity    = round_pr(quant, unit.rounding);
                        var decimals = Math.ceil(Math.log(1.0 / unit.rounding) / Math.log(10));
                        this.quantityStr = openerp.instances[this.pos.session.name].web.format_value(this.quantity, { type: 'float', digits: [69, decimals]});
                    } else {
                        this.quantity    = round_pr(quant, 1);
                        this.quantityStr = this.quantity.toFixed(0);
                    }
                }else{
                    this.quantity    = quant;
                    this.quantityStr = '' + this.quantity;
                }
            }
            this.trigger('change',this);
        },
        // return the quantity of product
        get_quantity: function(){
            return this.quantity;
        },
        get_quantity_str: function(){
            return this.quantityStr;
        },
        get_quantity_str_with_unit: function(){
            var unit = this.get_unit();
            if(unit && !unit.is_unit){
                return this.quantityStr + ' ' + unit.name;
            }else{
                return this.quantityStr;
            }
        },
        // return the unit of measure of the product
        get_unit: function(){
            var unit_id = this.product.uom_id;
            if(!unit_id){
                return undefined;
            }
            unit_id = unit_id[0];
            if(!this.pos){
                return undefined;
            }
            return this.pos.units_by_id[unit_id];
        },
        // return the product of this orderline
        get_product: function(){
            return this.product;
        },
        // selects or deselects this orderline
        set_selected: function(selected){
            this.selected = selected;
            this.trigger('change',this);
        },
        // returns true if this orderline is selected
        is_selected: function(){
            return this.selected;
        },
        // when we add an new orderline we want to merge it with the last line to see reduce the number of items
        // in the orderline. This returns true if it makes sense to merge the two
        can_be_merged_with: function(orderline){
            if( this.get_product().id !== orderline.get_product().id){    //only orderline of the same product can be merged
                return false;
            }else if(!this.get_unit() || !this.get_unit().groupable){
                return false;
            }else if(this.get_product_type() !== orderline.get_product_type()){
                return false;
            }else if(this.get_discount() > 0){             // we don't merge discounted orderlines
                return false;
            }else if(this.price !== orderline.price){
                return false;
            }else{ 
                return true;
            }
        },
        merge: function(orderline){
            this.set_quantity(this.get_quantity() + orderline.get_quantity());
        },
        export_as_JSON: function() {
            return {
                qty: this.get_quantity(),
                price_unit: this.get_unit_price(),
                discount: this.get_discount(),
                product_id: this.get_product().id,
            };
        },
        //used to create a json of the ticket, to be sent to the printer
        export_for_printing: function(){
            return {
                quantity:           this.get_quantity(),
                unit_name:          this.get_unit().name,
                price:              this.get_unit_price(),
                discount:           this.get_discount(),
                product_name:       this.get_product().display_name,
                price_display :     this.get_display_price(),
                price_with_tax :    this.get_price_with_tax(),
                price_without_tax:  this.get_price_without_tax(),
                tax:                this.get_tax(),
                product_description:      this.get_product().description,
                product_description_sale: this.get_product().description_sale,
            };
        },
        // changes the base price of the product for this orderline
        set_unit_price: function(price){
            this.price = round_di(parseFloat(price) || 0, this.pos.dp['Product Price']);
            this.trigger('change',this);
        },
        get_unit_price: function(){
            //return round_di(this.price || 0, this.pos.dp['Product Price'])
        	var result = round_di(this.price || 0, this.pos.dp['Product Price'])
        	console.log("result: " + result);
        	console.log(type(result));
        	return result
        },
        get_base_price:    function(){
            var rounding = this.pos.currency.rounding;
            return round_pr(this.get_unit_price() * this.get_quantity() * (1 - this.get_discount()/100), rounding);
        },
        get_display_price: function(){
            var result = this.get_base_price();
            console.log("Check1: ", result);
            return result;
        	//return this.get_base_price();
        },
        get_price_without_tax: function(){
            return this.get_all_prices().priceWithoutTax;
        },
        get_price_with_tax: function(){
            return this.get_all_prices().priceWithTax;
        },
        get_tax: function(){
            return this.get_all_prices().tax;
        },
        get_applicable_taxes: function(){
            // Shenaningans because we need
            // to keep the taxes ordering.
            var ptaxes_ids = this.get_product().taxes_id;
            var ptaxes_set = {};
            for (var i = 0; i < ptaxes_ids.length; i++) {
                ptaxes_set[ptaxes_ids[i]] = true;
            }
            var taxes = [];
            for (var i = 0; i < this.pos.taxes.length; i++) {
                if (ptaxes_set[this.pos.taxes[i].id]) {
                    taxes.push(this.pos.taxes[i]);
                }
            }
            return taxes;
        },
        get_tax_details: function(){
            return this.get_all_prices().taxDetails;
        },
        compute_all: function(taxes, price_unit) {
            var self = this;
            var res = [];
            var currency_rounding = this.pos.currency.rounding;
            if (this.pos.company.tax_calculation_rounding_method == "round_globally"){
               currency_rounding = currency_rounding * 0.00001;
            }
            var base = price_unit;
            _(taxes).each(function(tax) {
                if (tax.price_include) {
                    if (tax.type === "percent") {
                        tmp =  round_pr(base - round_pr(base / (1 + tax.amount),currency_rounding),currency_rounding);
                        data = {amount:tmp, price_include:true, id: tax.id};
                        res.push(data);
                    } else if (tax.type === "fixed") {
                        tmp = tax.amount * self.get_quantity();
                        data = {amount:tmp, price_include:true, id: tax.id};
                        res.push(data);
                    } else {
                        throw "This type of tax is not supported by the point of sale: " + tax.type;
                    }
                } else {
                    if (tax.type === "percent") {
                        tmp = round_pr(tax.amount * base, currency_rounding);
                        data = {amount:tmp, price_include:false, id: tax.id};
                        res.push(data);
                    } else if (tax.type === "fixed") {
                        tmp = tax.amount * self.get_quantity();
                        data = {amount:tmp, price_include:false, id: tax.id};
                        res.push(data);
                    } else {
                        throw "This type of tax is not supported by the point of sale: " + tax.type;
                    }

                    var base_amount = data.amount;
                    var child_amount = 0.0;
                    if (tax.child_depend) {
                        res.pop(); // do not use parent tax
                        child_tax = self.compute_all(tax.child_taxes, base_amount);
                        res.push(child_tax);
                        _(child_tax).each(function(child) {
                            child_amount += child.amount;
                        });
                    }
                    if (tax.include_base_amount) {
                        base += base_amount + child_amount;
                    }
                }
            });
            return res;
        },
        get_all_prices: function(){
            var base = round_pr(this.get_quantity() * this.get_unit_price() * (1.0 - (this.get_discount() / 100.0)), this.pos.currency.rounding);
            var totalTax = base;
            var totalNoTax = base;
            var taxtotal = 0;

            var product =  this.get_product();
            var taxes_ids = product.taxes_id;
            var taxes =  this.pos.taxes;
            var taxdetail = {};
            var product_taxes = [];

            _(taxes_ids).each(function(el){
                product_taxes.push(_.detect(taxes, function(t){
                    return t.id === el;
                }));
            });

            var all_taxes = _(this.compute_all(product_taxes, base)).flatten();

            _(all_taxes).each(function(tax) {
                if (tax.price_include) {
                    totalNoTax -= tax.amount;
                } else {
                    totalTax += tax.amount;
                }
                taxtotal += tax.amount;
                taxdetail[tax.id] = tax.amount;
            });
            totalNoTax = round_pr(totalNoTax, this.pos.currency.rounding);

            return {
                "priceWithTax": totalTax,
                "priceWithoutTax": totalNoTax,
                "tax": taxtotal,
                "taxDetails": taxdetail,
            };
        },
    });

    module.OrderlineCollection = Backbone.Collection.extend({
        model: module.Orderline,
    });

    
    module.PaymentlineCollection = Backbone.Collection.extend({
        model: module.Paymentline,
    });
    
    
    
    // Every Paymentline contains a cashregister and an amount of money.
    module.Paymentline = Backbone.Model.extend({
        initialize: function(attributes, options) {
            this.amount = 0;
            this.cashregister = options.cashregister;
            this.name = this.cashregister.journal_id[1];
            this.selected = false;
            this.pos = options.pos;
        },
        //sets the amount of money on this payment line
        set_amount: function(value){
            this.amount = round_di(parseFloat(value) || 0, this.pos.currency.decimals);
            this.trigger('change:amount',this);
        },
        // returns the amount of money on this paymentline
        get_amount: function(){
            return this.amount;
        },
        get_amount_str: function(){
            return openerp.instances[this.pos.session.name].web.format_value(this.amount, {
                type: 'float', digits: [69, this.pos.currency.decimals]
            });
        },
        set_selected: function(selected){
            if(this.selected !== selected){
                this.selected = selected;
                this.trigger('change:selected',this);
            }
        },
        // returns the payment type: 'cash' | 'bank'
        get_type: function(){
            return this.cashregister.journal.type
        },
        // returns the associated cashregister
        //exports as JSON for server communication
        export_as_JSON: function(){
            return {
                name: instance.web.datetime_to_str(new Date()),
                statement_id: this.cashregister.id,
                account_id: this.cashregister.account_id[0],
                journal_id: this.cashregister.journal_id[0],
                amount: this.get_amount()
            };
        },
        //exports as JSON for receipt printing
        export_for_printing: function(){        	        	
            return {            	
                amount: this.get_amount(),
                journal: this.cashregister.journal_id[1],
            };
        },
    });

    /*
    module.PaymentlineCollection = Backbone.Collection.extend({
        model: module.Paymentline,
    });
    */

    // An order more or less represents the content of a client's shopping cart (the OrderLines) 
    // plus the associated payment information (the Paymentlines) 
    // there is always an active ('selected') order in the Pos, a new one is created
    // automaticaly once an order is completed and sent to the server.
    module.Order = Backbone.Model.extend({
        initialize: function(attributes){
            Backbone.Model.prototype.initialize.apply(this, arguments);
            this.pos = attributes.pos; 
            this.sequence_number = this.pos.pos_session.sequence_number++;
            this.uid =     this.generateUniqueId();
            this.set({
                creationDate:   new Date(),
                orderLines:     new module.OrderlineCollection(),
                paymentLines:   new module.PaymentlineCollection(),
                name:           _t("Order ") + this.uid,
                client:         null,
            });
            this.selected_orderline   = undefined;
            this.selected_paymentline = undefined;
            this.screen_data = {};  // see ScreenSelector
            this.receipt_type = 'receipt';  // 'receipt' || 'invoice'
            this.temporary = attributes.temporary || false;
            return this;
        },
        is_empty: function(){
            return (this.get('orderLines').models.length === 0);
        },
        // Generates a public identification number for the order.
        // The generated number must be unique and sequential. They are made 12 digit long
        // to fit into EAN-13 barcodes, should it be needed 
        generateUniqueId: function() {
            function zero_pad(num,size){
                var s = ""+num;
                while (s.length < size) {
                    s = "0" + s;
                }
                return s;
            }
            return zero_pad(this.pos.pos_session.id,5) +'-'+
                   zero_pad(this.pos.pos_session.login_number,3) +'-'+
                   zero_pad(this.sequence_number,4);
        },
        addOrderline: function(line){
            if(line.order){
                line.order.removeOrderline(line);
            }
            line.order = this;
            this.get('orderLines').add(line);
            this.selectLine(this.getLastOrderline());
        },
        addProduct: function(product, options){
            if(this._printed){
                this.destroy();
                return this.pos.get('selectedOrder').addProduct(product, options);
            }
            options = options || {};
            var attr = JSON.parse(JSON.stringify(product));
            attr.pos = this.pos;
            attr.order = this;
            var line = new module.Orderline({}, {pos: this.pos, order: this, product: product});

            if(options.quantity !== undefined){
                line.set_quantity(options.quantity);
            }
            if(options.price !== undefined){
                line.set_unit_price(options.price);
            }
            if(options.discount !== undefined){
                line.set_discount(options.discount);
            }

            var last_orderline = this.getLastOrderline();
            if( last_orderline && last_orderline.can_be_merged_with(line) && options.merge !== false){
                last_orderline.merge(line);
            }else{
                this.get('orderLines').add(line);
            }
            this.selectLine(this.getLastOrderline());
        },
        removeOrderline: function( line ){
            this.get('orderLines').remove(line);
            this.selectLine(this.getLastOrderline());
        },
        getOrderline: function(id){
            var orderlines = this.get('orderLines').models;
            for(var i = 0; i < orderlines.length; i++){
                if(orderlines[i].id === id){
                    return orderlines[i];
                }
            }
            return null;
        },
        getLastOrderline: function(){
            return this.get('orderLines').at(this.get('orderLines').length -1);
        },
        addPaymentline: function(cashregister) {
            var paymentLines = this.get('paymentLines');
            var newPaymentline = new module.Paymentline({},{cashregister:cashregister, pos:this.pos});
            if(cashregister.journal.type !== 'cash'){
                newPaymentline.set_amount( Math.max(this.getDueLeft(),0) );
            }
            paymentLines.add(newPaymentline);
            this.selectPaymentline(newPaymentline);

        },
        removePaymentline: function(line){
            if(this.selected_paymentline === line){
                this.selectPaymentline(undefined);
            }
            this.get('paymentLines').remove(line);
        },
        getName: function() {
            return this.get('name');
        },
        getSubtotal : function(){
            return round_pr((this.get('orderLines')).reduce((function(sum, orderLine){
                return sum + orderLine.get_display_price();
            }), 0), this.pos.currency.rounding);
        },
        getTotalTaxIncluded: function() {
            return this.getTotalTaxExcluded() + this.getTax();
        },
        getDiscountTotal: function() {
            return round_pr((this.get('orderLines')).reduce((function(sum, orderLine) {
                return sum + (orderLine.get_unit_price() * (orderLine.get_discount()/100) * orderLine.get_quantity());
            }), 0), this.pos.currency.rounding);
        },
        getTotalTaxExcluded: function() {
            return round_pr((this.get('orderLines')).reduce((function(sum, orderLine) {
                return sum + orderLine.get_price_without_tax();
            }), 0), this.pos.currency.rounding);
        },
        getTax: function() {
            return round_pr((this.get('orderLines')).reduce((function(sum, orderLine) {
                return sum + orderLine.get_tax();
            }), 0), this.pos.currency.rounding);
        },
        getTaxDetails: function(){
            var details = {};
            var fulldetails = [];

            this.get('orderLines').each(function(line){
                var ldetails = line.get_tax_details();
                for(var id in ldetails){
                    if(ldetails.hasOwnProperty(id)){
                        details[id] = (details[id] || 0) + ldetails[id];
                    }
                }
            });
            
            for(var id in details){
                if(details.hasOwnProperty(id)){
                    fulldetails.push({amount: details[id], tax: this.pos.taxes_by_id[id], name: this.pos.taxes_by_id[id].name});
                }
            }

            return fulldetails;
        },
        getPaidTotal: function() {
            return round_pr((this.get('paymentLines')).reduce((function(sum, paymentLine) {
                return sum + paymentLine.get_amount();
            }), 0), this.pos.currency.rounding);
        },
        getChange: function() {
            return this.getPaidTotal() - this.getTotalTaxIncluded();
        },
        getDueLeft: function() {
            return this.getTotalTaxIncluded() - this.getPaidTotal();
        },
        // sets the type of receipt 'receipt'(default) or 'invoice'
        set_receipt_type: function(type){
            this.receipt_type = type;
        },
        get_receipt_type: function(){
            return this.receipt_type;
        },
        // the client related to the current order.
        set_client: function(client){
            this.set('client',client);
        },
        get_client: function(){
            return this.get('client');
        },
        get_client_name: function(){
            var client = this.get('client');
            return client ? client.name : "";
        },
        // the order also stores the screen status, as the PoS supports
        // different active screens per order. This method is used to
        // store the screen status.
        set_screen_data: function(key,value){
            if(arguments.length === 2){
                this.screen_data[key] = value;
            }else if(arguments.length === 1){
                for(key in arguments[0]){
                    this.screen_data[key] = arguments[0][key];
                }
            }
        },
        //see set_screen_data
        get_screen_data: function(key){
            return this.screen_data[key];
        },
        // exports a JSON for receipt printing
        export_for_printing: function(){
            var orderlines = [];
            this.get('orderLines').each(function(orderline){
                orderlines.push(orderline.export_for_printing());
            });            
            var paymentlines = [];
            this.get('paymentLines').each(function(paymentline){
                paymentlines.push(paymentline.export_for_printing());
            });
            var client  = this.get('client');
            var cashier = this.pos.cashier || this.pos.user;
            var company = this.pos.company;
            var shop    = this.pos.shop;
            var date = new Date();

            return {
                orderlines: orderlines,
                paymentlines: paymentlines,
                subtotal: this.getSubtotal(),
                total_with_tax: this.getTotalTaxIncluded(),
                total_without_tax: this.getTotalTaxExcluded(),
                total_tax: this.getTax(),
                total_paid: this.getPaidTotal(),
                total_discount: this.getDiscountTotal(),
                tax_details: this.getTaxDetails(),
                change: this.getChange(),
                name : this.getName(),
                client: client ? client.name : null ,
                invoice_id: null,   //TODO
                cashier: cashier ? cashier.name : null,
                header: this.pos.config.receipt_header || '',
                footer: this.pos.config.receipt_footer || '',
                precision: {
                    price: 2,
                    money: 2,
                    quantity: 3,
                },
                date: { 
                    year: date.getFullYear(), 
                    month: date.getMonth(), 
                    date: date.getDate(),       // day of the month 
                    day: date.getDay(),         // day of the week 
                    hour: date.getHours(), 
                    minute: date.getMinutes() ,
                    isostring: date.toISOString(),
                    localestring: date.toLocaleString(),
                }, 
                company:{
                    email: company.email,
                    website: company.website,
                    company_registry: company.company_registry,
                    contact_address: company.partner_id[1], 
                    vat: company.vat,
                    name: company.name,
                    phone: company.phone,
                    logo:  this.pos.company_logo_base64,
                },
                shop:{
                    name: shop.name,
                },
                currency: this.pos.currency,
            };
        },
        export_as_JSON: function() {
            var orderLines, paymentLines;
            orderLines = [];
            (this.get('orderLines')).each(_.bind( function(item) {
                return orderLines.push([0, 0, item.export_as_JSON()]);
            }, this));
            paymentLines = [];
            (this.get('paymentLines')).each(_.bind( function(item) {
                return paymentLines.push([0, 0, item.export_as_JSON()]);
            }, this));
            return {
                name: this.getName(),
                amount_paid: this.getPaidTotal(),
                amount_total: this.getTotalTaxIncluded(),
                amount_tax: this.getTax(),
                amount_return: this.getChange(),
                lines: orderLines,
                statement_ids: paymentLines,
                pos_session_id: this.pos.pos_session.id,
                partner_id: this.get_client() ? this.get_client().id : false,
                user_id: this.pos.cashier ? this.pos.cashier.id : this.pos.user.id,
                uid: this.uid,
                sequence_number: this.sequence_number,
            };
        },
        getSelectedLine: function(){
            return this.selected_orderline;
        },
        selectLine: function(line){
            if(line){
                if(line !== this.selected_orderline){
                    if(this.selected_orderline){
                        this.selected_orderline.set_selected(false);
                    }
                    this.selected_orderline = line;
                    this.selected_orderline.set_selected(true);
                }
            }else{
                this.selected_orderline = undefined;
            }
        },
        deselectLine: function(){
            if(this.selected_orderline){
                this.selected_orderline.set_selected(false);
                this.selected_orderline = undefined;
            }
        },
        selectPaymentline: function(line){
            if(line !== this.selected_paymentline){
                if(this.selected_paymentline){
                    this.selected_paymentline.set_selected(false);
                }
                this.selected_paymentline = line;
                if(this.selected_paymentline){
                    this.selected_paymentline.set_selected(true);
                }
                this.trigger('change:selected_paymentline',this.selected_paymentline);
            }
        },
    });

    module.OrderCollection = Backbone.Collection.extend({
        model: module.Order,
    });

    /*
     The numpad handles both the choice of the property currently being modified
     (quantity, price or discount) and the edition of the corresponding numeric value.
     */
    module.NumpadState = Backbone.Model.extend({
        defaults: {
            buffer: "0",
            mode: "quantity"
        },
        appendNewChar: function(newChar) {
            var oldBuffer;
            oldBuffer = this.get('buffer');
            if (oldBuffer === '0') {
                this.set({
                    buffer: newChar
                });
            } else if (oldBuffer === '-0') {
                this.set({
                    buffer: "-" + newChar
                });
            } else {
                this.set({
                    buffer: (this.get('buffer')) + newChar
                });
            }
            this.trigger('set_value',this.get('buffer'));
        },
        deleteLastChar: function() {
            if(this.get('buffer') === ""){
                if(this.get('mode') === 'quantity'){
                    this.trigger('set_value','remove');
                }else{
                    this.trigger('set_value',this.get('buffer'));
                }
            }else{
                var newBuffer = this.get('buffer').slice(0,-1) || "";
                this.set({ buffer: newBuffer });
                this.trigger('set_value',this.get('buffer'));
            }
        },
        switchSign: function() {
            var oldBuffer;
            oldBuffer = this.get('buffer');
            this.set({
                buffer: oldBuffer[0] === '-' ? oldBuffer.substr(1) : "-" + oldBuffer 
            });
            this.trigger('set_value',this.get('buffer'));
        },
        changeMode: function(newMode) {
            this.set({
                buffer: "0",
                mode: newMode
            });
        },
        reset: function() {
            this.set({
                buffer: "0",
                mode: "quantity"
            });
        },
        resetValue: function(){
            this.set({buffer:'0'});
        },
    });
}
