openerp.eq_dispatch = function(instance) {

    var module = instance.eq_dispatch;
    var _t     = instance.web._t;
    var QWeb   = instance.web.qweb;

    openerp.stock.PickingMainWidget.include({

		// reload the page
        eq_refresh_ui: function(){
            var self = this;
		    window.location = '/barcode/web/#picking_id='+self.picking.id; 
		    location.reload();
        },
        
        // Update the gross weight
        change_gross_wgt: function(op_id, value){
            var self = this;
            return new instance.web.Model('stock.quant.package')
                .call('write',[op_id, {'eq_gross_weight_changed':value}])
                .then(function(){
                    return self.eq_refresh_ui();
                });
        },
        
     });


    openerp.stock.PickingEditorWidget.include({
        get_rows: function(){
            var model = this.getParent();
            this.rows = [];
            var self = this;
            var pack_created = [];
            _.each( model.packoplines, function(packopline){
                    var pack = undefined;
                    var color = "";
                    if (packopline.product_id[1] !== undefined){ pack = packopline.package_id[1];}
                    if (packopline.product_qty == packopline.qty_done){ color = "success "; }
                    if (packopline.product_qty < packopline.qty_done){ color = "danger "; }
                    //also check that we don't have a line already existing for that package
                    if (packopline.result_package_id[1] !== undefined && $.inArray(packopline.result_package_id[0], pack_created) === -1){
                        var myPackage = $.grep(model.packages, function(e){ return e.id == packopline.result_package_id[0]; })[0];
                        self.rows.push({
                            cols: { product: packopline.result_package_id[1],
                                    qty: '',
                                    rem: '',
                                    uom: undefined,
                                    lot: undefined,
                                    pack: undefined,
                                    container: packopline.result_package_id[1],
                                    container_id: undefined,
                                    loc: packopline.location_id[1],
                                    dest: packopline.location_dest_id[1],
                                    id: packopline.result_package_id[0],
                                    product_id: undefined,
                                    can_scan: false,
                                    head_container: true,
                                    processed: packopline.processed,
                                    package_id: myPackage.id,
                                    ul_id: myPackage.ul_id[0],
                                    weight_net :myPackage.eq_weight_net,
                                    weight_gross : myPackage.eq_gross_weight,
				    updated_gross_weight : myPackage.eq_gross_weight_changed,
				    eq_ul_id : myPackage.eq_logistic_unit,
                            },
                            classes: ('success container_head ') + (packopline.processed === "true" ? 'processed hidden ':''),
                        });
                        pack_created.push(packopline.result_package_id[0]);
                    }
                    self.rows.push({
                        cols: { product: packopline.product_id[1] || packopline.package_id[1],
                                qty: packopline.product_qty,
                                rem: packopline.qty_done,
                                uom: packopline.product_uom_id[1],
                                lot: packopline.lot_id[1],
                                pack: pack,
                                container: packopline.result_package_id[1],
                                container_id: packopline.result_package_id[0],
                                loc: packopline.location_id[1],
                                dest: packopline.location_dest_id[1],
                                id: packopline.id,
                                product_id: packopline.product_id[0],
                                can_scan: packopline.result_package_id[1] === undefined ? true : false,
                                head_container: false,
                                processed: packopline.processed,
                                package_id: undefined,
                                ul_id: -1,
                        },
                        classes: color + (packopline.result_package_id[1] !== undefined ? 'in_container_hidden ' : '') + (packopline.processed === "true" ? 'processed hidden ':''),
                    });
            });
            //sort element by things to do, then things done, then grouped by packages
            group_by_container = _.groupBy(self.rows, function(row){
                return row.cols.container;
            });
            var sorted_row = [];
            if (group_by_container.undefined !== undefined){
                group_by_container.undefined.sort(function(a,b){return (b.classes === '') - (a.classes === '');});
                $.each(group_by_container.undefined, function(key, value){
                    sorted_row.push(value);
                });
            }

            $.each(group_by_container, function(key, value){
                if (key !== 'undefined'){
                    $.each(value, function(k,v){
                        sorted_row.push(v);
                    });
                }
            });

            return sorted_row;
        },
        

       renderElement: function(){
            var self = this;
            this._super();
            this.check_content_screen();
            this.$('.js_pick_done').click(function(){ self.getParent().done(); });
            this.$('.js_pick_print').click(function(){ self.getParent().print_picking(); });
            this.$('.oe_pick_app_header').text(self.get_header());
            this.$('.oe_searchbox').keyup(function(event){
                self.on_searchbox($(this).val());
            });
            this.$('.js_putinpack').click(function(){ self.getParent().pack(); });
            this.$('.js_drop_down').click(function(){ self.getParent().drop_down();});
            this.$('.js_clear_search').click(function(){
                self.on_searchbox('');
                self.$('.oe_searchbox').val('');
            });
            this.$('.oe_searchbox').focus(function(){
                self.getParent().barcode_scanner.disconnect();
            });
            this.$('.oe_searchbox').blur(function(){
                self.getParent().barcode_scanner.connect(function(ean){
                    self.get_Parent().scan(ean);
                });
            })
            this.$('#js_select').change(function(){
                var selection = self.$('#js_select option:selected').attr('value');
                if (selection === "ToDo"){
                    self.getParent().$('.js_pick_pack').removeClass('hidden')
                    self.getParent().$('.js_drop_down').removeClass('hidden')
                    self.$('.js_pack_op_line.processed').addClass('hidden')
                    self.$('.js_pack_op_line:not(.processed)').removeClass('hidden')
                }
                else{
                    self.getParent().$('.js_pick_pack').addClass('hidden')
                    self.getParent().$('.js_drop_down').addClass('hidden')
                    self.$('.js_pack_op_line.processed').removeClass('hidden')
                    self.$('.js_pack_op_line:not(.processed)').addClass('hidden')
                }
                self.on_searchbox(self.search_filter);
            });
            this.$('.js_plus').click(function(){
                var id = $(this).data('product-id');
                var op_id = $(this).parents("[data-id]:first").data('id');
                self.getParent().scan_product_id(id,true,op_id);
            });
            this.$('.js_minus').click(function(){
                var id = $(this).data('product-id');
                var op_id = $(this).parents("[data-id]:first").data('id');
                self.getParent().scan_product_id(id,false,op_id);
            });
            this.$('.js_unfold').click(function(){
                var op_id = $(this).parent().data('id');
                var line = $(this).parent();
                //select all js_pack_op_line with class in_container_hidden and correct container-id
                select = self.$('.js_pack_op_line.in_container_hidden[data-container-id='+op_id+']')
                if (select.length > 0){
                    //we unfold
                    line.addClass('warning');
                    select.removeClass('in_container_hidden');
                    select.addClass('in_container');
                }
                else{
                    //we fold
                    line.removeClass('warning');
                    select = self.$('.js_pack_op_line.in_container[data-container-id='+op_id+']')
                    select.removeClass('in_container');
                    select.addClass('in_container_hidden');
                }
            });
            this.$('.js_create_lot').click(function(){
                var op_id = $(this).parents("[data-id]:first").data('id');
                var lot_name = false;
                self.$('.js_lot_scan').val('');
                var $lot_modal = self.$el.siblings('#js_LotChooseModal');
                //disconnect scanner to prevent scanning a product in the back while dialog is open
                self.getParent().barcode_scanner.disconnect();
                $lot_modal.modal()
                //focus input
                $lot_modal.on('shown.bs.modal', function(){
                    self.$('.js_lot_scan').focus();
                })
                //reactivate scanner when dialog close
                $lot_modal.on('hidden.bs.modal', function(){
                    self.getParent().barcode_scanner.connect(function(ean){
                        self.getParent().scan(ean);
                    });
                })
                self.$('.js_lot_scan').focus();
                //button action
                self.$('.js_validate_lot').click(function(){
                    //get content of input
                    var name = self.$('.js_lot_scan').val();
                    if (name.length !== 0){
                        lot_name = name;
                    }
                    $lot_modal.modal('hide');
                    //we need this here since it is not sure the hide event
                    //will be catch because we refresh the view after the create_lot call
                    self.getParent().barcode_scanner.connect(function(ean){
                        self.getParent().scan(ean);
                    });
                    self.getParent().create_lot(op_id, lot_name);
                });
            });
            this.$('.js_delete_pack').click(function(){
                var pack_id = $(this).parents("[data-id]:first").data('id');
                self.getParent().delete_package_op(pack_id);
            });
            this.$('.js_print_pack').click(function(){
                var pack_id = $(this).parents("[data-id]:first").data('id');
                // $(this).parents("[data-id]:first").data('id')
                self.getParent().print_package(pack_id);
            });
            this.$('.js_submit_value').submit(function(event){
                var op_id = $(this).parents("[data-id]:first").data('id');
                var value = parseFloat($("input", this).val());
                if (value>=0){
                    self.getParent().set_operation_quantity(value, op_id);
                }
                $("input", this).val("");
                return false;
            });
            this.$('.js_qty').focus(function(){
                self.getParent().barcode_scanner.disconnect();
            });
            this.$('.js_qty').blur(function(){
                var op_id = $(this).parents("[data-id]:first").data('id');
                var value = parseFloat($(this).val());
                if (value>=0){
                    self.getParent().set_operation_quantity(value, op_id);
                }
                
                self.getParent().barcode_scanner.connect(function(ean){
                    self.getParent().scan(ean);
                });
            });
            this.$('.js_change_src').click(function(){
                var op_id = $(this).parents("[data-id]:first").data('id');//data('op_id');
                self.$('#js_loc_select').addClass('source');
                self.$('#js_loc_select').data('op-id',op_id);
                self.$el.siblings('#js_LocationChooseModal').modal();
            });
            this.$('.js_change_dst').click(function(){
                var op_id = $(this).parents("[data-id]:first").data('id');
                self.$('#js_loc_select').data('op-id',op_id);
                self.$el.siblings('#js_LocationChooseModal').modal();
            });
            this.$('.js_pack_change_dst').click(function(){
                var op_id = $(this).parents("[data-id]:first").data('id');
                self.$('#js_loc_select').addClass('pack');
                self.$('#js_loc_select').data('op-id',op_id);
                self.$el.siblings('#js_LocationChooseModal').modal();
            });


			// Change Gross weight
            this.$('.js_pack_gross_weight').click(function(){
            
            	var op_id = $(this).parents("[data-id]:first").data('id'); //Get pack id
				self.$('#js_loc_select').data('op-id',op_id);
            	self.$el.siblings('#js_PackchangGross').modal();
            });
            
			// Change Gross weight           
            this.$('.js_validate_gross_wgt').click(function(){
             		var select_dom_element = self.$('#js_loc_select');
             
					//get content of input
                    var value = parseFloat(self.$('.js_gross_wgt').val());
                    var op_id = select_dom_element.data('op-id');
                    self.getParent().change_gross_wgt(op_id, value);
              });


            this.$('.js_validate_location').click(function(){
                //get current selection
                var select_dom_element = self.$('#js_loc_select');
                var loc_id = self.$('#js_loc_select option:selected').data('loc-id');
                var src_dst = false;
                var op_id = select_dom_element.data('op-id');
                if (select_dom_element.hasClass('pack')){
                    select_dom_element.removeClass('source');
                    op_ids = [];
                    self.$('.js_pack_op_line[data-container-id='+op_id+']').each(function(){
                        op_ids.push($(this).data('id'));
                    });
                    op_id = op_ids;
                }
                else if (select_dom_element.hasClass('source')){
                    src_dst = true;
                    select_dom_element.removeClass('source');
                }
                if (loc_id === false){
                    //close window
                    self.$el.siblings('#js_LocationChooseModal').modal('hide');
                }
                else{
                    self.$el.siblings('#js_LocationChooseModal').modal('hide');
                    self.getParent().change_location(op_id, parseInt(loc_id), src_dst);

                }
            });
            this.$('.js_pack_configure').click(function(){
                var pack_id = $(this).parents(".js_pack_op_line:first").data('package-id');
                var ul_id = $(this).parents(".js_pack_op_line:first").data('ulid');
                self.$('#js_packconf_select').val(ul_id);
                self.$('#js_packconf_select').data('pack-id',pack_id);
                self.$el.siblings('#js_PackConfModal').modal();
            });
            this.$('.js_validate_pack').click(function(){
                //get current selection
                var select_dom_element = self.$('#js_packconf_select');
                var ul_id = self.$('#js_packconf_select option:selected').data('ul-id');
                var pack_id = select_dom_element.data('pack-id');
                self.$el.siblings('#js_PackConfModal').modal('hide');
                if (pack_id){
                    self.getParent().set_package_pack(pack_id, ul_id);
                    $('.container_head[data-package-id="'+pack_id+'"]').data('ulid', ul_id);
                }
		        location.reload();
            });
            
            //remove navigtion bar from default openerp GUI
            $('td.navbar').html('<div></div>');
        },

    });
    
}
