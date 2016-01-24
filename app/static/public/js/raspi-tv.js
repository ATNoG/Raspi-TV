////////////////////////////////////////////////////////
// Helper methods
////////////////////////////////////////////////////////

// Sets the current time
//
function updateTime() {
    var now = new Date();
    $('#date').text(now.toDateString());
    $('#time').text(now.toLocaleTimeString());
}

////////////////////////////////////////////////////////
// Main 'when ready' method
////////////////////////////////////////////////////////

$(document).ready(function () {
    setInterval(updateTime, 999);
});