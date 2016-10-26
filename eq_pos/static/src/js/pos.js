openerp.eq_pos = function (instance) {
    var _t = instance.web._t;
    var QWeb = instance.web.qweb;
    
    var round_di = instance.web.round_decimals;
    var round_pr = instance.web.round_precision;
    var module = instance.point_of_sale;
    
    // EQUITANIA: Extension of default functionality of module.posDB from db.js
    //-------------------- START - Extension of search function eq_internal_number --------------------------------------//
    instance.point_of_sale.PosDB = instance.point_of_sale.PosDB.extend({
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
//                            if (ret_o_ref.indexOf('Verkauf') == -1) {
//                                ret_o_ref = 'Verkauf ' + ret_o_ref.toString();
//                            }
                            // We use _t() that auto translate in language
                            if (ret_o_ref.indexOf(_t('Order ')) == -1) {
                                ret_o_ref = _t('Order ') + ret_o_ref.toString();
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
            this.changed_text = "";
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
        set_changed_text: function(changed_text){
        	this.set('changed_text', changed_text);
        },
        get_changed_text: function() {
        	return this.get('changed_text');
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
                changed_text: this.get_changed_text(),
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
                changed_text: this.get_changed_text(),
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
        addPaymentline: function(cashregister) {
            var paymentLines = this.get('paymentLines');
            var newPaymentline = new module.Paymentline({},{cashregister:cashregister, pos:this.pos});
            if(cashregister.journal.type !== 'cash'){
            	if(this.get_coupon_amount() > 0.0 && this.get_bonus_return_amount() > 0){
                	var amt = this.get_coupon_amount() + this.get_bonus_return_amount();
                	if(Math.max(this.getDueLeft(),0) > 0){
                		newPaymentline.set_amount( (Math.max(this.getDueLeft(),0) - amt).toFixed(2) );
                	}
                }else if(this.get_coupon_amount() > 0.0){
                	if(Math.max(this.getDueLeft(),0) > 0){
                		newPaymentline.set_amount( (Math.max(this.getDueLeft(),0) - this.get_coupon_amount()).toFixed(2) );
                	}
                } else if(this.get_bonus_return_amount() > 0.0){
                	if(Math.max(this.getDueLeft(),0) > 0){
                		newPaymentline.set_amount( (Math.max(this.getDueLeft(),0) - this.get_bonus_return_amount()).toFixed(2) );
                	}
                } else {
                	newPaymentline.set_amount( Math.max(this.getDueLeft(),0) );
                }
            }
            paymentLines.add(newPaymentline);
            this.selectPaymentline(newPaymentline);
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
//                barcode_src: "data:image/png;base64,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"
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
                                        }
                                    }
                            });
                        }
                    }
                });
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
                		
//                		// EQ: fixed an error in logic of calculation of totam price
//                		if (paid_total_cpn => 0){
//                			if (typeof sum_without_cpn === 'number') {
//                    			sum_without_cpn = round_di(sum_without_cpn, 2).toFixed(2);
//                    			sum_without_cpn = openerp.instances[this.session.name].web.format_value(round_di(sum_without_cpn, 2), { type: 'float', digits: [69, 2]});
//                            }
//                    		$('.paymentline-input').val(sum_without_cpn);	
//                		} 
                		
                		paid_total_cpn = paidTotal - cpn_amt;
                        remaining = dueTotal > paid_total_cpn ? dueTotal - paid_total_cpn : 0;
                        change = paid_total_cpn > dueTotal ? paid_total_cpn - dueTotal : 0;
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
    	init: function(parent, options) {
            var self = this;
            this._super(parent,options);
            this.line_dblclick_handler = function(event){
            	var product = this.orderline.get_product();
            	var line = this.orderline;
            	var old_prod_nm = product ? product.display_name : "Change Name";
            	
            	dialog = new instance.web.Dialog(this, {
                    title: _t(old_prod_nm),
                    size: 'medium',
                    buttons: [
                        {text: _t("Change"), click: function() {
                        	var new_prod_nm = dialog.$el.find("input#prod_nm").val();
                        	if(!jQuery.trim(new_prod_nm).length > 0){
                        		return alert("Please Enter Display Name");
                        	}
//                        	product.display_name = new_prod_nm;
                        	line.set_changed_text(new_prod_nm);
                        	self.rerender_orderline(line);
                        	this.parents('.modal').modal('hide'); 
                        }},
                        {text: _t("Cancel"), click: function() { 
                            this.parents('.modal').modal('hide'); 
                        }}
                    ]
                }).open();
                dialog.$el.html(QWeb.render("change_prod_name", self));
            };
    	},
    	render_orderline: function(orderline){
    		var el_node = this._super(orderline);
    		el_node.addEventListener('dblclick',this.line_dblclick_handler);
    		return el_node;
        },
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
