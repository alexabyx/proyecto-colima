    function aviso_historico(model, element_id, historico){
     	$.fancybox.showLoading();
     	if(historico == 2){
	     	var data = {mensaje: "¿Está seguro de querer enviar a historico este registro?"};     		
     	}
	    else{
	     	var data = {mensaje: "¿Está seguro de querer cancelar este registro?"};     		    	
	    }
     	$.get('/administracion/modal_aviso/', data, function(response){
     		$.fancybox({'content': response,
     					'openEffect': 'elastic',
						'closeEffect': 'elastic',
     					'afterShow':function(){
     						$('#aceptar').click(function(){
     								$(this).attr("disabled", "disabled");
									//$.fancybox.close();
									enviar_historico(model, element_id, historico);
     						});

     						$("#cancelar").click(function(){
									$.fancybox.close();
     						});
     					},
     					});

     	});
     }
     function enviar_historico(model, element_id, historico){
     	$.fancybox.showLoading();

     	var csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
     	var data = {'model': model, 'pk': element_id, 'historico': historico, 'csrfmiddlewaretoken': csrfmiddlewaretoken}

     	$.post('/administracion/en_historico/', data, function(response){
     		if(response.error){
     			$.get('/administracion/modal_error/', {}, function(_response){ 
					$.fancybox({'content': _response,
							//'afterShow': function(){ $('#fancybox-content').css("width", $('#fancybox-outer').width());},
							'afterClose':function(){ window.location.reload();},
								});
     			});
     		}
     		else{
     			$.fancybox.showLoading();
     			$.get('/administracion/modal_ok/', {}, function(_response){
					$.fancybox({'content': _response,
							//'afterShow': function(){ $('#fancybox-content').css("width", $('#fancybox-outer').width());},
							'afterClose':function(){ window.location.reload();},
							});
     			});

     		}

     	});
     }