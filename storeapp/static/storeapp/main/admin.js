$(document).on('click','.view_users_btn',function(){

    get_users()
})

async function get_users(){

    try {
        let response = await fetch(`/get_users/`);  // Send GET request
        let data = await response.json();  // Convert response to JSON
          $('.users-view').html('')
          for(a in data){
                
                if(data[a].address !=  ''){
                    address=data[a].address.split('-')
                    add=address[0]
                }else{
                    add='No Address!'
                }
            adtemp='<div class="product-list d-flex p-3 border-bottom">\
                                    <img src="media/uploads/profile.png" class="img-fluid" alt="...">\
                                    <div class="product-list-body px-3">\
                                       <span class="fw-bold mb-1 h6">'+data[a].user__last_name+', '+data[a].user__last_name+'</span> / <span>'+data[a].usertype+'</span>\
                                       <p class="mb-0 card-text small">'+add+'</p>\
                                        <p class="mb-0 text-success">Contact: <b>'+data[a].contact_no+'</b></p>\
                                    </div>\
                                    <div class="ms-auto mb-auto">\
                                      <div class="d-flex align-items-center gap-3 mt-3 mb-4"><div class="gap-2 d-flex">\
                                    <div class="col-auto px-0"><input type="radio" class="btn-check" name="btnradio" id="btnradio233" autocomplete="off">\
                                       <label class="btn btn-outline-success btn-sm user_details" id="'+data[a].user__id+'" for="btnradio233">Details</label></div>\
                                 <div class="small text-warning my-2"></div></div>\
                                       </div>\
                                 </div>'
                                 
            $('.users-view').append(adtemp)


            
           
        }
      
        
    } catch (error) {
        console.error("Error:", error);
    }

}


$('.search_user').on('keyup',function(){
    sval=$(this).val()
    $.ajax({
        method:'POST',
        url:'search_user',
        data:{sval},
        success:function(res){
            $('.users-view').html('')
            if(res.length == 0){
                $('.users-view').append('<h4 class="text-danger text-center">User not found!</h4>')
            }else{
                for(a in res){
                
                    adtemp='<div class="product-list d-flex p-3 border-bottom">\
                                    <img src="media/uploads/profile.png" class="img-fluid" alt="...">\
                                    <div class="product-list-body px-3">\
                                       <span class="fw-bold mb-1 h6">'+res[a].user__last_name+', '+res[a].user__last_name+'</span> / <span>'+res[a].usertype+'</span>\
                                       <p class="mb-0 card-text small">'+add+'</p>\
                                        <p class="mb-0 text-success">Contact: <b>'+res[a].contact_no+'</b></p>\
                                    </div>\
                                    <div class="ms-auto mb-auto">\
                                      <div class="d-flex align-items-center gap-3 mt-3 mb-4"><div class="gap-2 d-flex">\
                                    <div class="col-auto px-0"><input type="radio" class="btn-check" name="btnradio" id="btnradio233" autocomplete="off">\
                                       <label class="btn btn-outline-success btn-sm user_details" id="'+res[a].user__id+'" for="btnradio233">Details</label></div>\
                                 <div class="small text-warning my-2"></div></div>\
                                       </div>\
                                 </div>'
                                         
                    $('.users-view').append(adtemp)
                    
                   
                }

            }
            
        }
    })
})


$("#copyBtn").click(function () {
    let text = $("#farmer_link").val();
    navigator.clipboard.writeText(text).then(() => {
        toastr["success"]("Copied registration Link for Farmers!");
    }).catch(err => console.error("Failed to copy: ", err));
});

get_orders()
async function get_orders(){

    try {
        let response = await fetch(`/get_orders/`);  // Send GET request
        let data = await response.json();  // Convert response to JSON
          $('.order_view').html('')
          console.log(data)
          for(a in data){
            
            
            try {
                add=data[a].address.split('-')
            } catch (error) {
                add=data[a]
            } 
            ordlist='<div class="col">\
                    <div class="border rounded p-3 shadow-sm history-card">\
                    <div class="d-flex gap-3">\
                        <img src="#" alt="" class="img-fluid rounded bg-light h-40">\
                        <span class="text-start">\
                            <h6 class="mb-1 fw-bold">ORDER #'+data[a].order_code+'</h6>\
                            <div class="text-muted small text-opacity-100 mb-1">'+add[0]+'</div>\
                            <div class="text-muted small">ORDER #'+data[a].order_code+' | Sat, Jan 1, 2022, 03:06 PM</div>\
                        </span>\
                        <div class="ms-auto text-end">\
                            <small><i class="bi bi-check-circle-fill text-success"></i> Ordered on </small>\
                            <p class="mb-0 small text-success">'+data[a].created_at+'</p>\
                        </div>\
                    </div>\
                    <div class="d-flex align-items-center gap-3 border-top pt-3 mt-3">\
                        <span class="text-start">\
                            <p class="mb-0">Ordered By: <b>'+data[a].user__last_name+', '+data[a].user__first_name+'</b></p>\
                            <p class="mb-0 text-danger">Total Amount: &#8369; <b>'+data[a].order_total+'</b></p>\
                        </span>\
                        <div class="ms-auto text-end">\
                            <button class="btn btn-sm btn-outline-success text-uppercase me-2" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">REORDER</button>\
                            <button class="btn btn-sm btn-success text-uppercase" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">VIEW DETAILS</button>\
                        </div>\
                    </div>\
                    </div>'
                                 
            $('.order_view').append(ordlist)

        }
      
        
    } catch (error) {
        console.error("Error:", error);
    }

}