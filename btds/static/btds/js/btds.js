$(function() {
if ($('.btn-group #en')) {
	$('.btn-group #en').addClass("active");
	$('#links').children().not("#en").css("display","none");
} else {
	$('.btn-group button:first-child').addClass("active");
	$('#links').children().not("#" + $('.btn-group button:first-child').attr("id")).css("display","none");
}
});
$(".btn-group").children().click(function() {
	$('.btn-group').children().removeClass("active");
	$('.btn-group #' + $(this).attr("id")).addClass("active");
	$('#links').children().css("display","none");
	$('#links #' + $(this).attr("id")).css("display","block");
});

//$("[id^=edit]").on('show', function () { $('.modal-body',this).css({width:'auto',height:'auto', 'max-height':'90%'}); });
//$("[id^=add]").on('show', function () { $('.modal-body',this).css({width:'auto',height:'auto', 'max-height':'90%'}); });