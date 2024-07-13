function addTrain() {
    var trainName = $("#trainName").val();
    var departureCity = $("#departureCity").val();
    var arrivalCity = $("#arrivalCity").val();

    // Validation
    if (!trainName || !departureCity || !arrivalCity) {
        alert("Please fill in all fields.");
        return;
    }

    // Add a new row to the table
    var newRow = $("<tr>")
        .append($("<td>").text(trainName))
        .append($("<td>").text(departureCity))
        .append($("<td>").text(arrivalCity));

    $("#trainTable").append(newRow);

    // Clear the form
    $("#trainForm")[0].reset();
}
