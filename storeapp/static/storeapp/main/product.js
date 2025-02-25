$('#addproduct').submit( function(e){
    e.preventDefault();
    
    $.ajax({
        url: "add_product",
        type: "POST",
        data: new FormData(this),
        cenctype: 'multipart/form-data',
        processData: false,
        contentType: false,   
        success: function(res){
           
            if(res.data == 'ok'){
                $('#add-product').modal('hide');
                $('#addproduct').trigger('reset');
                toastr["success"]("Product Added Successfully!");
                get_myproducts()
            }else{
                toastr["error"]("Error Adding Product.");
               
            }
        }
    });

});

$('.view_product_btn').on('click', function(){

    farmer_products()
});
$('.view_myproduct_btn').on('click', function(){
    console.log('Potaka')
    get_myproducts()
});

// get_products()
async function farmer_products(){
    try {
        let response = await fetch(`/get_products/`);  // Send GET request
        let data = await response.json();  // Convert response to JSON
          $('.farmer_product_view').html('')
          if(data.length > 0){
            for(a in data){
            
                adtemp='<div class="product-list d-flex p-3 border-bottom">\
                                        <img src="media/'+data[a].image__pi_image+'" class="img-fluid" alt="...">\
                                        <div class="product-list-body px-3">\
                                           <span class="fw-bold mb-1 h6">'+data[a].prod_name+'</span>/<span>'+data[a].prod_desc+'</span>\
                                           <p class="card-text small text-muted mb-0">PRICE: <b>'+data[a].pricing__p_price+'</b></p>\
                                           <p class="card-text small text-muted mb-0">OWNER:<b>'+data[a].user__last_name+', '+data[a].user__first_name+'</b></p>\
                                           <p class="">STOCKS: <span class="fw-bold text-success">'+data[a].pricing__p_qty+'</span> / '+data[a].pricing__p_unit+'</p>\
                                        </div>\
                                        <div class="ms-auto mb-auto">\
                                          <div class="d-flex align-items-center gap-3 mt-3 mb-4"><div class="gap-2 d-flex">\
                                        <div class="col-auto px-0"><input type="radio" class="btn-check" name="btnradio" id="btnradio233" autocomplete="off">\
                                           <label class="btn btn-outline-success btn-sm view_product" id="'+data[a].prod_id+'" for="btnradio233">DETAILS</label></div>\
                                     <div class="small text-warning my-2"></div></div>\
                                           </div>\
                                     </div>';
                                     
                $('.farmer_product_view').append(adtemp)
    
    
                
               
            }
          }else{
            $('.farmer_product_view').append('<h4 class="text-danger">No Available Farmer Product!</h4>')
          }
       
        // document.getElementById("result").innerText = data.message;  // Display result
    } catch (error) {
        console.error("Error:", error);
    }

}

// view my products
async function get_myproducts(){
    try {
        let response = await fetch(`/get_myproducts/`);  // Send GET request
        let data = await response.json();  // Convert response to JSON
          $('.myproduct-view').html('')
          console.log(data)
          if(data.length > 0){
            for(a in data){

                if(data[a].prod_status == 'UNAVAILABLE'){
                    btn_stat='<div class="col-auto"><input type="radio" class="btn-check" name="btnradio" id="btnradio333" autocomplete="off">\
                                           <label class="btn btn-outline-warning btn-sm stat_product" id="'+data[a].prod_id+'" for="btnradio333">UNAVAILABLE</label></div></div>'
                }else if(data[a].prod_status == 'AVAILABLE'){
                    btn_stat='<div class="col-auto"><input type="radio" class="btn-check" name="btnradio" id="btnradio333" autocomplete="off">\
                                           <label class="btn btn-outline-success btn-sm stat_product" id="'+data[a].prod_id+'" for="btnradio333">AVAILABLE</label></div></div>'

                }else if(data[a].prod_status == 'OUT OF STOCK'){
                    btn_stat='<div class="col-auto"><input type="radio" class="btn-check" name="btnradio" id="btnradio333" autocomplete="off">\
                                           <label class="btn btn-outline-secondary btn-sm stat_product" id="'+data[a].prod_id+'" for="btnradio333">OUT OF STOCK</label></div></div>'

                }else{
                    btn_stat=''
                }

            
                adtemp='<div class="product-list d-flex p-3 border-bottom">\
                                        <img src="media/'+data[a].image__pi_image+'" class="img-fluid" alt="...">\
                                        <div class="product-list-body px-3">\
                                           <span class="fw-bold mb-1 h6">'+data[a].prod_name+'</span>/<span>'+data[a].prod_desc+'</span>\
                                           <p class="card-text small text-muted mb-2">'+data[a].pricing__p_price+'/'+data[a].pricing__p_unit+'</p>\
                                           <p class="">STOCK: <span class="fw-bold text-success"> '+data[a].pricing__p_qty+'</span></p>\
                                        </div>\
                                        <div class="ms-auto mb-auto">\
                                          <div class="d-flex align-items-center gap-3 mt-3 mb-4"><div class="gap-2 d-flex">\
                                        '+btn_stat+'<div class="col-auto px-0"><input type="radio" class="btn-check" name="btnradio" id="btnradio233" autocomplete="off">\
                                           <label class="btn btn-outline-success btn-sm update_product" id="'+data[a].prod_id+'" for="btnradio233">UPDATE</label></div>\
                                        <div class="col-auto"><input type="radio" class="btn-check" name="btnradio" id="btnradio333" autocomplete="off">\
                                           <label class="btn btn-outline-danger btn-sm delete_product" id="'+data[a].prod_id+'" for="btnradio333">DELETE</label></div></div>\
                                     <div class="small text-warning my-2"></div></div>\
                                           </div>\
                                     </div>'
                                     
                $('.myproduct-view').append(adtemp)
    
    
                
               
            }
          }else{
            $('.myproduct-view').append('<h4 class="text-danger">You don`t have product yet!</h4>')
          }
        
        // document.getElementById("result").innerText = data.message;  // Display result
    } catch (error) {
        console.error("Error:", error);
    }

}

