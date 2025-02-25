$(document).ready(function(){


$('.my_address').on('click',function(){
    get_address()
})

$('#location_frm').on('submit',function(e){
    e.preventDefault()
    data=$(this).serializeArray()
    // console.log(data)
    $.ajax({
        method:'POST',
        url:'../save_address',
        data:data,
        success:function(res){
            $('#location_frm').trigger('reset')
            $('#MapModal').modal('hide')
            toastr["success"]("The address has been successfully added!");
            setTimeout(function() {
                window.location.href = "../homepage"; // Redirect URL
            }, 3000);
            get_address()
        }
    })
})

$(document).on('click','.activate_address',function(){
    adid=$(this).attr('id')
    $.ajax({
        method:'POST',
        url:'../up_address',
        data:{adid:adid},
        success:function(res){
            get_address()
        }
    })

})

get_address()
async function get_address(){
    try {
        let response = await fetch(`/get_address/`);  // Send GET request
        let data = await response.json();  // Convert response to JSON
          $('.address_field').html('')
          $('#address_display').html('')
          
        for(a in data){
            
            if(data[a].ad_status == 'ACTIVE'){
                chk='checked'
                txt='text-success'
                $('.cur_add').text(data[a].ad_name)
                $('#c_address').text(data[a].ad_name)
                $('.c_address').val(data[a].ad_name)
            }else{
                chk=''
                txt=''
            }
            adtemp='<div class="btn-group gap-3 osahan-btn-group d-flex col-md-6 mb-2" role="group" aria-label="Basic radio toggle button group">\
                    <input type="radio" class="btn-check activate_address" '+chk+' name="btnradiod" id="'+data[a].ad_id+'" autocomplete="off">\
                    <label  class="btn btn-outline-light d-flex align-items-center gap-3 rounded p-3 col-6" for="'+data[a].ad_id+'">\
                        <i class="bi bi-house h5 mb-0"></i>\
                        <span class="text-start"><h6 class="mb-1 fw-bold">'+data[a].ad_type+' - <i>'+data[a].ad_status+'</i></h6><div class="text-muted small text-opacity-50">'+data[a].ad_name+'</div></span>\
                        <i class="bi bi-check-circle-fill ms-auto"></i>\
                    </label>\
                    </div>'
            
            $('.address_field').append(adtemp)

            addis='<div class="btn-group gap-3 osahan-btn-group d-flex col-12 mb-2" role="group" aria-label="Basic radio toggle button group">\
                    <input type="radio" class="btn-check activate_address" '+chk+' name="btnradiod" id="'+data[a].ad_id+'" autocomplete="off">\
                    <label  class="btn btn-outline-light d-flex align-items-center gap-3 rounded p-3 col-6" for="'+data[a].ad_id+'">\
                        <i class="bi bi-house h5 mb-0"></i>\
                        <span class="text-start"><h6 class="mb-1 fw-bold">'+data[a].ad_type+' - <i>'+data[a].ad_status+'</i></h6><div class="text-muted small text-opacity-50">'+data[a].ad_name+'</div></span>\
                        <i class="bi bi-check-circle-fill ms-auto"></i>\
                    </label>\
                    </div>'
            
            $('#address_display').append(addis)
        }
        // document.getElementById("result").innerText = data.message;  // Display result
    } catch (error) {
        console.error("Error:", error);
    }

}




})