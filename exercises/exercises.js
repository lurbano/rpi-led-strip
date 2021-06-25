$(".toggle-next").click(function(){
  $(this).next().toggle();
  if ($(this).next().is(":visible")){
    $(this).parent().css("border", "1px solid red");
    let txt = $(this).html().replace("Show", "Hide").replace("▼", "▲");
    $(this).html(txt);
  }
  else {
    $(this).parent().css("border", "1px solid black");
    let txt = $(this).html().replace("Hide", "Show").replace("▲", "▼");
    $(this).html(txt);
  }
})
