$(function(){

  // This is the initializer of the canvas
  $('#plano_animado').particleground({
      dotColor: 'rgb(175, 163, 163)',
      lineColor: 'rgb(175, 163, 163)'
  });

  $('#success-modal').modal();

  $('#register-form').submit( function (){
    form = new FormData(this);
    $.ajax({
      type: 'POST',
      url: '/signup/',
      data: form,
      success:function(data){
        $('#success-modal').modal('open');
      },
      error:function(error){
        console.log("error");
      }
    });
  });

});
