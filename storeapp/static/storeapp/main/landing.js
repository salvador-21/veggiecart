get_client_products()
async function get_client_products(){
    try {
        let response = await fetch(`/get_client_products/`);  // Send GET request
        let data = await response.json();  // Convert response to JSON
          $('#products-display').html('')
          $('.available_products').html('')
          console.log(data)
        for(a in data){
            
            adtemp='<div class="col">\
             <div class="text-center position-relative border rounded pb-4">\
                <img src="media/'+data[a].image__pi_image+'" class="img-fluid rounded-3 p-3" alt="...">\
                <div class="listing-card-body pt-0">\
                   <h6 class="card-title mb-1 fs-14">'+data[a].prod_name+'</h6>\
                   <p class="card-text small text-success">'+data[a].pricing__p_qty+' Available</p>\
                </div>\
                <a href="/products" class="stretched-link"></a>\
             </div>\
          </div>'
                                 
            $('#products-display').append(adtemp)

        

         aProducts='<div class="col">\
         <div class="card h-100 overflow-hidden shadow-sm border-0">\
            <img src="media/'+data[a].image__pi_image+'" class="card-img-top of-cover " alt="...">\
            <div class="card-body px-3 pb-3 pt-3">\
               <p class="card-title">'+data[a].prod_name+'</p>\
               <p class="card-text text-muted small">Per '+data[a].pricing__p_unit+'</p>\
            </div>\
            <div class="px-3 pt-0 pb-3 card-footer bg-white border-0 d-flex align-items-center justify-content-between">\
               <div class="fw-bold">&#8369;'+data[a].pricing__p_price+'</div>\
               <button type="button" class="btn btn-outline-success px-3 btn-sm rounded-pill addToCart" id="'+data[a].prod_id+'"><span><i class="bi bi-plus-lg"></i></span>&nbsp;Add to Cart</button>\
            </div>\
         </div>\
      </div>'

            $('.available_product').append(aProducts)
           
        }

     
    } catch (error) {
        console.error("Error:", error);
    }

}

$(document).on('click', '.addToCart', function(){

    pid=$(this).attr('id')
 
    add_to_cart(pid)
 
 })

 function add_to_cart(pid){
  
    $.ajax({
        type: "POST",
        url: "add_to_cart",
        data: {
            'pid': pid,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(res){
            // console.log(res)
            if(res.data == 'ok'){
                toastr["success"]("Product Added to Cart.");
                cart_count()
            }else{
                toastr["error"](res.data);
               
            }
        }
    });
}