$(document).ready(function(){


    $('#login_frm').on('submit',function(e){
        e.preventDefault()
        $('.msg').html('')
        data=$(this).serializeArray()
        $.ajax({
            method:'POST',
            url:'auth_user',
            data:data,
            success:function(res){
                if(res.data == 'login'){
                    window.location.href = 'homepage';
                }else{
                    $('.msg').append('<div class="alert alert-danger alert-dismissible fade show" role="alert">\
                                 <strong>Account not found!</strong> Please Try Again!\
                                 <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
                                 </div>')
                }
            }
        })

    })



    $('#signup_frm').on('submit',function(e){
        e.preventDefault()
        $('.rmsg').html('')
        data=$(this).serializeArray()
        p1=$('.pass1').val()
        p2=$('.pass2').val()
        if(p1 != p2){
            toastr["error"]("Password not matched!");
        }else{
            $.ajax({
                method:'POST',
                url:'signup',
                data:data,
                success:function(res){
                    if(res.data == 'valid'){
                        toastr["success"]("Registered Successfully!");
                        window.location.href = 'homepage';
                    }else{
                        for(err in res.data){
                            toastr["error"](res.data[err]);
                        }
                    }
                }
            })
        }

    })

    $('#signup_farmer').on('submit',function(e){
        e.preventDefault()
        $('.rmsg').html('')
        data=$(this).serializeArray()
        p1=$('.pass1').val()
        p2=$('.pass2').val()
        if(p1 != p2){
            toastr["error"]("Password not matched!");
        }else{
            $.ajax({
                method:'POST',
                url:'../../signup',
                data:data,
                success:function(res){
                    
                    if(res.data == 'valid'){
                        toastr["success"]("Registered Successfully!");
                        window.location.href = '../../farmer_address';
                    }else{
                        for(err in res.data){
                            toastr["error"](res.data[err]);
                        }
                    }
                }
            })
        }

    })









})