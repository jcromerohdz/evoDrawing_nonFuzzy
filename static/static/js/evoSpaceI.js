
$(document).ready(function () {
    var hm = $("body").wHumanMsg();

   $("#input-21e").rating({hoverEnabled: true, hoverChangeStars: true});

    $( document ).tooltip();

    $( "#tabs" ).tabs({collapsible: true});
    //$( "#selectable" ).selectable();


    var get_collections = function(){
        var user=$("#username").val();
        //alert(user);
        $.ajax({
            type: "GET",
            url: "/get_user_collections/"+user+"/",
            dataType: "json",
            success: function(data) {

                $("#selectable").html("");
                //
                // Esto es un foreach
                //
                for (var i=0; i<data.collections.length; i++){
                    $('<a />',
                            {
                                //"class":"glyphicon glyphicon-folder-open",
                                href:"/get_collection/"+user+"/" + data.collections[i].id

                             }
                     ).append(

                            $('<li />' ,
                                    {   "class":"ui-widget-content folder",
                                        //"class":"glyphicon glyphicon-folder-open",
                                        text:  "   "+data.collections[i].name.substr(0,40)



                                    })


                    ).appendTo("#selectable");

                }

            }
        });

    };


 //   $(function() {
 //       $( "#selectable" ).selectable();
 //   });

    $.ajaxSetup({
         beforeSend: function(xhr, settings) {
             function getCookie(name) {
                 var cookieValue = null;
                 if (document.cookie && document.cookie != '') {
                     var cookies = document.cookie.split(';');
                     for (var i = 0; i < cookies.length; i++) {
                         var cookie = jQuery.trim(cookies[i]);
                         // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
             }
             if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                 // Only send the token to relative URLs i.e. locally.
                 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
             }
         }
    });

    var $dialog = $('<div></div>')
            .dialog({
                autoOpen: false,
                title: 'Liked by',
                modal:true,
                                show:'fadeIn', //crh
                                hide:'fadeOut' //crh
            });

     var $dialog2 = $('#box2')
             .dialog({
                 autoOpen: false,
                 title: 'Collection',
                 modal:true,
                 show:'fadeIn', //crh
                 hide:'fadeOut',
                 buttons: { "Add": function(e) {
                            e.preventDefault();

                            $.ajaxSetup({
                                beforeSend: function(xhr, settings) {
                                function getCookie(name) {
                                    var cookieValue = null;
                                    if (document.cookie && document.cookie != '') {
                                        var cookies = document.cookie.split(';');
                                        for (var i = 0; i < cookies.length; i++) {
                                            var cookie = jQuery.trim(cookies[i]);
                                            // Does this cookie string begin with the name we want?
                                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                                break;
                                            }
                                        }
                                    }
                                    return cookieValue;
                                }
                                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                                    // Only send the token to relative URLs i.e. locally.
                                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                                }
                              }
                             });


                            var dataString = $("#add_collec").serialize();
                            console.log('datastring '+dataString);
                            //Tomar el usuario del HTML y hacer la cadena del URL
                            var col_name = $("#col_name").val();
                            var col_description = $("#col_description").val();
                            var col_option = $("#col_option").val();
                            var username =$("#username").val();
                            $.ajax({
                                type: "POST",
                                url: "/add_collection/"+username+"/",
                                data: JSON.stringify({"name":col_name, "description":col_description, "option":col_option}),
                                dataType: "json",
                                contentType:"application/json",
                                success: function(data) {

                                    get_collections();
                                    hm.wHumanMsg(data.message);
                                    //console.log('message :'+data.message);

                                }


                            });


                            $(this).dialog("close");
                          },
                           "Cancel": function() {
                           $(this).dialog("close");
                          }
                        }
             });

    var $dialog3 = $('#box3')
            .dialog({
                autoOpen: false,
                title: 'Add to',
                modal:true,
                show:'fadeIn', //crh
                hide:'fadeOut',
                buttons: { "Add to Collection": function() {

                    //var dataString = $("#add_ind_col").serialize();
                    var individual = $("#individual_id").val()
                    var user_collection = $("#uc").val()
                    //Tomar el usuario del HTML y hacer la cadena del URL
                    var username =$("#username").val();
                    //alert(username);
                    var URL="/add_ind_to_col/"+username+"/";
                    //console.log('datastring '+dataString);
                    $.ajax({
                        type: "POST",
                        url: URL,
                        data: JSON.stringify({"id":individual, "userCollection":user_collection}),
                        dataType: "json",
                        contentType:"application/json",
                        success: function(data) {
                            //alert(data.name);

                            //console.log('hola '+data.visibility);
                            hm.wHumanMsg(data.message);

                            //console.log('message :'+data.message);

                        }


                    });

                    $(this).dialog("close");
                },
                    "Cancel": function() {
                        $(this).dialog("close");
                    }
                }
            });





    $('.grid-item.slidedown').hover(function(){
        $(".cover", this).stop().animate({top:'5px', left:'5px'},{queue:false,duration:300});
    }, function() {
        $(".cover", this).stop().animate({top:'-560px',left:'5px'},{queue:false,duration:300});
    });

    $('.grid-item.slideup').hover(function(){
        $(".cover", this).stop().animate({top:'422px', left:'5px'},{queue:false,duration:300});
    }, function() {
        $(".cover", this).stop().animate({top:'480px',left:'5px'},{queue:false,duration:300});
    });

    $("canvas").click(function () {
        $(this).toggleClass("ilike");

    });



    $(".fitness").click(function ()
    {

        var slot_index = $(this)[0].parentElement.previousSibling.previousSibling.id.substr(4);

        var details ="";
        for (var index in sample.sample[slot_index].fitness){
            if (index != "DefaultContext"){
            var id = index.split(":")[0];

            details+= "<img src='http://graph.facebook.com/"+id+"/picture?type=square'/>";
            //details+= "<fb:profile-pic size='square' facebook-logo='true' uid='"+id+"'/>";
            }
         }
        $dialog.html(details);
        $dialog.dialog('open');
        return false;

    });

    //crh
    $(".addto").click(function ()

    {
        var slot_index = $(this)[0].parentElement.previousSibling.previousSibling.id.substr(4);

        var dataSample =sample.sample[slot_index].id;

        var inp ='<input type="text'+ '" id="individual_id" name="individual" value="'+dataSample+'" readonly>';


        $("#col_ind").html(inp);


        $(function(){
            //Tomar el usuario desde un campo del HTML
            var username =$("#username").val();
            $.ajax({
                type: "GET",
                url: "/get_user_collections/"+username+"/",
                dataType: "json",
                success: function(data) {
                    var options = '';
                    for (var i=0; i<data.collections.length; i++){
                        options += '<option value="' + data.collections[i].id + '">' + data.collections[i].name + '</option>';
                    }
                    $("#uc").html(options);


                }
            });

        })

        //$dialog.html(details);
        $dialog3.dialog('open');
        return false;

    });


    $("#get_more").click(function () {
        if (sample )
        {
            var individuals = $(".ilike").length;
            sample.individuals_with_like=[];

            var value1= $("#input-21e").val();
            var value2= $("#input-22e").val()

            $("canvas").each(
                    function(i, element){
                        var slot_index = element.id.substr(4);
                        var timestamp = Date.now()



                            var username =$("#username").val();


                        //if ( $(this).hasClass("ilike"))
                        if ( $(this).hasClass("ilike"))
                        {
                            if (value1){
                                sample.sample[slot_index].fitness[username+":"+timestamp] = value1;
                                $(this).toggleClass("ilike");
                                sample.individuals_with_like.push(sample.sample[slot_index].id);
                                //alert(value1)

                            }

                            if (value2){
                                sample.sample[slot_index].fitness[username+":"+timestamp] = value2;
                                $(this).toggleClass("ilike");
                                sample.individuals_with_like.push(sample.sample[slot_index].id);
                                //alert(value2)

                            }
                            //sample.sample[slot_index].fitness[username+":"+timestamp] = 1;
                            
                        }

                        sample.sample[slot_index].views += 1;
                        $("#input-21e").val(0);


                    }

            );


            //Put them back
            $("#get_more")[0].disabled = true;
            $("#get_more")[0].innerHTML = "Wait..."
            $.ajax(
                    {
                        url: '/EvoSpace',
                        type: "POST",
                        contentType: "application/json",
                        data: JSON.stringify({"jsonrpc": "2.0", "method": "putSample", "params": [sample], "id": 1}),

                        //data: {"jsonrpc": "2.0", "method": "putSample", "params": [sample], "id": 1},
                        dataType: "json",
                        success: function(data, textStatus, jqXHR) {
                            //  alert(sample.sample[0].chromosome);
                        },
                        error: function(jqXHR, textStatus, errorThrown)  {
                            alert ("Error: putSample" + textStatus+" "+errorThrown+" "+jqXHR.responseText);}

                    });

            hm.wHumanMsg('Likes:'+ individuals + ', new paintings received',{color: 'yellow',  displayLength: 400});

            //Get More!
        }

        dataRequest();


    });


    $('.rating').on('rating.change', function(event, value, caption) {
       //alert("evento"); 
       //alert(value);
       //alert($(this).parent().parent().parent().parent().prev()[0].id);
       var user=$("#username").val();
       //alert("soy: :ooo "+user);

         var inputbox = $(this)[0].id; 
      if (sample){
         //alert(value);
          sample.individuals_with_like=[];
          var slot = $(this).parent().parent().parent().parent().prev()[0].id;
          
          slot = "#" + slot;
          //alert(slot); 
          

            $(slot).each(
                    function(i, element){
                        var slot_index = element.id.substr(4);
                        var timestamp = Date.now()



                        var username =$("#username").val();


                        //if ( $(this).hasClass("ilike"))
                        if ( value )
                        {
                            sample.sample[slot_index].fitness[username+":"+timestamp] = value;
                            sample.individuals_with_like.push(sample.sample[slot_index].id);
                            //alert(value);
         
                            //sample.sample[slot_index].fitness[username+":"+timestamp] = 1;
                            
                        }
                        sample.sample[slot_index].views += 1;
                        
                        //$(inputbox).value() = 0;
                
                    }

            );

            //crh-change disable true
            
            
            $('#evaluation').hide();
            $('#loading').show();
             
            
            //alert(sample);    
            $.ajax(
                    {
                        url: '/EvoSpace',
                        type: "POST",
                        contentType: "application/json",
                        data: JSON.stringify({"jsonrpc": "2.0", "method": "putSample", "params": [sample], "id": 1}),

                        //data: {"jsonrpc": "2.0", "method": "putSample", "params": [sample], "id": 1},
                        dataType: "json",
                    
                        success: function(data, textStatus, jqXHR) {

                            //alert(sample.sample[0].chromosome);
                        },
                        error: function(jqXHR, textStatus, errorThrown)  {
                            //alert("jejejjej error");
                            alert ("Error: putSample" + textStatus+" "+errorThrown+" "+jqXHR.responseText);}

                    });

            hm.wHumanMsg('Likes:'+ ', new paintings received',{color: 'yellow',  displayLength: 400});

      }
        var delay=5000;//1 seconds
             setTimeout(function(){
               
                inputbox = "#" + inputbox;
                //alert(inputbox);

                $(inputbox).rating('reset');
                $('#loading').hide();
                $('#evaluation').show();
                

                //alert("delay");    

             //your code to be executed after 1 seconds
            },delay); 

        //respawn();     
        var container = $(this).parent().parent().parent().parent().prev()[0].id;    
        dataRequestPaints(container);
        

        //Aqui UserLeve Score & level

         //UserScore and rankin
         $(function(){
            //var user=$("#username").val();

             //alert("lider board!");

             //Lider boad

             $.ajax(
                 {
                     url: "/get_liders/",
                     type: "GET",
                     contentType: "application/json",
                     dataType: "json",
                     success: function(data, textStatus, jqXHR) {


                        //alert(data.length);
                        var c = 0;
                        var txt = ""; 
                        //alert(Object.keys(data.leaders).length);
                        for(var obj in data.leaders){
                             //alert(data[obj].score);
                             //alert(Object.keys(data).length);
                             
                             if (c < Object.keys(data.leaders).length){
                                c = c + 1;
                            //alert(data.leaders[obj].user)

                                //alert(c);
                             //alert(data[obj]);   
                            
                             }

                                    //alert(prop + ':' + jsonData[obj][prop]);
                                                                        
                                    txt += "<tr>";
                                    txt += "<th>"+c+"</th>"; 
                                    txt += "<td>"+data.leaders[obj].user+ "</td>";
                                    txt += "<td>"+data.leaders[obj].score+ "</td>";
                                    txt += "<td>"+data.leaders[obj].ranking+ "</td>";
                                    txt += "</tr>";  
                                    document.getElementById('lider-board-t').innerHTML = txt; 
                                    document.getElementById('lider-board').innerHTML = txt;                                                      
                       
                                   
                         
                        }
                        
                         

                        // for (var i in data){
                        //     //alert("for");
                        //     var c = parseInt([i]) + 1;
                        //     var sn = c.toString();
                        //     var lid = "lider"+sn;
                        //     alert(lid);
                        //     alert(Object.keys(data).length);
                        //     alert(Object.keys(data));
                        //     var k = Object.keys(data);

                        //     alert(i.user);
                            
                            
                        // }


                       


                     },
                     error: function(jqXHR, textStatus, errorThrown)  {
                         alert ("Error:" + textStatus+" "+errorThrown+" "+jqXHR.responseText);}
                 });


        });

            $.ajax(
                {
                    url: "/get_user_level/"+user+"/",
                    type: "GET",
                    contentType: "application/json",
                    dataType: "json",
                    success: function(data, textStatus, jqXHR) {
                        
                        userScore =data.user_level.score;
                        userLevel = data.user_level.level;

                    //alert(userScore);
                    //alert(userLevel);

                    $("#badge1").text(userScore);
                    $("#badge2").text(userLevel);





                        if  (data.user_level == null)
                            alert("No user level!!") ;


                    },
                    error: function(jqXHR, textStatus, errorThrown)  {
                        alert ("Error:" + textStatus+" "+errorThrown+" "+jqXHR.responseText);}
                });



    
    });

    // $('#input-22e').on('rating.change', function(event, value, caption) {
        
    //   if (sample){
    //      //alert(value);
    //      sample.individuals_with_like=[];
    //      alert(event);
    //      alert($(this));

    //         $("#slot0").each(
    //                 function(i, element){
    //                     var slot_index = element.id.substr(4);
    //                     var timestamp = Date.now()



    //                     var username =$("#username").val();


    //                     //if ( $(this).hasClass("ilike"))
    //                     if ( value )
    //                     {
    //                         sample.sample[slot_index].fitness[username+":"+timestamp] = value;
    //                         sample.individuals_with_like.push(sample.sample[slot_index].id);
    //                         alert(value);
         
    //                         //sample.sample[slot_index].fitness[username+":"+timestamp] = 1;
                            
    //                     }
                
    //                 }

    //         );

    //         alert(sample);    
    //         $.ajax(
    //                 {
    //                     url: '/EvoSpace',
    //                     type: "POST",
    //                     contentType: "application/json",
    //                     data: JSON.stringify({"jsonrpc": "2.0", "method": "putSample", "params": [sample], "id": 1}),

    //                     //data: {"jsonrpc": "2.0", "method": "putSample", "params": [sample], "id": 1},
    //                     dataType: "json",
    //                     success: function(data, textStatus, jqXHR) {
    //                         //  alert(sample.sample[0].chromosome);
    //                     },
    //                     error: function(jqXHR, textStatus, errorThrown)  {
    //                         alert ("Error: putSample" + textStatus+" "+errorThrown+" "+jqXHR.responseText);}

    //                 });

    //         hm.wHumanMsg('Likes:'+ ', new paintings received',{color: 'yellow',  displayLength: 400});

    //   }
    //     var container = "#slot1"    
    //     dataRequestPaints(container);
    
    // });

    $("#evolve").click(function () {

        //Put them back
        $.ajax(
                {
                    url: '/EvoSpace',
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({"jsonrpc": "2.0", "method": "evolve", "params": [16], "id": 1 }),
                    dataType: "json",
                    success: function(data, textStatus, jqXHR) {


                        hm.wHumanMsg('Success in evolution of population',{color: 'green',  displayLength: 400});

                    },

                    error: function(jqXHR, textStatus, errorThrown)  {
                        alert ("Error:" + textStatus+" "+errorThrown+" "+jqXHR.responseText);}

                });

    });

    $("#respawn").click(function () {

        //Put them back
        $.ajax(
                {
                    url: '/EvoSpace',
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({"jsonrpc": "2.0", "method": "respawn", "params": [2], "id": 1 }),
                    dataType: "json",
                    success: function(data, textStatus, jqXHR) {


                        hm.wHumanMsg('Samples respawned',{color: 'red',  displayLength: 400});

                    },

                    error: function(jqXHR, textStatus, errorThrown)  {
                        alert ("Error:" + textStatus+" "+errorThrown+" "+jqXHR.responseText);}

                });

    });

    function respawn(){
         //Put them back
        $.ajax(
                {
                    url: '/EvoSpace',
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({"jsonrpc": "2.0", "method": "respawn", "params": [2], "id": 1 }),
                    dataType: "json",
                    success: function(data, textStatus, jqXHR) {


                        hm.wHumanMsg('Samples respawned',{color: 'red',  displayLength: 400});

                    },

                    error: function(jqXHR, textStatus, errorThrown)  {
                        alert ("Error:" + textStatus+" "+errorThrown+" "+jqXHR.responseText);}

                });

    }



    function dataRequestPaints(container){
        //alert(container);
        container = "#"+container;
        $.ajax(
                {
                    url: '/EvoSpace',
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({"jsonrpc": "2.0", "method": "getSample", "params": [1], "id": 1 }),
                    dataType: "json",
                    success: function(data, textStatus, jqXHR) {
                        //data = jQuery.parseJSON(data);
                        sample =data.result;
                        //Put them back
                        $("#get_more")[0].disabled = false;
                        $("#get_more")[0].innerHTML = "Get More"


                        if  (data.result == null)
                            alert("No more paintings in evospace: respawn some samples") ;

                        

                        $(container).each(
                                function(i, element){



                                    var bound = false;
                                    var chromosome = sample.sample[i].chromosome;

                                    function getPJS() {
                                        var pjs = Processing.getInstanceById(element.id);
                                        if(pjs!=null) {
                                            var chrome = pjs.getChromosome();
                                            //alert(chrome)
                                            chrome.length = 0;
                                            Array.prototype.push.apply(chrome, chromosome);
                                            pjs.setup();//Se resetea el canvas
                                            pjs.draw();
                                            bound = true; }
                                        if(!bound) setTimeout(getPJS, 50);
                                    }

                                    getPJS();




                                    slot_index = element.id.substr(4);

                                    element.nextElementSibling.childNodes[1].setAttribute(
                                        "href","/individual/"+sample.sample[slot_index].id.substr(15));
                                    element.nextElementSibling.childNodes[1].setAttribute(
                                            "target","_blank");
                                    element.nextElementSibling.childNodes[1].textContent = "Details";//"id:" + sample.sample[slot_index].id.substr(15) ;


                                    var suma = 0;
                                    for (var index in sample.sample[slot_index].fitness){
                                        suma+=sample.sample[slot_index].fitness[index];
                                    }

                                    element.nextElementSibling.childNodes[3].textContent= suma +" likes";

                                }
                        );
                    },
                    error: function(jqXHR, textStatus, errorThrown)  {
                        //alert("SUper Oso");
                        alert ("Error:" + textStatus+" "+errorThrown+" "+jqXHR.responseText);}
                });
        //$("#evaluation").show();
    }

    function dataRequest(){
         $("#get_more").hide();
         $("#loading").hide();  

        var user=$("#username").val();
        //alert("soy: :P "+user);  


        $.ajax(
                {
                    url: '/EvoSpace',
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({"jsonrpc": "2.0", "method": "getSample", "params": [1
                        ], "id": 1 }),
                    dataType: "json",
                    success: function(data, textStatus, jqXHR) {
                        //data = jQuery.parseJSON(data);
                        sample =data.result;
                        //Put them back
                        //$("#get_more")[0].hide();

                        //$("#get_more")[0].innerHTML = "Get More"


                        if  (data.result == null)
                            alert("No more paintings in evospace: respawn some samples") ;


                        $("canvas").each(
                                function(i, element){



                                    var bound = false;
                                    var chromosome = sample.sample[i].chromosome;

                                    function getPJS() {
                                        var pjs = Processing.getInstanceById(element.id);
                                        if(pjs!=null) {
                                            var chrome = pjs.getChromosome();
                                            //alert(chrome)
                                            chrome.length = 0;
                                            Array.prototype.push.apply(chrome, chromosome);
                                            pjs.setup();//Se resetea el canvas
                                            pjs.draw();
                                            bound = true; }
                                        if(!bound) setTimeout(getPJS, 50);
                                    }

                                    getPJS();




                                    slot_index = element.id.substr(4);

                                    element.nextElementSibling.childNodes[1].setAttribute(
                                        "href","/individual/"+sample.sample[slot_index].id.substr(15));
                                    element.nextElementSibling.childNodes[1].setAttribute(
                                            "target","_blank");
                                    element.nextElementSibling.childNodes[1].textContent = "Details";//"id:" + sample.sample[slot_index].id.substr(15) ;


                                    var suma = 0;
                                    for (var index in sample.sample[slot_index].fitness){
                                        suma+=sample.sample[slot_index].fitness[index];
                                    }

                                    element.nextElementSibling.childNodes[3].textContent= suma +" likes";

                                }
                        );
                    },
                    error: function(jqXHR, textStatus, errorThrown)  {
                        alert ("Error:" + textStatus+" "+errorThrown+" "+jqXHR.responseText);}
                });

            //UserScore and ranking

            $.ajax(
                {
                    url: "/get_user_level/"+user+"/",
                    type: "GET",
                    contentType: "application/json",
                    dataType: "json",
                    success: function(data, textStatus, jqXHR) {
                        
                        userScore =data.user_level.score;
                        userLevel = data.user_level.level;

                    //alert(userScore);
                    //alert(userLevel);

                    $("#badge1").text(userScore);
                    $("#badge2").text(userLevel);





                        if  (data.user_level == null)
                            alert("No user level!!") ;


                    },
                    error: function(jqXHR, textStatus, errorThrown)  {
                        alert ("Error:" + textStatus+" "+errorThrown+" "+jqXHR.responseText);}
                });

                
    }

    //alert("ready");
    //dataRequest();
        //me lider board implementantion
        $('#add_collection').click(function(){

             $dialog2.dialog('open');

        });

        $("a.leaders").click(function() {
                 //alert("Leaders");

                 $.ajax(
                     {
                         url: "/get_liders/",
                         type: "GET",
                         contentType: "application/json",
                         dataType: "json",
                         success: function(data, textStatus, jqXHR) {


                            //alert(data.length);
                            var c = 0;
                            var txt = ""; 
                            //alert(Object.keys(data.leaders).length);
                            for(var obj in data.leaders){
                                 //alert(data[obj].score);
                                 //alert(Object.keys(data).length);
                                 
                                 if (c < Object.keys(data.leaders).length){
                                    c = c + 1;
                                //alert(data.leaders[obj].user)

                                    //alert(c);
                                 //alert(data[obj]);   
                                
                                 }

                                        //alert(prop + ':' + jsonData[obj][prop]);
                                                                            
                                        txt += "<tr>";
                                        txt += "<th>"+c+"</th>"; 
                                        txt += "<td>"+data.leaders[obj].user+ "</td>";
                                        txt += "<td>"+data.leaders[obj].score+ "</td>";
                                        txt += "<td>"+data.leaders[obj].ranking+ "</td>";
                                        txt += "</tr>";  
                                        //document.getElementById('lider-board-t').innerHTML = txt; 
                                        document.getElementById('lider-board').innerHTML = txt;                                                      
                           
                                       
                             
                            }
                            
                             

                            // for (var i in data){
                            //     //alert("for");
                            //     var c = parseInt([i]) + 1;
                            //     var sn = c.toString();
                            //     var lid = "lider"+sn;
                            //     alert(lid);
                            //     alert(Object.keys(data).length);
                            //     alert(Object.keys(data));
                            //     var k = Object.keys(data);

                            //     alert(i.user);
                                
                                
                            // }


                           


                         },
                         error: function(jqXHR, textStatus, errorThrown)  {
                             alert ("Error:" + textStatus+" "+errorThrown+" "+jqXHR.responseText);}
                     });
        });


        $('#lider_button').click(function(){
            //var user=$("#username").val();

             //alert("lider board!");

             //Lider boad

             


        });
    dataRequest();
    get_collections();

    $(function () {
        $("a.youtube").YouTubePopup({ autoplay: 1 });
    });

    //setTimeout(dataRequest,5000);

});/**
 * Created by chris on 5/27/14.
 */
