function getmessages() {
    request = $.ajax({
        type: "GET",
        url: "/api",
        data: ""
    });

    request.fail(function(error) {
            console.log(error);
            });
    
    request.done(function(response) {
        if (response.length > 0) {
            var tabledata = $.map(response, function(item, i) {
                return "<tr><td>" + item[0] + "</td><td>" + item[1] + "</td><td>" + item[2] + "</td></tr>";
            }).join("");
            
            $("#messages").empty().append(tabledata);
        }
    });
}

$(document).ready(function() {
    getmessages();
});
setInterval(function() {
    getmessages();
}, 3000);
