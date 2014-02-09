$(window).load(function() {
	$('.vote-btn').on('click', function() {
		var idPresentation = $(this).attr('data-presentation');
		$.post("/vote/" + idPresentation + "/1", function() {});
	});
});