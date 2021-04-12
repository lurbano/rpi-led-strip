$(".toggle-next").click(function(){
  $(this).next().toggle();
  if ($(this).next().is(":visible")){
    $(this).parent().css("border", "1px solid red");
  }
  else {
    $(this).parent().css("border", "none");
  }
})
