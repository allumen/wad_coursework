$( document ).ready(function() {
    // hide ingredient input specified by button
    $(".button-remove").click(function() {
        var ingredient_id = "#ingredient-" + $(this).val();
        
        $(ingredient_id).children().each(function() {
            $(this).attr('value', '');
        });
                
        $(ingredient_id).hide();
    });
    
    // show another ingredient input on button click
    $(".button-add").click(function() {
        $("#ingredients").children(".ingredient").each(function() {
            var hidden = $(this).is(":hidden");
            if ( hidden === true ) {
                $(this).toggle();
                return false;
            }
        });
        alert("Maximum number of ingredients reached!");
    });

    // hide excess ingedient inputs shon by default
    var counter = 0;
    $("#ingredients").children(".ingredient").each(function() {
        counter++;
        if (counter > 3) {
            $(this).toggle();
        }
    });
});