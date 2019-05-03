// Begin by loading the dashboard page
$('#pageContent').load("pages/dashboard.php");
$('#dashboard').addClass("active");

// Sidebar Navigation
$('.nav-item').click(function(e){
    e.preventDefault();

    // Set the clicked link as active and remove class from others
    $('.nav-item').removeClass("active")
    $(this).addClass("active");

    // Grab id value and craft php file
    var pageToLoad = "pages/" + $(this).attr('id') + ".php"
    $('#pageContent').load(pageToLoad);

    // Update page Title
    var pageTitle = $(this).find("p").html();
    $("#pageTitle").text(pageTitle)

});

// Temp status change
var scanning = true;
$('#scan-status').click(function(){
    if (scanning == true) {
        $(this).find("i:first").html("done").removeClass("scanning")
        $(this).css("color", "green")
        $(this).find("span").html("Scan Complete")
        scanning = false
    } else {
        $(this).find("i:first").html("autorenew").addClass("scanning")
        $(this).css("color", "orange")
        $(this).find("span").html("Scanning")
        scanning = true
    }
});
