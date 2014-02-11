var NB_VOTES_REACHED = "maximum-number-of-votes-reached";

$(window).load(function() {
	$('.vote-btn').on('click', function() {
		var idPresentation = $(this).attr('data-presentation');

		$.ajax({
  			type: "POST",
  			url: "/vote/" + idPresentation,
  			dataType: "text",
		})
  		.success(function (data) {
  			var presentationIdClass = "presentation-" + idPresentation;
    		var $btnVote = $('.' + presentationIdClass);

    		if ($btnVote.hasClass('btn-default')) {
    			$btnVote.removeClass('btn-default');
    			$btnVote.addClass('btn-primary');
    		} else {
    			$btnVote.removeClass('btn-primary');
    			$btnVote.addClass('btn-default');
    		}
  		})
  		.fail(function (data) {
			if (data.responseText == NB_VOTES_REACHED) {
				var $alertsContainer = $(".alert-container");
				$alertsContainer.html("<div class=\"alert alert-warning alert-dismissable\">" +
  "<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\">&times;</button>" +
  "You have reached your number of votes, please deselect a presentation if you changed your mind!</div>");
			}	
		});
	});
});