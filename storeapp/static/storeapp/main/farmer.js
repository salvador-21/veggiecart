get_myproducts()
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


    get_myproducts()

});

// get_products()
async function get_myproducts(){
    try {
        let response = await fetch(`/get_myproducts/`);  // Send GET request
        let data = await response.json();  // Convert response to JSON
          $('.myproduct-view').html('')
          
        for(a in data){
            
            adtemp='<div class="product-list d-flex p-3 border-bottom">\
                                    <img src="media/'+data[a].image__pi_image+'" class="img-fluid" alt="...">\
                                    <div class="product-list-body px-3">\
                                       <span class="fw-bold mb-1 h6">'+data[a].prod_name+'</span>/<span>'+data[a].prod_desc+'</span>\
                                       <p class="card-text small text-muted mb-2">'+data[a].pricing__p_price+'/'+data[a].pricing__p_unit+'</p>\
                                       <p class="fw-bold text-success">'+data[a].prod_category+'</p>\
                                    </div>\
                                    <div class="ms-auto mb-auto">\
                                      <div class="d-flex align-items-center gap-3 mt-3 mb-4"><div class="gap-2 d-flex">\
                                    <div class="col-auto px-0"><input type="radio" class="btn-check" name="btnradio" id="btnradio233" autocomplete="off">\
                                       <label class="btn btn-outline-success btn-sm update_product" id="'+data[a].prod_id+'" for="btnradio233">UPDATE</label></div>\
                                    <div class="col-auto"><input type="radio" class="btn-check" name="btnradio" id="btnradio333" autocomplete="off">\
                                       <label class="btn btn-outline-warning btn-sm transfer_product" id="'+data[a].prod_id+'" for="btnradio333">TRANSFER</label></div></div>\
                                 <div class="small text-warning my-2"></div></div>\
                                       </div>\
                                 </div>'
                                 
            $('.myproduct-view').append(adtemp)


            
           
        }
        // document.getElementById("result").innerText = data.message;  // Display result
    } catch (error) {
        console.error("Error:", error);
    }

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
                get_myproducts()
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
                    get_myproducts()
                }else{
                    toastr["error"]("Error Deleting Product.");
                }
            }
        })
     }
    
})

$(document).on('click', '.transfer_product', function(){

    pid=$(this).attr('id')

    if (confirm("Transfer Product to Admin?")){
        $.ajax({
            method:'POST',
            url:'transfer_product',
            data:{pid},
            success:function(res){
               
                if(res.data == 'ok'){
                    toastr["success"]("Product Transfered Successfully!");
                    get_myproducts()
                }else{
                    toastr["error"]("Error Transfering Product.");
                }
            }
        })
     }
    
})

$('.search_myproduct').on('keyup',function(){
    sval=$(this).val()
    $.ajax({
        method:'POST',
        url:'searc_product',
        data:{sval},
        success:function(res){
            $('.myproduct-view').html('')
            if(res.length == 0){
                $('.myproduct-view').append('<h4 class="text-danger text-center">No Product Found!</h4>')
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
                                         
                    $('.myproduct-view').append(adtemp)
                    
                   
                }

            }
            
        }
    })
})