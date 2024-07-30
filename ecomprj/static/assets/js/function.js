console.log("working fine");

const monthNames = months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];



$("#commentForm").submit(function(e) {

    e.preventDefault();

    let dt = new Date();
    let time = dt.getDate() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()+ " ";



    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function(response) {
            console.log("Comment saved to DB");


            if(response.bool == true){
                $("#review-rsp").html("Review Added Successfully.!!")
                $(".hide-comment-form").hide()
                $(".add-review").hide()


                
                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html += '<div class="user justify-content-between d-flex">'
                    _html += '<div class="thumb text-center">'
                    _html += ' <img src="https://img.freepik.com/free-vector/illustration-businessman_53876-5856.jpg" alt="" />'
                    _html += '<a href="#" class="font-heading text-brand">'+ response.context.user +'</a>'
                    _html += '</div>'

                    _html += ' <div class="desc">'
                    _html += ' <div class="d-flex justify-content-between mb-10">'
                    _html += ' <div class="d-flex align-items-center">'
                    _html += ' <span class="font-xs text-muted">'+ time +' </span>'
                    _html += ' </div>'

                    for(let i = 1; i <= response.context.rating; i++){
                        _html += '<i class="fas fa-star text-warning"></i>'
                    }

                    _html += '</div>'
                    _html += ' <p class="mb-10"> '+ response.context.review +' </p>'

                    _html += ' </div>'
                    _html += ' </div>'
                    _html += '</div>'
                    $(".comment-list").prepend(_html)
            }

            $(".comment-list").prepend(_html)
            // console.log(response);
        },
        // error: function(xhr, status, error) {
        //     console.error("An error occurred: " + status + " - " + error);
        // }
    });
});
//filter

$(document).ready(function (){
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        console.log("   A check");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key =$(this).data("filter")


            // console.log("filter value:",filter_value);
            // console.log("filter key:",filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter = ' + filter_key  + ']:checked')).map(function(element){
                return element.value
            })
        })
        console.log("Filter object is:", filter_object)
        $.ajax({
            url : '/filter-product',
            data: filter_object,
            dataType : 'json',
            beforeSend: function(){
                console.log('sending data');
            },
            success: function(response){
                console.log(response)
                $("#filtered-product").html(response.data)
            }

        })
    })
    $("#max_price").on("blur", function(){
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()
        
        // console.log("current price is:", min_price);

        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
           console.log("Eroor");
           min_price = Math.round(min_price * 100) / 100
           max_price = Math.round(max_price * 100) / 100
        //    console.log("min", min_Price)
        alert("Price must be between ৳" +min_price+ " and ৳" + max_price)
        $(this).val(min_price)
        
        $('#range').val(min_price)
        $(this).focus()

        return false



        }
    })

})
//
