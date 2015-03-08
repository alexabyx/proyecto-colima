function confirmarAlarma() {
  $("#div_formulario").css('display', 'none');
  $("#div_confirmacion").css('display', 'block'); 
}

function cerrarConfirmacionAlarma() {
  $("#div_formulario").css('display', 'block');
  $("#div_confirmacion").css('display', 'none');
}

function crearAlarma(tipo){
  
  if(tipo == 0){
    var method = "GET";
    var data_aux = {};        
  }
  else{
    var method = "POST";
    var data_aux = $("#formulario").serialize();
    $("#div_confirmacion").css('display', 'none');
    $("#div_formulario").css('display', 'block');
  }

  $.ajax({
    type: method,
    url: "/administracion/crear_alarma/",
    data: data_aux,
    'beforeSend': function(data2){
                  $.fancybox.showLoading();
                  $("#div_formulario").css('display', 'none');
                  $("#div_confirmacion").css('display', 'none');
    },
    'success': function(data1){
                  $.fancybox.showLoading();
                  $.fancybox(data1);
    },
    dataType: 'html'
  });
}