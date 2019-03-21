
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})


$("input[name=inlineRadioOptions]").change(function() {
    var test = $(this).val();
    if (test === 'source-url') {
      $(".o-js-source-url").show();
      $(".o-js-source-pdf").hide();
    } else if (test === 'source-pdf') {
      $(".o-js-source-pdf").show();
      $(".o-js-source-url").hide();
    }
});


function onClickShowComment () {
    $('.showComments').click(function (event) {
        event.preventDefault()
        console.log(event.target)
        // $('.o-comments').slideToggle(750)
        $(this).parentsUntil('.card')
        .siblings('.rounded-bottom')
        .children('.o-comments').slideToggle(600)
    })
}


onClickShowComment()


/*
$(".clickable-cell, .clickable-row").hover(function() {
    $(this).css("cursor", "pointer");
});

$(".clickable-cell, .clickable-row").click(function() {
    window.location = $(this).data("href");
});


$(".o-js-card-project.o-card-hover").click(function(event) {
    window.location = $(this).data("href");
});
*/











//$('textarea').focus(function () {
//      $(this).animate({
//        height: "6em"
//      }, 500);
//});

//$('textarea').focusout(function () {
//  if ($("textarea").val() === "") {
//    $(this).animate({
//      height: "2.5em"
//    }, 500);
//  }
//});