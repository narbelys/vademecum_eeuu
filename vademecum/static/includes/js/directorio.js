/**
 * Callback function that displays the content.
 *
 * Gets called every time the user clicks on a pagination link.
 *
 * @param {int}page_index New Page index
 * @param {jQuery} jq the container with the pagination links as a jQuery object
 */
function pageselectCallback(page_index, jq){
    
    var panama = $('#pais').val()

    // Get number of elements per pagionation page from form
    var items_per_page = 40;
    var max_elem = Math.min((page_index+1) * items_per_page, directorio.length);
    var newcontent = '';

    // Iterate through a selection of the content and build an HTML string
    for(var i=page_index*items_per_page;i<max_elem;i++)
    {
        if (panama=="panama"){
            newcontent += '<li value='+ (i+1) +'><a href=/centro_america/panama'+ directorio[i][0]+'>' + directorio[i][1] + '</a></li>';
        }else{
            newcontent += '<li value='+ (i+1) +'><a href='+ directorio[i][0]+'>' + directorio[i][1] + '</a></li>';
        }
    }

    // Replace old content with new content
    $('#lista').html(newcontent);

    // Prevent click eventpropagation
    return false;
}

function pageselectCallbackLab(page_index, jq){

    // Get number of elements per pagionation page from form
    var items_per_page = 40;
    var max_elem = Math.min((page_index+1) * items_per_page, directorio.length);
    var newcontent = '';

     var panama = $('#pais').val()
    // Iterate through a selection of the content and build an HTML string
    for(var i=page_index*items_per_page;i<max_elem;i++)
    {
        if (panama=="panama"){
            newcontent += '<li><a href=../centro_america/panama/Medicamentos/'+ directorio[i][0] +'>' + directorio[i][1] + '</a></li>';
        }else{
            newcontent += '<li><a href=../Medicamentos/'+ directorio[i][0] +'>' + directorio[i][1] + '</a></li>';
        }
    }

    // Replace old content with new content
    $('#lista').html(newcontent);

    // Prevent click eventpropagation
    return false;
}

function pageselectCallbackTab(page_index, jq){
    
    var panama = $('#pais').val()

    // Get number of elements per pagionation page from form
//    var items_per_page = 40;
    var items_per_page = 20;
    var max_elem = Math.min((page_index+1) * items_per_page, directorio.length);
    var newcontent = '';
    var marcas_paises={};

    // Iterate through a selection of the content and build an HTML string
    var i=page_index*items_per_page;
    for(var j=page_index*items_per_page;j<max_elem;i++)
    {
            if (!directorio[i]){
                break
            }
            j=j+1
//            marcas_paises.push(directorio[i][1]);
            if (directorio[i][1] in marcas_paises){
                marcas_paises[directorio[i][1]].paises.push(directorio[i][2])
                marcas_paises[directorio[i][1]].id_vademecum.push(directorio[i][0])
                marcas_paises[directorio[i][1]].link.push(directorio[i][3])
                marcas_paises[directorio[i][1]].nombre.push(directorio[i][4])
                if (j>0){
//                    alert("---"+directorio[i][1]+i)
                    j=j-1
                }
            }else{
                marcas_paises[directorio[i][1]] = {'paises':[directorio[i][2]], 'id_vademecum':[directorio[i][0]], 'link':[directorio[i][3]], 'nombre':[directorio[i][4]]};
//                alert("\\"+directorio[i][1]+i)
            }
//            alert(i)
    }
    
    var i=0;
    for (var key in marcas_paises) {
        
//        alert(marcas_paises[key].paises)
        newcontent +='<tr value='+ (i+1) +'><td>' + key + '</td><td>'
        for (j in marcas_paises[key].paises){
            newcontent +="<a href="+marcas_paises[key].link[j]+"/Marcas/"+ marcas_paises[key].id_vademecum[j]+" title='"+key+" "+marcas_paises[key].nombre[j]+"'><img src='"+static_url +"images/banderas/"+marcas_paises[key].paises[j]+ "' alt='flag' style='height:12px; width:auto'></a>  "
                
//                marcas_paises[key].paises[j]+" "
        }
        newcontent +='</td></tr>'
        i=i+1
    
    }

    $('#lista').html(newcontent);
//    $('#lista').html("gfhgfhf");

    // Prevent click eventpropagation
    return false;
}


function paginar(directorio) {

    $("#Pagination").pagination(directorio.length, {
          items_per_page:40,
          num_display_entries:5,
          prev_text: "&laquo;",
          next_text: "&raquo;",
          callback: pageselectCallback
    });
}

function paginar_paises(directorio) {

    $("#Pagination").pagination(directorio.length, {
          items_per_page:40,
          num_display_entries:5,
          prev_text: "&laquo;",
          next_text: "&raquo;",
          callback: pageselectCallbackTab
    });    
    
}