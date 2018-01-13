  $(function () {
        $(".item_title").click(function () {
            alert($(this).text());
            $(this).next().toggleClass("hide")
        });
    });