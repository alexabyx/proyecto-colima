    $(document).ready(function(){
      $(".editar").height(20);

      $(".ocultar").click(function(){
        $(this).attr("hidden", true);
        $(this).parent().next().attr("hidden", true);
        $($(this).siblings()[0]).attr("hidden", false)
      });
      $(".mostrar").click(function(){
        $(this).attr("hidden", true);
        $(this).parent().next().attr("hidden", false);
        $($(this).siblings()[0]).attr("hidden", false);
      });
    });

    function confirmarEdicion() {
      $("#div_formulario").css('display', 'none');
      $("#div_confirmacion").css('display', 'block'); 
    }

    function cerrarConfirmarEdicion() {
      $("#div_formulario").css('display', 'block');
      $("#div_confirmacion").css('display', 'none');
    }

    function editarEntregable(tipo, id){
      
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
        url: "/administracion/editar_entregable_1/"+id+"/",
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

    function editarAnexotecnico(tipo, id){
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
        url: "/administracion/editar_anexotecnico_1/"+id+"/",
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

    function editarConvenio(tipo, id){
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
        url: "/administracion/editar_convenio_1/"+id+"/",
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

    function editarContrato(tipo, id){
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
        url: "/administracion/editar_contrato_1/"+id+"/",
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

    function editarPropuesta(tipo, id){
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
        url: "/administracion/editar_propuesta_1/"+id+"/",
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

    function editarDocGeneral(tipo, id){
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
        url: "/administracion/editar_doc_general_1/"+id+"/",
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
  function editarDetalleDocGeneral(tipo, id){
    if(tipo == 0){
      var method = "GET";
      var data_aux = {};        
    }
    else{
      var method = "POST";
      var data_aux = $("#formulario").serialize();

      // $("#formulario").find(":input").each(function(){
      //                                                 data_aux[$(this).attr("name")]=$(this).val();
      //                                               });

      // var data_aux = new FormData();
      // data_aux.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());
      // data_aux.append('files[]', $("input:file")[1].files[0].valueOf());
      //console.log(data_aux)

      //$("#formulario").serialize();

      $("#div_confirmacion").css('display', 'none');
      $("#div_formulario").css('display', 'block');
    }

    $.ajax({
      type: method,
      url: "/administracion/editar_detalle_doc_general_1/"+id+"/",
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

  function editarDetalleDocResponsiva(tipo, id){
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
      url: "/administracion/editar_detalle_doc_responsiva_1/"+id+"/",
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

  function editarDetallePagoEmpleado(tipo, id){
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
      url: "/administracion/editar_detalle_pago_empleado_1/"+id+"/",
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

  function editarFactura(tipo, id){
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
      url: "/administracion/editar_factura_1/"+id+"/",
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

  function editarProyecto(tipo, id){
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
      url: "/administracion/editar_proyecto_1/"+id+"/",
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
  function editarDetalleEntregable(tipo, id){
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
      url: "/administracion/editar_detalle_entregable_1/"+id+"/",
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
  function editarDetalleFactura(tipo, id){
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
      url: "/administracion/editar_detalle_factura_1/"+id+"/",
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
  function editarEntidadProyecto(tipo, id){
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
      url: "/administracion/editar_entidad_proyecto_1/"+id+"/",
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
