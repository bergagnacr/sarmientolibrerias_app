$(document).ready( function () {
    var table = $('#table_id').DataTable();
    table.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
        var cell = table.cell({ row: rowIdx, column: 4 }).node();
        $(cell).css('background-color', 'red');
    });
});