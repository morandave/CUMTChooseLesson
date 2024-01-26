$(document).ready(function() {
    $(".carousel-item").first().addClass("active");
    $(".carousel-item").each(function() {
      var imgSrc = $(this).find("img").attr("src");
      $(this).css("background-image", "url('" + imgSrc + "')");
      $(this).find("img").remove();
    });
    setInterval(function() {
      $(".carousel-item.active").removeClass("active").next(".carousel-item").addClass("active");
      if ($(".carousel-item.active").length === 0) {
        $(".carousel-item").first().addClass("active");
      }
    }, 5000);
  });