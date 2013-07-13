$("td:not(#auta)").click(function () {
    window.location.href = $(this).find("a").attr("href");
});