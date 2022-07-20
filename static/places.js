let rows = []
$('table tbody tr').each(function(i, row) {
	return rows.push(row);
});

$('#pagination').pagination({
    dataSource: rows,
    pageSize: 15,
    prevText: '<i class="fa-solid fa-circle-chevron-left fa-xl"></i>',
    nextText: '<i class="fa-solid fa-circle-chevron-right fa-xl"></i>',
    showPageNumbers: false,
    callback: function(data, pagination) {
        $('tbody').html(data);
    }
});