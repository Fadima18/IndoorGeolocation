select = document.querySelector("select");
select.classList = "form-select";
console.log(select.classList);

console.log("Moussa");

let rowsList = [];
$('table tbody tr').each(function(i, row) {
	return rowsList.push(row);
});

$('#pagination').pagination({
    dataSource: rowsList,
    pageSize: 15,
    prevText: '<i class="fa-solid fa-circle-chevron-left fa-xl"></i>',
    nextText: '<i class="fa-solid fa-circle-chevron-right fa-xl"></i>',
    showPageNumbers: false,
    callback: function(data, pagination) {
        $('tbody').html(data);
    }
});