$(document).on('click','.view_product',function(){
    pid=$(this).attr('id')
    get_products_details(pid)
    $('#view_product_modal').modal('show') 
})

function get_products_details(pid){
    $.ajax({
        method:'POST',
        url:'get_singel_product',
        data:{'pid':pid},
        success:function(res){
            console.log(res)
            // $('#update_product_modal').find('#product_id').val(res.prod_id)
            // $('#update_product_modal').find('#id_prod_name').val(res.prod_name)
            // $('#update_product_modal').find('#id_prod_desc').val(res.prod_desc)
            // $('#update_product_modal').find('#id_prod_category').val(res.prod_category)
            // $('#update_product_modal').find('#id_p_price').val(res.pricing__p_price)
            // $('#update_product_modal').find('#id_p_unit').val(res.pricing__p_unit)
            // $('#update_product_modal').find('#id_p_qty').val(res.pricing__p_qty)
            // $('#product_image').attr('src','media/'+res.image__pi_image)
        }
    })
}

$(document).on('click', '.update_product', function(){

    pid=$(this).attr('id')
    $.ajax({
        method:'POST',
        url:'get_singel_product',
        data:{'pid':pid},
        success:function(res){
     
            $('#update_product_modal').find('#product_id').val(res.prod_id)
            $('#update_product_modal').find('#id_prod_name').val(res.prod_name)
            $('#update_product_modal').find('#id_prod_desc').val(res.prod_desc)
            $('#update_product_modal').find('#id_prod_category').val(res.prod_category)
            $('#update_product_modal').find('#id_p_price').val(res.pricing__p_price)
            $('#update_product_modal').find('#id_p_unit').val(res.pricing__p_unit)
            $('#update_product_modal').find('#id_p_qty').val(res.pricing__p_qty)
            $('#product_image').attr('src','media/'+res.image__pi_image)
        }
    })
    $('#update_product_modal').modal('show')    

})

$('#updateproduct').submit( function(e){
    e.preventDefault();
    
    $.ajax({
        url: "update_product",
        type: "POST",
        data: new FormData(this),
        cenctype: 'multipart/form-data',
        processData: false,
        contentType: false,   
        success: function(res){
 
            if(res.data == 'ok'){
                $('#update_product_modal').modal('hide');
                $('#updateproduct').trigger('reset');
                toastr["success"]("Product Updated Successfully!");
                get_products()
            }else{
                toastr["error"]("Error Updating Product.");
          
            }
        }
    });
})

$(document).on('click', '.delete_product', function(){

    pid=$(this).attr('id')

    if (confirm("Delete Product?")){
        $.ajax({
            method:'POST',
            url:'delete_product',
            data:{'pid':pid},
            success:function(res){
                if(res.data == 'ok'){
                    toastr["success"]("Product Deleted Successfully!");
                    get_products()
                }else{
                    toastr["error"]("Error Deleting Product.");
                }
            }
        })
     }
    
})

$(document).on('click','.stat_product',function(){
    pid=$(this).attr('id')
    if (confirm("Send Product in Market?")){
        $.ajax({
            method:'POST',
            url:'stat_product',
            data:{'pid':pid},
            success:function(res){
                if(res.data == 'ok'){
                    toastr["success"]("Product has sent to Market Successfully!");
                    get_myproducts()
                }else{
                    toastr["error"]("Error Publishing Product.");
                }
            }
        })
     }

})

$('.search_product').on('keyup',function(){
    sval=$(this).val()
    $.ajax({
        method:'POST',
        url:'searc_product',
        data:{sval},
        success:function(res){
            $('.product-view').html('')
            if(res.length == 0){
                $('.product-view').append('<h4 class="text-danger text-center">No Product Found!</h4>')
            }else{
                for(a in res){
                
                    adtemp='<div class="product-list d-flex p-3 border-bottom">\
                                            <img src="media/'+res[a].image__pi_image+'" class="img-fluid" alt="...">\
                                            <div class="product-list-body px-3">\
                                               <span class="fw-bold mb-1 h6">'+res[a].prod_name+'</span>/<span>'+res[a].prod_desc+'</span>\
                                               <p class="card-text small text-muted mb-2">'+res[a].pricing__p_price+'/'+res[a].pricing__p_unit+'</p>\
                                               <p class="fw-bold text-success">'+res[a].prod_category+'</p>\
                                            </div>\
                                            <div class="ms-auto mb-auto">\
                                              <div class="d-flex align-items-center gap-3 mt-3 mb-4"><div class="gap-2 d-flex">\
                                            <div class="col-auto px-0"><input type="radio" class="btn-check" name="btnradio" id="btnradio233" autocomplete="off">\
                                               <label class="btn btn-outline-success btn-sm update_product" id="'+res[a].prod_id+'" for="btnradio233">UPDATE</label></div>\
                                            <div class="col-auto"><input type="radio" class="btn-check" name="btnradio" id="btnradio333" autocomplete="off">\
                                               <label class="btn btn-outline-danger btn-sm delete_product" id="'+res[a].prod_id+'" for="btnradio333">DELETE</label></div></div>\
                                         <div class="small text-warning my-2"></div></div>\
                                               </div>\
                                         </div>'
                                         
                    $('.product-view').append(adtemp)
                    
                   
                }

            }
            
        }
    })
})