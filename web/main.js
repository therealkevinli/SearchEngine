function loadTable(jsonData, query) {
    console.log("populating query results into table");
    //let jsonData = JSON.parse(data);

    let resultsTableBodyElement = $('#resultsTableBody');

    for( let i = 0; i < jsonData.length; ++i ) {
        let rowHTML = "";
        rowHTML += '<tr>';
        rowHTML += '<td>';
        rowHTML += '<a href="https://' + jsonData[i] + '">' + jsonData[i] + '</a>';
        rowHTML += '</td>';
        rowHTML += '</tr>';
        resultsTableBodyElement.append(rowHTML);
    }
}

function handleNormalSearch(query) {
    $('#resultsTableBody').empty();
    console.log("Doing normal search with query: " + query);

    $.ajax({
        "method": "POST",
        "url"   : "http://127.0.0.1:5000/api/search",
        "data"  : JSON.stringify( {"query" : query} ),
        "contentType" : "application/json;charset=UTF-8",
        "success": function(data) {
            if( data == null) data = [];
            console.log("Ajax success. Result set size: " + data.length)
            loadTable(data, query);
        }, 
        "error" : function(errData) {
            console.log("lookup ajax error");
            console.log(errData);
        }
    });
}

$('#search').keypress(function(event) {
    if(event.keyCode == 13) {
        event.preventDefault();
        handleNormalSearch($('#search').val());
    }
});

$('#search-button').click(function(event) {
    event.preventDefault();
    handleNormalSearch($('#search').val());
});
