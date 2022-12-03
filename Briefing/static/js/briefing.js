$( function() {
    $( ".column" ).sortable({
      connectWith: ".column",
      handle: ".portlet-header",
      cancel: ".portlet-toggle",
      placeholder: "portlet-placeholder ui-corner-all"
    });

    $('.column').on('sortupdate',function(e,ui) {
        if (this === ui.item.parent()[0]) {
          var widgets = [];
          $('.column').each(function (e) {
            var column = [];
            $(this).find(".portlet").each(function (portlet_e) {
              var portlet = {
                "feed": $(this).data('feed'),
                "name": $(this).data('title'),
                "template": $(this).data('template')
              }
              column.push(portlet);
            });
            widgets.push(column);
          });
          json = JSON.stringify(widgets);
          
          $.ajax({
            type: "POST",
            url: "/update",
            // The key needs to match your method's input parameter (case-sensitive).
            data: json,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){console.log("update successful")},
            error: function(errMsg) {
              console.log("Update Failed: " + JSON.stringify(errMsg));
            }
          });
        }
    });

    $( ".portlet" )
      .addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" )
      .find( ".portlet-header" )
        .addClass( "ui-widget-header ui-corner-all" )
        .prepend( "<span class='ui-icon ui-icon-minusthick portlet-toggle'></span>");
    
 
    $( ".portlet-toggle" ).on( "click", function() {
      var icon = $( this );
      icon.toggleClass( "ui-icon-minusthick ui-icon-plusthick" );
      icon.closest( ".portlet" ).find( ".portlet-content" ).toggle();
    });
  } );