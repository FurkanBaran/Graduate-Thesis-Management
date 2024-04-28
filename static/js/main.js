$(document).ready(function() {   
    $("#id").prepend("<option value='' >&nbsp;</option>");

    $(".chosen-select").chosen({
       no_results_text: "Oops, nothing found!"
     })
   });


  // Script for changing institute options according to university selection 

   $(document).ready(function() {
    $("#uni1").change(function() {
        var uni_id = $(this).val();
        var options = '';
        for (var i = 0; i < institute_list.length; i++) {
            if (institute_list[i][2] == uni_id) {
                options += '<option value="' + institute_list[i][0] + '">' + institute_list[i][1] + '</option>';
            }
        }
        $("#ins").html(options);
    });
});


function countdown() {
    var i = document.getElementById('counter');
    if (parseInt(i.innerHTML) <= 0) {
        location.href = '/';
        return;
    }
    i.innerHTML = parseInt(i.innerHTML) - 1;
}
setInterval(function () {
    countdown();
}, 1000);


// Script for adding empty option to the beginning of the select options
$(document).ready(function() {   
    $("#author").prepend("<option value='' >&nbsp;</option>");
    $("#supervisors").prepend("<option value='' >&nbsp;</option>");
    $("#cosupervisors").prepend("<option value='' >&nbsp;</option>");
    $("#topic").prepend("<option value='' >&nbsp;</option>");
    $("#keywords").prepend("<option value='' >&nbsp;</option>");
    $("#uni1").prepend("<option value='' >&nbsp;</option>");
    $("#ins").prepend("<option value='' >&nbsp;</option>");
    $("#type").prepend("<option value='' >&nbsp;</option>");
    $("#language").prepend("<option value='' >&nbsp;</option>");

    $(".chosen-select").chosen({
        no_results_text: "Oops, nothing found!"
        })
    });


function searchThesisByNumber() {
    // Get the thesis number from the input
    var thesisNumber = document.getElementById('thesis_no').value;
    
    // Redirect to the thesis detail page with the given thesis number
    window.location.href = '/get_thesis/' + thesisNumber;
}